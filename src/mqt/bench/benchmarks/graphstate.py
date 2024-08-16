"""Graophstate benchmark definition."""

from __future__ import annotations

import numpy as np
import networkx as nx
from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit.library import GraphState


def create_circuit(num_qubits: int, degree: int = 2) -> QuantumCircuit:
    """Returns a quantum circuit implementing a graph state.

    Arguments:
        num_qubits: number of qubits of the returned quantum circuit
        degree: number of edges per node
    """
    q = QuantumRegister(num_qubits, "q")
    qc = QuantumCircuit(q, name="graphstate")

    g = nx.random_regular_graph(degree, num_qubits)
    #a = nx.convert_matrix.to_numpy_array(g)
    a = np.diag([1] * num_qubits, k=1) + np.diag([1] * num_qubits, k=-1)
    a[0, -1] = 1 # always use a simple cycle graph
    a[-1, 0] = 1

    qc.compose(GraphState(a), inplace=True)
    qc.measure_all()

    return qc
