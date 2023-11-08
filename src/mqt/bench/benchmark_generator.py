from __future__ import annotations

import argparse
import json
import signal
import sys
from pathlib import Path
from typing import TYPE_CHECKING, Any, Callable, Literal, TypedDict, overload

from joblib import Parallel, delayed
from qiskit import QuantumCircuit

from mqt.bench import qiskit_helper, tket_helper, utils

if TYPE_CHECKING:  # pragma: no cover
    from types import ModuleType

    from pytket.circuit import Circuit

if TYPE_CHECKING or sys.version_info >= (3, 10, 0):  # pragma: no cover
    from importlib import resources
else:
    import importlib_resources as resources

from dataclasses import dataclass


class Benchmark(TypedDict, total=False):
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
    optimization_level: int = 1


@dataclass
class TKETSettings:
    placement: str = "lineplacement"


@dataclass
class CompilerSettings:
    qiskit: QiskitSettings | None = None
    tket: TKETSettings | None = None


class BenchmarkGenerator:
    def __init__(self, cfg_path: str = "./config.json", qasm_output_path: str | None = None) -> None:
        with Path(cfg_path).open() as jsonfile:
            self.cfg = json.load(jsonfile)
            print("Read config successful")
        self.timeout = self.cfg["timeout"]
        if qasm_output_path is None:
            self.qasm_output_path = str(resources.files("mqt.benchviewer") / "static" / "files" / "qasm_output")
        else:
            self.qasm_output_path = qasm_output_path

        Path(self.qasm_output_path).mkdir(exist_ok=True, parents=True)

    def create_benchmarks_from_config(self, num_jobs: int) -> bool:
        benchmarks = [Benchmark(benchmark) for benchmark in self.cfg["benchmarks"]]  # type: ignore[misc]
        Parallel(n_jobs=num_jobs, verbose=100)(
            delayed(self.define_benchmark_instances)(benchmark) for benchmark in benchmarks
        )
        return True

    def define_benchmark_instances(self, benchmark: Benchmark) -> None:
        lib = utils.get_module_for_benchmark(benchmark["name"])
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

            elif benchmark["name"] in ("routing", "tsp"):
                instances = range(benchmark["min_nodes"], benchmark["max_nodes"])

            elif benchmark["name"] == "groundstate":
                instances = benchmark["instances"]

            elif benchmark["name"] in ("pricingcall", "pricingput"):
                instances = range(benchmark["min_uncertainty"], benchmark["max_uncertainty"])

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
        self.generate_indep_levels(file_precheck, lib, parameter_space)
        self.generate_native_gates_levels(file_precheck, lib, parameter_space)
        self.generate_mapped_levels(file_precheck, lib, parameter_space)

    def generate_mapped_levels(
        self,
        file_precheck: bool,
        lib: ModuleType,
        parameter_space: list[tuple[int, str]] | list[int] | list[str] | range,
    ) -> None:
        for gate_set_name, devices in utils.get_compilation_paths():
            for device_name, max_qubits in devices:
                for opt_level in range(4):
                    for parameter_instance in parameter_space:
                        qc = timeout_watcher(lib.create_circuit, self.timeout, parameter_instance)
                        if not qc:
                            break
                        assert isinstance(qc, QuantumCircuit)
                        if qc.num_qubits <= max_qubits:
                            res = timeout_watcher(
                                qiskit_helper.get_mapped_level,
                                self.timeout,
                                [
                                    qc,
                                    gate_set_name,
                                    qc.num_qubits,
                                    device_name,
                                    opt_level,
                                    file_precheck,
                                    False,
                                    self.qasm_output_path,
                                ],
                            )
                            if not res:
                                break
                        else:
                            break

                for lineplacement in (False, True):
                    for parameter_instance in parameter_space:
                        qc = timeout_watcher(lib.create_circuit, self.timeout, parameter_instance)
                        if not qc:
                            break
                        assert isinstance(qc, QuantumCircuit)
                        if qc.num_qubits <= max_qubits:
                            res = timeout_watcher(
                                tket_helper.get_mapped_level,
                                self.timeout,
                                [
                                    qc,
                                    gate_set_name,
                                    qc.num_qubits,
                                    device_name,
                                    lineplacement,
                                    file_precheck,
                                    False,
                                    self.qasm_output_path,
                                ],
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
        for gate_set in utils.get_supported_gatesets():
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
                            gate_set,
                            qc.num_qubits,
                            opt_level,
                            file_precheck,
                            False,
                            self.qasm_output_path,
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
                        gate_set,
                        qc.num_qubits,
                        file_precheck,
                        False,
                        self.qasm_output_path,
                    ],
                )
                if not res:
                    break

    def generate_indep_levels(
        self,
        file_precheck: bool,
        lib: ModuleType,
        parameter_space: list[tuple[int, str]] | list[int] | list[str] | range,
    ) -> None:
        for function in [qiskit_helper.get_indep_level, tket_helper.get_indep_level]:
            for parameter_instance in parameter_space:
                qc = timeout_watcher(lib.create_circuit, self.timeout, parameter_instance)
                if not qc:
                    break
                assert isinstance(qc, QuantumCircuit)
                res = timeout_watcher(
                    function,
                    self.timeout,
                    [qc, qc.num_qubits, file_precheck, False, self.qasm_output_path],
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
    gate_set_name: str = "ibm",
    device_name: str = "ibm_washington",
) -> QuantumCircuit:
    ...


@overload
def get_benchmark(
    benchmark_name: str,
    level: str | int,
    circuit_size: int | None = None,
    benchmark_instance_name: str | None = None,
    compiler: Literal["tket"] = "tket",
    compiler_settings: CompilerSettings | None = None,
    gate_set_name: str = "ibm",
    device_name: str = "ibm_washington",
) -> Circuit:
    ...


@overload
def get_benchmark(
    benchmark_name: str,
    level: str | int,
    circuit_size: int | None = None,
    benchmark_instance_name: str | None = None,
    compiler: str = "qiskit",
    compiler_settings: CompilerSettings | None = None,
    gate_set_name: str = "ibm",
    device_name: str = "ibm_washington",
) -> QuantumCircuit | Circuit:
    ...


def get_benchmark(
    benchmark_name: str,
    level: str | int,
    circuit_size: int | None = None,
    benchmark_instance_name: str | None = None,
    compiler: str = "qiskit",
    compiler_settings: CompilerSettings | None = None,
    gate_set_name: str = "ibm",
    device_name: str = "ibm_washington",
) -> QuantumCircuit | Circuit:
    """Returns one benchmark as a qiskit.QuantumCircuit Object or a pytket.Circuit object.

    Args:
        benchmark_name: name of the to be generated benchmark
        level: Choice of level, either as a string ("alg", "indep", "nativegates" or "mapped") or as a number between 0-3 where 0 corresponds to "alg" level and 3 to "mapped" level
        circuit_size: Input for the benchmark creation, in most cases this is equal to the qubit number
        benchmark_instance_name: Input selection for some benchmarks, namely "groundstate" and "shor"
        compiler: "qiskit" or "tket"
        CompilerSettings: Data class containing the respective compiler settings for the specified compiler (e.g., optimization level for Qiskit or placement for TKET)
        gate_set_name: "ibm", "rigetti", "ionq", "oqc", or "quantinuum"
        device_name: "ibm_washington", "ibm_montreal", "rigetti_aspen_m2", "ionq_harmony", "ionq_aria1", "oqc_lucy", "quantinuum_h2",

    Returns:
        Quantum Circuit Object representing the benchmark with the selected options, either as Qiskit::QuantumCircuit or Pytket::Circuit object (depending on the chosen compiler---while the algorithm level is always provided using Qiskit)
    """

    if benchmark_name not in utils.get_supported_benchmarks():
        msg = f"Selected benchmark is not supported. Valid benchmarks are {utils.get_supported_benchmarks()}."
        raise ValueError(msg)

    if level not in utils.get_supported_levels():
        msg = f"Selected level must be in {utils.get_supported_levels()}."
        raise ValueError(msg)

    if benchmark_name not in ["shor", "groundstate"] and not (isinstance(circuit_size, int) and circuit_size > 0):
        msg = "circuit_size must be None or int for this benchmark."
        raise ValueError(msg)

    if benchmark_name in ["shor", "groundstate"] and not isinstance(benchmark_instance_name, str):
        msg = "benchmark_instance_name must be defined for this benchmark."
        raise ValueError(msg)

    lib = utils.get_module_for_benchmark(
        benchmark_name.split("-")[0]
    )  # split is used to filter the ancillary mode for grover and qwalk

    if "grover" in benchmark_name or "qwalk" in benchmark_name:
        if "noancilla" in benchmark_name:
            anc_mode = "noancilla"
        elif "v-chain" in benchmark_name:
            anc_mode = "v-chain"
        else:
            msg = "Either `noancilla` or `v-chain` must be specified for ancillary mode of Grover and QWalk benchmarks."
            raise ValueError(msg)

        qc = lib.create_circuit(circuit_size, ancillary_mode=anc_mode)

    elif benchmark_name == "shor":
        to_be_factored_number, a_value = lib.get_instance(benchmark_instance_name)
        qc = lib.create_circuit(to_be_factored_number, a_value)

    elif benchmark_name == "groundstate":
        qc = lib.create_circuit(benchmark_instance_name)

    else:
        qc = lib.create_circuit(circuit_size)

    if level in ("alg", 0):
        return qc

    compiler = compiler.lower()

    if compiler.lower() not in utils.get_supported_compilers():
        msg = f"Selected compiler must be in {utils.get_supported_compilers()}."
        raise ValueError(msg)

    if compiler_settings is None:
        compiler_settings = CompilerSettings(QiskitSettings(), TKETSettings())
    elif not isinstance(compiler_settings, CompilerSettings):
        msg = "compiler_settings must be of type CompilerSettings or None."  # type: ignore[unreachable]
        raise ValueError(msg)

    assert (compiler_settings.tket is not None) or (compiler_settings.qiskit is not None)

    independent_level = 1
    if level in ("indep", independent_level):
        if compiler == "qiskit":
            return qiskit_helper.get_indep_level(qc, circuit_size, False, True)
        if compiler == "tket":
            return tket_helper.get_indep_level(qc, circuit_size, False, True)

    if gate_set_name not in utils.get_supported_gatesets():
        msg = f"Selected gate_set_name must be in {utils.get_supported_gatesets()}."
        raise ValueError(msg)

    native_gates_level = 2
    if level in ("nativegates", native_gates_level):
        assert gate_set_name is not None
        if compiler == "qiskit":
            assert compiler_settings.qiskit is not None
            opt_level = compiler_settings.qiskit.optimization_level
            return qiskit_helper.get_native_gates_level(qc, gate_set_name, circuit_size, opt_level, False, True)
        if compiler == "tket":
            return tket_helper.get_native_gates_level(qc, gate_set_name, circuit_size, False, True)

    if device_name not in utils.get_supported_devices():
        msg = f"Selected device_name must be in {utils.get_supported_devices()}."
        raise ValueError(msg)

    mapped_level = 3
    if level in ("mapped", mapped_level):
        assert gate_set_name is not None
        assert device_name is not None
        if compiler == "qiskit":
            assert compiler_settings.qiskit is not None
            opt_level = compiler_settings.qiskit.optimization_level
            assert isinstance(opt_level, int)
            return qiskit_helper.get_mapped_level(
                qc,
                gate_set_name,
                circuit_size,
                device_name,
                opt_level,
                False,
                True,
            )
        if compiler == "tket":
            assert compiler_settings.tket is not None
            placement = compiler_settings.tket.placement.lower()
            lineplacement = placement == "lineplacement"
            return tket_helper.get_mapped_level(
                qc,
                gate_set_name,
                circuit_size,
                device_name,
                lineplacement,
                False,
                True,
            )

    msg = f"Invalid level specified. Must be in {utils.get_supported_levels()}."
    raise ValueError(msg)


def generate(num_jobs: int = -1) -> None:
    parser = argparse.ArgumentParser(description="Create Configuration")
    parser.add_argument("--file-name", type=str, help="optional filename", default="./config.json")
    args = parser.parse_args()
    benchmark_generator = BenchmarkGenerator(args.file_name)
    benchmark_generator.create_benchmarks_from_config(num_jobs)


def timeout_watcher(
    func: Callable[..., bool | QuantumCircuit],
    timeout: int,
    args: list[Any] | int | tuple[int, str] | str,
) -> bool | QuantumCircuit | Circuit:
    class TimeoutException(Exception):  # Custom exception class
        pass

    def timeout_handler(_signum: Any, _frame: Any) -> None:  # Custom signal handler
        raise TimeoutException

    # Change the behavior of SIGALRM
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(timeout)
    try:
        res = func(*args) if isinstance(args, (tuple, list)) else func(args)
    except TimeoutException:
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
