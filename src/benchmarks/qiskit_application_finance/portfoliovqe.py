# Code from https://qiskit.org/documentation/tutorials/finance/01_portfolio_optimization.html

from qiskit import Aer
from qiskit.circuit.library import TwoLocal
from qiskit.aqua import QuantumInstance
from qiskit.finance.applications.ising import portfolio
from qiskit.finance.data_providers import RandomDataProvider
from qiskit.aqua.algorithms import VQE
from qiskit.aqua.components.optimizers import COBYLA
import datetime


def create_circuit(num_qubits: int):
    """Returns a quantum circuit of VQE applied to a specific portfolio optimization task.

    Keyword arguments:
    num_qubits -- number of qubits of the returned quantum circuit
    """

    # set number of assets (= number of qubits)
    num_assets = num_qubits

    # Generate expected return and covariance matrix from (random) time-series
    stocks = [("TICKER%s" % i) for i in range(num_assets)]
    data = RandomDataProvider(tickers=stocks, start=datetime.datetime(2016, 1, 1), end=datetime.datetime(2016, 1, 30))
    data.run()
    mu = data.get_period_return_mean_vector()
    sigma = data.get_period_return_covariance_matrix()

    q = 0.5  # set risk factor
    budget = num_assets // 2  # set budget
    penalty = num_assets  # set parameter to scale the budget penalty term

    qubit_op, offset = portfolio.get_operator(mu, sigma, q, budget, penalty)
    backend = Aer.get_backend('statevector_simulator')
    seed = 50

    cobyla = COBYLA()
    cobyla.set_options(maxiter=50)
    ry = TwoLocal(qubit_op.num_qubits, 'ry', 'cz', reps=3, entanglement='full')
    vqe = VQE(qubit_op, ry, cobyla)
    vqe.random_seed = seed

    quantum_instance = QuantumInstance(backend=backend, seed_simulator=seed, seed_transpiler=seed)

    result = vqe.run(quantum_instance)
    qc = vqe.get_optimal_circuit()
    qc.name = "portfoliovqe"
    qc.measure_all()

    return qc
