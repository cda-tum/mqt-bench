# Code from https://github.com/qiskit-community/qiskit-application-modules-demo-sessions/blob/main/qiskit-optimization/qiskit-optimization-demo.ipynb

from qiskit import Aer
from qiskit.utils import QuantumInstance
from qiskit_optimization.algorithms import MinimumEigenOptimizer
from qiskit.algorithms import QAOA
from qiskit.algorithms.optimizers import SLSQP

from src.utils import get_examplary_max_cut_qp


def create_circuit(num_qubits: int):
    """Returns a quantum circuit implementing the Quantum Approximation Optimization Algorithm for a specific max-cut
     example.

    Keyword arguments:
    num_qubits -- number of qubits of the returned quantum circuit
    """

    qp = get_examplary_max_cut_qp(num_qubits)
    sim = QuantumInstance(
        backend=Aer.get_backend("qasm_simulator"), shots=1024, seed_simulator=123
    )

    qaoa = QAOA(reps=2, optimizer=SLSQP(), quantum_instance=sim)
    qaoa_optimizer = MinimumEigenOptimizer(min_eigen_solver=qaoa)
    qaoa_result = qaoa_optimizer.solve(qp)
    qc = qaoa.get_optimal_circuit()

    qc.measure_all()
    qc.name = "qaoa"

    return qc
