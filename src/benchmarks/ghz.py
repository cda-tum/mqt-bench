from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister

def create_circuit(n: int):
    q = QuantumRegister(n, 'q')
    c = ClassicalRegister(n, 'c')
    qc = QuantumCircuit(q, c, name='ghz')
    qc.h(q[-1])
    for i in range(1, n):
        qc.cx(q[n - i], q[n - i - 1])
    qc.measure_all()

    return qc