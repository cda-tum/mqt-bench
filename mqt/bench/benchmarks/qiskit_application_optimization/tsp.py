# Code based on https://qiskit.org/documentation/optimization/tutorials/06_examples_max_cut_and_tsp.html

from __future__ import annotations

from qiskit import Aer
from qiskit.algorithms import VQE
from qiskit.algorithms.optimizers import SPSA
from qiskit.circuit.library import TwoLocal
from qiskit.utils import QuantumInstance, algorithm_globals
from qiskit_optimization.applications import Tsp
from qiskit_optimization.converters import QuadraticProgramToQubo


def create_circuit(num_nodes: int):
    """Returns a quantum circuit solving the Travelling Salesman Problem (TSP).

    Keyword arguments:
    num_nodes -- number of to be visited nodes
    """

    # Generating a graph of 3 nodes
    n = num_nodes
    tsp = Tsp.create_random_instance(n, seed=10)

    qp = tsp.to_quadratic_program()

    qp2qubo = QuadraticProgramToQubo()
    qubo = qp2qubo.convert(qp)
    qubit_op, offset = qubo.to_ising()

    algorithm_globals.random_seed = 10
    seed = 10
    backend = Aer.get_backend("aer_simulator")
    quantum_instance = QuantumInstance(
        backend, seed_simulator=seed, seed_transpiler=seed, shots=1024
    )

    spsa = SPSA(maxiter=25)
    ry = TwoLocal(qubit_op.num_qubits, "ry", "cz", reps=5, entanglement="linear")
    vqe = VQE(ry, optimizer=spsa, quantum_instance=quantum_instance)

    vqe_result = vqe.compute_minimum_eigenvalue(qubit_op)
    qc = vqe.ansatz.bind_parameters(vqe_result.optimal_point)
    qc.measure_all()
    qc.name = "tsp"

    return qc
