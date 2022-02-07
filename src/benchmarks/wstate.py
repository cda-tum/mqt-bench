import numpy as np
from qiskit import QuantumRegister, QuantumCircuit


def create_circuit(num_qubits: int):
    """Returns a quantum circuit implementing the W state.

    Keyword arguments:
    num_qubits -- number of qubits of the returned quantum circuit
    """

    q = QuantumRegister(num_qubits, 'q')
    qc = QuantumCircuit(q, name="wstate")

    def f_gate(qc: QuantumCircuit, q: QuantumRegister, i: int, j: int, n: int, k: int):
        theta = np.arccos(np.sqrt(1 / (n - k + 1)))
        qc.ry(-theta, q[j])
        qc.cz(q[i], q[j])
        qc.ry(theta, q[j])

    qc.x(q[-1])

    for l in range(1, num_qubits):
        f_gate(qc, q, num_qubits - l, num_qubits - l - 1, num_qubits, l)

    for l in reversed(range(1, num_qubits)):
        qc.cx(l - 1, l)

    qc.measure_all()

    return qc
