"""Module for the benchmark generation and benchmark retrieval."""

from __future__ import annotations

import argparse
import json
import signal
import sys
from pathlib import Path
from typing import TYPE_CHECKING, Any, Literal, TypedDict, overload
from warnings import warn

from joblib import Parallel, delayed
from qiskit import QuantumCircuit

from . import qiskit_helper, tket_helper
from .devices import (
    get_available_device_names,
    get_available_devices,
    get_available_native_gatesets,
    get_device_by_name,
    get_native_gateset_by_name,
)
from .utils import (
    get_default_config_path,
    get_default_qasm_output_path,
    get_module_for_benchmark,
    get_supported_benchmarks,
    get_supported_compilers,
    get_supported_levels,
)

if TYPE_CHECKING:  # pragma: no cover
    from collections.abc import Callable
    from types import ModuleType

    from pytket.circuit import Circuit

    from .devices import Gateset

from dataclasses import dataclass


class Benchmark(TypedDict, total=False):
    """Data class for the benchmark generation configuration."""

    name: str
    include: bool
    min_qubits: int
    max_qubits: int
    min_nodes: int
    max_nodes: int
    min_index: int
    max_index: int
    min_uncertainty: int
    max_uncertainty: int
    instances: list[str]
    ancillary_mode: list[str]
    stepsize: int
    precheck_possible: bool


@dataclass
class QiskitSettings:
    """Data class for the Qiskit compiler settings."""

    optimization_level: int = 1


@dataclass
class CompilerSettings:
    """Data class for the compiler settings."""

    qiskit: QiskitSettings | None = None


class BenchmarkGenerator:
    """Class to generate benchmarks based on a configuration file."""

    def __init__(self, cfg_path: str | None = None, qasm_output_path: str | None = None) -> None:
        """Initialize the BenchmarkGenerator."""
        if cfg_path is None:
            cfg_path = get_default_config_path()
        with Path(cfg_path).open(encoding="locale") as jsonfile:
            self.cfg = json.load(jsonfile)
            print("Read config successful")
        self.timeout = self.cfg["timeout"]
        if qasm_output_path is None:
            self.qasm_output_path = get_default_qasm_output_path()
        else:
            self.qasm_output_path = qasm_output_path

        Path(self.qasm_output_path).mkdir(exist_ok=True, parents=True)

    def create_benchmarks_from_config(self, num_jobs: int) -> bool:
        """Create benchmarks based on the configuration file.

        Arguments:
            num_jobs: number of parallel jobs to run

        Returns:
            True if successful
        """
        benchmarks = [Benchmark(benchmark) for benchmark in self.cfg["benchmarks"]]  # type: ignore[misc]
        Parallel(n_jobs=num_jobs, verbose=100)(
            delayed(self.define_benchmark_instances)(benchmark) for benchmark in benchmarks
        )
        return True

    def define_benchmark_instances(self, benchmark: Benchmark) -> None:
        """Define the instances for a benchmark."""
        lib = get_module_for_benchmark(benchmark["name"])
        file_precheck = benchmark["precheck_possible"]
        instances: list[tuple[int, str]] | list[int] | list[str] | range
        if benchmark["include"]:
            if benchmark["name"] in ("grover", "qwalk"):
                instances_without_anc_mode = range(
                    benchmark["min_qubits"],
                    benchmark["max_qubits"],
                    benchmark["stepsize"],
                )
                instances = [
                    (instance, anc_mode)
                    for instance in instances_without_anc_mode
                    for anc_mode in benchmark["ancillary_mode"]
                ]

            elif benchmark["name"] == "shor":
                instances = [lib.get_instance(choice) for choice in benchmark["instances"]]

            else:
                instances = range(
                    benchmark["min_qubits"],
                    benchmark["max_qubits"],
                    benchmark["stepsize"],
                )

            self.generate_all_benchmarks(lib, instances, file_precheck)

    def generate_all_benchmarks(
        self,
        lib: ModuleType,
        parameter_space: list[tuple[int, str]] | list[int] | list[str] | range,
        file_precheck: bool,
    ) -> None:
        """Generate all benchmarks for a given benchmark."""
        self.generate_alg_levels(file_precheck, lib, parameter_space)
        self.generate_indep_levels(file_precheck, lib, parameter_space)
        self.generate_native_gates_levels(file_precheck, lib, parameter_space)
        self.generate_mapped_levels(file_precheck, lib, parameter_space)

    def generate_mapped_levels(
        self,
        file_precheck: bool,
        lib: ModuleType,
        parameter_space: list[tuple[int, str]] | list[int] | list[str] | range,
    ) -> None:
        """Generate mapped level benchmarks for a given benchmark."""
        for qasm_format in ["qasm2", "qasm3"]:
            for device in get_available_devices():
                for opt_level in [0, 1, 2, 3]:
                    for parameter_instance in parameter_space:
                        qc = timeout_watcher(lib.create_circuit, self.timeout, parameter_instance)
                        if not qc:
                            break
                        assert isinstance(qc, QuantumCircuit)
                        if qc.num_qubits <= device.num_qubits:
                            res = timeout_watcher(
                                qiskit_helper.get_mapped_level,
                                self.timeout,
                                [
                                    qc,
                                    qc.num_qubits,
                                    device,
                                    opt_level,
                                    file_precheck,
                                    False,
                                    self.qasm_output_path,
                                    qasm_format,
                                ],
                            )
                            if not res:
                                break
                        else:
                            break

                for parameter_instance in parameter_space:
                    qc = timeout_watcher(lib.create_circuit, self.timeout, parameter_instance)
                    if not qc:
                        break
                    assert isinstance(qc, QuantumCircuit)
                    if qc.num_qubits <= device.num_qubits:
                        res = timeout_watcher(
                            tket_helper.get_mapped_level,
                            self.timeout,
                            [qc, qc.num_qubits, device, file_precheck, False, self.qasm_output_path, qasm_format],
                        )
                        if not res:
                            break
                    else:
                        break

    def generate_native_gates_levels(
        self,
        file_precheck: bool,
        lib: ModuleType,
        parameter_space: list[tuple[int, str]] | list[int] | list[str] | range,
    ) -> None:
        """Generate native gates level benchmarks for a given benchmark."""
        for qasm_format in ["qasm2", "qasm3"]:
            for native_gateset in get_available_native_gatesets():
                for opt_level in [0, 1, 2, 3]:
                    for parameter_instance in parameter_space:
                        qc = timeout_watcher(lib.create_circuit, self.timeout, parameter_instance)
                        if not qc:
                            break
                        assert isinstance(qc, QuantumCircuit)
                        res = timeout_watcher(
                            qiskit_helper.get_native_gates_level,
                            self.timeout,
                            [
                                qc,
                                native_gateset,
                                qc.num_qubits,
                                opt_level,
                                file_precheck,
                                False,
                                self.qasm_output_path,
                                qasm_format,
                            ],
                        )
                        if not res:
                            break

                for parameter_instance in parameter_space:
                    qc = timeout_watcher(lib.create_circuit, self.timeout, parameter_instance)
                    if not qc:
                        break
                    assert isinstance(qc, QuantumCircuit)
                    res = timeout_watcher(
                        tket_helper.get_native_gates_level,
                        self.timeout,
                        [
                            qc,
                            native_gateset,
                            qc.num_qubits,
                            file_precheck,
                            False,
                            self.qasm_output_path,
                            qasm_format,
                        ],
                    )
                    if not res:
                        break

    def generate_alg_levels(
        self,
        file_precheck: bool,
        lib: ModuleType,
        parameter_space: list[tuple[int, str]] | list[int] | list[str] | range,
    ) -> None:
        """Generate algorithm level benchmarks for a given benchmark."""
        for function in [qiskit_helper.get_alg_level]:
            for parameter_instance in parameter_space:
                for qasm_format in ["qasm3"]:
                    qc = timeout_watcher(lib.create_circuit, self.timeout, parameter_instance)
                    if not qc:
                        break
                    assert isinstance(qc, QuantumCircuit)
                    res = timeout_watcher(
                        function,
                        self.timeout,
                        [qc, qc.num_qubits, file_precheck, False, self.qasm_output_path, qasm_format],
                    )
                    if not res:
                        break

    def generate_indep_levels(
        self,
        file_precheck: bool,
        lib: ModuleType,
        parameter_space: list[tuple[int, str]] | list[int] | list[str] | range,
    ) -> None:
        """Generate independent level benchmarks for a given benchmark."""
        for function in [qiskit_helper.get_indep_level, tket_helper.get_indep_level]:
            for parameter_instance in parameter_space:
                for qasm_format in ["qasm2", "qasm3"]:
                    qc = timeout_watcher(lib.create_circuit, self.timeout, parameter_instance)
                    if not qc:
                        break
                    assert isinstance(qc, QuantumCircuit)
                    res = timeout_watcher(
                        function,
                        self.timeout,
                        [qc, qc.num_qubits, file_precheck, False, self.qasm_output_path, qasm_format],
                    )
                    if not res:
                        break


@overload
def get_benchmark(
    benchmark_name: str,
    level: str | int,
    circuit_size: int | None = None,
    benchmark_instance_name: str | None = None,
    compiler: Literal["qiskit"] = "qiskit",
    compiler_settings: CompilerSettings | None = None,
    gateset: str | Gateset = "ibm_falcon",
    device_name: str = "ibm_washington",
    **kwargs: str,
) -> QuantumCircuit: ...


@overload
def get_benchmark(
    benchmark_name: str,
    level: str | int,
    circuit_size: int | None = None,
    benchmark_instance_name: str | None = None,
    compiler: Literal["tket"] = "tket",
    compiler_settings: CompilerSettings | None = None,
    gateset: str | Gateset = "ibm_falcon",
    device_name: str = "ibm_washington",
    **kwargs: str,
) -> Circuit: ...


@overload
def get_benchmark(
    benchmark_name: str,
    level: str | int,
    circuit_size: int | None = None,
    benchmark_instance_name: str | None = None,
    compiler: str = "qiskit",
    compiler_settings: CompilerSettings | None = None,
    gateset: str | Gateset = "ibm_falcon",
    device_name: str = "ibm_washington",
    **kwargs: str,
) -> QuantumCircuit | Circuit: ...


def get_benchmark(
    benchmark_name: str,
    level: str | int,
    circuit_size: int | None = None,
    benchmark_instance_name: str | None = None,
    compiler: str = "qiskit",
    compiler_settings: CompilerSettings | None = None,
    gateset: str | Gateset = "ibm_falcon",
    device_name: str = "ibm_washington",
    **kwargs: str,
) -> QuantumCircuit | Circuit:
    """Returns one benchmark as a qiskit.QuantumCircuit Object or a pytket.Circuit object.

    Arguments:
        benchmark_name: name of the to be generated benchmark
        level: Choice of level, either as a string ("alg", "indep", "nativegates" or "mapped") or as a number between 0-3 where 0 corresponds to "alg" level and 3 to "mapped" level
        circuit_size: Input for the benchmark creation, in most cases this is equal to the qubit number
        benchmark_instance_name: Input selection for some benchmarks, namely and "shor"
        compiler: "qiskit" or "tket"
        compiler_settings: Data class containing the respective compiler settings for the specified compiler (e.g., optimization level for Qiskit)
        gateset: Name of the gateset or tuple containing the name of the gateset and the gateset itself (required for "nativegates" level)
        device_name: "ibm_washington", "ibm_montreal", "rigetti_aspen_m3", "ionq_harmony", "ionq_aria1", "oqc_lucy", "quantinuum_h2" (required for "mapped" level)
        kwargs: Additional arguments for the benchmark generation

    Returns:
        Quantum Circuit Object representing the benchmark with the selected options, either as Qiskit::QuantumCircuit or Pytket::Circuit object (depending on the chosen compiler---while the algorithm level is always provided using Qiskit)
    """
    if benchmark_name not in get_supported_benchmarks():
        msg = f"Selected benchmark is not supported. Valid benchmarks are {get_supported_benchmarks()}."
        raise ValueError(msg)

    if level not in get_supported_levels():
        msg = f"Selected level must be in {get_supported_levels()}."
        raise ValueError(msg)

    if benchmark_name != "shor" and not (isinstance(circuit_size, int) and circuit_size > 0):
        msg = "circuit_size must be None or int for this benchmark."
        raise ValueError(msg)

    if benchmark_name == "shor" and not isinstance(benchmark_instance_name, str):
        msg = "benchmark_instance_name must be defined for this benchmark."
        raise ValueError(msg)

    lib = get_module_for_benchmark(
        benchmark_name.split("-")[0]
    )  # split is used to filter the ancillary mode for grover and qwalk

    if "grover" in benchmark_name or "qwalk" in benchmark_name:
        if "noancilla" in benchmark_name:
            anc_mode = "noancilla"
        elif "v-chain" in benchmark_name:
            anc_mode = "v-chain"

        qc = lib.create_circuit(circuit_size, ancillary_mode=anc_mode)

    elif benchmark_name == "shor":
        to_be_factored_number, a_value = lib.get_instance(benchmark_instance_name)
        qc = lib.create_circuit(to_be_factored_number, a_value)

    else:
        qc = lib.create_circuit(circuit_size)

    if level in ("alg", 0):
        return qc

    compiler = compiler.lower()

    if compiler.lower() not in get_supported_compilers():
        msg = f"Selected compiler must be in {get_supported_compilers()}."
        raise ValueError(msg)

    if compiler_settings is None:
        compiler_settings = CompilerSettings(QiskitSettings())
    elif not isinstance(compiler_settings, CompilerSettings):
        msg = "compiler_settings must be of type CompilerSettings or None."  # type: ignore[unreachable]
        raise ValueError(msg)

    independent_level = 1
    if level in ("indep", independent_level):
        if compiler == "qiskit":
            return qiskit_helper.get_indep_level(qc, circuit_size, False, True)
        if compiler == "tket":
            return tket_helper.get_indep_level(qc, circuit_size, False, True)

    native_gates_level = 2
    if level in ("nativegates", native_gates_level):
        if isinstance(gateset, str):
            gateset = get_native_gateset_by_name(gateset)
        if compiler == "qiskit":
            assert compiler_settings.qiskit is not None
            opt_level = compiler_settings.qiskit.optimization_level
            return qiskit_helper.get_native_gates_level(qc, gateset, circuit_size, opt_level, False, True)
        if compiler == "tket":
            return tket_helper.get_native_gates_level(qc, gateset, circuit_size, False, True)

    if device_name not in get_available_device_names():
        msg = f"Selected device_name must be in {get_available_device_names()}."
        raise ValueError(msg)

    mapped_level = 3
    if level in ("mapped", mapped_level):
        device = get_device_by_name(device_name)
        if compiler == "qiskit":
            assert compiler_settings.qiskit is not None
            opt_level = compiler_settings.qiskit.optimization_level
            assert isinstance(opt_level, int)
            return qiskit_helper.get_mapped_level(
                qc,
                circuit_size,
                device,
                opt_level,
                False,
                True,
            )
        if compiler == "tket":
            return tket_helper.get_mapped_level(
                qc,
                circuit_size,
                device,
                False,
                True,
            )
    return None


def generate(num_jobs: int = -1) -> None:
    """Generate benchmarks based on the configuration file."""
    parser = argparse.ArgumentParser(description="Create Configuration")
    parser.add_argument("--file-name", type=str, help="optional filename", default=None)
    args = parser.parse_args()
    benchmark_generator = BenchmarkGenerator(args.file_name)
    benchmark_generator.create_benchmarks_from_config(num_jobs)


def timeout_watcher(
    func: Callable[..., bool | QuantumCircuit],
    timeout: int,
    args: list[Any] | int | tuple[int, str] | str,
) -> bool | QuantumCircuit | Circuit:
    """Function to handle timeouts for the benchmark generation."""
    if sys.platform == "win32":
        warn("Timeout is not supported on Windows.", category=RuntimeWarning, stacklevel=2)
        return func(*args) if isinstance(args, tuple | list) else func(args)

    class TimeoutExceptionError(Exception):  # Custom exception class
        """Custom exception class for timeout."""

    def timeout_handler(_signum: int, _frame: Any) -> None:  # noqa: ANN401
        """Function to handle the timeout."""
        raise TimeoutExceptionError

    # Change the behavior of SIGALRM
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(timeout)
    try:
        res = func(*args) if isinstance(args, tuple | list) else func(args)
    except TimeoutExceptionError:
        print(
            "Calculation/Generation exceeded timeout limit for ",
            func.__name__,
            func.__module__.split(".")[-1],
        )
        if isinstance(args, list) and isinstance(args[0], QuantumCircuit):
            print(args[0].name, args[1:])
        else:
            print(args)
        return False
    except Exception as e:
        print(
            "Exception: ",
            e,
            func.__name__,
            func.__module__.split(".")[-1],
            args,
        )
        return False
    else:
        # Reset the alarm
        signal.alarm(0)

    return res
