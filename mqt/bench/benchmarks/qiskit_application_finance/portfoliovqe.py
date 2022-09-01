# Code based on https://qiskit.org/documentation/tutorials/finance/01_portfolio_optimization.html

from __future__ import annotations

import datetime

from qiskit import Aer
from qiskit.algorithms import VQE
from qiskit.algorithms.optimizers import COBYLA
from qiskit.circuit.library import TwoLocal
from qiskit.utils import QuantumInstance
from qiskit_finance.applications import PortfolioOptimization
from qiskit_finance.data_providers import RandomDataProvider
from qiskit_optimization.converters import QuadraticProgramToQubo


def create_circuit(num_qubits: int):
    """Returns a quantum circuit of VQE applied to a specific portfolio optimization task.

    Keyword arguments:
    num_qubits -- number of qubits of the returned quantum circuit
    """

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
    ry = TwoLocal(num_assets, "ry", "cz", reps=3, entanglement="full")
    sim = QuantumInstance(
        backend=backend, seed_simulator=seed, seed_transpiler=seed, shots=1024
    )

    vqe = VQE(ry, optimizer=cobyla, quantum_instance=sim)
    vqe.random_seed = seed
    vqe_result = vqe.compute_minimum_eigenvalue(qp_qubo.to_ising()[0])
    qc = vqe.ansatz.bind_parameters(vqe_result.optimal_point)

    qc.name = "portfoliovqe"
    qc.measure_all()

    return qc
