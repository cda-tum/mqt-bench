import random
from fractions import Fraction

import numpy as np
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from qiskit.circuit.library import QFT
from utils import measure


def create_circuit(n: int, include_measurements: bool = True):
    q = QuantumRegister(n, 'q')
    psi = QuantumRegister(1, 'psi')
    c = ClassicalRegister(n + 1, 'c')
    qc = QuantumCircuit(q, psi, c, name="qpe_inexact")

    # get random n+1-bit string as target phase
    theta = 0
    while theta == 0 or (theta & 1) == 0:
        theta = random.getrandbits(n + 1)
    lam = Fraction(0, 1)
    # print("theta : ", theta, "correspond to", theta / (1 << (n+1)), "bin: ")
    for i in range(n + 1):
        if theta & (1 << (n - i)):
            lam += Fraction(1, (1 << i))

    qc.x(psi)
    qc.h(q)

    for i in range(n):
        angle = (lam * (1 << i)) % 2
        if angle > 1:
            angle -= 2
        if angle != 0:
            qc.cp(angle * np.pi, psi, q[i])

    qc.compose(QFT(num_qubits=n, inverse=True), inplace=True, qubits=list(range(n)))

    if include_measurements:
        measure(qc, q, c)

    return qc