## Code from https://qiskit.org/documentation/finance/tutorials/00_amplitude_estimation.html

from qiskit.algorithms import AmplitudeEstimation

from src import utils

# checked

def create_circuit(num_qubits: int):
    ae = AmplitudeEstimation(
        num_eval_qubits=num_qubits - 1,  # magic number one because of to be estimated qubit
    )
    problem = utils.get_estimation_problem()

    qc = ae.construct_circuit(problem)
    qc.name = "canonical_ae"
    qc.measure_all()

    return qc
