# Code from https://qiskit.org/documentation/finance/tutorials/00_amplitude_estimation.html

from __future__ import annotations

import numpy as np
from qiskit import QuantumCircuit
from qiskit.algorithms import AmplitudeEstimation, EstimationProblem


def create_circuit(num_qubits: int) -> QuantumCircuit:
    """Returns a quantum circuit implementing Quantum Amplitude Estimation.

    Keyword arguments:
    num_qubits -- number of qubits of the returned quantum circuit
    """

    ae = AmplitudeEstimation(
        num_eval_qubits=num_qubits - 1,  # -1 because of the to be estimated qubit
    )
    problem = get_estimation_problem()

    qc = ae.construct_circuit(problem)
    qc.name = "ae"
    qc.measure_all()

    return qc


class BernoulliQ(QuantumCircuit):  # type: ignore[misc]
    """A circuit representing the Bernoulli Q operator."""

    def __init__(self, probability: float) -> None:
        super().__init__(1)  # circuit on 1 qubit

        self._theta_p = 2 * np.arcsin(np.sqrt(probability))
        self.ry(2 * self._theta_p, 0)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, BernoulliQ) and self._theta_p == other._theta_p

    def power(self, power: float, _matrix_power: bool = True) -> QuantumCircuit:
        # implement the efficient power of Q
        q_k = QuantumCircuit(1)
        q_k.ry(2 * power * self._theta_p, 0)
        return q_k


def get_estimation_problem() -> EstimationProblem:
    """Returns a estimation problem instance for a fixed p value."""

    p = 0.2

    """A circuit representing the Bernoulli A operator."""
    a = QuantumCircuit(1)
    theta_p = 2 * np.arcsin(np.sqrt(p))
    a.ry(theta_p, 0)

    """A circuit representing the Bernoulli Q operator."""
    q = BernoulliQ(p)

    return EstimationProblem(
        state_preparation=a,  # A operator
        grover_operator=q,  # Q operator
        objective_qubits=[0],  # the "good" state Psi1 is identified as measuring |1> in qubit 0
    )
