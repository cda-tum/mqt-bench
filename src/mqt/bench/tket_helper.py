from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Literal, overload

from pytket import OpType
from pytket.architecture import Architecture
from pytket.extensions.qiskit import qiskit_to_tk
from pytket.passes import (
    CXMappingPass,
    FullPeepholeOptimise,
    PeepholeOptimise2Q,
    PlacementPass,
    RoutingPass,
    SynthesiseTket,
    auto_rebase_pass,
)
from pytket.placement import GraphPlacement, LinePlacement
from pytket.qasm import circuit_to_qasm_str
from qiskit import QuantumCircuit, transpile

from mqt.bench import utils

if TYPE_CHECKING:  # pragma: no cover
    from pytket._tket.passes import BasePass
    from pytket.circuit import Circuit

    from mqt.bench.devices import Device, Provider


def get_rebase(gate_set: list[str]) -> BasePass:
    op_dict = {
        "rx": OpType.Rx,
        "ry": OpType.Ry,
        "rz": OpType.Rz,
        "rxx": OpType.XXPhase,
        "rzz": OpType.ZZPhase,
        "sx": OpType.SX,
        "x": OpType.X,
        "cx": OpType.CX,
        "cz": OpType.CZ,
        "ecr": OpType.ECR,
        "measure": OpType.Measure,
    }
    return auto_rebase_pass({op_dict[key] for key in gate_set if key in op_dict})


@overload
def get_indep_level(
    qc: QuantumCircuit,
    num_qubits: int | None,
    file_precheck: bool,
    return_qc: Literal[True],
    target_directory: str = "./",
    target_filename: str = "",
) -> Circuit: ...


@overload
def get_indep_level(
    qc: QuantumCircuit,
    num_qubits: int | None,
    file_precheck: bool,
    return_qc: Literal[False],
    target_directory: str = "./",
    target_filename: str = "",
) -> bool: ...


def get_indep_level(
    qc: QuantumCircuit,
    num_qubits: int | None,
    file_precheck: bool,
    return_qc: bool = False,
    target_directory: str = "./",
    target_filename: str = "",
) -> bool | Circuit:
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
    filename_indep = target_filename if target_filename else qc.name + "_indep_tket_" + str(num_qubits)

    path = Path(target_directory, filename_indep + ".qasm")
    if file_precheck and path.is_file():
        return True
    try:
        gates = list(set(utils.get_openqasm_gates()) - {"rccx"})
        qc = transpile(
            qc,
            basis_gates=gates,
            seed_transpiler=10,
            optimization_level=0,
        )
        qc_tket = qiskit_to_tk(qc)
    except Exception as e:
        print("TKET Exception Indep: ", e)
        return False

    if return_qc:
        return qc_tket
    return utils.save_as_qasm(
        circuit_to_qasm_str(qc_tket, maxwidth=qc.num_qubits),
        filename_indep,
        target_directory=target_directory,
    )


@overload
def get_native_gates_level(
    qc: QuantumCircuit,
    provider: Provider,
    num_qubits: int | None,
    file_precheck: bool,
    return_qc: Literal[True],
    target_directory: str = "./",
    target_filename: str = "",
) -> Circuit: ...


@overload
def get_native_gates_level(
    qc: QuantumCircuit,
    provider: Provider,
    num_qubits: int | None,
    file_precheck: bool,
    return_qc: Literal[False],
    target_directory: str = "./",
    target_filename: str = "",
) -> bool: ...


def get_native_gates_level(
    qc: QuantumCircuit,
    provider: Provider,
    num_qubits: int | None,
    file_precheck: bool,
    return_qc: bool = False,
    target_directory: str = "./",
    target_filename: str = "",
) -> bool | Circuit:
    """Handles the creation of the benchmark on the target-dependent native gates level.

    Keyword arguments:
    qc -- quantum circuit which the to be created benchmark circuit is based on
    provider -- determines the native gate set
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
        filename_native = qc.name + "_nativegates_" + provider.provider_name + "_tket_" + str(num_qubits)
    else:
        filename_native = target_filename

    path = Path(target_directory, filename_native + ".qasm")
    if file_precheck and path.is_file():
        return True
    try:
        gates = list(set(utils.get_openqasm_gates()) - {"rccx"})
        qc = transpile(
            qc,
            basis_gates=gates,
            seed_transpiler=10,
            optimization_level=0,
        )

        qc_tket = qiskit_to_tk(qc)
    except Exception as e:
        print("TKET Exception NativeGates: ", e)
        return False

    gate_set = provider.get_native_gates()
    native_gate_set_rebase = get_rebase(gate_set)
    native_gate_set_rebase.apply(qc_tket)
    FullPeepholeOptimise(target_2qb_gate=OpType.TK2).apply(qc_tket)
    native_gate_set_rebase.apply(qc_tket)

    if return_qc:
        return qc_tket
    return utils.save_as_qasm(
        circuit_to_qasm_str(qc_tket, maxwidth=qc.num_qubits),
        filename_native,
        gate_set,
        target_directory=target_directory,
    )


@overload
def get_mapped_level(
    qc: QuantumCircuit,
    num_qubits: int | None,
    device: Device,
    lineplacement: bool,
    file_precheck: bool,
    return_qc: Literal[True],
    target_directory: str = "./",
    target_filename: str = "",
) -> Circuit: ...


@overload
def get_mapped_level(
    qc: QuantumCircuit,
    num_qubits: int | None,
    device: Device,
    lineplacement: bool,
    file_precheck: bool,
    return_qc: Literal[False],
    target_directory: str = "./",
    target_filename: str = "",
) -> bool: ...


def get_mapped_level(
    qc: QuantumCircuit,
    num_qubits: int | None,
    device: Device,
    lineplacement: bool,
    file_precheck: bool,
    return_qc: bool = False,
    target_directory: str = "./",
    target_filename: str = "",
) -> bool | Circuit:
    """Handles the creation of the benchmark on the target-dependent mapped level.

    Keyword arguments:
    qc -- quantum circuit which the to be created benchmark circuit is based on
    num_qubits -- number of qubits
    device -- target device
    lineplacement -- if true line placement is used, else graph placement
    file_precheck -- flag indicating whether to check whether the file already exists before creating it (again)
    return_qc -- flag if the actual circuit shall be returned
    target_directory -- alternative directory to the default one to store the created circuit
    target_filename -- alternative filename to the default one

    Return values:
    if return_qc == True -- quantum circuit object
    else -- True/False indicating whether the function call was successful or not
    """

    placement = "line" if lineplacement else "graph"

    if not target_filename:
        filename_mapped = qc.name + "_mapped_" + device.name + "_tket_" + placement + "_" + str(num_qubits)
    else:
        filename_mapped = target_filename

    path = Path(target_directory, filename_mapped + ".qasm")
    if file_precheck and path.is_file():
        return True

    try:
        gates = list(set(utils.get_openqasm_gates()) - {"rccx"})
        qc = transpile(
            qc,
            basis_gates=gates,
            seed_transpiler=10,
            optimization_level=0,
        )

        qc_tket = qiskit_to_tk(qc)
    except Exception as e:
        print("TKET Exception Mapped: ", e)
        return False

    cmap = device.coupling_map
    cmap_converted = utils.convert_cmap_to_tuple_list(cmap)
    arch = Architecture(cmap_converted)

    # add blank wires to the circuit such that afterwards the number of qubits is equal to the number of qubits of the architecture
    highest_used_qubit_index = max(max(sublist) for sublist in cmap)
    diff = highest_used_qubit_index + 1 - qc_tket.n_qubits  # offset of one is added because the indices start at 0
    qc_tket.add_blank_wires(diff)

    native_gate_set_rebase = get_rebase(device.basis_gates)
    native_gate_set_rebase.apply(qc_tket)
    FullPeepholeOptimise(target_2qb_gate=OpType.TK2).apply(qc_tket)
    placer = LinePlacement(arch) if lineplacement else GraphPlacement(arch)
    PlacementPass(placer).apply(qc_tket)
    RoutingPass(arch).apply(qc_tket)
    PeepholeOptimise2Q(allow_swaps=False).apply(qc_tket)
    SynthesiseTket().apply(qc_tket)
    if not qc_tket.valid_connectivity(arch, directed=True):
        CXMappingPass(arc=arch, placer=placer, directed_cx=True, delay_measures=False).apply(qc_tket)
    native_gate_set_rebase.apply(qc_tket)

    if return_qc:
        return qc_tket
    return utils.save_as_qasm(
        circuit_to_qasm_str(qc_tket, maxwidth=qc.num_qubits),
        filename_mapped,
        device.basis_gates,
        True,
        cmap,
        target_directory,
    )
