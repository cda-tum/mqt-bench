# Code from qiskit-optimization demo

from qiskit import Aer
from qiskit.utils import QuantumInstance
from qiskit_optimization.algorithms import MinimumEigenOptimizer
from qiskit.algorithms import QAOA

from src.utils import get_examplary_max_cut_qp


def create_circuit(n: int):
    qp = get_examplary_max_cut_qp(n)
    qins = QuantumInstance(backend=Aer.get_backend('qasm_simulator'), shots=1024, seed_simulator=123)

    # Define QAOA solver
    qaoa = QAOA(reps=1, quantum_instance=qins)
    meo = MinimumEigenOptimizer(min_eigen_solver=qaoa)
    qaoa_result = meo.solve(qp)


    qc = qaoa.get_optimal_circuit()
    qc.name="QAOA"
    qc.measure_all()

    return qc