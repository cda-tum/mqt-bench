"""Amplitude estimation benchmark definition. Code is based on https://qiskit.org/documentation/finance/tutorials/00_amplitude_estimation.html."""

from __future__ import annotations

import numpy as np
from qiskit import QuantumCircuit


def create_circuit(num_qubits: int, probability: float = 0.2) -> QuantumCircuit:
    """Returns a quantum circuit implementing Quantum Amplitude Estimation.

    Arguments:
        num_qubits: Total number of qubits, including evaluation and target qubits.
        probability: Probability of the "good" state.

    Returns:
        QuantumCircuit: The constructed amplitude estimation circuit.
    """
    if num_qubits < 2:
        msg = "Number of qubits must be at least 2 (1 evaluation + 1 target)."
        raise ValueError(msg)

    num_eval_qubits = num_qubits - 1  # Number of evaluation qubits
    qc = QuantumCircuit(num_qubits, num_eval_qubits)

    # Define the Bernoulli A operator
    theta_p = 2 * np.arcsin(np.sqrt(probability))
    a = QuantumCircuit(1)
    a.ry(theta_p, 0)

    # Define the Grover operator Q = -A S_0 A† S_f
    def grover_operator() -> QuantumCircuit:
        """Construct the Grover operator."""
        q = QuantumCircuit(1)
        # Apply A
        q.ry(theta_p, 0)
        # Apply S0 (reflection around |0>)
        q.z(0)
        # Apply A†
        q.ry(-theta_p, 0)
        return q

    q = grover_operator()

    # Apply Hadamard gates to the evaluation qubits
    qc.h(range(num_eval_qubits))

    # Controlled applications of A and powers of Q
    for i in range(num_eval_qubits):
        qc.append(a.control(1), [i, num_eval_qubits])  # Controlled A
        qc.append(q.control(1), [i, num_eval_qubits])  # Controlled powers of Q

    # Apply the inverse QFT to the evaluation qubits
    qc.append(inverse_qft(num_eval_qubits), range(num_eval_qubits))

    # Measure the evaluation qubits
    qc.measure(range(num_eval_qubits), range(num_eval_qubits))

    qc.name = "ae"
    return qc


def inverse_qft(num_qubits: int) -> QuantumCircuit:
    """Constructs the inverse Quantum Fourier Transform circuit.

    Arguments:
        num_qubits: Number of qubits.

    Returns:
        QuantumCircuit: The inverse QFT circuit.
    """
    qc = QuantumCircuit(num_qubits)
    for i in range(num_qubits // 2):
        qc.swap(i, num_qubits - i - 1)
    for i in range(num_qubits):
        qc.h(i)
        for j in range(i + 1, num_qubits):
            qc.cp(-np.pi / (2 ** (j - i)), j, i)
    return qc
