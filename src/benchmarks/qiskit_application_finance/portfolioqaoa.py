## Code from https://qiskit.org/documentation/tutorials/finance/01_portfolio_optimization.html

from qiskit import Aer
from qiskit.aqua import QuantumInstance
from qiskit.finance.applications.ising import portfolio
from qiskit.optimization.applications.ising.common import sample_most_likely
from qiskit.finance.data_providers import RandomDataProvider
from qiskit.aqua.algorithms import QAOA
from qiskit.aqua.components.optimizers import COBYLA

import numpy as np
import datetime


def create_circuit(n: int):
    # set number of assets (= number of qubits)
    num_assets = n

    # Generate expected return and covariance matrix from (random) time-series
    stocks = [("TICKER%s" % i) for i in range(num_assets)]
    data = RandomDataProvider(tickers=stocks,
                     start=datetime.datetime(2016,1,1),
                     end=datetime.datetime(2016,1,30))
    data.run()
    mu = data.get_period_return_mean_vector()
    sigma = data.get_period_return_covariance_matrix()

    q = 0.5                   # set risk factor
    budget = num_assets // 2  # set budget
    penalty = num_assets      # set parameter to scale the budget penalty term

    qubitOp, offset = portfolio.get_operator(mu, sigma, q, budget, penalty)

    def index_to_selection(i, num_assets):
        s = "{0:b}".format(i).rjust(num_assets)
        x = np.array([1 if s[i]=='1' else 0 for i in reversed(range(num_assets))])
        return x

    def print_result(result):
        selection = sample_most_likely(result.eigenstate)
        value = portfolio.portfolio_value(selection, mu, sigma, q, budget, penalty)

        eigenvector = result.eigenstate if isinstance(result.eigenstate, np.ndarray) else result.eigenstate.to_matrix()
        probabilities = np.abs(eigenvector)**2
        i_sorted = reversed(np.argsort(probabilities))

        for i in i_sorted:
            x = index_to_selection(i, num_assets)
            value = portfolio.portfolio_value(x, mu, sigma, q, budget, penalty)
            probability = probabilities[i]

    backend = Aer.get_backend('statevector_simulator')
    seed = 50

    cobyla = COBYLA()
    cobyla.set_options(maxiter=250)
    qaoa = QAOA(qubitOp, cobyla, 3)

    qaoa.random_seed = seed

    quantum_instance = QuantumInstance(backend=backend, seed_simulator=seed, seed_transpiler=seed)

    result = qaoa.run(quantum_instance)

    qc = qaoa.get_optimal_circuit()
    qc.name = "portfolioqaoa"
    qc.measure_all()

    return qc