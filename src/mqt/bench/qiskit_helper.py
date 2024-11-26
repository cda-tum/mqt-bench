"""Compilation functions to create benchmarks on different levels of abstraction using Qiskit."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Literal, overload

if TYPE_CHECKING:  # pragma: no cover
    from qiskit import QuantumCircuit

    from .devices import Device, Gateset

from qiskit import transpile
from qiskit.synthesis import generate_basic_approximations
from qiskit.transpiler.passes import SolovayKitaev

from .utils import get_openqasm_gates, save_as_qasm


@overload
def get_indep_level(
    qc: QuantumCircuit,
    num_qubits: int | None,
    file_precheck: bool,
    return_qc: Literal[True],
    target_directory: str = "./",
    target_filename: str = "",
    qasm_format: str = "qasm3",
) -> QuantumCircuit: ...


@overload
def get_indep_level(
    qc: QuantumCircuit,
    num_qubits: int | None,
    file_precheck: bool,
    return_qc: Literal[False],
    target_directory: str = "./",
    target_filename: str = "",
    qasm_format: str = "qasm3",
) -> bool: ...


def get_indep_level(
    qc: QuantumCircuit,
    num_qubits: int | None,
    file_precheck: bool,
    return_qc: bool = False,
    target_directory: str = "./",
    target_filename: str = "",
    qasm_format: str = "qasm3",
) -> bool | QuantumCircuit:
    """Handles the creation of the benchmark on the target-independent level.

    Arguments:
        qc: quantum circuit which the to be created benchmark circuit is based on
        num_qubits: number of qubits
        file_precheck: flag indicating whether to check whether the file already exists before creating it (again)
        return_qc: flag if the actual circuit shall be returned
        target_directory: alternative directory to the default one to store the created circuit
        target_filename: alternative filename to the default one
        qasm_format: qasm format (qasm2 or qasm3)


    Returns:
        if return_qc == True: quantum circuit object
        else: True/False indicating whether the function call was successful or not
    """
    filename_indep = target_filename or qc.name + "_indep_qiskit_" + str(num_qubits) + "_" + qasm_format

    path = Path(target_directory, filename_indep + ".qasm")
    print(path, target_directory)
    if file_precheck and path.is_file():
        return True
    openqasm_gates = get_openqasm_gates()
    target_independent = transpile(qc, basis_gates=openqasm_gates, optimization_level=1, seed_transpiler=10)

    if return_qc:
        return target_independent

    return save_as_qasm(
        qc=target_independent, filename=filename_indep, qasm_format=qasm_format, target_directory=target_directory
    )


@overload
def get_native_gates_level(
    qc: QuantumCircuit,
    gateset: Gateset,
    num_qubits: int | None,
    opt_level: int,
    file_precheck: bool,
    return_qc: Literal[True],
    target_directory: str = "./",
    target_filename: str = "",
    qasm_format: str = "qasm3",
) -> QuantumCircuit: ...


@overload
def get_native_gates_level(
    qc: QuantumCircuit,
    gateset: Gateset,
    num_qubits: int | None,
    opt_level: int,
    file_precheck: bool,
    return_qc: Literal[False],
    target_directory: str = "./",
    target_filename: str = "",
    qasm_format: str = "qasm3",
) -> bool: ...


def get_native_gates_level(
    qc: QuantumCircuit,
    gateset: Gateset,
    num_qubits: int | None,
    opt_level: int,
    file_precheck: bool,
    return_qc: bool = False,
    target_directory: str = "./",
    target_filename: str = "",
    qasm_format: str = "qasm3",
) -> bool | QuantumCircuit:
    """Handles the creation of the benchmark on the target-dependent native gates level.

    Arguments:
        qc: quantum circuit which the to be created benchmark circuit is based on
        gateset: contains the name of the gateset and a list of native gates
        num_qubits: number of qubits
        opt_level: optimization level
        file_precheck: flag indicating whether to check whether the file already exists before creating it (again)
        return_qc: flag if the actual circuit shall be returned
        target_directory: alternative directory to the default one to store the created circuit
        target_filename: alternative filename to the default one
        qasm_format: qasm format (qasm2 or qasm3)

    Returns:
        if return_qc == True: quantum circuit object
        else: True/False indicating whether the function call was successful or not
    """
    if not target_filename:
        filename_native = (
            qc.name + "_nativegates_" + gateset.gateset_name + "_qiskit_opt" + str(opt_level) + "_" + str(num_qubits)
        )
    else:
        filename_native = target_filename

    path = Path(target_directory, filename_native + ".qasm")
    if file_precheck and path.is_file():
        return True

    if gateset.gateset_name == "clifford+t":
        gateset_without_cx = gateset.gates.copy()
        gateset_without_cx.remove("cx")
        approx = generate_basic_approximations(gateset_without_cx, depth=3)
        skd = SolovayKitaev(recursion_degree=2, basic_approximations=approx)
        compiled_without_architecture = skd(qc.decompose(reps=3).remove_final_measurements(inplace=False))
        compiled_without_architecture.measure_all()
    else:
        compiled_without_architecture = transpile(
            qc, basis_gates=gateset.gates, optimization_level=opt_level, seed_transpiler=10
        )
    if return_qc:
        return compiled_without_architecture

    return save_as_qasm(
        qc=compiled_without_architecture,
        filename=filename_native,
        qasm_format=qasm_format,
        gateset=gateset.gates,
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
    qasm_format: str = "qasm3",
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
    qasm_format: str = "qasm3",
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
    qasm_format: str = "qasm3",
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
        qasm_format: qasm format (qasm2 or qasm3)

    Returns:
        if return_qc == True: quantum circuit object
        else: True/False indicating whether the function call was successful or not
    """
    if not target_filename:
        filename_mapped = qc.name + "_mapped_" + device.name + "_qiskit_opt" + str(opt_level) + "_" + str(num_qubits)
    else:
        filename_mapped = target_filename

    path = Path(target_directory, filename_mapped + ".qasm")
    if file_precheck and path.is_file():
        return True

    c_map = device.coupling_map
    compiled_with_architecture = transpile(
        qc,
        optimization_level=opt_level,
        basis_gates=device.gateset.gates,
        coupling_map=c_map,
        seed_transpiler=10,
    )
    if return_qc:
        return compiled_with_architecture

    return save_as_qasm(
        qc=compiled_with_architecture,
        filename=filename_mapped,
        qasm_format=qasm_format,
        gateset=device.gateset.gates,
        mapped=True,
        c_map=c_map,
        target_directory=target_directory,
    )
