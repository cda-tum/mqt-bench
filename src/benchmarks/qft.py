from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.circuit.library import QFT


def create_circuit(n: int):
    q = QuantumRegister(n, 'q')
    c = ClassicalRegister(n, 'c')
    qc = QuantumCircuit(q, c, name='qft')
    qc.compose(QFT(num_qubits=n), inplace=True)
    qc.measure_all()

    return qc