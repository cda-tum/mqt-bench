## Code from https://qiskit.org/documentation/stubs/qiskit.algorithms.HHL.html#qiskit.algorithms.HHL

import numpy as np
from qiskit import QuantumCircuit
from qiskit.algorithms.linear_solvers.hhl import HHL
from qiskit.algorithms.linear_solvers.matrices import TridiagonalToeplitz
from qiskit.algorithms.linear_solvers.observables import MatrixFunctional

# def create_circuit():
#     matrix = TridiagonalToeplitz(2, 1, 1 / 3, trotter_steps=2)
#     right_hand_side = [1.0, -2.1, 3.2, -4.3]
#     observable = MatrixFunctional(1, 1 / 2)
#     rhs = right_hand_side / np.linalg.norm(right_hand_side)
#
#     # Initial state circuit
#     num_qubits = matrix.num_state_qubits
#     qc = QuantumCircuit(num_qubits)
#     qc.isometry(rhs, list(range(num_qubits)), None)
#
#     hhl = HHL()
#     solution = hhl.solve(matrix, qc, observable)
#     approx_result = solution.observable


## Code from https://qiskit.org/textbook/ch-applications/hhl_tutorial.html
from scipy.sparse import diags
from qiskit import transpile
import numpy as np
from qiskit.algorithms.linear_solvers.numpy_linear_solver import NumPyLinearSolver
from qiskit.algorithms.linear_solvers.matrices.tridiagonal_toeplitz import TridiagonalToeplitz
from qiskit.algorithms.linear_solvers.hhl import HHL

def create_circuit(n: int, include_measurements: bool = True):

    a = 1
    b = -1 / 3

    #matrix = diags([b, a, b], [-1, 0, 1], shape=(2 ** nb, 2 ** nb)).toarray()
    vector = np.array([1] + [0] * (2 ** n - 1))

    #naive_hhl_solution = HHL().solve(matrix, vector)
    tridi_matrix = TridiagonalToeplitz(n, a, b)
    tridi_solution = HHL().solve(tridi_matrix, vector)

    #return naive_hhl_solution.state
    return tridi_solution.state

