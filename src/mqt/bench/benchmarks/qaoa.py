# Code from https://github.com/qiskit-community/qiskit-application-modules-demo-sessions/blob/main/qiskit-optimization/qiskit-optimization-demo.ipynb

from __future__ import annotations

from typing import TYPE_CHECKING

from qiskit.algorithms.minimum_eigensolvers import QAOA
from qiskit.algorithms.optimizers import SLSQP
from qiskit.primitives import Sampler
from qiskit_optimization import QuadraticProgram

from mqt.bench.utils import get_examplary_max_cut_qp

if TYPE_CHECKING:  # pragma: no cover
    from qiskit import QuantumCircuit


def create_circuit(num_qubits: int) -> QuantumCircuit:
    """Returns a quantum circuit implementing the Quantum Approximation Optimization Algorithm for a specific max-cut
     example.

    Keyword arguments:
    num_qubits -- number of qubits of the returned quantum circuit
    """

    qp = get_examplary_max_cut_qp(num_qubits)
    assert isinstance(qp, QuadraticProgram)

    qaoa = QAOA(sampler=Sampler(), reps=2, optimizer=SLSQP(maxiter=25))
    qaoa_result = qaoa.compute_minimum_eigenvalue(qp.to_ising()[0])
    qc = qaoa.ansatz.bind_parameters(qaoa_result.optimal_point)

    qc.name = "qaoa"

    return qc
