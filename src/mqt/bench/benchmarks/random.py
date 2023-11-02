from __future__ import annotations

from qiskit import QuantumCircuit, transpile
from qiskit.circuit.random import random_circuit

from mqt.bench import utils


def create_circuit(num_qubits: int) -> QuantumCircuit:
    """Returns a random quantum circuit twice as deep as wide. The random gate span over four qubits maximum.

    Keyword arguments:
    num_qubits -- number of qubits of the returned quantum circuit
    """
    qc = random_circuit(num_qubits, num_qubits * 2, measure=False, seed=10)
    gates = list(set(utils.get_openqasm_gates()) - {"rccx", "csx", "cu"})
    qc = transpile(
        qc,
        basis_gates=gates,
        seed_transpiler=10,
        optimization_level=1,
    )
    qc.measure_all()
    qc.name = "random"
    return qc
