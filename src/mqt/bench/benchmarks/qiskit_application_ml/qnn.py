# inspired from https://qiskit.org/ecosystem/machine-learning/stubs/qiskit_machine_learning.neural_networks.EstimatorQNN.html
from __future__ import annotations

import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit.library import RealAmplitudes, ZZFeatureMap


def create_circuit(num_qubits: int) -> QuantumCircuit:
    """Returns a quantum circuit implementing a Quantum Neural Network (QNN) with a ZZ FeatureMap and a RealAmplitudes ansatz.

    Keyword arguments:
    num_qubits -- number of qubits of the returned quantum circuit
    """
    feature_map = ZZFeatureMap(feature_dimension=num_qubits)
    ansatz = RealAmplitudes(num_qubits=num_qubits, reps=1)

    qc = QuantumCircuit(num_qubits)
    feature_map = feature_map.bind_parameters([1 for _ in range(feature_map.num_parameters)])
    ansatz = ansatz.bind_parameters(np.random.rand(ansatz.num_parameters))
    qc.compose(feature_map, inplace=True)
    qc.compose(ansatz, inplace=True)

    qc.name = "qnn"
    qc.measure_all()
    return qc
