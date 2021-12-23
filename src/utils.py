from qiskit import QuantumCircuit, __qiskit_version__
from qiskit.compiler import transpile
from qiskit.transpiler import CouplingMap
from qiskit.providers.ibmq.ibmqbackend import IBMQBackend
from qiskit_optimization.applications import Maxcut
from qiskit.visualization import plot_histogram
from qiskit.circuit import qpy_serialization
from qiskit.algorithms import EstimationProblem

from datetime import date

import networkx as nx
import numpy as np

def get_compiled_circuit(qc: QuantumCircuit, opt_level: int = 2, basis_gates: list = ['id', 'rz', 'sx', 'x', 'cx', 'reset'], c_map: CouplingMap = None):
    t_qc = transpile(qc, basis_gates=basis_gates, optimization_level=opt_level, coupling_map=c_map)
    return t_qc


def get_IBM_cmap(quantum_computer: IBMQBackend):
    return quantum_computer.configuration().coupling_map


def save_as_qasm(qc: QuantumCircuit, n_qubits: int, filename: str, gate_set: list, opt_level: int,
                 mapped: bool = False, c_map: list = [], arch_name: str = ""):

    with open("qasm_output/" + filename + ".qasm", "w") as f:
        f.write("// Benchmark was created by qTUMbench on " + str(date.today()) + "\n")
        f.write("// Qiskit version: \n" + str(__qiskit_version__) + "\n")
        f.write("// Used Gate Set: " + str(gate_set) + "\n")
        f.write("// Optimization Level: " + str(opt_level) + "\n")
        if mapped:
            f.write("// Coupling List: " + str(c_map) + "\n")
            if arch_name:
                f.write("// Compiled for architecture: " + arch_name + "\n")
        f.write("\n")
        f.write(qc.qasm())
    f.close()

def serialize_qc(qc: QuantumCircuit, n_qubits: int, filename:str):
    with open("qpy_output/" + filename + '.qpy', 'wb') as f:
        qpy_serialization.dump(qc, f)
    f.close()

def get_examplary_max_cut_qp(n_qubits: int, degree:int = 2):
    graph = nx.random_regular_graph(d=degree, n=n_qubits, seed=111)
    maxcut = Maxcut(graph)
    return maxcut.to_quadratic_program()


def sim_and_print_hist(qc: QuantumCircuit, simulator, filename: str):
    result = simulator.run(qc, shots=1024).result()
    counts = result.get_counts()
    plot = plot_histogram(counts, figsize=(15, 5), title=filename)
    plot.savefig("hist_output/" + filename + '_hist' + '.png', bbox_inches="tight")


def save_circ(qc: QuantumCircuit, filename: str):
    circ_plot = qc.draw(output="mpl", filename="hist_output/" + filename + '.png')

class BernoulliA(QuantumCircuit):
    """A circuit representing the Bernoulli A operator."""

    def __init__(self, probability):
        super().__init__(1)  # circuit on 1 qubit

        theta_p = 2 * np.arcsin(np.sqrt(probability))
        self.ry(theta_p, 0)


class BernoulliQ(QuantumCircuit):
    """A circuit representing the Bernoulli Q operator."""

    def __init__(self, probability):
        super().__init__(1)  # circuit on 1 qubit

        self._theta_p = 2 * np.arcsin(np.sqrt(probability))
        self.ry(2 * self._theta_p, 0)

    def power(self, k):
        # implement the efficient power of Q
        q_k = QuantumCircuit(1)
        q_k.ry(2 * k * self._theta_p, 0)
        return q_k


def get_estimation_problem():
    p = 0.2

    A = BernoulliA(p)
    Q = BernoulliQ(p)

    problem = EstimationProblem(
        state_preparation=A,  # A operator
        grover_operator=Q,  # Q operator
        objective_qubits=[0],  # the "good" state Psi1 is identified as measuring |1> in qubit 0
    )

    return problem


def get_rigetti_c_map():
    c_map_rigetti = []
    for j in range(4):
        for i in range(0, 7):
            elem = [i + j * 10, i + 1 + j * 10]
            c_map_rigetti.append(elem)
            if i == 6:
                c_map_rigetti.append([0 + j * 10, 7 + j * 10])

    return c_map_rigetti


def get_google_c_map():
    c_map_google = []
    for j in range(8):
        for i in range(6):
            if j % 2 == 0:
                if i != 0:
                    elem = [i + 6 * j, i + 6 * j + 5]
                    c_map_google.append(elem)

                if i != 6:
                    elem = [i + 6 * j, i + 6 * j + 6]
                    c_map_google.append(elem)

            else:
                if i != 0:
                    elem = [i + 6 * j, i + 6 * j + 6]
                    c_map_google.append(elem)

                if i != 6:
                    elem = [i + 6 * j, i + 6 * j + 7]
                    c_map_google.append(elem)

    return c_map_google