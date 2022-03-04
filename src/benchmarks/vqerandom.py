from qiskit.circuit.library import RealAmplitudes
import numpy as np


def create_circuit(num_qubits: int):
    """Returns a quantum circuit implementing the Variational Quantum Eigensolver Algorithm with random parameter
    values.

    Keyword arguments:
    num_qubits -- number of qubits of the returned quantum circuit
    """

    np.random.seed = 10
    qc = RealAmplitudes(num_qubits, reps=2)
    num_params = qc.num_parameters
    qc = qc.bind_parameters(np.random.rand(num_params))
    qc.measure_all()
    qc.name = "vqerandom"

    return qc
