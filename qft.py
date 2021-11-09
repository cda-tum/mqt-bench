from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, AncillaRegister
from qiskit.circuit.library import QFT

from utils import measure

def create_circuit(n: int, include_measurements: bool = True):
    q = QuantumRegister(n, 'q')
    c = ClassicalRegister(n, 'c')
    qc = QuantumCircuit(q, c, name='qft')
    qc.compose(QFT(num_qubits=n), inplace=True)
    if include_measurements:
        measure(qc, q, c)
    return qc