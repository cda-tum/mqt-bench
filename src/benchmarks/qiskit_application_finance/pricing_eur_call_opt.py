## Code from https://qiskit.org/documentation/tutorials/finance/03_european_call_option_pricing.html

from qiskit.finance.applications import EuropeanCallExpectedValue
import numpy as np
from qiskit import Aer
from qiskit.aqua.algorithms import IterativeAmplitudeEstimation
from qiskit_finance.circuit.library import LogNormalDistribution

def create_circuit(num_uncertainty_qubits:int = 5):
    num_uncertainty_qubits = num_uncertainty_qubits

    # parameters for considered random distribution
    S = 2.0  # initial spot price
    vol = 0.4  # volatility of 40%
    r = 0.05  # annual interest rate of 4%
    T = 40 / 365  # 40 days to maturity

    mu = ((r - 0.5 * vol ** 2) * T + np.log(S))
    sigma = vol * np.sqrt(T)
    mean = np.exp(mu + sigma ** 2 / 2)
    variance = (np.exp(sigma ** 2) - 1) * np.exp(2 * mu + sigma ** 2)
    stddev = np.sqrt(variance)

    # lowest and highest value considered for the spot price; in between, an equidistant discretization is considered.
    low = np.maximum(0, mean - 3 * stddev)
    high = mean + 3 * stddev

    # construct A operator for QAE for the payoff function by
    # composing the uncertainty model and the objective
    uncertainty_model = LogNormalDistribution(num_uncertainty_qubits, mu=mu, sigma=sigma ** 2, bounds=(low, high))


    # set the strike price (should be within the low and the high value of the uncertainty)
    strike_price = 1.896

    # set the approximation scaling for the payoff function
    c_approx = 0.25

    european_call_objective = EuropeanCallExpectedValue(num_uncertainty_qubits,
                                                        strike_price,
                                                        rescaling_factor=c_approx,
                                                        bounds=(low, high))

    # append the uncertainty model to the front
    european_call = european_call_objective.compose(uncertainty_model, front=True)
    # set target precision and confidence level
    epsilon = 0.01
    alpha = 0.05

    # construct amplitude estimation
    iae = IterativeAmplitudeEstimation(epsilon=epsilon, alpha=alpha,
                                      state_preparation=european_call,
                                      objective_qubits=[1],
                                      post_processing=european_call_objective.post_processing)
    result = iae.run(quantum_instance=Aer.get_backend('qasm_simulator'), shots=100)


    qc = iae.construct_circuit(1)
    qc.name = "pricing_call"

    return qc