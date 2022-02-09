# Code from https://qiskit.org/textbook/ch-algorithms/deutsch-jozsa.html

from qiskit import QuantumCircuit
import numpy as np


def dj_oracle(case, n):
    # plus one output qubit
    oracle_qc = QuantumCircuit(n + 1)

    # First, let's deal with the case in which oracle is balanced
    if case == "balanced":
        # First generate a random number that tells us which CNOTs to
        # wrap in X-gates:
        rng = np.random.default_rng(12345)
        b_str=""
        for _ in range(n):
            b = np.random.randint(0, 2)
            b_str = b_str + str(b)
        #b = rng.integers(low=0, high=2)
        #b = np.random.randint(1, 2 ** n, dtype=np.int64())
        # Next, format 'b' as a binary string of length 'n', padded with zeros:
        #b_str = format(b, '0' + str(n) + 'b')
        # Next, we place the first X-gates. Each digit in our binary string
        # corresponds to a qubit, if the digit is 0, we do nothing, if it's 1
        # we apply an X-gate to that qubit:
        for qubit in range(len(b_str)):
            if b_str[qubit] == '1':
                oracle_qc.x(qubit)
        # Do the controlled-NOT gates for each qubit, using the output qubit
        # as the target:
        for qubit in range(n):
            oracle_qc.cx(qubit, n)
        # Next, place the final X-gates
        for qubit in range(len(b_str)):
            if b_str[qubit] == '1':
                oracle_qc.x(qubit)

    # Case in which oracle is constant
    if case == "constant":
        # First decide what the fixed output of the oracle will be
        # (either always 0 or always 1)
        output = np.random.randint(2)
        if output == 1:
            oracle_qc.x(n)

    oracle_gate = oracle_qc.to_gate()
    oracle_gate.name = "Oracle"  # To show when we display the circuit
    return oracle_gate


def dj_algorithm(oracle, n):
    dj_circuit = QuantumCircuit(n + 1, n)
    # Set up the output qubit:
    dj_circuit.x(n)
    dj_circuit.h(n)
    # And set up the input register:
    for qubit in range(n):
        dj_circuit.h(qubit)
    # Let's append the oracle gate to our circuit:
    dj_circuit.append(oracle, range(n + 1))
    # Finally, perform the H-gates again and measure:
    for qubit in range(n):
        dj_circuit.h(qubit)

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
        oracle_mode = 'balanced'
    else:
        oracle_mode = 'constant'
    n = n - 1  # because of ancilla qubit
    oracle_gate = dj_oracle(oracle_mode, n)
    qc = dj_algorithm(oracle_gate, n)
    qc.name = "dj"

    return qc
