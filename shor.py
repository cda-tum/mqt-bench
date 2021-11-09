from qiskit.algorithms.factorizers import Shor


def create_circuit(N: int, a: int = 2, include_measurements: bool = True):
    qc = Shor().construct_circuit(N, a, include_measurements)
    qc.name = "shor_" + str(N) + '_' + str(a)

    return qc