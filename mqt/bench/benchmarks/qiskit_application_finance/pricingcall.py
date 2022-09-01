# Code based on https://qiskit.org/documentation/tutorials/finance/03_european_call_option_pricing.html

from __future__ import annotations

import numpy as np
from qiskit.algorithms import IterativeAmplitudeEstimation
from qiskit_finance.applications.estimation import EuropeanCallPricing
from qiskit_finance.circuit.library import LogNormalDistribution


def create_circuit(num_uncertainty_qubits: int = 5):
    """Returns a quantum circuit of Iterative Amplitude Estimation applied to a problem instance of
    pricing call options.

    Keyword arguments:
    num_uncertainty_qubits -- number of qubits to measure uncertainty
    """

    num_uncertainty_qubits = num_uncertainty_qubits

    # parameters for considered random distribution
    s = 2.0  # initial spot price
    vol = 0.4  # volatility of 40%
    r = 0.05  # annual interest rate of 4%
    t = 40 / 365  # 40 days to maturity

    mu = (r - 0.5 * vol**2) * t + np.log(s)
    sigma = vol * np.sqrt(t)
    mean = np.exp(mu + sigma**2 / 2)
    variance = (np.exp(sigma**2) - 1) * np.exp(2 * mu + sigma**2)
    stddev = np.sqrt(variance)

    # lowest and highest value considered for the spot price; in between, an equidistant discretization is considered.
    low = np.maximum(0, mean - 3 * stddev)
    high = mean + 3 * stddev

    # construct A operator for QAE for the payoff function by
    # composing the uncertainty model and the objective
    uncertainty_model = LogNormalDistribution(
        num_uncertainty_qubits, mu=mu, sigma=sigma**2, bounds=(low, high)
    )

    # set the strike price (should be within the low and the high value of the uncertainty)
    strike_price = 1.896

    # set the approximation scaling for the payoff function
    c_approx = 0.25

    european_call_pricing = EuropeanCallPricing(
        num_state_qubits=num_uncertainty_qubits,
        strike_price=strike_price,
        rescaling_factor=c_approx,
        bounds=(low, high),
        uncertainty_model=uncertainty_model,
    )

    # set target precision and confidence level
    epsilon = 0.01
    alpha = 0.05

    problem = european_call_pricing.to_estimation_problem()
    iae = IterativeAmplitudeEstimation(epsilon, alpha=alpha)

    qc = iae.construct_circuit(problem)
    qc.measure_all()
    qc.name = "pricingcall"

    return qc
