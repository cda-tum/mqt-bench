from qiskit.circuit.random import random_circuit
from qiskit import QuantumCircuit, transpile
from mqt.bench import utils


def create_circuit(num_qubits: int) -> QuantumCircuit:
    qc = random_circuit(num_qubits, num_qubits*2, measure=True, seed=10)
    gates = list(set(utils.get_openqasm_gates()) - {"rccx", "csx", "cu"})
    qc = transpile(
        qc,
        basis_gates=gates,
        seed_transpiler=10,
        optimization_level=1,
    )
    qc.name = "random"
    return qc