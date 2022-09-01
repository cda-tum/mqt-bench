# Code based on https://qiskit.org/textbook/ch-applications/hhl_tutorial.html

from __future__ import annotations

import numpy as np
from qiskit.algorithms.linear_solvers.hhl import HHL
from qiskit.algorithms.linear_solvers.matrices.tridiagonal_toeplitz import (
    TridiagonalToeplitz,
)


def create_circuit(num_qubits: int):
    """Returns a quantum circuit implementing the HHL algorithm for a specific example matrix.

    Keyword arguments:
    num_qubits -- number of qubits of the returned quantum circuit
    """

    a = 1
    b = -1 / 3

    vector = np.array([1] + [0] * (2**num_qubits - 1))
    tridi_matrix = TridiagonalToeplitz(num_qubits, a, b)
    qc = HHL().solve(tridi_matrix, vector).state

    qc.name = "hhl"
    qc.measure_all()

    return qc
