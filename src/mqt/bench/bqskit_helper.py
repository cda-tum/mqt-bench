from __future__ import annotations

import atexit
import math
from cmath import exp
from pathlib import Path
from typing import TYPE_CHECKING, Literal, overload

import numpy as np
import numpy.typing as npt
from bqskit import compile
from bqskit.compiler import Compiler, MachineModel
from bqskit.ext import qiskit_to_bqskit
from bqskit.ir.gates import CNOTGate, CZGate, RXGate, RXXGate, RYGate, RZGate, RZZGate, SXGate, XGate
from bqskit.ir.gates.constantgate import ConstantGate
from bqskit.ir.gates.qubitgate import QubitGate
from bqskit.qis.unitary.differentiable import DifferentiableUnitary
from bqskit.qis.unitary.unitarymatrix import UnitaryMatrix
from bqskit.utils.cachedclass import CachedClass
from qiskit import transpile

from mqt.bench import utils

if TYPE_CHECKING:  # pragma: no cover
    from bqskit.ir import Gate
    from bqskit.ir.circuit import Circuit
    from bqskit.qis.unitary.unitary import RealVector
    from qiskit import QuantumCircuit

    from mqt.bench.devices import Device, Provider


class CachedCompiler:
    _instance: CachedCompiler | None = None
    _compiler: Compiler | None = None

    # Ruff seems to give a false positive check for the return type of this function.
    def __new__(cls) -> CachedCompiler:  # noqa: PYI034
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._compiler = Compiler()
            atexit.register(cls.close_compiler)
        return cls._instance

    @property
    def compiler(self) -> Compiler:
        return self._compiler

    @classmethod
    def close_compiler(cls) -> None:
        if cls._compiler is not None:
            cls._compiler.close()


class XXPlusYYGate(QubitGate, DifferentiableUnitary, CachedClass):  # type: ignore[misc]
    """XX+YY interaction gate.

    A 2-qubit parameterized XX+YY interaction, also known as an XY gate. Its action is to induce
    a coherent rotation by some angle between :math:`|01\\rangle` and :math:`|10\\rangle`.

    .. math::
            \\renewcommand{\\rotationangle}{\\frac{\\theta}{2}}
            \\begin{pmatrix}
                1 & 0 & 0 & 0  \\
                0 & \cos\left(\\rotationangle\\right) & -i\sin\left(\\rotationangle\\right)e^{-i\\beta} & 0 \\\\
                0 & -i\sin\left(\\rotationangle\\right)e^{i\\beta} & \cos\left(\\rotationangle\\right) & 0 \\\\
                0 & 0 & 0 & 1
            \\end{pmatrix}
    """

    _num_qudits = 2
    _num_params = 2
    _qasm_name = "opaque xx_plus_yy"

    def get_unitary(self, params: RealVector = None) -> UnitaryMatrix:
        """Return the unitary for this gate, see :class:`Unitary` for more."""
        if params is None:
            params = []
        self.check_parameters(params)

        half_theta = float(params[0]) / 2
        beta = float(params[1])
        cos = math.cos(half_theta)
        sin = math.sin(half_theta)
        return UnitaryMatrix(
            [
                [1, 0, 0, 0],
                [0, cos, -1j * sin * exp(-1j * beta), 0],
                [0, -1j * sin * exp(1j * beta), cos, 0],
                [0, 0, 0, 1],
            ],
        )

    def get_grad(self, params: RealVector = None) -> npt.NDArray[np.complex128]:
        """
        Return the gradient for this gate.

        See :class:`DifferentiableUnitary` for more info.
        """
        if params is None:
            params = []
        self.check_parameters(params)

        half_theta = params[0] / 2
        d11 = d22 = -1 / 2 * np.sin(half_theta)
        d21 = -1 / 2 * 1j * exp(1j * params[1]) * np.cos(half_theta)
        d12 = -1 / 2 * 1j * exp(-1j * params[1]) * np.cos(half_theta)

        d_wrt_theta = np.array(
            [
                [0, 0, 0, 0],
                [0, d11, d12, 0],
                [0, d21, d22, 0],
                [0, 0, 0, 0],
            ],
            dtype=np.complex128,
        )

        d12 = -exp(-1j * params[1]) * np.sin(half_theta)
        d21 = exp(1j * params[1]) * np.sin(half_theta)

        d_wrt_beta = np.array(
            [
                [0, 0, 0, 0],
                [0, 0, d12, 0],
                [0, d21, 0, 0],
                [0, 0, 0, 0],
            ],
            dtype=np.complex128,
        )

        return np.array(
            [d_wrt_theta, d_wrt_beta],
            dtype=np.complex128,
        )


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
    _sqrt2 = math.sqrt(2)
    _utry = UnitaryMatrix(
        [
            [0, 1 / _sqrt2, 0, 1j / _sqrt2],
            [1 / _sqrt2, 0, -1j / _sqrt2, 0],
            [0, 1j / _sqrt2, 0, 1 / _sqrt2],
            [-1j / _sqrt2, 0, 1 / _sqrt2, 0],
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
        "xx_plus_yy": XXPlusYYGate(),
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
    compiler = CachedCompiler().compiler
    qc_bqskit = compile(qc_bqskit, model=model, optimization_level=opt_level, compiler=compiler, seed=10)

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
        print("BQSKit Exception Mapped: ", e)
        return False

    cmap = device.coupling_map
    cmap_converted = utils.convert_cmap_to_tuple_list(cmap)
    native_gate_set_rebase = get_rebase(device.basis_gates)
    model = MachineModel(
        max(max(cmap)) + 1,
        coupling_graph=cmap_converted,
        gate_set=native_gate_set_rebase,
    )
    compiler = CachedCompiler().compiler
    qc_bqskit = compile(qc_bqskit, model=model, optimization_level=opt_level, compiler=compiler, seed=10)

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
