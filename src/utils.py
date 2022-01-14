from qiskit import QuantumCircuit, Aer, __qiskit_version__
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
import os

from qiskit.test.mock import FakeBogota, FakeCasablanca, FakeGuadalupe, FakeMontreal, FakeManhattan


def get_compiled_circuit(qc: QuantumCircuit, opt_level: int = 2, basis_gates: list = ['id', 'rz', 'sx', 'x', 'cx', 'reset'], c_map: CouplingMap = None):
    t_qc = transpile(qc, basis_gates=basis_gates, optimization_level=opt_level, coupling_map=c_map)
    return t_qc


def get_IBM_cmap(quantum_computer: IBMQBackend):
    return quantum_computer.configuration().coupling_map


def save_as_qasm(qc: QuantumCircuit, filename: str, gate_set: list, opt_level: int,
                 mapped: bool = False, c_map: list = [], arch_name: str = ""):

    with open("qasm_output/" + filename + ".qasm", "w") as f:
        f.write("// Benchmark was created by qTUMbench on " + str(date.today()) + "\n")
        f.write("// Qiskit version: " + str(__qiskit_version__) + "\n")
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


def sim_and_print_hist(qc: QuantumCircuit, filename: str):
    simulator = Aer.get_backend('qasm_simulator')
    result = simulator.run(qc.decompose(), shots=1024).result()
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

            c_map_rigetti.append([i + j * 8, i + 1 + j * 8])

            if i == 6:
                c_map_rigetti.append([0 + j * 8, 7 + j * 8])

        if j != 0:
            c_map_rigetti.append([j * 8 - 6, j * 8 + 5])
            c_map_rigetti.append([j * 8 - 7, j * 8 + 6])

    inversed = [[item[1], item[0]] for item in c_map_rigetti]
    c_map_rigetti = c_map_rigetti + inversed

    return c_map_rigetti


def get_google_c_map():
    c_map_google = []
    # iterate through each second line of qubits in sycamore architecture
    for j in range(1, 8, 2):
        for i in range(6):
            # connect qubit to upper left und lower left qubits
            c_map_google.append([i + 6 * j, i + 6 * j + 5])
            c_map_google.append([i + 6 * j, i + 6 * j - 6])

            # as long as it is not the most right qubit: connect it to upper right and lower right qubit
            if i != 5:
                c_map_google.append([i + 6 * j, i + 6 * j - 5])
                c_map_google.append([i + 6 * j, i + 6 * j + 7])

    inversed = [[item[1], item[0]] for item in c_map_google]
    c_map_google = c_map_google + inversed

    return c_map_google

def handle_algorithm_layer(qc:QuantumCircuit, n:int, save_png:bool, save_hist:bool):
    filename_algo = qc.name + "_algorithm_" + str(n)
    if os.path.isfile("qpy_output/" + filename_algo + '.qpy'):
        path = "qpy_output/" + filename_algo + '.qpy'
        print(path + " already existed")
        with open(path, 'rb') as fd:
            qc = qpy_serialization.load(fd)[0]
        depth = qc.depth()
    else:
        serialize_qc(qc, n, filename_algo)
        if save_png: save_circ(qc, filename_algo)
        if save_hist: sim_and_print_hist(qc, filename_algo)
        depth = qc.depth()

    return filename_algo, depth


def get_indep_layer(qc: QuantumCircuit, n:int, save_png:bool, save_hist:bool):
    filename_indep = qc.name + "_t-indep_" + str(n)
    if os.path.isfile("qpy_output/" + filename_indep + '.qpy'):
        path = "qpy_output/" + filename_indep + '.qpy'
        print(path + " already existed")
        with open(path, 'rb') as fd:
            qc = qpy_serialization.load(fd)[0]
        depth = qc.depth()

    else:
        target_independent = transpile(qc, optimization_level=1)
        serialize_qc(target_independent, n, filename_indep)
        if save_png: save_circ(qc, filename_indep)
        if save_hist: sim_and_print_hist(qc, filename_indep)
        depth = target_independent.depth()

    return filename_indep, depth


def get_transpiled_layer(qc: QuantumCircuit, gate_set: list, gate_set_name:str, opt_level:int, n:int,
                         save_png:bool, save_hist:bool, file_precheck:bool):

    filename_transpiled = qc.name + "_transpiled_" + gate_set_name + "_opt" + str(opt_level) + "_" + str(n)

    if os.path.isfile("qasm_output/" + filename_transpiled + '.qasm') and file_precheck:
        print("qasm_output/" + filename_transpiled + '.qasm' + " already existed")
        qc = QuantumCircuit.from_qasm_file("qasm_output/" + filename_transpiled + '.qasm')
        depth = qc.depth()
        return filename_transpiled, depth, n

    else:
        compiled_without_architecure = get_compiled_circuit(qc=qc, opt_level=opt_level, basis_gates=gate_set)
        n_actual = compiled_without_architecure.num_qubits
        filename_transpiled = qc.name + "_transpiled_" + gate_set_name + "_opt" + str(opt_level) + "_" + str(n_actual)
        save_as_qasm(compiled_without_architecure, filename_transpiled, gate_set, opt_level)
        if save_png: save_circ(compiled_without_architecure, filename_transpiled)
        if save_hist: sim_and_print_hist(compiled_without_architecure, filename_transpiled)

        depth = compiled_without_architecure.depth()
        return filename_transpiled, depth, n_actual

def get_mapped_layer(qc: QuantumCircuit, gate_set:str, gate_set_name:str, opt_level:int, n_actual:int,
                     ibm_smallest_fitting:bool, save_png:bool, save_hist:bool, file_precheck:bool):

    c_map, backend_name, gate_set_name_mapped, c_map_found = select_c_map(gate_set_name, ibm_smallest_fitting, n_actual)

    if (c_map_found):
        filename_mapped = qc.name + "_mapped_" + gate_set_name_mapped + "_opt" + str(opt_level) + "_" + str(n_actual)
        if os.path.isfile("qasm_output/" + filename_mapped + '.qasm') and file_precheck:
            print("qasm_output/" + filename_mapped + '.qasm' + " already existed")
            qc = QuantumCircuit.from_qasm_file("qasm_output/" + filename_mapped + '.qasm')
            depth = qc.depth()
        else:
            compiled_with_architecture = get_compiled_circuit(qc=qc, opt_level=opt_level,
                                                              basis_gates=gate_set, c_map=c_map)
            save_as_qasm(compiled_with_architecture, filename_mapped, gate_set,
                         opt_level, True, c_map, gate_set_name_mapped + "-" + backend_name)

            if save_png: save_circ(compiled_with_architecture, filename_mapped)
            if save_hist: sim_and_print_hist(compiled_with_architecture, filename_mapped)

            depth = compiled_with_architecture.depth()
        return filename_mapped, depth
    else: return

def select_c_map(gate_set_name:str, ibm_smallest_fitting:bool, n_actual:int):
    if gate_set_name == "rigetti":
        c_map = get_rigetti_c_map()
        backend_name = "32 qubits"
        gate_set_name_mapped = gate_set_name
    elif gate_set_name == "ibm":
        if ibm_smallest_fitting:
            if n_actual <= 5:
                backend = FakeBogota()
            elif n_actual <= 7:
                backend = FakeCasablanca()
            elif n_actual <= 16:
                backend = FakeGuadalupe()
            elif n_actual <= 27:
                backend = FakeMontreal()
            elif n_actual <= 65:
                backend = FakeManhattan()
            gate_set_name_mapped = gate_set_name + "-s"
        else:
            backend = FakeManhattan()
            gate_set_name_mapped = gate_set_name + "-b"

        c_map = backend.configuration().coupling_map
        backend_name = backend.name()
    else:
        raise ValueError("Gate Set Error")
    c_map_found = (max(max(c_map)) + 1) >=n_actual # +1 because coupling list indices start at 0

    return c_map, backend_name, gate_set_name_mapped, c_map_found