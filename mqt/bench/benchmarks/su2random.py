from __future__ import annotations

import numpy as np
from qiskit.circuit.library import EfficientSU2


def create_circuit(num_qubits: int):
    """Returns a quantum circuit implementing EfficientSU2 ansatz with random parameter
    values.

    Keyword arguments:
    num_qubits -- number of qubits of the returned quantum circuit
    """

    np.random.seed = 10
    qc = EfficientSU2(num_qubits, entanglement="full", reps=3)
    num_params = qc.num_parameters
    qc = qc.bind_parameters(np.random.rand(num_params))
    qc.measure_all()
    qc.name = "su2random"

    return qc
