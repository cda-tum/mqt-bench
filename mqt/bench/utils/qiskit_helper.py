from qiskit import QuantumCircuit, __qiskit_version__
from qiskit.compiler import transpile

from os import path

from utils import utils


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
):
    """Handles the creation of the benchmark on the target-independent level.

    Keyword arguments:
    qc -- quantum circuit which the to be created benchmark circuit is based on
    num_qubits -- number of qubits
    file_precheck -- flag indicating whether to check whether the file already exists before creating it (again)

    Return values:
    filename_indep -- the filename of the created and saved benchmark
    depth -- circuit depth of created benchmark
    num_qubits -- number of qubits of generated circuit
    """

    filename_indep = qc.name + "_indep_qiskit_" + str(num_qubits)
    qasm_output_folder = utils.get_qasm_output_path()
    filepath = qasm_output_folder + filename_indep + ".qasm"
    if not (path.isfile(filepath) and file_precheck):
        print(filepath + " does not already exists and is newly created")
        openqasm_gates = utils.get_openqasm_gates()
        target_independent = transpile(
            qc, basis_gates=openqasm_gates, optimization_level=1, seed_transpiler=10
        )
        utils.save_as_qasm(target_independent.qasm(), filename_indep)

        return target_independent.num_qubits
    return 0


def get_native_gates_level(
    qc: QuantumCircuit,
    gate_set_name: str,
    num_qubits: int,
    opt_level: int,
    file_precheck: bool,
):
    """Handles the creation of the benchmark on the target-dependent native gates level.

    Keyword arguments:
    qc -- quantum circuit which the to be created benchmark circuit is based on
    gate_set_name -- name of this gate set
    opt_level -- optimization level
    num_qubits -- number of qubits
    file_precheck -- flag indicating whether to check whether the file already exists before creating it (again)
    """

    filename_nativegates = (
        qc.name
        + "_nativegates_"
        + gate_set_name
        + "_qiskit_opt"
        + str(opt_level)
        + "_"
        + str(num_qubits)
    )
    gate_set = get_native_gates(gate_set_name)
    qasm_output_folder = utils.get_qasm_output_path()
    if not (
        path.isfile(qasm_output_folder + filename_nativegates + ".qasm")
        and file_precheck
    ):
        print(
            qasm_output_folder
            + filename_nativegates
            + ".qasm"
            + " does not already exists and is newly created"
        )
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
        utils.save_as_qasm(
            compiled_without_architecture.qasm(),
            filename_nativegates,
            gate_set,
            opt_level,
        )
        return qc.num_qubits
    return 0


def get_mapped_level(
    qc: QuantumCircuit,
    gate_set_name: str,
    num_qubits: int,
    device_name: str,
    opt_level: int,
    file_precheck: bool,
):
    """Handles the creation of the benchmark on the target-dependent mapped level.

    Keyword arguments:
    qc -- quantum circuit which the to be created benchmark circuit is based on
    gate_set -- set of to be used gates
    gate_set_name -- name of this gate set
    opt_level -- optimization level
    num_qubits -- number of qubits
    smallest_fitting_arch -- flag indicating whether smallest fitting mapping scheme shall be used
    file_precheck -- flag indicating whether to check whether the file already exists before creating it (again)

    Return values:
    filename_mapped -- the filename of the created and saved benchmark
    depth -- circuit depth of created benchmark
    num_qubits -- number of qubits of generated circuit
    """

    gate_set = get_native_gates(gate_set_name)
    c_map = utils.get_cmap_from_devicename(device_name)

    filename_mapped = (
        qc.name
        + "_mapped_"
        + device_name
        + "_"
        + gate_set_name
        + "_qiskit_opt"
        + str(opt_level)
        + "_"
        + str(num_qubits)
    )
    qasm_output_folder = utils.get_qasm_output_path()
    if not (
        path.isfile(qasm_output_folder + filename_mapped + ".qasm") and file_precheck
    ):
        print(
            qasm_output_folder
            + filename_mapped
            + ".qasm"
            + " does not already exists and is newly created"
        )
        compiled_with_architecture = transpile(
            qc,
            optimization_level=opt_level,
            basis_gates=gate_set,
            coupling_map=c_map,
            seed_transpiler=10,
        )
        utils.save_as_qasm(
            compiled_with_architecture.qasm(), filename_mapped, gate_set, True, c_map
        )
        return compiled_with_architecture.num_qubits
    return 0
