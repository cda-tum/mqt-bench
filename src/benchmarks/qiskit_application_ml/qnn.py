## code from https://qiskit.org/documentation/machine-learning/tutorials/01_neural_networks.html

import numpy as np
from qiskit.circuit.library import RealAmplitudes, ZZFeatureMap

from qiskit_machine_learning.neural_networks import CircuitQNN

def create_circuit(num_qubits: int):
    num_qubits = num_qubits
    qc = RealAmplitudes(num_qubits, entanglement='linear', reps=2)

    # specify circuit QNN
    qnn = CircuitQNN(qc, [], qc.parameters, sparse=True, quantum_instance=qi_qasm)
    # define (random) input and weights
    np.random.seed(0)

    input = np.random.rand(qnn.num_inputs)
    weights = np.random.rand(qnn.num_weights)
    # QNN forward pass

    qc = qnn.circuit
    qc.name = "qnn"

    return qc