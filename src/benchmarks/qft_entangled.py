from src.benchmarks import ghz
from qiskit.circuit.library import QFT
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
# checked

def create_circuit(n: int):
    q = QuantumRegister(n, 'q')
    qc = QuantumCircuit(q)
    qc.h(q[-1])
    for i in range(1, n):
        qc.cx(q[n - i], q[n - i - 1])

    qc.compose(QFT(num_qubits=n), inplace=True)

    qc.measure_all()
    qc.name = "qft_entangled"

    return qc