## Code based on https://github.com/qiskit-community/qiskit-application-modules-demo-sessions/blob/main/qiskit-optimization/qiskit-optimization-demo.ipynb

from src.utils import get_examplary_max_cut_qp
from qiskit.algorithms import VQE
from qiskit.algorithms.optimizers import SLSQP
from qiskit_optimization.algorithms import MinimumEigenOptimizer
from qiskit.circuit.library import RealAmplitudes
from qiskit import Aer
from qiskit.utils import QuantumInstance


def create_circuit(num_qubits: int):
    """Returns a quantum circuit implementing the Variational Quantum Eigensolver Algorithm for a specific max-cut
     example.

    Keyword arguments:
    num_qubits -- number of qubits of the returned quantum circuit
    """

    qp = get_examplary_max_cut_qp(num_qubits)
    sim = QuantumInstance(backend=Aer.get_backend('qasm_simulator'), shots=1024, seed_simulator=123)

    ansatz = RealAmplitudes(num_qubits, reps=2)
    vqe = VQE(ansatz, optimizer=SLSQP(), quantum_instance=sim)
    vqe_optimizer = MinimumEigenOptimizer(min_eigen_solver=vqe)
    vqe_result = vqe_optimizer.solve(qp)
    qc = vqe.get_optimal_circuit()

    qc.measure_all()
    qc.name = "vqe"

    return qc
