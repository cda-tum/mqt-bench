from __future__ import annotations

import argparse
import json
import signal
import sys
from pathlib import Path
from typing import TYPE_CHECKING, Any, Callable, TypedDict

from joblib import Parallel, delayed
from mqt.bench import qiskit_helper, tket_helper, utils
from qiskit import QuantumCircuit

if TYPE_CHECKING:  # pragma: no cover
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

    def create_benchmarks_from_config(self, num_jobs: int = -1) -> bool:
        benchmarks = [Benchmark(benchmark) for benchmark in self.cfg["benchmarks"]]  # type: ignore[misc]
        Parallel(n_jobs=num_jobs, verbose=100)(delayed(self.generate_benchmark)(benchmark) for benchmark in benchmarks)
        return True

    def generate_benchmark(self, benchmark: Benchmark) -> None:  # noqa: PLR0912
        lib = utils.get_module_for_benchmark(benchmark["name"])
        file_precheck = benchmark["precheck_possible"]
        if benchmark["include"]:
            if benchmark["name"] == "grover" or benchmark["name"] == "qwalk":
                for anc_mode in benchmark["ancillary_mode"]:
                    for n in range(
                        benchmark["min_qubits"],
                        benchmark["max_qubits"],
                        benchmark["stepsize"],
                    ):
                        success_flag = self.start_benchmark_generation(lib.create_circuit, [n, anc_mode], file_precheck)
                        if not success_flag:
                            break

            elif benchmark["name"] == "shor":
                for choice in benchmark["instances"]:
                    to_be_factored_number, a_value = lib.get_instance(choice)
                    success_flag = self.start_benchmark_generation(
                        lib.create_circuit, [to_be_factored_number, a_value], file_precheck
                    )
                    if not success_flag:
                        break

            elif benchmark["name"] == "hhl":
                for i in range(benchmark["min_index"], benchmark["max_index"]):
                    success_flag = self.start_benchmark_generation(lib.create_circuit, [i], file_precheck)
                    if not success_flag:
                        break

            elif benchmark["name"] == "routing":
                for nodes in range(benchmark["min_nodes"], benchmark["max_nodes"]):
                    success_flag = self.start_benchmark_generation(lib.create_circuit, [nodes, 2], file_precheck)
                    if not success_flag:
                        break

            elif benchmark["name"] == "tsp":
                for nodes in range(benchmark["min_nodes"], benchmark["max_nodes"]):
                    success_flag = self.start_benchmark_generation(lib.create_circuit, [nodes], file_precheck)
                    if not success_flag:
                        break

            elif benchmark["name"] == "groundstate":
                for choice in benchmark["instances"]:
                    success_flag = self.start_benchmark_generation(lib.create_circuit, [choice], file_precheck)
                    if not success_flag:
                        break

            elif benchmark["name"] == "pricingcall" or benchmark["name"] == "pricingput":
                for nodes in range(benchmark["min_uncertainty"], benchmark["max_uncertainty"]):
                    success_flag = self.start_benchmark_generation(lib.create_circuit, [nodes], file_precheck)
                    if not success_flag:
                        break
            else:
                for n in range(
                    benchmark["min_qubits"],
                    benchmark["max_qubits"],
                    benchmark["stepsize"],
                ):
                    success_flag = self.start_benchmark_generation(lib.create_circuit, [n], file_precheck)
                    if not success_flag:
                        break

    def generate_circuits_on_all_levels(self, qc: QuantumCircuit, num_qubits: int, file_precheck: bool) -> bool:
        success_generated_circuits_t_indep = self.generate_target_indep_level_circuit(qc, num_qubits, file_precheck)

        if not success_generated_circuits_t_indep:
            return False

        self.generate_target_dep_level_circuit(qc, num_qubits, file_precheck)
        return True

    def generate_target_indep_level_circuit(self, qc: QuantumCircuit, num_qubits: int, file_precheck: bool) -> bool:
        num_generated_circuits = 0
        res_indep_qiskit = timeout_watcher(
            qiskit_helper.get_indep_level,
            self.timeout,
            [qc, num_qubits, file_precheck, False, self.qasm_output_path],
        )
        if res_indep_qiskit:
            num_generated_circuits += 1

        res_indep_tket = timeout_watcher(
            tket_helper.get_indep_level,
            self.timeout,
            [qc, num_qubits, file_precheck, False, self.qasm_output_path],
        )
        if res_indep_tket:
            num_generated_circuits += 1

        return num_generated_circuits != 0

    def generate_target_dep_level_circuit(self, qc: QuantumCircuit, num_qubits: int, file_precheck: bool) -> bool:
        compilation_paths: list[tuple[str, list[tuple[str, int]]]] = [
            ("ibm", [("ibm_washington", 127), ("ibm_montreal", 27)]),
            ("rigetti", [("rigetti_aspen_m2", 80)]),
            ("ionq", [("ionq11", 11)]),
            ("oqc", [("oqc_lucy", 8)]),
        ]
        num_generated_benchmarks = 0
        for gate_set_name, devices in compilation_paths:
            # Creating the circuit on both target-dependent levels for qiskit
            for opt_level in range(4):
                res = timeout_watcher(
                    qiskit_helper.get_native_gates_level,
                    self.timeout,
                    [
                        qc,
                        gate_set_name,
                        num_qubits,
                        opt_level,
                        file_precheck,
                        False,
                        self.qasm_output_path,
                    ],
                )
                if not res:
                    break
                num_generated_benchmarks += 1

            for device_name, max_qubits in devices:
                for opt_level in range(4):
                    # Creating the circuit on target-dependent: mapped level qiskit
                    if max_qubits >= qc.num_qubits:
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
                                self.qasm_output_path,
                            ],
                        )
                        if not res:
                            break
                        num_generated_benchmarks += 1

            # Creating the circuit on both target-dependent levels for tket

            res = timeout_watcher(
                tket_helper.get_native_gates_level,
                self.timeout,
                [
                    qc,
                    gate_set_name,
                    num_qubits,
                    file_precheck,
                    False,
                    self.qasm_output_path,
                ],
            )
            if not res:
                continue
            num_generated_benchmarks += 1

            for device_name, max_qubits in devices:
                if max_qubits >= qc.num_qubits:
                    for lineplacement in (False, True):
                        # Creating the circuit on target-dependent: mapped level tket
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
                            continue
                        num_generated_benchmarks += 1
        return num_generated_benchmarks != 0

    def start_benchmark_generation(
        self, create_circuit_function: Callable[..., QuantumCircuit], parameters: list[int | str], file_precheck: bool
    ) -> bool:
        res_qc_creation = timeout_watcher(create_circuit_function, self.timeout, parameters)
        if not res_qc_creation:
            return False
        assert isinstance(res_qc_creation, QuantumCircuit)
        return self.generate_circuits_on_all_levels(res_qc_creation, res_qc_creation.num_qubits, file_precheck)


def get_benchmark(  # noqa: PLR0911, PLR0912, PLR0915
    benchmark_name: str,
    level: str | int,
    circuit_size: int | None = None,
    benchmark_instance_name: str | None = None,
    compiler: str | None = "qiskit",
    compiler_settings: CompilerSettings | None = None,
    gate_set_name: str | None = "ibm",
    device_name: str | None = "ibm_washington",
) -> QuantumCircuit | Circuit:
    """Returns one benchmark as a Qiskit::QuantumCircuit Object.
    Keyword arguments:
    benchmark_name -- name of the to be generated benchmark
    level -- Choice of level, either as a string ("alg", "indep", "nativegates" or "mapped") or as a number between 0-3 where 0 corresponds to "alg" level and 3 to "mapped" level
    circuit_size -- Input for the benchmark creation, in most cases this is equal to the qubit number
    benchmark_instance_name -- Input selection for some benchmarks, namely "groundstate" and "shor"
    compiler -- "qiskit" or "tket"
    CompilerSettings -- Data class containing the respective compiler settings for the specified compiler (e.g., optimization level for Qiskit or placement for TKET)
    gate_set_name -- "ibm", "rigetti", "ionq", or "oqc"
    device_name -- "ibm_washington", "ibm_montreal", "rigetti_aspen_m2", "ionq11", ""oqc_lucy""
    Return values:
    Quantum Circuit Object -- Representing the benchmark with the selected options, either as Qiskit::QuantumCircuit or Pytket::Circuit object (depending on the chosen compiler---while the algorithm level is always provided using Qiskit)
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

    if compiler is not None and compiler.lower() not in utils.get_supported_compilers():
        msg = f"Selected compiler must be in {utils.get_supported_compilers()}."
        raise ValueError(msg)

    if compiler_settings is not None and not isinstance(compiler_settings, CompilerSettings):
        msg = "compiler_settings must be of type CompilerSettings or None."  # type:ignore[unreachable]
        raise ValueError(msg)

    if gate_set_name is not None and gate_set_name not in utils.get_supported_gatesets():
        msg = f"Selected gate_set_name must be None or in {utils.get_supported_gatesets()}."
        raise ValueError(msg)

    if device_name is not None and device_name not in utils.get_supported_devices():
        msg = f"Selected device_name must be None or in {utils.get_supported_devices()}."
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

    if level == "alg" or level == 0:
        return qc

    if compiler is None:
        msg = "Compiler must be specified for non-algorithmic levels."
        raise ValueError(msg)

    compiler = compiler.lower()

    if compiler not in utils.get_supported_compilers():
        msg = f"Selected compiler must be in {utils.get_supported_compilers()}."
        raise ValueError(msg)

    if compiler_settings is None:
        compiler_settings = CompilerSettings(QiskitSettings(), TKETSettings())
    assert (compiler_settings.tket is not None) or (compiler_settings.qiskit is not None)

    independent_level = 1
    if level == "indep" or level == independent_level:
        if compiler == "qiskit":
            return qiskit_helper.get_indep_level(qc, circuit_size, False, True)
        if compiler == "tket":
            return tket_helper.get_indep_level(qc, circuit_size, False, True)

    native_gates_level = 2
    if level == "nativegates" or level == native_gates_level:
        assert gate_set_name is not None
        if compiler == "qiskit":
            assert compiler_settings.qiskit is not None
            opt_level = compiler_settings.qiskit.optimization_level
            return qiskit_helper.get_native_gates_level(qc, gate_set_name, circuit_size, opt_level, False, True)
        if compiler == "tket":
            return tket_helper.get_native_gates_level(qc, gate_set_name, circuit_size, False, True)

    mapped_level = 3
    if level == "mapped" or level == mapped_level:
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
    func: Callable[..., bool | QuantumCircuit], timeout: int, args: list[Any]
) -> bool | QuantumCircuit | Circuit:
    class TimeoutException(Exception):  # Custom exception class
        pass

    def timeout_handler(_signum: Any, _frame: Any) -> None:  # Custom signal handler
        raise TimeoutException()

    # Change the behavior of SIGALRM
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(timeout)
    try:
        res = func(*args)
    except TimeoutException:
        print(
            "Calculation/Generation exceeded timeout limit for ",
            func.__name__,
            func.__module__.split(".")[-1],
            args[0].name,
            args[1:],
        )
        return False
    except Exception as e:
        print(
            "Exception: ",
            e,
            func.__name__,
            func.__module__.split(".")[-1],
            args[0],
            args[1:],
        )
        return False
    else:
        # Reset the alarm
        signal.alarm(0)

    return res
