# Code from https://github.com/qiskit-community/qiskit-application-modules-demo-sessions/blob/main/qiskit-optimization/qiskit-optimization-demo.ipynb

from __future__ import annotations

from qiskit import Aer
from qiskit.algorithms import QAOA
from qiskit.algorithms.optimizers import SLSQP
from qiskit.utils import QuantumInstance

from mqt.bench.utils.utils import get_examplary_max_cut_qp


def create_circuit(num_qubits: int):
    """Returns a quantum circuit implementing the Quantum Approximation Optimization Algorithm for a specific max-cut
     example.

    Keyword arguments:
    num_qubits -- number of qubits of the returned quantum circuit
    """

    qp = get_examplary_max_cut_qp(num_qubits)
    sim = QuantumInstance(
        backend=Aer.get_backend("aer_simulator"), shots=1024, seed_simulator=10
    )

    qaoa = QAOA(reps=2, optimizer=SLSQP(maxiter=25), quantum_instance=sim)
    qaoa_result = qaoa.compute_minimum_eigenvalue(qp.to_ising()[0])
    qc = qaoa.ansatz.bind_parameters(qaoa_result.optimal_point)

    qc.measure_all()
    qc.name = "qaoa"

    return qc
