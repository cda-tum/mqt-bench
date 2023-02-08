from __future__ import annotations

from qiskit.algorithms.factorizers import Shor


def create_circuit(num_to_be_factorized: int, a: int = 2):
    """Returns a quantum circuit implementing the Shor's algorithm.

    Keyword arguments:
    num_to_be_factorized -- number which shall be factorized
    a -- any integer that satisfies 1 < a < num_to_be_factorized and gcd(a, num_to_be_factorized) = 1
    """

    qc = Shor().construct_circuit(num_to_be_factorized, a)
    qc.measure_all()
    qc.name = "shor_" + str(num_to_be_factorized) + "_" + str(a)

    return qc
