from qiskit import QuantumCircuit, Aer, __qiskit_version__
from qiskit.compiler import transpile
from qiskit.transpiler import CouplingMap
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

def save_as_qasm(qc: QuantumCircuit, filename: str, gate_set: list=None, opt_level: int=-1,
                 mapped: bool = False, c_map: list = [], arch_name: str = ""):

    with open("qasm_output/" + filename + ".qasm", "w") as f:
        f.write("// Benchmark was created by qTUMbench on " + str(date.today()) + "\n")
        f.write("// Qiskit version: " + str(__qiskit_version__) + "\n")
        if gate_set:
            f.write("// Used Gate Set: " + str(gate_set) + "\n")
        if opt_level >= 0:
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


def get_rigetti_c_map(circles: int = 4):
    c_map_rigetti = []
    for j in range(circles):
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
    path = "qasm_output/" + filename_indep + '.qasm'
    if os.path.isfile(path):
        print(path + " already existed")
        qc = QuantumCircuit.from_qasm_file(path)
        depth = qc.depth()
        return filename_indep, depth

    else:
        openQASM_gates = get_openQASM_gates()
        target_independent = transpile(qc, basis_gates=openQASM_gates, optimization_level=1) # decompose because otherwise error occur due to custom gates
        save_as_qasm(target_independent, filename_indep)
        if save_png: save_circ(target_independent, filename_indep)
        if save_hist: sim_and_print_hist(target_independent, filename_indep)

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
                     smallest_fitting_arch:bool, save_png:bool, save_hist:bool, file_precheck:bool):

    c_map, backend_name, gate_set_name_mapped, c_map_found = select_c_map(gate_set_name, smallest_fitting_arch, n_actual)

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
    else: return "", 0

def select_c_map(gate_set_name:str, smallest_fitting_arch:bool, n_actual:int):
    c_map_found = False
    if gate_set_name == "rigetti":
        if smallest_fitting_arch:
            if n_actual <= 8:
                c_map = get_rigetti_c_map(1)
                backend_name = "8 qubits"
                c_map_found = True
            elif n_actual <= 16:
                c_map = get_rigetti_c_map(2)
                backend_name = "Aspen-3: 16 qubits"
                c_map_found = True
            elif n_actual <= 32:
                c_map = get_rigetti_c_map(4)
                backend_name = "Aspen-10: 32 qubits"
                c_map_found = True
            elif n_actual <= 40:
                c_map = get_rigetti_c_map(5)
                backend_name = "Aspen-11: 40 qubits"
                c_map_found = True
            elif n_actual <= 80:
                c_map = get_rigetti_c_map(10)
                backend_name = "80 qubits"
                c_map_found = True
            gate_set_name_mapped = gate_set_name + "-s"

        elif n_actual <= 80:
            c_map = get_rigetti_c_map(10)
            backend_name = "80 qubits"
            c_map_found = True
            gate_set_name_mapped = gate_set_name + "-b"

    elif gate_set_name == "ibm":
        if smallest_fitting_arch:
            if n_actual <= 5:
                backend = FakeBogota()
                c_map = backend.configuration().coupling_map
                backend_name = backend.name()
                c_map_found = True
            elif n_actual <= 7:
                backend = FakeCasablanca()
                c_map = backend.configuration().coupling_map
                backend_name = backend.name()
                c_map_found = True
            elif n_actual <= 16:
                backend = FakeGuadalupe()
                c_map = backend.configuration().coupling_map
                backend_name = backend.name()
                c_map_found = True
            elif n_actual <= 27:
                backend = FakeMontreal()
                c_map = backend.configuration().coupling_map
                backend_name = backend.name()
                c_map_found = True
            elif n_actual <= 65:
                backend = FakeManhattan()
                c_map = backend.configuration().coupling_map
                backend_name = backend.name()
                c_map_found = True
            elif n_actual <= 127:
                c_map = get_cmap_imbq_washington()
                backend_name = "Washington"
                c_map_found = True
            gate_set_name_mapped = gate_set_name + "-s"

        elif n_actual <= 127:
            c_map = get_cmap_imbq_washington()
            backend_name = "Washington"
            c_map_found = True
            gate_set_name_mapped = gate_set_name + "-b"


    else:
        raise ValueError("Gate Set Error")

    if c_map_found:
        return c_map, backend_name, gate_set_name_mapped, c_map_found
    else:
        return False, False, False, False

def get_cmap_imbq_washington():
    c_map_ibmq_washington = [[0, 1],
                        [1, 2],
                        [2, 3],
                        [3, 4],
                        [4, 5],
                        [5, 6],
                        [6, 7],
                        [7, 8],
                        [0, 14],
                        [14, 18],
                        [18, 19],
                        [19, 20],
                        [20, 21],
                        [21, 22],
                        [4, 15],
                        [15, 22],
                        [22, 23],
                        [23, 24],
                        [24, 25],
                        [25, 26],
                        [8, 16],
                        [16, 26],
                        [26, 27],
                        [27, 28],
                        [28, 29],
                        [29, 30],
                        [30, 31],
                        [31, 32],
                        [9, 10],
                        [10, 11],
                        [11, 12],
                        [12, 13],
                        [12, 17],
                        [17, 30],
                        [32, 36],
                        [36, 51],
                        [20, 33],
                        [33, 39],
                        [24, 34],
                        [34, 43],
                        [28, 35],
                        [35, 47],
                        [37, 38],
                        [38, 39],
                        [39, 40],
                        [40, 41],
                        [41, 42],
                        [42, 43],
                        [43, 44],
                        [44, 45],
                        [45, 46],
                        [46, 47],
                        [47, 48],
                        [48, 49],
                        [49, 50],
                        [50, 51],
                        [37, 52],
                        [52, 56],
                        [41, 53],
                        [53, 60],
                        [45, 54],
                        [54, 64],
                        [49, 55],
                        [55, 68],
                        [56, 57],
                        [57, 58],
                        [58, 59],
                        [59, 60],
                        [60, 61],
                        [61, 62],
                        [62, 63],
                        [63, 64],
                        [64, 65],
                        [65, 66],
                        [66, 67],
                        [67, 68],
                        [68, 69],
                        [69, 70],
                        [70, 74],
                        [74, 89],
                        [58, 71],
                        [71, 77],
                        [62, 72],
                        [72, 81],
                        [66, 73],
                        [73, 85],
                        [75, 76],
                        [76, 77],
                        [77, 78],
                        [78, 79],
                        [79, 80],
                        [80, 81],
                        [81, 82],
                        [82, 83],
                        [83, 84],
                        [84, 85],
                        [85, 86],
                        [86, 87],
                        [87, 88],
                        [88, 89],
                        [75, 90],
                        [90, 94],
                        [79, 91],
                        [91, 98],
                        [83, 92],
                        [92, 102],
                        [87, 93],
                        [93, 106],
                        [94, 95],
                        [95, 96],
                        [96, 97],
                        [97, 98],
                        [98, 99],
                        [99, 100],
                        [100, 101],
                        [101, 102],
                        [102, 103],
                        [103, 104],
                        [104, 105],
                        [105, 106],
                        [106, 107],
                        [107, 108],
                        [108, 112],
                        [112, 126],
                        [96, 109],
                        [100, 110],
                        [110, 118],
                        [104, 111],
                        [111, 122],
                        [113, 114],
                        [114, 115],
                        [115, 116],
                        [116, 117],
                        [117, 118],
                        [118, 119],
                        [119, 120],
                        [120, 121],
                        [121, 122],
                        [122, 123],
                        [123, 124],
                        [124, 125],
                        [125, 126]]

    inversed = [[item[1], item[0]] for item in c_map_ibmq_washington]
    c_map_ibmq_washington = c_map_ibmq_washington + inversed
    return c_map_ibmq_washington

def get_openQASM_gates():
    # according to QASMbench paper
    gate_list = [
        "u3",
        "u2",
        "u1",
        "cx",
        "id",
        "x",
        "y",
        "z",
        "h",
        "s",
        "sdg",
        "t",
        "tdg",
        "rx",
        "ry",
        "rz",
        "cz",
        "cy",
        "swap",
        "ch",
        "ccx",
        "cswap",
        "crx",
        "cry",
        "crz",
        "cu1",
        "cu3",
        "rxx",
        "rzz",
        "rccx",
        "rc3x",
        "c3x",
        "c3xsqrtx",
        "c4x"]
    return gate_list