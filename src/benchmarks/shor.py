from qiskit.algorithms.factorizers import Shor


def create_circuit(N: int, a: int = 2):
    qc = Shor().construct_circuit(N, a, measurement=True)
    qc.name = "shor_" + str(N) + '_' + str(a)

    return qc