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

import utils
from os import path


def get_rebase(gate_set_name: str):
    if gate_set_name == "ionq":
        return get_ionq_rebase()
    elif gate_set_name == "oqc":
        return get_oqc_rebase()
    elif gate_set_name == "ibm":
        return get_ibm_rebase()
    elif gate_set_name == "rigetti":
        return get_rigetti_rebase()


def get_ionq_rebase():
    ionq_rebase = auto_rebase_pass(
        {OpType.Rz, OpType.Ry, OpType.Rx, OpType.XXPhase, OpType.Measure}
    )
    return ionq_rebase


def get_oqc_rebase():
    oqc_rebase = auto_rebase_pass(
        {OpType.Rz, OpType.SX, OpType.X, OpType.ECR, OpType.Measure}
    )
    return oqc_rebase


def get_rigetti_rebase():
    rigetti_rebase = auto_rebase_pass({OpType.Rz, OpType.Rx, OpType.CZ, OpType.Measure})
    return rigetti_rebase


def get_ibm_rebase():
    ibm_rebase = auto_rebase_pass(
        {OpType.Rz, OpType.SX, OpType.X, OpType.CX, OpType.Measure}
    )
    return ibm_rebase


def get_indep_level(
    qc: circuit,
    num_qubits: int,
    file_precheck: bool,
):
    pass


def get_native_gates_level(
    qc: circuit,
    gate_set: list,
    gate_set_name: str,
    opt_level: int,
    num_qubits: int,
    file_precheck: bool,
):
    pass


def get_mapped_level(
    qc: circuit,
    gate_set_name: str,
    num_qubits: int,
    lineplacement: bool,
    device: str,
    file_precheck: bool,
):

    qasm_output_folder = utils.get_qasm_output_path()

    if lineplacement:
        placement = "line"
    else:
        placement = "graph"

    filename_mapped = (
        qc.name
        + "_mapped_"
        + device
        + "_"
        + gate_set_name
        + "_tket_"
        + placement
        + "_"
        + str(num_qubits)
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
        native_gate_set_rebase = get_rebase(gate_set_name)
        arch = architecture.Architecture(cmap)

        native_gate_set_rebase.apply(qc)
        FullPeepholeOptimise().apply(qc)
        if gate_set_name != "ionq":
            if lineplacement:
                PlacementPass(LinePlacement(arch)).apply(qc)
            else:
                PlacementPass(GraphPlacement(arch)).apply(qc)
            RoutingPass(arch).apply(qc)
        native_gate_set_rebase.apply(qc)
        utils.save_as_qasm(
            circuit_to_qasm_str(qc), filename_mapped, native_gate_set_rebase
        )

    return qc
