## Code from qiskit-optimization demo

# checked

from qiskit import Aer
from qiskit.utils import QuantumInstance
from qiskit_optimization.algorithms import MinimumEigenOptimizer
from qiskit.algorithms import QAOA
from qiskit.algorithms.optimizers import SLSQP

from src.utils import get_examplary_max_cut_qp


def create_circuit(n: int):
    qp = get_examplary_max_cut_qp(n)
    sim = QuantumInstance(backend=Aer.get_backend('qasm_simulator'), shots=1024, seed_simulator=123)

    qaoa = QAOA(reps=2, optimizer=SLSQP(), quantum_instance=sim)
    qaoa_optimizer = MinimumEigenOptimizer(min_eigen_solver=qaoa)
    qaoa_result = qaoa_optimizer.solve(qp)
    qc = qaoa.get_optimal_circuit()

    qc.measure_all()
    qc.name="QAOA"

    return qc