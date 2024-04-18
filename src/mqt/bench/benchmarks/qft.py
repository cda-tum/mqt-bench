from __future__ import annotations

from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit.library import QFT


def create_circuit(num_qubits: int) -> QuantumCircuit:
    """Returns a quantum circuit implementing the Quantum Fourier Transform algorithm.

    Keyword Arguments:
    num_qubits -- number of qubits of the returned quantum circuit
    """
    q = QuantumRegister(num_qubits, "q")
    qc = QuantumCircuit(q, name="qft")
    qc.compose(QFT(num_qubits=num_qubits), inplace=True)
    qc.measure_all()

    return qc
