# Code from qiskit-optimization demo
import networkx as nx
from qiskit import Aer
from qiskit.utils import QuantumInstance
from qiskit_optimization.algorithms import MinimumEigenOptimizer
from qiskit.algorithms import QAOA
from qiskit_optimization.applications import Maxcut

def create_circuit(n: int, include_measurements: bool = True):
    graph = nx.random_regular_graph(d=2, n=n, seed=111)
    maxcut = Maxcut(graph)
    qp = maxcut.to_quadratic_program()
    qins = QuantumInstance(backend=Aer.get_backend('qasm_simulator'), shots=1024, seed_simulator=123)

    # Define QAOA solver
    qaoa = QAOA(reps=1, quantum_instance=qins)
    meo = MinimumEigenOptimizer(min_eigen_solver=qaoa)
    result = meo.solve(qp)


    qc = qaoa.get_optimal_circuit()
    qc.name="QAOA"
    if (include_measurements): qc.measure_all()

    return qc