from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister

# checked

def create_circuit(n: int):
    q = QuantumRegister(n, 'q')
    qc = QuantumCircuit(q, name='ghz')
    qc.h(q[-1])
    for i in range(1, n):
        qc.cx(q[n - i], q[n - i - 1])
    qc.measure_all()

    return qc