# Code based on https://qiskit.org/documentation/machine-learning/tutorials/04_qgans_for_loading_random_distributions.html

from __future__ import annotations

import numpy as np
from qiskit import Aer
from qiskit.circuit.library import TwoLocal
from qiskit.utils import QuantumInstance, algorithm_globals
from qiskit_finance.circuit.library import UniformDistribution
from qiskit_machine_learning.algorithms import QGAN, NumPyDiscriminator


def create_circuit(num_qubits: int):
    """Returns a quantum circuit implementing Quantum Generative Adversarial Networks algorithm.

    Keyword arguments:
    num_qubits -- number of qubits of the returned quantum circuit
    """

    seed = 10
    np.random.seed = seed
    algorithm_globals.random_seed = seed

    # Number training data samples
    n = 100

    # Load data samples from log-normal distribution with mean=1 and standard deviation=1
    mu = 1
    sigma = 1
    real_data = np.random.lognormal(mean=mu, sigma=sigma, size=n)

    # Set the data resolution
    # Set upper and lower data values as list of k min/max data values [[min_0,max_0],...,[min_k-1,max_k-1]]
    upper_bound_value = 2**num_qubits - 1
    bounds = np.array([0.0, upper_bound_value])
    # Set number of qubits per data dimension as list of k qubit values[#q_0,...,#q_k-1]
    num_qubits = [num_qubits]

    # Set number of training epochs
    # Note: The algorithm's runtime can be shortened by reducing the number of training epochs.
    num_epochs = 5
    # Batch size
    batch_size = 10

    # Initialize qGAN
    qgan = QGAN(
        real_data, bounds, num_qubits, batch_size, num_epochs, snapshot_dir=None
    )
    qgan.seed = 10
    # Set quantum instance to run the quantum generator
    quantum_instance = QuantumInstance(
        backend=Aer.get_backend("aer_simulator"),
        seed_transpiler=seed,
        seed_simulator=seed,
        shots=1024,
    )

    # Set an initial state for the generator circuit
    init_dist = UniformDistribution(sum(num_qubits))

    # Set the ansatz circuit
    ansatz = TwoLocal(
        int(np.sum(num_qubits)), "ry", "cz", reps=1
    )  # entanglement=entangler_map,

    # You can increase the number of training epochs and use random initial parameters.
    init_params = np.random.rand(ansatz.num_parameters_settable) * 2 * np.pi

    # Set generator circuit by adding the initial distribution infront of the ansatz
    g_circuit = ansatz.compose(init_dist, front=True)

    # Set quantum generator
    qgan.set_generator(generator_circuit=g_circuit, generator_init_params=init_params)
    # The parameters have an order issue that following is a temp. workaround
    qgan._generator._free_parameters = sorted(
        g_circuit.parameters, key=lambda p: p.name
    )
    # Set classical discriminator neural network
    discriminator = NumPyDiscriminator(len(num_qubits))
    qgan.set_discriminator(discriminator)

    qgan.run(quantum_instance)

    param_values = qgan.generator.parameter_values
    qc = qgan.generator.construct_circuit(params=param_values)
    qc.measure_all()
    qc.name = "qgan"

    return qc
