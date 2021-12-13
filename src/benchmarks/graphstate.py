from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.circuit.library import GraphState

import networkx as nx

#checked

def create_circuit(num_qubits:int, degree:int = 2):
    q = QuantumRegister(num_qubits, 'q')
    qc = QuantumCircuit(q, name="graphstate")

    G = nx.random_regular_graph(degree, num_qubits)
    A = nx.convert_matrix.to_numpy_array(G)
    qc.compose(GraphState(A), inplace=True)
    qc.measure_all()

    return qc

