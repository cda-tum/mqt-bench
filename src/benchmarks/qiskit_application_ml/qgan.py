## code from https://qiskit.org/documentation/machine-learning/tutorials/04_qgans_for_loading_random_distributions.html

import numpy as np
from qiskit import QuantumRegister, QuantumCircuit, BasicAer
from qiskit.circuit.library import TwoLocal
from qiskit_finance.circuit.library import UniformDistribution

from qiskit.utils import QuantumInstance, algorithm_globals
from qiskit_machine_learning.algorithms import NumPyDiscriminator, QGAN

def create_circuit(n: int):
    seed = 71
    np.random.seed = seed
    algorithm_globals.random_seed = seed

    # Number training data samples
    N = 1000

    # Load data samples from log-normal distribution with mean=1 and standard deviation=1
    mu = 1
    sigma = 1
    real_data = np.random.lognormal(mean=mu, sigma=sigma, size=N)

    # Set the data resolution
    # Set upper and lower data values as list of k min/max data values [[min_0,max_0],...,[min_k-1,max_k-1]]
    upper_bound_value = 2**n - 1
    bounds = np.array([0., upper_bound_value])
    # Set number of qubits per data dimension as list of k qubit values[#q_0,...,#q_k-1]
    num_qubits = [n]
    k = len(num_qubits)

    # Set number of training epochs
    # Note: The algorithm's runtime can be shortened by reducing the number of training epochs.
    num_epochs = 10
    # Batch size
    batch_size = 100

    # Initialize qGAN
    qgan = QGAN(real_data, bounds, num_qubits, batch_size, num_epochs, snapshot_dir=None)
    qgan.seed = 1
    # Set quantum instance to run the quantum generator
    quantum_instance = QuantumInstance(
        backend=BasicAer.get_backend("statevector_simulator"), seed_transpiler=seed, seed_simulator=seed
    )

    # Set entangler map
    #entangler_map = [[0, 1]]


    # Set an initial state for the generator circuit
    init_dist = UniformDistribution(sum(num_qubits))

    # Set the ansatz circuit
    ansatz = TwoLocal(int(np.sum(num_qubits)), "ry", "cz",  reps=1) #entanglement=entangler_map,

    # Set generator's initial parameters - in order to reduce the training time and hence the
    # total running time for this notebook
    #init_params = [3.0, 1.0, 0.6, 1.6]

    # You can increase the number of training epochs and use random initial parameters.
    init_params = np.random.rand(ansatz.num_parameters_settable) * 2 * np.pi

    # Set generator circuit by adding the initial distribution infront of the ansatz
    g_circuit = ansatz.compose(init_dist, front=True)

    # Set quantum generator
    qgan.set_generator(generator_circuit=g_circuit, generator_init_params=init_params)
    # The parameters have an order issue that following is a temp. workaround
    qgan._generator._free_parameters = sorted(g_circuit.parameters, key=lambda p: p.name)
    # Set classical discriminator neural network
    discriminator = NumPyDiscriminator(len(num_qubits))
    qgan.set_discriminator(discriminator)

    result = qgan.run(quantum_instance)

    param_values = qgan.generator.parameter_values
    qc = qgan.generator.construct_circuit(params=param_values)
    qc.name = "qgan"

    return qc