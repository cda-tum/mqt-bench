# Code based on https://qiskit.org/documentation/tutorials/finance/04_european_put_option_pricing.html

from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from qiskit.algorithms import EstimationProblem, IterativeAmplitudeEstimation
from qiskit.circuit.library import LinearAmplitudeFunction
from qiskit_finance.circuit.library import LogNormalDistribution

if TYPE_CHECKING:  # pragma: no cover
    from qiskit import QuantumCircuit


def create_circuit(num_uncertainty_qubits: int = 5) -> QuantumCircuit:
    """Returns a quantum circuit of Iterative Amplitude Estimation applied to a problem instance of pricing put options.

    Keyword arguments:
    num_uncertainty_qubits -- number of qubits to measure uncertainty
    """
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
    uncertainty_model = LogNormalDistribution(num_uncertainty_qubits, mu=mu, sigma=sigma**2, bounds=(low, high))

    # set the strike price (should be within the low and the high value of the uncertainty)
    strike_price = 2.126

    # set the approximation scaling for the payoff function
    rescaling_factor = 0.25

    # setup piecewise linear objective fcuntion
    breakpoints = [low, strike_price]
    slopes = [-1, 0]
    offsets = [strike_price - low, 0]
    f_min = 0
    f_max = strike_price - low
    european_put_objective = LinearAmplitudeFunction(
        num_uncertainty_qubits,
        slopes,
        offsets,
        domain=(low, high),
        image=(f_min, f_max),
        breakpoints=breakpoints,
        rescaling_factor=rescaling_factor,
    )

    # construct A operator for QAE for the payoff function by
    # composing the uncertainty model and the objective
    european_put = european_put_objective.compose(uncertainty_model, front=True)

    # set target precision and confidence level
    epsilon = 0.01
    alpha = 0.05

    problem = EstimationProblem(
        state_preparation=european_put,
        objective_qubits=[num_uncertainty_qubits],
        post_processing=european_put_objective.post_processing,
    )

    iae = IterativeAmplitudeEstimation(epsilon, alpha=alpha)
    qc = iae.construct_circuit(problem)

    qc.measure_all()
    qc.name = "pricingput"

    return qc
