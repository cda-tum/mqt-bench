## Code from qiskit finance demo

## checked

from src.utils import get_examplary_max_cut_qp
from qiskit.algorithms import VQE
from qiskit.algorithms.optimizers import SLSQP
from qiskit_optimization.algorithms import MinimumEigenOptimizer
from qiskit.circuit.library import RealAmplitudes
from qiskit import Aer
from qiskit.utils import QuantumInstance


def create_circuit(n: int):
    qp = get_examplary_max_cut_qp(n)
    sim = QuantumInstance(backend=Aer.get_backend('qasm_simulator'), shots=1024, seed_simulator=123)

    ansatz = RealAmplitudes(n, reps=2)
    vqe = VQE(ansatz, optimizer=SLSQP(), quantum_instance=sim)
    vqe_optimizer = MinimumEigenOptimizer(vqe)
    vqe_result = vqe_optimizer.solve(qp)
    qc = vqe.get_optimal_circuit()

    qc.measure_all()
    qc.name="VQE"

    return qc