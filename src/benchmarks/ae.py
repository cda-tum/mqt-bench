## Code from https://qiskit.org/documentation/finance/tutorials/00_amplitude_estimation.html

import numpy as np
from qiskit.circuit import QuantumCircuit
from qiskit.algorithms import EstimationProblem
from qiskit.algorithms import AmplitudeEstimation

class BernoulliA(QuantumCircuit):
    """A circuit representing the Bernoulli A operator."""

    def __init__(self, probability):
        super().__init__(1)  # circuit on 1 qubit

        theta_p = 2 * np.arcsin(np.sqrt(probability))
        self.ry(theta_p, 0)


class BernoulliQ(QuantumCircuit):
    """A circuit representing the Bernoulli Q operator."""

    def __init__(self, probability):
        super().__init__(1)  # circuit on 1 qubit

        self._theta_p = 2 * np.arcsin(np.sqrt(probability))
        self.ry(2 * self._theta_p, 0)

    def power(self, k):
        # implement the efficient power of Q
        q_k = QuantumCircuit(1)
        q_k.ry(2 * k * self._theta_p, 0)
        return q_k

def create_circuit(n: int):
    p = 0.2
    A = BernoulliA(p)
    Q = BernoulliQ(p)

    problem = EstimationProblem(
        state_preparation = A,  # A operator
        grover_operator = Q,  # Q operator
        objective_qubits = [0],  # the "good" state Psi1 is identified as measuring |1> in qubit 0
    )

    # Magic -1 because the to be estimated amplitude is one qubit
    ae = AmplitudeEstimation(
        num_eval_qubits = n-1
    )
    qc = ae.construct_circuit(estimation_problem=problem)
    qc.name="ae"

    qc.measure_all()
    return qc
