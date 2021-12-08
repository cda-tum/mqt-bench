## Code maybe from https://qiskit.org/textbook/ch-applications/hhl_tutorial.html, example looks slightly different though

## checked

import numpy as np
from qiskit.algorithms.linear_solvers.matrices.tridiagonal_toeplitz import TridiagonalToeplitz
from qiskit.algorithms.linear_solvers.hhl import HHL

def create_circuit(n: int):
    a = 1
    b = -1 / 3

    vector = np.array([1] + [0] * (2 ** n - 1))
    tridi_matrix = TridiagonalToeplitz(n, a, b)
    qc = HHL().solve(tridi_matrix, vector).state

    qc.name = "HHL"
    qc.measure_all()

    return qc

