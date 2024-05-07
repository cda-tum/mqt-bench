"""Routing benchmark definition. Code is based on https://qiskit.org/documentation/tutorials/optimization/7_examples_vehicle_routing.html."""

from __future__ import annotations

from typing import TYPE_CHECKING, cast

import numpy as np
from qiskit.circuit.library import RealAmplitudes
from qiskit.primitives import Estimator
from qiskit_algorithms.minimum_eigensolvers import VQE
from qiskit_algorithms.optimizers import SLSQP
from qiskit_optimization import QuadraticProgram
from qiskit_optimization.problems import LinearExpression, QuadraticExpression

if TYPE_CHECKING:  # pragma: no cover
    from numpy.typing import NDArray
    from qiskit import QuantumCircuit


class Initializer:
    """Initializes the problem by randomly generating the instance."""

    def __init__(self, n: int) -> None:
        """Initializes the problem by randomly generating the instance."""
        self.n = n

    def generate_instance(
        self,
    ) -> tuple[
        NDArray[np.float64],
        NDArray[np.float64],
        NDArray[np.float64],
    ]:
        """Generates a random instance of the problem."""
        n = self.n
        rng = np.random.default_rng(10)

        xc = (rng.random(n) - 0.5) * 10
        yc = (rng.random(n) - 0.5) * 10

        instance = np.zeros([n, n])
        for ii in range(n):
            for jj in range(ii + 1, n):
                instance[ii, jj] = (xc[ii] - xc[jj]) ** 2 + (yc[ii] - yc[jj]) ** 2
                instance[jj, ii] = instance[ii, jj]

        return xc, yc, instance


class QuantumOptimizer:
    """Class to solve the problem using a quantum optimizer."""

    def __init__(self, instance: NDArray[np.float64], n: int, k: int) -> None:
        """Initializes the class to solve the problem using a quantum optimizer."""
        self.instance = instance
        self.n = n
        self.k = k

    def binary_representation(
        self, x_sol: NDArray[np.float64]
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], float, float]:
        """Returns the binary representation of the problem."""
        instance = self.instance
        n = self.n
        k = self.k

        a = np.max(instance) * 100  # A parameter of cost function

        # Determine the weights w
        instance_vec = instance.reshape(n**2)
        w_list = [instance_vec[x] for x in range(n**2) if instance_vec[x] > 0]
        w = np.zeros(n * (n - 1))
        for ii in range(len(w_list)):
            w[ii] = w_list[ii]

        # Some variables I will use
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
        g = w - 2 * a * (np.kron(iv_n_1, iv_n) + vn.T) - 2 * a * k * (np.kron(neg_iv_n_1, iv_n) + v[0].T)

        # c is the constant offset
        c = 2 * a * (n - 1) + 2 * a * (k**2)

        try:
            # Evaluates the cost distance from a binary representation of a path
            def fun(x: NDArray[np.float64]) -> float:
                return cast(
                    float,
                    np.dot(np.around(x), np.dot(q, np.around(x))) + np.dot(g, np.around(x)) + c,
                )

            cost = fun(x_sol)
        except Exception:
            cost = 0

        return q, g, cast(float, c), cost

    def construct_problem(self, q: QuadraticExpression, g: LinearExpression, c: float) -> QuadraticProgram:
        """Constructs the problem."""
        qp = QuadraticProgram()
        for i in range(self.n * (self.n - 1)):
            qp.binary_var(str(i))

        qp.objective.quadratic = q
        qp.objective.linear = g
        qp.objective.constant = c
        return qp

    def solve_problem(self, qp: QuadraticProgram) -> QuantumCircuit:
        """Solves the problem."""
        ansatz = RealAmplitudes(self.n)
        vqe = VQE(estimator=Estimator(), optimizer=SLSQP(maxiter=25), ansatz=ansatz)
        vqe.random_seed = 10
        vqe_result = vqe.compute_minimum_eigenvalue(qp.to_ising()[0])
        return vqe.ansatz.assign_parameters(vqe_result.optimal_point)


def create_circuit(num_nodes: int = 3, num_vehs: int = 2) -> QuantumCircuit:
    """Returns a quantum circuit solving a routing problem.

    Arguments:
        num_nodes: number of to be visited nodes
        num_vehs: number of used vehicles

    Returns:
        QuantumCircuit: quantum circuit solving the routing problem
    """
    # Initialize the problem by defining the parameters
    n = num_nodes  # number of nodes + depot (n+1)
    k = num_vehs  # number of vehicles
    # Initialize the problem by randomly generating the instance
    initializer = Initializer(n)
    _xc, _yc, instance = initializer.generate_instance()

    quantum_optimizer = QuantumOptimizer(instance, n, k)
    q, g, c, _binary_cost = quantum_optimizer.binary_representation(x_sol=np.array(0.0, dtype=float))
    q_casted = cast(QuadraticExpression, q)
    g_casted = cast(LinearExpression, g)
    qp = quantum_optimizer.construct_problem(q_casted, g_casted, c)
    # Instantiate the quantum optimizer class with parameters:
    qc = quantum_optimizer.solve_problem(qp)

    qc.measure_all()
    qc.name = "routing"

    return qc
