# Code based on https://qiskit.org/documentation/tutorials/optimization/7_examples_vehicle_routing.html

from __future__ import annotations

from typing import TYPE_CHECKING, cast

import numpy as np
from qiskit.algorithms.minimum_eigensolvers import VQE
from qiskit.algorithms.optimizers import SLSQP
from qiskit.circuit.library import RealAmplitudes
from qiskit.primitives import Estimator
from qiskit.utils import algorithm_globals
from qiskit_optimization import QuadraticProgram
from qiskit_optimization.problems import LinearExpression, QuadraticExpression

if TYPE_CHECKING:  # pragma: no cover
    from numpy.typing import NDArray
    from qiskit import QuantumCircuit


class Initializer:
    def __init__(self, n: int) -> None:
        self.n = n

    def generate_instance(
        self,
    ) -> tuple[
        NDArray[np.float_],
        NDArray[np.float_],
        NDArray[np.float_],
    ]:
        n = self.n
        np.random.seed(10)

        xc = (np.random.rand(n) - 0.5) * 10
        yc = (np.random.rand(n) - 0.5) * 10

        instance = np.zeros([n, n])
        for ii in range(n):
            for jj in range(ii + 1, n):
                instance[ii, jj] = (xc[ii] - xc[jj]) ** 2 + (yc[ii] - yc[jj]) ** 2
                instance[jj, ii] = instance[ii, jj]

        return xc, yc, instance


class QuantumOptimizer:
    def __init__(self, instance: NDArray[np.float_], n: int, K: int) -> None:
        self.instance = instance
        self.n = n
        self.K = K

    def binary_representation(
        self, x_sol: NDArray[np.float_]
    ) -> tuple[NDArray[np.float_], NDArray[np.float_], float, float]:
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
        g = w - 2 * A * (np.kron(Iv_n_1, Iv_n) + vn.T) - 2 * A * K * (np.kron(neg_Iv_n_1, Iv_n) + v[0].T)

        # c is the constant offset
        c = 2 * A * (n - 1) + 2 * A * (K**2)

        try:
            # Evaluates the cost distance from a binary representation of a path
            def fun(x: NDArray[np.float_]) -> float:
                return cast(
                    float,
                    np.dot(np.around(x), np.dot(Q, np.around(x))) + np.dot(g, np.around(x)) + c,
                )

            cost = fun(x_sol)
        except Exception:
            cost = 0

        return Q, g, cast(float, c), cost

    def construct_problem(self, Q: QuadraticExpression, g: LinearExpression, c: float) -> QuadraticProgram:
        qp = QuadraticProgram()
        for i in range(self.n * (self.n - 1)):
            qp.binary_var(str(i))

        qp.objective.quadratic = Q
        qp.objective.linear = g
        qp.objective.constant = c
        return qp

    def solve_problem(self, qp: QuadraticProgram) -> QuantumCircuit:
        algorithm_globals.random_seed = 10

        ansatz = RealAmplitudes(self.n)
        vqe = VQE(estimator=Estimator(), optimizer=SLSQP(maxiter=25), ansatz=ansatz)
        vqe_result = vqe.compute_minimum_eigenvalue(qp.to_ising()[0])
        return vqe.ansatz.bind_parameters(vqe_result.optimal_point)


def create_circuit(num_nodes: int = 3, num_vehs: int = 2) -> QuantumCircuit:
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
    q, g, c, binary_cost = quantum_optimizer.binary_representation(x_sol=np.array(0.0, dtype=float))
    q_casted = cast(QuadraticExpression, q)
    g_casted = cast(LinearExpression, g)
    qp = quantum_optimizer.construct_problem(q_casted, g_casted, c)
    # Instantiate the quantum optimizer class with parameters:
    qc = quantum_optimizer.solve_problem(qp)

    qc.measure_all()
    qc.name = "routing"

    return qc
