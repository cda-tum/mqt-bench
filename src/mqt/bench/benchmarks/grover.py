from __future__ import annotations

import numpy as np
from qiskit import AncillaRegister, QuantumCircuit, QuantumRegister
from qiskit.algorithms import Grover
from qiskit.circuit.library import GroverOperator


def create_circuit(num_qubits: int, ancillary_mode: str = "noancilla") -> QuantumCircuit:
    """Returns a quantum circuit implementing Grover's algorithm.

    Keyword arguments:
    num_qubits -- number of qubits of the returned quantum circuit
    ancillary_mode -- defining the decomposition scheme
    """

    num_qubits = num_qubits - 1  # -1 because of the flag qubit
    q = QuantumRegister(num_qubits, "q")
    flag = AncillaRegister(1, "flag")

    state_preparation = QuantumCircuit(q, flag)
    state_preparation.h(q)
    state_preparation.x(flag)

    oracle = QuantumCircuit(q, flag)
    oracle.mcp(np.pi, q, flag)

    operator = GroverOperator(oracle, mcx_mode=ancillary_mode)
    iterations = Grover.optimal_num_iterations(1, num_qubits)

    num_qubits = operator.num_qubits - 1  # -1 because last qubit is "flag" qubit and already taken care of

    # num_qubits may differ now depending on the mcx_mode
    q2 = QuantumRegister(num_qubits, "q")
    qc = QuantumCircuit(q2, flag, name="grover")
    qc.compose(state_preparation, inplace=True)

    qc.compose(operator.power(iterations), inplace=True)
    qc.measure_all()
    qc.name = qc.name + "-" + ancillary_mode

    return qc
