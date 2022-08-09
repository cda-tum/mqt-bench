from pytket.passes import auto_rebase_pass

from pytket import OpType
from pytket.passes import (
    PlacementPass,
    RoutingPass,
    FullPeepholeOptimise,
    auto_rebase_pass,
)
from pytket.placement import GraphPlacement, LinePlacement
from pytket.qasm import circuit_to_qasm_str, circuit_to_qasm
from pytket import architecture, circuit

from mqt.bench.utils import utils
from os import path
from pytket.extensions.qiskit import qiskit_to_tk

from qiskit import transpile


def get_rebase(gate_set_name: str, get_gatenames: bool = False):
    if gate_set_name == "ionq":
        return get_ionq_rebase(get_gatenames)
    elif gate_set_name == "oqc":
        return get_oqc_rebase(get_gatenames)
    elif gate_set_name == "ibm":
        return get_ibm_rebase(get_gatenames)
    elif gate_set_name == "rigetti":
        return get_rigetti_rebase(get_gatenames)


def get_ionq_rebase(get_gatenames: bool = False):
    if get_gatenames:
        return ["rz", "ry", "rx", "rxx", "measure"]
    else:
        ionq_rebase = auto_rebase_pass(
            {OpType.Rz, OpType.Ry, OpType.Rx, OpType.XXPhase, OpType.Measure}
        )
        return ionq_rebase


def get_oqc_rebase(get_gatenames: bool = False):
    if get_gatenames:
        return ["rz", "sx", "x", "ecr", "measure"]
    else:
        oqc_rebase = auto_rebase_pass(
            {OpType.Rz, OpType.SX, OpType.X, OpType.ECR, OpType.Measure}
        )
        return oqc_rebase


def get_rigetti_rebase(get_gatenames: bool = False):
    if get_gatenames:
        return ["rz", "rx", "cz", "measure"]
    else:
        rigetti_rebase = auto_rebase_pass(
            {OpType.Rz, OpType.Rx, OpType.CZ, OpType.Measure}
        )
        return rigetti_rebase


def get_ibm_rebase(get_gatenames: bool = False):
    if get_gatenames:
        return ["rz", "sx", "x", "cx", "measure"]
    else:
        ibm_rebase = auto_rebase_pass(
            {OpType.Rz, OpType.SX, OpType.X, OpType.CX, OpType.Measure}
        )
        return ibm_rebase


def get_indep_level(
    qc: circuit,
    num_qubits: int,
    file_precheck: bool,
    return_qc: bool = False,
):
    qasm_output_folder = utils.get_qasm_output_path()

    filename_native = qc.name + "_indep_tket_" + str(num_qubits)

    if not (
        path.isfile(qasm_output_folder + filename_native + ".qasm") and file_precheck
    ):
        print(
            qasm_output_folder
            + filename_native
            + ".qasm"
            + " does not already exists and is newly created"
        )
        openqasm_gates = utils.get_openqasm_gates()
        target_independent_qiskit = transpile(
            qc, basis_gates=openqasm_gates, optimization_level=1, seed_transpiler=10
        )
        qc_tket = qiskit_to_tk(target_independent_qiskit)
        FullPeepholeOptimise().apply(qc_tket)
        if return_qc:
            return qc_tket
        else:

            res = utils.save_as_qasm(circuit_to_qasm_str(qc_tket), filename_native)
            return res
    else:
        return True


def get_native_gates_level(
    qc: circuit,
    gate_set_name: str,
    num_qubits: int,
    file_precheck: bool,
    return_qc: bool = False,
):
    qasm_output_folder = utils.get_qasm_output_path()

    filename_native = (
        qc.name + "_nativegates_" + gate_set_name + "_tket_" + str(num_qubits)
    )
    if not (
        path.isfile(qasm_output_folder + filename_native + ".qasm") and file_precheck
    ):
        print(
            qasm_output_folder
            + filename_native
            + ".qasm"
            + " does not already exists and is newly created"
        )
        openqasm_gates = utils.get_openqasm_gates()
        target_independent_qiskit = transpile(
            qc, basis_gates=openqasm_gates, optimization_level=1, seed_transpiler=10
        )
        qc_tket = qiskit_to_tk(target_independent_qiskit)
        native_gatenames = get_rebase(gate_set_name, True)
        native_gate_set_rebase = get_rebase(gate_set_name)
        native_gate_set_rebase.apply(qc_tket)
        FullPeepholeOptimise().apply(qc_tket)
        native_gate_set_rebase.apply(qc_tket)

        if return_qc:
            return qc_tket
        else:
            res = utils.save_as_qasm(
                circuit_to_qasm_str(qc_tket), filename_native, native_gatenames
            )
            return res
    else:
        return True


def get_mapped_level(
    qc: circuit,
    gate_set_name: str,
    num_qubits: int,
    device: str,
    lineplacement: bool,
    file_precheck: bool,
    return_qc: bool = False,
):

    qasm_output_folder = utils.get_qasm_output_path()

    if lineplacement:
        placement = "line"
    else:
        placement = "graph"

    filename_mapped = (
        qc.name + "_mapped_" + device + "_tket_" + placement + "_" + str(num_qubits)
    )
    if not (
        path.isfile(qasm_output_folder + filename_mapped + ".qasm") and file_precheck
    ):
        cmap = utils.get_cmap_from_devicename(device)
        print(
            qasm_output_folder
            + filename_mapped
            + ".qasm"
            + " does not already exists and is newly created"
        )
        openqasm_gates = utils.get_openqasm_gates()
        target_independent_qiskit = transpile(
            qc, basis_gates=openqasm_gates, optimization_level=1, seed_transpiler=10
        )
        qc_tket = qiskit_to_tk(target_independent_qiskit)

        native_gatenames = get_rebase(gate_set_name, True)
        native_gate_set_rebase = get_rebase(gate_set_name)
        arch = architecture.Architecture(cmap)

        native_gate_set_rebase.apply(qc_tket)
        FullPeepholeOptimise().apply(qc_tket)
        if lineplacement:
            PlacementPass(LinePlacement(arch)).apply(qc_tket)
        else:
            PlacementPass(GraphPlacement(arch)).apply(qc_tket)
        RoutingPass(arch).apply(qc_tket)
        native_gate_set_rebase.apply(qc_tket)
        if return_qc:
            return qc_tket
        else:
            res = utils.save_as_qasm(
                circuit_to_qasm_str(qc_tket),
                filename_mapped,
                native_gatenames,
                True,
                cmap,
            )
            return res
    else:
        return True
