from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.circuit.library import GraphState

import networkx as nx

def create_circuit(n):
    q = QuantumRegister(n, 'q')
    c = ClassicalRegister(n, 'c')
    qc = QuantumCircuit(q, c, name="graph_state")

    G = nx.random_regular_graph(4, n)
    A = nx.convert_matrix.to_numpy_array(G)
    qc.compose(GraphState(A), inplace=True)
    qc.measure_all()

    return qc

