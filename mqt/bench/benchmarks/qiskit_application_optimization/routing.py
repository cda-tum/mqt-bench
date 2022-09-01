# Code based on https://qiskit.org/documentation/tutorials/optimization/7_examples_vehicle_routing.html

from __future__ import annotations

import numpy as np
from qiskit import Aer
from qiskit.algorithms import VQE
from qiskit.algorithms.optimizers import SLSQP
from qiskit.utils import QuantumInstance, algorithm_globals
from qiskit_optimization import QuadraticProgram
from qiskit_optimization.algorithms import MinimumEigenOptimizer


class Initializer:
    def __init__(self, n):
        self.n = n

    def generate_instance(self):
        n = self.n
        np.random.seed = 10

        xc = (np.random.rand(n) - 0.5) * 10
        yc = (np.random.rand(n) - 0.5) * 10

        instance = np.zeros([n, n])
        for ii in range(0, n):
            for jj in range(ii + 1, n):
                instance[ii, jj] = (xc[ii] - xc[jj]) ** 2 + (yc[ii] - yc[jj]) ** 2
                instance[jj, ii] = instance[ii, jj]

        return xc, yc, instance


class QuantumOptimizer:
    def __init__(self, instance, n, k):

        self.instance = instance
        self.n = n
        self.K = k

    def binary_representation(self, x_sol=0):

        instance = self.instance
        n = self.n
        k = self.K

        a = np.max(instance) * 100  # A parameter of cost function

        # Determine the weights w
        instance_vec = instance.reshape(n**2)
        w_list = [instance_vec[x] for x in range(n**2) if instance_vec[x] > 0]
        w = np.zeros(n * (n - 1))
        for ii in range(len(w_list)):
            w[ii] = w_list[ii]

        id_n = np.eye(n)
        im_n_1 = np.ones([n - 1, n - 1])
        iv_n_1 = np.ones(n)
        iv_n_1[0] = 0
        iv_n = np.ones(n - 1)
        neg_iv_n_1 = np.ones(n) - iv_n_1

        v = np.zeros([n, n * (n - 1)])
        for ii in range(n):
            count = ii - 1
            for jj in range(n * (n - 1)):

                if jj // (n - 1) == ii:
                    count = ii

                if jj // (n - 1) != ii and jj % (n - 1) == count:
                    v[ii][jj] = 1.0

        vn = np.sum(v[1:], axis=0)

        # Q defines the interactions between variables
        q = a * (np.kron(id_n, im_n_1) + np.dot(v.T, v))

        # g defines the contribution from the individual variables
        g = (
            w
            - 2 * a * (np.kron(iv_n_1, iv_n) + vn.T)
            - 2 * a * k * (np.kron(neg_iv_n_1, iv_n) + v[0].T)
        )

        # c is the constant offset
        c = 2 * a * (n - 1) + 2 * a * (k**2)

        try:
            max(x_sol)
            # Evaluates the cost distance from a binary representation of a path
            fun = (
                lambda x: np.dot(np.around(x), np.dot(q, np.around(x)))
                + np.dot(g, np.around(x))
                + c
            )
            cost = fun(x_sol)
        except Exception:
            cost = 0

        return q, g, c, cost

    def construct_problem(self, q, g, c):

        qp = QuadraticProgram()
        for i in range(self.n * (self.n - 1)):
            qp.binary_var(str(i))
        qp.objective.quadratic = q
        qp.objective.linear = g
        qp.objective.constant = c
        return qp

    def solve_problem(self, qp):

        algorithm_globals.random_seed = 10
        quantum_instance = QuantumInstance(
            Aer.get_backend("aer_simulator"),
            seed_simulator=algorithm_globals.random_seed,
            seed_transpiler=algorithm_globals.random_seed,
            shots=1024,
        )

        vqe = VQE(quantum_instance=quantum_instance, optimizer=SLSQP(maxiter=25))
        optimizer = MinimumEigenOptimizer(min_eigen_solver=vqe)
        result = optimizer.solve(qp)
        # compute cost of the obtained result
        _, _, _, level = self.binary_representation(x_sol=result.x)
        return result.x, level, vqe


def create_circuit(num_nodes: int = 3, num_vehs: int = 2):
    """Returns a quantum circuit solving a routing problem.

    Keyword arguments:
    num_nodes -- number of to be visited nodes
    num_vehs -- number of used vehicles
    """

    # Initialize the problem by defining the parameters
    n = num_nodes  # number of nodes + depot (n+1)
    k = num_vehs  # number of vehicles
    # Initialize the problem by randomly generating the instance
    initializer = Initializer(n)
    xc, yc, instance = initializer.generate_instance()

    quantum_optimizer = QuantumOptimizer(instance, n, k)
    q, g, c, binary_cost = quantum_optimizer.binary_representation()
    qp = quantum_optimizer.construct_problem(q, g, c)
    # Instantiate the quantum optimizer class with parameters:
    quantum_solution, quantum_cost, vqe = quantum_optimizer.solve_problem(qp)

    vqe_result = vqe.compute_minimum_eigenvalue(qp.to_ising()[0])
    qc = vqe.ansatz.bind_parameters(vqe_result.optimal_point)

    qc.measure_all()
    qc.name = "routing"

    return qc
