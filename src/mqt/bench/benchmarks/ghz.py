from __future__ import annotations

from qiskit import QuantumCircuit, QuantumRegister


def create_circuit(num_qubits: int) -> QuantumCircuit:
    """Returns a quantum circuit implementing the GHZ state.

    Keyword arguments:
    num_qubits -- number of qubits of the returned quantum circuit
    """

    q = QuantumRegister(num_qubits, "q")
    qc = QuantumCircuit(q, name="ghz")
    qc.h(q[-1])
    for i in range(1, num_qubits):
        qc.cx(q[num_qubits - i], q[num_qubits - i - 1])
    qc.measure_all()

    return qc
