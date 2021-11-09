from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.circuit.library import GraphState

import networkx as nx
from utils import measure

def create_circuit(n, include_measurements: bool = True):
    q = QuantumRegister(n, 'q')
    c = ClassicalRegister(n, 'c')
    qc = QuantumCircuit(q, c, name="graph_state")

    G = nx.random_regular_graph(3, n)
    A = nx.convert_matrix.to_numpy_array(G)
    qc.compose(GraphState(A), inplace=True)
    if include_measurements:
        measure(qc, q, c)
    return qc

