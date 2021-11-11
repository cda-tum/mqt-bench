## Code from https://qiskit.org/documentation/stubs/qiskit.algorithms.HHL.html#qiskit.algorithms.HHL

import numpy as np
from qiskit import QuantumCircuit
from qiskit.algorithms.linear_solvers.hhl import HHL
from qiskit.algorithms.linear_solvers.matrices import TridiagonalToeplitz
from qiskit.algorithms.linear_solvers.observables import MatrixFunctional

def create_circuit():
    matrix = TridiagonalToeplitz(2, 1, 1 / 3, trotter_steps=2)
    right_hand_side = [1.0, -2.1, 3.2, -4.3]
    observable = MatrixFunctional(1, 1 / 2)
    rhs = right_hand_side / np.linalg.norm(right_hand_side)

    # Initial state circuit
    num_qubits = matrix.num_state_qubits
    qc = QuantumCircuit(num_qubits)
    qc.isometry(rhs, list(range(num_qubits)), None)

    hhl = HHL()
    solution = hhl.solve(matrix, qc, observable)
    approx_result = solution.observable