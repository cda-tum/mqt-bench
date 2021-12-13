import random
from fractions import Fraction

import numpy as np
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from qiskit.circuit.library import QFT


def create_circuit(n: int):
    n = n-1 # because of ancilla qubit
    q = QuantumRegister(n, 'q')
    psi = QuantumRegister(1, 'psi')
    c = ClassicalRegister(n, 'c')
    qc = QuantumCircuit(q, psi, c, name="qpeexact")

    # get random n-bit string as target phase
    theta = 0
    while theta == 0:
        theta = random.getrandbits(n)
    lam = Fraction(0, 1)
    #print("theta : ", theta, "correspond to", theta / (1 << n), "bin: ")
    for i in range(n):
        if theta & (1 << (n - i - 1)):
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
    qc.measure(q, c)

    return qc