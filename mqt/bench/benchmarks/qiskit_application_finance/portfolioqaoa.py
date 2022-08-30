# Code based on https://qiskit.org/documentation/tutorials/finance/01_portfolio_optimization.html

import datetime

from qiskit import Aer
from qiskit.algorithms import QAOA
from qiskit.algorithms.optimizers import COBYLA
from qiskit.utils import QuantumInstance


def create_circuit(num_qubits: int):
    """Returns a quantum circuit of QAOA applied to a specific portfolio optimization task.

    Keyword arguments:
    num_qubits -- number of qubits of the returned quantum circuit
    """
    try:
        from qiskit_finance.applications import PortfolioOptimization
        from qiskit_finance.data_providers import RandomDataProvider

    except:
        print("Please install qiskit_finance.")
        return None

    try:
        from qiskit_optimization.converters import QuadraticProgramToQubo
    except:
        print("Please install qiskit_optimization.")
        return None

    # set number of assets (= number of qubits)
    num_assets = num_qubits

    # Generate expected return and covariance matrix from (random) time-series
    stocks = [("TICKER%s" % i) for i in range(num_assets)]
    data = RandomDataProvider(
        tickers=stocks,
        start=datetime.datetime(2016, 1, 1),
        end=datetime.datetime(2016, 1, 30),
    )
    data.run()
    mu = data.get_period_return_mean_vector()
    sigma = data.get_period_return_covariance_matrix()

    q = 0.5  # set risk factor
    budget = num_assets // 2  # set budget
    penalty = num_assets  # set parameter to scale the budget penalty term

    portfolio = PortfolioOptimization(
        expected_returns=mu, covariances=sigma, risk_factor=q, budget=budget
    )
    qp = portfolio.to_quadratic_program()
    conv = QuadraticProgramToQubo()
    qp_qubo = conv.convert(qp)

    backend = Aer.get_backend("aer_simulator")
    seed = 10

    cobyla = COBYLA()
    cobyla.set_options(maxiter=25)

    sim = QuantumInstance(
        backend=backend, seed_simulator=seed, seed_transpiler=seed, shots=1024
    )

    qaoa = QAOA(cobyla, 3, quantum_instance=sim)
    qaoa.random_seed = seed
    qaoa_result = qaoa.compute_minimum_eigenvalue(qp_qubo.to_ising()[0])
    qc = qaoa.ansatz.bind_parameters(qaoa_result.optimal_point)

    qc.name = "portfolioqaoa"
    qc.measure_all()

    return qc
