from __future__ import annotations

from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit.library import QFT


def create_circuit(num_qubits: int):
    """Returns a quantum circuit implementing the Quantum Fourier Transform algorithm using entangled qubits.

    Keyword arguments:
    num_qubits -- number of qubits of the returned quantum circuit
    """

    q = QuantumRegister(num_qubits, "q")
    qc = QuantumCircuit(q)
    qc.h(q[-1])
    for i in range(1, num_qubits):
        qc.cx(q[num_qubits - i], q[num_qubits - i - 1])

    qc.compose(QFT(num_qubits=num_qubits), inplace=True)

    qc.measure_all()
    qc.name = "qftentangled"

    return qc
