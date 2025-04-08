"""QAOA benchmark definition. Code is based on https://github.com/qiskit-community/qiskit-application-modules-demo-sessions/blob/main/qiskit-optimization/qiskit-optimization-demo.ipynb."""

from __future__ import annotations

import numpy as np
from qiskit import QuantumCircuit


def create_circuit(num_qubits: int, repetitions: int = 2) -> QuantumCircuit:
    """Constructs a quantum circuit implementing QAOA for a Max-Cut example with random parameters.

    Arguments:
        num_qubits: Number of qubits in the circuit (equal to the number of graph nodes).
        repetitions: Number of QAOA layers (repetitions of the ansatz).

    Returns:
        QuantumCircuit: Quantum circuit implementing QAOA.
    """
    # Set the random number generator
    rng = np.random.default_rng(10)

    # Example adjacency matrix for Max-Cut (toy problem)
    adjacency_matrix = rng.integers(0, 2, size=(num_qubits, num_qubits))
    adjacency_matrix = np.triu(adjacency_matrix, 1)  # Upper triangular part for undirected graph

    # Random initialization of parameters
    gamma_values = rng.uniform(0, np.pi, repetitions)
    beta_values = rng.uniform(0, np.pi, repetitions)

    # Initialize QAOA circuit
    qc = QuantumCircuit(num_qubits)

    # Start in uniform superposition
    qc.h(range(num_qubits))

    # Define cost and mixer operators for each layer
    for layer in range(repetitions):
        # Cost Hamiltonian
        for i in range(num_qubits):
            for j in range(i + 1, num_qubits):
                if adjacency_matrix[i, j] != 0:
                    qc.rzz(2 * gamma_values[layer], i, j)

        # Mixer Hamiltonian
        for i in range(num_qubits):
            qc.rx(2 * beta_values[layer], i)

    qc.name = "qaoa"

    return qc
