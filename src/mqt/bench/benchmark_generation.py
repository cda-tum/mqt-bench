"""Module for the benchmark generation and benchmark retrieval."""

from __future__ import annotations

from importlib import import_module, resources
from pathlib import Path
from typing import TYPE_CHECKING, Literal, TypedDict, overload

from qiskit import QuantumCircuit, transpile

from .devices import (
    get_available_device_names,
    get_available_provider_names,
    get_device_by_name,
    get_provider_by_name,
)
from .output import (
    save_as_qasm,
)

if TYPE_CHECKING:  # pragma: no cover
    from types import ModuleType

    from .devices import Device, Provider

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


def get_alg_level(
    qc: QuantumCircuit,
    num_qubits: int | None,
    file_precheck: bool,
    return_qc: bool = False,
    target_directory: str = "./",
    target_filename: str = "",
    output_format: str = "qasm3",
) -> bool | QuantumCircuit:
    """Handles the creation of the benchmark on the algorithm level.

    Arguments:
        qc: quantum circuit which the to be created benchmark circuit is based on
        num_qubits: number of qubits
        file_precheck: flag indicating whether to check whether the file already exists before creating it (again)
        return_qc: flag if the actual circuit shall be returned
        target_directory: alternative directory to the default one to store the created circuit
        target_filename: alternative filename to the default one
        output_format: qasm format (qasm2 or qasm3)


    Returns:
        if return_qc == True: quantum circuit object
        else: True/False indicating whether the function call was successful or not
    """
    if return_qc:
        return qc

    if output_format == "qasm2":
        msg = "'qasm2' is not supported for the algorithm level, please use 'qasm3' instead."
        raise ValueError(msg)
    filename_alg = target_filename or qc.name + "_alg_" + str(num_qubits) + "_" + output_format

    path = Path(target_directory, filename_alg + ".qasm")

    if file_precheck and path.is_file():
        return True

    return save_as_qasm(qc=qc, filename=filename_alg, output_format="qasm3", target_directory=target_directory)


@overload
def get_indep_level(
    qc: QuantumCircuit,
    num_qubits: int | None,
    file_precheck: bool,
    return_qc: Literal[True],
    target_directory: str = "./",
    target_filename: str = "",
    output_format: str = "qasm3",
) -> QuantumCircuit: ...


@overload
def get_indep_level(
    qc: QuantumCircuit,
    num_qubits: int | None,
    file_precheck: bool,
    return_qc: Literal[False],
    target_directory: str = "./",
    target_filename: str = "",
    output_format: str = "qasm3",
) -> bool: ...


def get_indep_level(
    qc: QuantumCircuit,
    num_qubits: int | None,
    file_precheck: bool,
    return_qc: bool = False,
    target_directory: str = "./",
    target_filename: str = "",
    output_format: str = "qasm3",
) -> bool | QuantumCircuit:
    """Handles the creation of the benchmark on the target-independent level.

    Arguments:
        qc: quantum circuit which the to be created benchmark circuit is based on
        num_qubits: number of qubits
        file_precheck: flag indicating whether to check whether the file already exists before creating it (again)
        return_qc: flag if the actual circuit shall be returned
        target_directory: alternative directory to the default one to store the created circuit
        target_filename: alternative filename to the default one
        output_format: qasm format (qasm2 or qasm3)


    Returns:
        if return_qc == True: quantum circuit object
        else: True/False indicating whether the function call was successful or not
    """
    filename_indep = target_filename or qc.name + "_indep_" + str(num_qubits) + "_" + output_format

    path = Path(target_directory, filename_indep + ".qasm")
    if file_precheck and path.is_file():
        return True
    openqasm_gates = get_openqasm_gates()
    target_independent = transpile(qc, basis_gates=openqasm_gates, optimization_level=1, seed_transpiler=10)

    if return_qc:
        return target_independent

    return save_as_qasm(
        qc=target_independent, filename=filename_indep, output_format=output_format, target_directory=target_directory
    )


@overload
def get_native_gates_level(
    qc: QuantumCircuit,
    provider: Provider,
    num_qubits: int | None,
    opt_level: int,
    file_precheck: bool,
    return_qc: Literal[True],
    target_directory: str = "./",
    target_filename: str = "",
    output_format: str = "qasm3",
) -> QuantumCircuit: ...


@overload
def get_native_gates_level(
    qc: QuantumCircuit,
    provider: Provider,
    num_qubits: int | None,
    opt_level: int,
    file_precheck: bool,
    return_qc: Literal[False],
    target_directory: str = "./",
    target_filename: str = "",
    output_format: str = "qasm3",
) -> bool: ...


def get_native_gates_level(
    qc: QuantumCircuit,
    provider: Provider,
    num_qubits: int | None,
    opt_level: int,
    file_precheck: bool,
    return_qc: bool = False,
    target_directory: str = "./",
    target_filename: str = "",
    output_format: str = "qasm3",
) -> bool | QuantumCircuit:
    """Handles the creation of the benchmark on the target-dependent native gates level.

    Arguments:
        qc: quantum circuit which the to be created benchmark circuit is based on
        provider: determines the native gate set
        num_qubits: number of qubits
        opt_level: optimization level
        file_precheck: flag indicating whether to check whether the file already exists before creating it (again)
        return_qc: flag if the actual circuit shall be returned
        target_directory: alternative directory to the default one to store the created circuit
        target_filename: alternative filename to the default one
        output_format: qasm format (qasm2 or qasm3)

    Returns:
        if return_qc == True: quantum circuit object
        else: True/False indicating whether the function call was successful or not
    """
    if not target_filename:
        filename_native = (
            qc.name + "_nativegates_" + provider.provider_name + "_opt" + str(opt_level) + "_" + str(num_qubits)
        )
    else:
        filename_native = target_filename

    path = Path(target_directory, filename_native + ".qasm")
    if file_precheck and path.is_file():
        return True

    gate_set = provider.get_native_gates()
    compiled_without_architecture = transpile(
        qc, basis_gates=gate_set, optimization_level=opt_level, seed_transpiler=10
    )
    if return_qc:
        return compiled_without_architecture

    return save_as_qasm(
        qc=compiled_without_architecture,
        filename=filename_native,
        output_format=output_format,
        gate_set=gate_set,
        target_directory=target_directory,
    )


@overload
def get_mapped_level(
    qc: QuantumCircuit,
    num_qubits: int | None,
    device: Device,
    opt_level: int,
    file_precheck: bool,
    return_qc: Literal[True],
    target_directory: str = "./",
    target_filename: str = "",
    output_format: str = "qasm3",
) -> QuantumCircuit: ...


@overload
def get_mapped_level(
    qc: QuantumCircuit,
    num_qubits: int | None,
    device: Device,
    opt_level: int,
    file_precheck: bool,
    return_qc: Literal[False],
    target_directory: str = "./",
    target_filename: str = "",
    output_format: str = "qasm3",
) -> bool: ...


def get_mapped_level(
    qc: QuantumCircuit,
    num_qubits: int | None,
    device: Device,
    opt_level: int,
    file_precheck: bool,
    return_qc: bool = False,
    target_directory: str = "./",
    target_filename: str = "",
    output_format: str = "qasm3",
) -> bool | QuantumCircuit:
    """Handles the creation of the benchmark on the target-dependent mapped level.

    Arguments:
        qc: quantum circuit which the to be created benchmark circuit is based on
        num_qubits: number of qubits
        device: target device
        opt_level: optimization level
        file_precheck: flag indicating whether to check whether the file already exists before creating it (again)
        return_qc: flag if the actual circuit shall be returned
        target_directory: alternative directory to the default one to store the created circuit
        target_filename: alternative filename to the default one
        output_format: qasm format (qasm2 or qasm3)

    Returns:
        if return_qc == True: quantum circuit object
        else: True/False indicating whether the function call was successful or not
    """
    if not target_filename:
        filename_mapped = qc.name + "_mapped_" + device.name + "_opt" + str(opt_level) + "_" + str(num_qubits)
    else:
        filename_mapped = target_filename

    path = Path(target_directory, filename_mapped + ".qasm")
    if file_precheck and path.is_file():
        return True

    c_map = device.coupling_map
    compiled_with_architecture = transpile(
        qc,
        optimization_level=opt_level,
        basis_gates=device.basis_gates,
        coupling_map=c_map,
        seed_transpiler=10,
    )
    if return_qc:
        return compiled_with_architecture

    return save_as_qasm(
        qc=compiled_with_architecture,
        filename=filename_mapped,
        output_format=output_format,
        gate_set=device.basis_gates,
        mapped=True,
        c_map=c_map,
        target_directory=target_directory,
    )


def get_benchmark(
    benchmark_name: str,
    level: str | int,
    circuit_size: int | None = None,
    benchmark_instance_name: str | None = None,
    compiler_settings: CompilerSettings | None = None,
    provider_name: str = "ibm",
    device_name: str = "ibm_washington",
    **kwargs: str,
) -> QuantumCircuit:
    """Returns one benchmark as a qiskit.QuantumCircuit object.

    Arguments:
        benchmark_name: name of the to be generated benchmark
        level: Choice of level, either as a string ("alg", "indep", "nativegates" or "mapped") or as a number between 0-3 where 0 corresponds to "alg" level and 3 to "mapped" level
        circuit_size: Input for the benchmark creation, in most cases this is equal to the qubit number
        benchmark_instance_name: Input selection for some benchmarks, namely and "shor"
        compiler_settings: Data class containing the respective compiler settings for the specified compiler (e.g., optimization level for Qiskit)
        provider_name: "ibm", "rigetti", "ionq", "oqc", or "quantinuum" (required for "nativegates" level)
        device_name: "ibm_washington", "ibm_montreal", "rigetti_aspen_m3", "ionq_harmony", "ionq_aria1", "oqc_lucy", "quantinuum_h2" (required for "mapped" level)
        kwargs: Additional arguments for the benchmark generation

    Returns:
        Qiskit::QuantumCircuit object representing the benchmark with the selected options
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
        else:
            msg = "Either `noancilla` or `v-chain` must be specified for ancillary mode of Grover and QWalk benchmarks."
            raise ValueError(msg)

        qc = lib.create_circuit(circuit_size, ancillary_mode=anc_mode)

    elif benchmark_name == "shor":
        to_be_factored_number, a_value = lib.get_instance(benchmark_instance_name)
        qc = lib.create_circuit(to_be_factored_number, a_value)

    else:
        qc = lib.create_circuit(circuit_size)

    if level in ("alg", 0):
        return qc

    if compiler_settings is None:
        compiler_settings = CompilerSettings(QiskitSettings())
    elif not isinstance(compiler_settings, CompilerSettings):
        msg = "compiler_settings must be of type CompilerSettings or None."  # type: ignore[unreachable]
        raise ValueError(msg)

    independent_level = 1
    if level in ("indep", independent_level):
        return get_indep_level(qc, circuit_size, False, True)

    native_gates_level = 2
    if level in ("nativegates", native_gates_level):
        if provider_name not in get_available_provider_names():
            msg = f"Selected provider_name must be in {get_available_provider_names()}."
            raise ValueError(msg)
        provider = get_provider_by_name(provider_name)
        assert compiler_settings.qiskit is not None
        opt_level = compiler_settings.qiskit.optimization_level
        return get_native_gates_level(qc, provider, circuit_size, opt_level, False, True)

    if device_name not in get_available_device_names():
        msg = f"Selected device_name must be in {get_available_device_names()}."
        raise ValueError(msg)

    mapped_level = 3
    if level in ("mapped", mapped_level):
        device = get_device_by_name(device_name)
        assert compiler_settings.qiskit is not None
        opt_level = compiler_settings.qiskit.optimization_level
        assert isinstance(opt_level, int)
        return get_mapped_level(
            qc,
            circuit_size,
            device,
            opt_level,
            False,
            True,
        )

    msg = f"Invalid level specified. Must be in {get_supported_levels()}."
    raise ValueError(msg)


def get_supported_benchmarks() -> list[str]:
    """Returns a list of all supported benchmarks."""
    return [
        "ae",
        "bv",
        "dj",
        "grover-noancilla",
        "grover-v-chain",
        "ghz",
        "graphstate",
        "qaoa",
        "qft",
        "qftentangled",
        "qnn",
        "qpeexact",
        "qpeinexact",
        "qwalk-noancilla",
        "qwalk-v-chain",
        "randomcircuit",
        "vqerealamprandom",
        "vqesu2random",
        "vqetwolocalrandom",
        "wstate",
        "shor",
    ]


def get_supported_levels() -> list[str | int]:
    """Returns a list of all supported benchmark levels."""
    return ["alg", "indep", "nativegates", "mapped", 0, 1, 2, 3]


def get_default_qasm_output_path() -> str:
    """Returns the path where all .qasm files are stored."""
    return str(resources.files("mqt.bench") / "viewer" / "static" / "files" / "qasm_output")


def get_zip_folder_path() -> str:
    """Returns the path where the zip file is stored."""
    return str(resources.files("mqt.bench") / "viewer" / "static" / "files")


def get_openqasm_gates() -> list[str]:
    """Returns a list of all quantum gates within the openQASM 2.0 standard header."""
    # according to https://github.com/Qiskit/qiskit-terra/blob/main/qiskit/qasm/libs/qelib1.inc
    return [
        "u3",
        "u2",
        "u1",
        "cx",
        "id",
        "u0",
        "u",
        "p",
        "x",
        "y",
        "z",
        "h",
        "s",
        "sdg",
        "t",
        "tdg",
        "rx",
        "ry",
        "rz",
        "sx",
        "sxdg",
        "cz",
        "cy",
        "swap",
        "ch",
        "ccx",
        "cswap",
        "crx",
        "cry",
        "crz",
        "cu1",
        "cp",
        "cu3",
        "csx",
        "cu",
        "rxx",
        "rzz",
        "rccx",
        "rc3x",
        "c3x",
        "c3sqrtx",
        "c4x",
    ]


def get_module_for_benchmark(benchmark_name: str) -> ModuleType:
    """Returns the module for a specific benchmark."""
    return import_module("mqt.bench.benchmarks." + benchmark_name)
