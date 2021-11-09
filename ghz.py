from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, AncillaRegister
from utils import measure

def create_circuit(n: int, include_measurements: bool = True):
    q = QuantumRegister(n, 'q')
    c = ClassicalRegister(n, 'c')
    qc = QuantumCircuit(q, c, name='ghz')
    qc.h(q[-1])
    for i in range(1, n):
        qc.cx(q[n - i], q[n - i - 1])
    if include_measurements:
        measure(qc, q, c)
    return qc