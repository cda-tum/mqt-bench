from __future__ import annotations

import math
from pathlib import Path
from typing import TYPE_CHECKING, Literal, overload

from bqskit import compile
from bqskit.compiler import MachineModel
from bqskit.ext import qiskit_to_bqskit
from bqskit.ir.gates import CNOTGate, CZGate, RXGate, RXXGate, RYGate, RZGate, RZZGate, SXGate, XGate
from bqskit.ir.gates.constantgate import ConstantGate
from bqskit.ir.gates.qubitgate import QubitGate
from bqskit.qis.unitary.unitarymatrix import UnitaryMatrix
from qiskit import transpile

from mqt.bench import utils

if TYPE_CHECKING:  # pragma: no cover
    from bqskit.ir import Gate
    from bqskit.ir.circuit import Circuit
    from qiskit import QuantumCircuit

    from mqt.bench.devices import Device, Provider


# mypy type checking is ignored for the ECRGate class because
# ConstantGate and QubitGate has type Any
class ECRGate(ConstantGate, QubitGate):  # type: ignore[misc]
    """
    The echoed cross-resonance gate.

    The ECR gate is given by the following unitary:

    .. math::

        \\frac{1}{\sqrt{2}}\begin{pmatrix}
        0 & 1 & 0 & i \\\\
        1 & 0 & -i & 0 \\\\
        0 & i & 0 & 1 \\\\
        -i & 0 & 1 & 0
        \\end{pmatrix}
    """

    _num_qudits = 2
    _qasm_name = "opaque ecr"
    _utry = UnitaryMatrix(
        [
            [0, 1 / math.sqrt(2), 0, 1j / math.sqrt(2)],
            [1 / math.sqrt(2), 0, -1j / math.sqrt(2), 0],
            [0, 1j / math.sqrt(2), 0, 1 / math.sqrt(2)],
            [-1j / math.sqrt(2), 0, 1 / math.sqrt(2), 0],
        ]
    )


def get_rebase(gate_set: list[str]) -> list[Gate]:
    op_dict = {
        "rx": RXGate(),
        "ry": RYGate(),
        "rz": RZGate(),
        "rxx": RXXGate(),
        "rzz": RZZGate(),
        "sx": SXGate(),
        "x": XGate(),
        "cx": CNOTGate(),
        "cz": CZGate(),
        "ecr": ECRGate(),
    }
    return [op_dict[key] for key in gate_set if key in op_dict]


@overload
def get_indep_level(
    qc: QuantumCircuit,
    num_qubits: int | None,
    file_precheck: bool,
    return_qc: Literal[True],
    target_directory: str = "./",
    target_filename: str = "",
) -> Circuit:
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
    filename_indep = target_filename if target_filename else qc.name + "_indep_bqskit_" + str(num_qubits)

    path = Path(target_directory, filename_indep + ".qasm")
    if file_precheck and path.is_file():
        return True
    try:
        gates = utils.get_openqasm_gates()
        qc = transpile(
            qc,
            basis_gates=gates,
            seed_transpiler=10,
            optimization_level=0,
        )
        qc_bqskit = qiskit_to_bqskit(qc)
    except Exception as e:
        print("BQSKit Exception Indep: ", e)
        return False

    if return_qc:
        return qc_bqskit
    return utils.save_as_qasm(
        qc_bqskit.to("qasm"),
        filename_indep,
        target_directory=target_directory,
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
) -> Circuit:
    ...


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
) -> bool:
    ...


def get_native_gates_level(
    qc: QuantumCircuit,
    provider: Provider,
    num_qubits: int | None,
    opt_level: int,
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
    opt_level -- optimization level
    file_precheck -- flag indicating whether to check whether the file already exists before creating it (again)
    return_qc -- flag if the actual circuit shall be returned
    target_directory -- alternative directory to the default one to store the created circuit
    target_filename -- alternative filename to the default one

    Return values:
    if return_qc == True -- quantum circuit object
    else -- True/False indicating whether the function call was successful or not
    """

    if not target_filename:
        filename_native = (
            qc.name + "_nativegates_" + provider.provider_name + "_bqskit_opt" + str(opt_level) + "_" + str(num_qubits)
        )
    else:
        filename_native = target_filename

    path = Path(target_directory, filename_native + ".qasm")
    if file_precheck and path.is_file():
        return True
    try:
        gates = utils.get_openqasm_gates()
        qc = transpile(
            qc,
            basis_gates=gates,
            seed_transpiler=10,
            optimization_level=0,
        )
        qc_bqskit = qiskit_to_bqskit(qc)
    except Exception as e:
        print("BQSKit Exception NativeGates: ", e)
        return False

    gate_set = provider.get_native_gates()
    native_gate_set_rebase = get_rebase(gate_set)
    model = MachineModel(
        num_qudits=qc_bqskit.num_qudits,
        gate_set=native_gate_set_rebase,
    )
    qc_bqskit = compile(qc_bqskit, model=model, optimization_level=opt_level, error_threshold=0, seed=10)

    if return_qc:
        return qc_bqskit
    return utils.save_as_qasm(
        qc_bqskit.to("qasm"),
        filename_native,
        gate_set,
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
) -> Circuit:
    ...


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
) -> bool:
    ...


def get_mapped_level(
    qc: QuantumCircuit,
    num_qubits: int | None,
    device: Device,
    opt_level: int,
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
    opt_level -- optimization level
    file_precheck -- flag indicating whether to check whether the file already exists before creating it (again)
    return_qc -- flag if the actual circuit shall be returned
    target_directory -- alternative directory to the default one to store the created circuit
    target_filename -- alternative filename to the default one

    Return values:
    if return_qc == True -- quantum circuit object
    else -- True/False indicating whether the function call was successful or not
    """

    if not target_filename:
        filename_mapped = qc.name + "_mapped_" + device.name + "_bqskit_opt" + str(opt_level) + "_" + str(num_qubits)
    else:
        filename_mapped = target_filename

    path = Path(target_directory, filename_mapped + ".qasm")
    if file_precheck and path.is_file():
        return True

    # try:
    #     gates = list(set(utils.get_openqasm_gates()) - {"rccx"})
    #     qc = transpile(
    #         qc,
    #         basis_gates=gates,
    #         seed_transpiler=10,
    #         optimization_level=0,
    #     )

    #     qc_tket = qiskit_to_tk(qc)
    # except Exception as e:
    #     print("TKET Exception Mapped: ", e)
    #     return False

    qc_bqskit = qiskit_to_bqskit(qc.decompose())
    cmap = device.coupling_map
    cmap_converted = utils.convert_cmap_to_tuple_list(cmap)
    native_gate_set_rebase = get_rebase(device.basis_gates)
    model = MachineModel(
        max(max(cmap)) + 1,
        coupling_graph=cmap_converted,
        gate_set=native_gate_set_rebase,
    )
    qc_bqskit = compile(qc_bqskit, model=model, optimization_level=opt_level, error_threshold=0)

    if return_qc:
        return qc_bqskit
    return utils.save_as_qasm(
        qc_bqskit.to("qasm"),
        filename_mapped,
        device.basis_gates,
        True,
        cmap,
        target_directory,
    )
