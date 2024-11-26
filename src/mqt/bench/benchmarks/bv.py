"""Bernstein-Vazirani benchmark definition."""

from __future__ import annotations

from qiskit import QuantumCircuit


def create_circuit(num_qubits, hidden_string, dynamic=False) -> QuantumCircuit:
    """
    Create a quantum circuit for the Bernstein-Vazirani algorithm.

    :param num_qubits: Number of input qubits (excluding the flag qubit).
    :param hidden_string: The hidden bitstring (as a string of '0's and '1's).
    :param dynamic: Whether to use a dynamic layout (process one qubit at a time).
    :return: A QuantumCircuit object implementing the Bernstein-Vazirani algorithm.
    """
    # Ensure the hidden string matches the number of qubits
    if len(hidden_string) != num_qubits:
        raise ValueError("Length of hidden_string must match num_qubits.")

    # Create a quantum circuit with num_qubits + 1 for the flag qubit and num_qubits classical bits
    circuit = QuantumCircuit(num_qubits + 1, num_qubits)

    # Prepare the flag qubit in the |1⟩ state
    circuit.x(0)

    if dynamic:
        # Dynamic layout: process one qubit at a time
        for i in range(num_qubits):
            # Apply Hadamard to the working qubit
            circuit.h(1)

            # Apply controlled-Z based on the hidden bitstring
            if hidden_string[num_qubits - i - 1] == '1':
                circuit.cz(1, 0)

            # Apply Hadamard to the working qubit again
            circuit.h(1)

            # Measure the working qubit
            circuit.measure(1, i)

            # Reset the working qubit if more rounds are needed
            if i < num_qubits - 1:
                circuit.reset(1)
    else:
        # Static layout: process all qubits at once
        # Apply Hadamard to all input qubits
        for i in range(1, num_qubits + 1):
            circuit.h(i)

        # Apply controlled-Z gates based on the hidden bitstring
        for i in range(1, num_qubits + 1):
            if hidden_string[num_qubits - i] == '1':
                circuit.cz(i, 0)

        # Apply Hadamard to all input qubits again
        for i in range(1, num_qubits + 1):
            circuit.h(i)

        # Measure all input qubits
        for i in range(num_qubits):
            circuit.measure(i + 1, i)

    return circuit