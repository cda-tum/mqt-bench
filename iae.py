## Code from Qiskit Finance Demo Notebook

import numpy as np
from qiskit.algorithms import IterativeAmplitudeEstimation
from qiskit_finance.applications import EuropeanCallPricing
from qiskit_finance.circuit.library import LogNormalDistribution

def create_circuit(num_uncertainty_qubits: int):
    num_uncertainty_qubits = num_uncertainty_qubits

    strike_price = 1.896   # agreed upon strike price
    T = 40 / 365         # 40 days to maturity

    S = 2.0              # initial spot price
    vol = 0.4            # volatility of 40%
    r = 0.05             # annual interest rate of 4%

    # resulting parameters for log-normal distribution
    mu = ((r - 0.5 * vol**2) * T + np.log(S))
    sigma = vol * np.sqrt(T)
    mean = np.exp(mu + sigma**2/2)
    variance = (np.exp(sigma**2) - 1) * np.exp(2*mu + sigma**2)
    stddev = np.sqrt(variance)

    # lowest and highest value considered for the spot price; in between, an equidistant discretization is considered.
    low = np.maximum(0, mean - 3*stddev)
    high = mean + 3*stddev

    distribution = LogNormalDistribution(num_uncertainty_qubits, mu=mu, sigma=sigma**2, bounds=(low, high))


    european_call_pricing = EuropeanCallPricing(num_state_qubits=num_uncertainty_qubits,
                                                strike_price=strike_price,
                                                rescaling_factor=0.25,  # approximation constant for payoff function
                                                bounds=(low, high),
                                                uncertainty_model=distribution)
    problem = european_call_pricing.to_estimation_problem()

    epsilon = 0.01  # determines final accuracy
    alpha = 0.05  # determines how certain we are of the result

    iae = IterativeAmplitudeEstimation(epsilon, alpha=alpha)
    qc = iae.construct_circuit(problem)
    qc.name = "iae"

    return qc
