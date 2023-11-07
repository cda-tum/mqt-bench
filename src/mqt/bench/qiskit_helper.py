from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Literal, overload

if TYPE_CHECKING:  # pragma: no cover
    from qiskit import QuantumCircuit

from qiskit.compiler import transpile

from mqt.bench import utils


def get_native_gates(gate_set_name: str) -> list[str]:
    if gate_set_name == "ionq":
        return get_ionq_native_gates()
    if gate_set_name == "oqc":
        return get_oqc_native_gates()
    if gate_set_name == "ibm":
        return get_ibm_native_gates()
    if gate_set_name == "rigetti":
        return get_rigetti_native_gates()
    if gate_set_name == "quantinuum":
        return get_quantinuum_native_gates()
    raise ValueError("Unknown gate set name: " + gate_set_name)


def get_ibm_native_gates() -> list[str]:
    return ["rz", "sx", "x", "cx", "measure"]


def get_rigetti_native_gates() -> list[str]:
    return ["rx", "rz", "cz", "measure"]


def get_ionq_native_gates() -> list[str]:
    return ["rxx", "rz", "ry", "rx", "measure"]


def get_oqc_native_gates() -> list[str]:
    return ["rz", "sx", "x", "ecr", "measure"]


def get_quantinuum_native_gates() -> list[str]:
    return ["rzz", "rz", "ry", "rx", "measure"]


@overload
def get_indep_level(
    qc: QuantumCircuit,
    num_qubits: int | None,
    file_precheck: bool,
    return_qc: Literal[True],
    target_directory: str = "./",
    target_filename: str = "",
) -> QuantumCircuit:
    ...


@overload
def get_indep_level(
    qc: QuantumCircuit,
    num_qubits: int | None,
    file_precheck: bool,
    return_qc: Literal[False],
    target_directory: str = "./",
    target_filename: str = "",
) -> bool:
    ...


def get_indep_level(
    qc: QuantumCircuit,
    num_qubits: int | None,
    file_precheck: bool,
    return_qc: bool = False,
    target_directory: str = "./",
    target_filename: str = "",
) -> bool | QuantumCircuit:
    """Handles the creation of the benchmark on the target-independent level.

    Keyword arguments:
    qc -- quantum circuit which the to be created benchmark circuit is based on
    num_qubits -- number of qubits
    file_precheck -- flag indicating whether to check whether the file already exists before creating it (again)
    return_qc -- flag if the actual circuit shall be returned
    target_directory -- alternative directory to the default one to store the created circuit
    target_filename -- alternative filename to the default one

    Return values:
    if return_qc == True -- quantum circuit object
    else -- True/False indicating whether the function call was successful or not
    """

    filename_indep = target_filename if target_filename else qc.name + "_indep_qiskit_" + str(num_qubits)

    path = Path(target_directory, filename_indep + ".qasm")
    if file_precheck and path.is_file():
        return True
    openqasm_gates = utils.get_openqasm_gates()
    target_independent = transpile(qc, basis_gates=openqasm_gates, optimization_level=1, seed_transpiler=10)

    if return_qc:
        return target_independent
    return utils.save_as_qasm(
        target_independent.qasm(),
        filename_indep,
        target_directory=target_directory,
    )


@overload
def get_native_gates_level(
    qc: QuantumCircuit,
    gate_set_name: str,
    num_qubits: int | None,
    opt_level: int,
    file_precheck: bool,
    return_qc: Literal[True],
    target_directory: str = "./",
    target_filename: str = "",
) -> QuantumCircuit:
    ...


@overload
def get_native_gates_level(
    qc: QuantumCircuit,
    gate_set_name: str,
    num_qubits: int | None,
    opt_level: int,
    file_precheck: bool,
    return_qc: Literal[False],
    target_directory: str = "./",
    target_filename: str = "",
) -> bool:
    ...


def get_native_gates_level(
    qc: QuantumCircuit,
    gate_set_name: str,
    num_qubits: int | None,
    opt_level: int,
    file_precheck: bool,
    return_qc: bool = False,
    target_directory: str = "./",
    target_filename: str = "",
) -> bool | QuantumCircuit:
    """Handles the creation of the benchmark on the target-dependent native gates level.

    Keyword arguments:
    qc -- quantum circuit which the to be created benchmark circuit is based on
    gate_set_name -- name of this gate set
    num_qubits -- number of qubits
    opt_level -- optimization level
    file_precheck -- flag indicating whether to check whether the file already exists before creating it (again)
    return_qc -- flag if the actual circuit shall be returned
    target_directory -- alternative directory to the default one to store the created circuit
    target_filename -- alternative filename to the default one

    Return values:
    if return_qc == True -- quantum circuit object
    else -- True/False indicating whether the function call was successful or not
    """

    gate_set = get_native_gates(gate_set_name)
    if not target_filename:
        filename_native = (
            qc.name + "_nativegates_" + gate_set_name + "_qiskit_opt" + str(opt_level) + "_" + str(num_qubits)
        )
    else:
        filename_native = target_filename

    path = Path(target_directory, filename_native + ".qasm")
    if file_precheck and path.is_file():
        return True
    compiled_without_architecture = transpile(
        qc, basis_gates=gate_set, optimization_level=opt_level, seed_transpiler=10
    )

    if return_qc:
        return compiled_without_architecture
    return utils.save_as_qasm(
        compiled_without_architecture.qasm(),
        filename_native,
        gate_set,
        target_directory=target_directory,
    )


@overload
def get_mapped_level(
    qc: QuantumCircuit,
    gate_set_name: str,
    num_qubits: int | None,
    device_name: str,
    opt_level: int,
    file_precheck: bool,
    return_qc: Literal[True],
    target_directory: str = "./",
    target_filename: str = "",
) -> QuantumCircuit:
    ...


@overload
def get_mapped_level(
    qc: QuantumCircuit,
    gate_set_name: str,
    num_qubits: int | None,
    device_name: str,
    opt_level: int,
    file_precheck: bool,
    return_qc: Literal[False],
    target_directory: str = "./",
    target_filename: str = "",
) -> bool:
    ...


def get_mapped_level(
    qc: QuantumCircuit,
    gate_set_name: str,
    num_qubits: int | None,
    device_name: str,
    opt_level: int,
    file_precheck: bool,
    return_qc: bool = False,
    target_directory: str = "./",
    target_filename: str = "",
) -> bool | QuantumCircuit:
    """Handles the creation of the benchmark on the target-dependent mapped level.

    Keyword arguments:
    qc -- quantum circuit which the to be created benchmark circuit is based on
    gate_set_name -- name of the gate set
    num_qubits -- number of qubits
    device_name -- -- name of the target device
    opt_level -- optimization level
    file_precheck -- flag indicating whether to check whether the file already exists before creating it (again)
    return_qc -- flag if the actual circuit shall be returned
    target_directory -- alternative directory to the default one to store the created circuit
    target_filename -- alternative filename to the default one

    Return values:
    if return_qc == True -- quantum circuit object
    else -- True/False indicating whether the function call was successful or not
    """

    gate_set = get_native_gates(gate_set_name)
    c_map = utils.get_cmap_from_devicename(device_name)

    if not target_filename:
        filename_mapped = qc.name + "_mapped_" + device_name + "_qiskit_opt" + str(opt_level) + "_" + str(num_qubits)
    else:
        filename_mapped = target_filename

    path = Path(target_directory, filename_mapped + ".qasm")
    if file_precheck and path.is_file():
        return True
    compiled_with_architecture = transpile(
        qc,
        optimization_level=opt_level,
        basis_gates=gate_set,
        coupling_map=c_map,
        seed_transpiler=10,
    )
    if return_qc:
        return compiled_with_architecture
    return utils.save_as_qasm(
        compiled_with_architecture.qasm(),
        filename_mapped,
        gate_set,
        True,
        c_map,
        target_directory,
    )
