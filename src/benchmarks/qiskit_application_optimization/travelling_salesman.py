## Code from https://qiskit.org/documentation/optimization/tutorials/06_examples_max_cut_and_tsp.html

import networkx as nx

from qiskit import Aer
from qiskit.circuit.library import TwoLocal
from qiskit_optimization.applications import Tsp
from qiskit.algorithms import VQE
from qiskit.algorithms.optimizers import SPSA
from qiskit.utils import algorithm_globals, QuantumInstance
from qiskit_optimization.algorithms import MinimumEigenOptimizer
from qiskit_optimization.converters import QuadraticProgramToQubo
import warnings


def create_circuit(nodes: int):
    # Generating a graph of 3 nodes
    n = nodes
    num_qubits = n ** 2
    tsp = Tsp.create_random_instance(n, seed=123)
    adj_matrix = nx.to_numpy_matrix(tsp.graph)

    qp = tsp.to_quadratic_program()

    qp2qubo = QuadraticProgramToQubo()
    qubo = qp2qubo.convert(qp)
    qubitOp, offset = qubo.to_ising()

    algorithm_globals.random_seed = 123
    seed = 10598
    backend = Aer.get_backend("aer_simulator_statevector")
    quantum_instance = QuantumInstance(backend, seed_simulator=seed, seed_transpiler=seed)

    spsa = SPSA(maxiter=300)
    ry = TwoLocal(qubitOp.num_qubits, "ry", "cz", reps=5, entanglement="linear")
    vqe = VQE(ry, optimizer=spsa, quantum_instance=quantum_instance)

    result = vqe.compute_minimum_eigenvalue(qubitOp)

    x = tsp.sample_most_likely(result.eigenstate)
    z = tsp.interpret(x)

    # create minimum eigen optimizer based on VQE

    warnings.filterwarnings("ignore", category=UserWarning)
    vqe_optimizer = MinimumEigenOptimizer(vqe)

    # solve quadratic program
    result = vqe_optimizer.solve(qp)
    z = tsp.interpret(x)

    qc = vqe.get_optimal_circuit()
    qc.name = "tsp"

    return qc