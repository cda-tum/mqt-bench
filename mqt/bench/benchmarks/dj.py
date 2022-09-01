# Code from https://qiskit.org/textbook/ch-algorithms/deutsch-jozsa.html

from __future__ import annotations

import numpy as np
from qiskit import QuantumCircuit


def dj_oracle(case, n):
    # plus one output qubit
    oracle_qc = QuantumCircuit(n + 1)

    if case == "balanced":
        np.random.seed = 10
        b_str = ""
        for _ in range(n):
            b = np.random.randint(0, 2)
            b_str = b_str + str(b)

        for qubit in range(len(b_str)):
            if b_str[qubit] == "1":
                oracle_qc.x(qubit)

        for qubit in range(n):
            oracle_qc.cx(qubit, n)

        for qubit in range(len(b_str)):
            if b_str[qubit] == "1":
                oracle_qc.x(qubit)

    if case == "constant":
        output = np.random.randint(2)
        if output == 1:
            oracle_qc.x(n)

    oracle_gate = oracle_qc.to_gate()
    oracle_gate.name = "Oracle"  # To show when we display the circuit
    return oracle_gate


def dj_algorithm(oracle, n):
    dj_circuit = QuantumCircuit(n + 1, n)

    dj_circuit.x(n)
    dj_circuit.h(n)

    for qubit in range(n):
        dj_circuit.h(qubit)

    dj_circuit.append(oracle, range(n + 1))

    for qubit in range(n):
        dj_circuit.h(qubit)

    dj_circuit.barrier()
    for i in range(n):
        dj_circuit.measure(i, i)

    return dj_circuit


def create_circuit(n: int, balanced: bool = True):
    """Returns a quantum circuit implementing the Deutsch-Josza algorithm.

    Keyword arguments:
    num_qubits -- number of qubits of the returned quantum circuit
    balanced -- True for a balanced and False for a constant oracle
    """

    if balanced:
        oracle_mode = "balanced"
    else:
        oracle_mode = "constant"
    n = n - 1  # because of ancilla qubit
    oracle_gate = dj_oracle(oracle_mode, n)
    qc = dj_algorithm(oracle_gate, n)
    qc.name = "dj"

    return qc
