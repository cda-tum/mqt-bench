import numpy as np
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from utils import measure


def create_circuit(n: int, include_measurements: bool = True):
    q = QuantumRegister(n, 'q')
    c = ClassicalRegister(n, 'c')
    qc = QuantumCircuit(q, c, name="w_state")

    def f_gate(qc: QuantumCircuit, q: QuantumRegister, i: int, j: int, n: int, k: int):
        theta = np.arccos(np.sqrt(1 / (n - k + 1)))
        qc.ry(-theta, q[j])
        qc.cz(q[i], q[j])
        qc.ry(theta, q[j])

    qc.x(q[-1])
    for l in range(1, n):
        f_gate(qc, q, n - l, n - l - 1, n, l)
    for l in reversed(range(1, n)):
        qc.cx(l - 1, l)

    if include_measurements:
        measure(qc, q, c)

    return qc