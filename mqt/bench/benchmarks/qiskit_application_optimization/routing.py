# Code based on https://qiskit.org/documentation/tutorials/optimization/7_examples_vehicle_routing.html

from __future__ import annotations

import numpy as np
from qiskit.algorithms.minimum_eigensolvers import VQE
from qiskit.algorithms.optimizers import SLSQP
from qiskit.circuit.library import RealAmplitudes
from qiskit.primitives import Estimator
from qiskit.utils import algorithm_globals
from qiskit_optimization import QuadraticProgram


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
    def __init__(self, instance, n, K):

        self.instance = instance
        self.n = n
        self.K = K

    def binary_representation(self, x_sol=0):

        instance = self.instance
        n = self.n
        K = self.K

        A = np.max(instance) * 100  # A parameter of cost function

        # Determine the weights w
        instance_vec = instance.reshape(n**2)
        w_list = [instance_vec[x] for x in range(n**2) if instance_vec[x] > 0]
        w = np.zeros(n * (n - 1))
        for ii in range(len(w_list)):
            w[ii] = w_list[ii]

        # Some variables I will use
        Id_n = np.eye(n)
        Im_n_1 = np.ones([n - 1, n - 1])
        Iv_n_1 = np.ones(n)
        Iv_n_1[0] = 0
        Iv_n = np.ones(n - 1)
        neg_Iv_n_1 = np.ones(n) - Iv_n_1

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
        Q = A * (np.kron(Id_n, Im_n_1) + np.dot(v.T, v))

        # g defines the contribution from the individual variables
        g = (
            w
            - 2 * A * (np.kron(Iv_n_1, Iv_n) + vn.T)
            - 2 * A * K * (np.kron(neg_Iv_n_1, Iv_n) + v[0].T)
        )

        # c is the constant offset
        c = 2 * A * (n - 1) + 2 * A * (K**2)

        try:
            max(x_sol)
            # Evaluates the cost distance from a binary representation of a path
            fun = (
                lambda x: np.dot(np.around(x), np.dot(Q, np.around(x)))
                + np.dot(g, np.around(x))
                + c
            )
            cost = fun(x_sol)
        except Exception:
            cost = 0

        return Q, g, c, cost

    def construct_problem(self, Q, g, c) -> QuadraticProgram:
        qp = QuadraticProgram()
        for i in range(self.n * (self.n - 1)):
            qp.binary_var(str(i))
        qp.objective.quadratic = Q
        qp.objective.linear = g
        qp.objective.constant = c
        return qp

    def solve_problem(self, qp):

        algorithm_globals.random_seed = 10

        ansatz = RealAmplitudes(self.n)
        vqe = VQE(estimator=Estimator(), optimizer=SLSQP(maxiter=25), ansatz=ansatz)
        vqe_result = vqe.compute_minimum_eigenvalue(qp.to_ising()[0])
        qc = vqe.ansatz.bind_parameters(vqe_result.optimal_point)
        return qc


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
    qc = quantum_optimizer.solve_problem(qp)

    qc.measure_all()
    qc.name = "routing"

    return qc
