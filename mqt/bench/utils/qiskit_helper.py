from __future__ import annotations

from os import path

from qiskit import QuantumCircuit
from qiskit.compiler import transpile

from mqt.bench.utils import utils


def get_native_gates(gate_set_name: str):
    if gate_set_name == "ionq":
        return get_ionq_native_gates()
    elif gate_set_name == "oqc":
        return get_oqc_native_gates()
    elif gate_set_name == "ibm":
        return get_ibm_native_gates()
    elif gate_set_name == "rigetti":
        return get_rigetti_native_gates()


def get_ibm_native_gates():
    ibm_gates = ["rz", "sx", "x", "cx", "measure"]
    return ibm_gates


def get_rigetti_native_gates():
    rigetti_gates = ["rx", "rz", "cz", "measure"]
    return rigetti_gates


def get_ionq_native_gates():
    ionq_gates = ["rxx", "rz", "ry", "rx", "measure"]
    return ionq_gates


def get_oqc_native_gates():
    oqc_gates = ["rz", "sx", "x", "ecr", "measure"]
    return oqc_gates


def get_indep_level(
    qc: QuantumCircuit,
    num_qubits: int,
    file_precheck: bool,
    return_qc: bool = False,
    target_directory: str = "",
    target_filename: str = "",
):
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

    if not target_filename:
        filename_indep = qc.name + "_indep_qiskit_" + str(num_qubits)
        target_directory = utils.get_qasm_output_path()
    else:
        filename_indep = target_filename

    if not (
        path.isfile(path.join(target_directory, filename_indep) + ".qasm")
        and file_precheck
    ):
        openqasm_gates = utils.get_openqasm_gates()
        target_independent = transpile(
            qc, basis_gates=openqasm_gates, optimization_level=1, seed_transpiler=10
        )

        if return_qc:
            return target_independent
        else:
            res = utils.save_as_qasm(
                target_independent.qasm(),
                filename_indep,
                target_directory=target_directory,
            )
            return res
    else:
        return True


def get_native_gates_level(
    qc: QuantumCircuit,
    gate_set_name: str,
    num_qubits: int,
    opt_level: int,
    file_precheck: bool,
    return_qc: bool = False,
    target_directory: str = "",
    target_filename: str = "",
):
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
            qc.name
            + "_nativegates_"
            + gate_set_name
            + "_qiskit_opt"
            + str(opt_level)
            + "_"
            + str(num_qubits)
        )
        target_directory = utils.get_qasm_output_path()
    else:
        filename_native = target_filename

    if not (
        path.isfile(path.join(target_directory, filename_native) + ".qasm")
        and file_precheck
    ):

        compiled_without_architecture = transpile(
            qc, basis_gates=gate_set, optimization_level=opt_level, seed_transpiler=10
        )
        n_actual = compiled_without_architecture.num_qubits
        filename_nativegates = (
            qc.name
            + "_nativegates_"
            + gate_set_name
            + "_qiskit_opt"
            + str(opt_level)
            + "_"
            + str(n_actual)
        )

        if return_qc:
            return compiled_without_architecture
        else:
            res = utils.save_as_qasm(
                compiled_without_architecture.qasm(),
                filename_nativegates,
                gate_set,
                target_directory=target_directory,
            )
            return res
    else:
        return True


def get_mapped_level(
    qc: QuantumCircuit,
    gate_set_name: str,
    num_qubits: int,
    device_name: str,
    opt_level: int,
    file_precheck: bool,
    return_qc: bool = False,
    target_directory: str = "",
    target_filename: str = "",
):
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
        filename_mapped = (
            qc.name
            + "_mapped_"
            + device_name
            + "_qiskit_opt"
            + str(opt_level)
            + "_"
            + str(num_qubits)
        )
        target_directory = utils.get_qasm_output_path()
    else:
        filename_mapped = target_filename

    if not (
        path.isfile(path.join(target_directory, target_filename) + ".qasm")
        and file_precheck
    ):

        compiled_with_architecture = transpile(
            qc,
            optimization_level=opt_level,
            basis_gates=gate_set,
            coupling_map=c_map,
            seed_transpiler=10,
        )
        if return_qc:
            return compiled_with_architecture
        else:
            res = utils.save_as_qasm(
                compiled_with_architecture.qasm(),
                filename_mapped,
                gate_set,
                True,
                c_map,
                target_directory,
            )
            return res
    else:
        return True
