from __future__ import annotations

import numpy as np
from qiskit.circuit.library import RealAmplitudes


def create_circuit(num_qubits: int):
    """Returns a quantum circuit implementing the RealAmplitudes ansatz with random parameter
    values.

    Keyword arguments:
    num_qubits -- number of qubits of the returned quantum circuit
    """

    np.random.seed = 10
    qc = RealAmplitudes(num_qubits, entanglement="full", reps=3)
    num_params = qc.num_parameters
    qc = qc.bind_parameters(np.random.rand(num_params))
    qc.measure_all()
    qc.name = "realamprandom"

    return qc
