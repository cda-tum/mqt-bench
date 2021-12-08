from qiskit.algorithms.factorizers import Shor

## checked


def create_circuit(num_to_be_factorized: int, a: int = 2):
    qc = Shor().construct_circuit(num_to_be_factorized, a, measurement=True)
    qc.name = "shor_" + str(num_to_be_factorized) + '_' + str(a)

    return qc