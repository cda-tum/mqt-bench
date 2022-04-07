from qiskit import QuantumCircuit, Aer, __qiskit_version__
from qiskit.compiler import transpile
from qiskit.transpiler import CouplingMap
from qiskit.visualization import plot_histogram
from qiskit.circuit import qpy_serialization
from qiskit.algorithms import EstimationProblem

from datetime import date

import networkx as nx
import numpy as np
from os import path, mkdir

from qiskit.test.mock import (
    FakeBogota,
    FakeCasablanca,
    FakeGuadalupe,
    FakeMontreal,
    FakeManhattan,
)

qasm_path = "./benchviewer/static/files/qasm_output/"


def set_qasm_output_path(new_path: str = "./benchviewer/static/files/qasm_output/"):
    global qasm_path
    qasm_path = new_path


def get_qasm_output_path():
    """Returns the path where all .qasm files are stored."""
    return qasm_path


def get_compiled_circuit_with_gateset(
    qc: QuantumCircuit,
    opt_level: int = 1,
    basis_gates=None,
    c_map: CouplingMap = None,
):
    """Returns a transpiled quantum circuit according to the given input parameters.

    Keyword arguments:
    qc -- to be transpiled QuantumCircuit
    opt_level -- optimization level
    basis_gates -- used gates of resulting quantum circuit
    c_map -- to be used coupling map
    """

    if basis_gates is None:
        basis_gates = ["id", "rz", "sx", "x", "cx", "reset"]

    t_qc = transpile(
        qc, basis_gates=basis_gates, optimization_level=opt_level, coupling_map=c_map
    )
    return t_qc


def get_rigetti_native_gates():
    return ["rx", "rz", "cz", "id", "reset"]


def save_as_qasm(
    qc: QuantumCircuit,
    filename: str,
    gate_set: list = None,
    opt_level: int = -1,
    mapped: bool = False,
    c_map=None,
    arch_name: str = "",
):
    """Saves a quantum circuit as a qasm file.

    Keyword arguments:
    qc -- to be saved QuantumCircuit
    filename -- filename
    gate_set -- set of used gates
    opt_level -- optimization level
    mapped -- boolean indicating whether the quantum circuit is mapped to a specific hardware layout
    c_map -- coupling map of used hardware layout
    arch_name -- name of used hardware layout
    """

    if c_map is None:
        c_map = []

    qasm_output_folder = get_qasm_output_path()
    print(qasm_output_folder)
    with open(qasm_output_folder + filename + ".qasm", "w") as f:
        f.write("// Benchmark was created by MQT Bench on " + str(date.today()) + "\n")
        f.write(
            "// For more information about MQT Bench, please visit https://www.cda.cit.tum.de/mqtbench/"
            + "\n"
        )
        f.write("// MQT Bench version: " + "0.1.0" + "\n")
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


def serialize_qc(qc: QuantumCircuit, filename: str):
    """Saves a quantum circuit as a qpy file.

    Keyword arguments:
    qc -- to be saved QuantumCircuit
    filename -- filename
    """

    with open("qpy_output/" + filename + ".qpy", "wb") as f:
        qpy_serialization.dump(qc, f)
    f.close()


def get_examplary_max_cut_qp(n_nodes: int, degree: int = 2):
    """Returns a quadratic problem formulation of a max cut problem of a random graph.

    Keyword arguments:
    n_nodes -- number of graph nodes (and also number of qubits)
    degree -- edges per node
    """
    try:
        from qiskit_optimization.applications import Maxcut
    except:

        print("Please install qiskit_optimization.")
        return None
    graph = nx.random_regular_graph(d=degree, n=n_nodes, seed=111)
    maxcut = Maxcut(graph)
    return maxcut.to_quadratic_program()


def sim_and_print_hist(qc: QuantumCircuit, filename: str):
    """Simulates a given quantum circuit and prints its resulting histogram.

    Keyword arguments:
    qc -- to be simulated quantum circuit
    filename -- filename of the histogram
    """

    if not path.isdir("./hist_output"):
        mkdir("hist_output")

    simulator = Aer.get_backend("aer_simulator")
    result = simulator.run(qc.decompose(), shots=1024).result()
    counts = result.get_counts()
    plot = plot_histogram(counts, figsize=(15, 5), title=filename)
    plot.savefig("hist_output/" + filename + "_hist" + ".png", bbox_inches="tight")


def save_circ(qc: QuantumCircuit, filename: str):
    """Save schematic picture of a given quantum circuit.

    Keyword arguments:
    qc -- to be saved quantum circuit
    filename -- filename of the schematic picture
    """
    if not path.isdir("./hist_output"):
        mkdir("hist_output")

    qc.draw(output="mpl", filename="hist_output/" + filename + ".png")


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
    """Returns a estimation problem instance for a fixed p value."""

    p = 0.2

    a = BernoulliA(p)
    q = BernoulliQ(p)

    problem = EstimationProblem(
        state_preparation=a,  # A operator
        grover_operator=q,  # Q operator
        objective_qubits=[
            0
        ],  # the "good" state Psi1 is identified as measuring |1> in qubit 0
    )

    return problem


def get_rigetti_c_map(circles: int = 4):
    """Returns a coupling map of the circular layout scheme used by Rigetti.

    Keyword arguments:
    circles -- number of circles, each one comprises 8 qubits
    """
    if circles != 10:
        c_map_rigetti = []
        for j in range(circles):
            for i in range(0, 7):
                c_map_rigetti.append([i + j * 8, i + 1 + j * 8])

                if i == 6:
                    c_map_rigetti.append([0 + j * 8, 7 + j * 8])

            if j != 0:
                c_map_rigetti.append([j * 8 - 6, j * 8 + 5])
                c_map_rigetti.append([j * 8 - 7, j * 8 + 6])

        inverted = [[item[1], item[0]] for item in c_map_rigetti]
        c_map_rigetti = c_map_rigetti + inverted
    else:
        c_map_rigetti = []
        for j in range(5):
            for i in range(0, 7):
                c_map_rigetti.append([i + j * 8, i + 1 + j * 8])

                if i == 6:
                    c_map_rigetti.append([0 + j * 8, 7 + j * 8])

            if j != 0:
                c_map_rigetti.append([j * 8 - 6, j * 8 + 5])
                c_map_rigetti.append([j * 8 - 7, j * 8 + 6])

        for j in range(5):
            m = 8 * j + 5 * 8
            for i in range(0, 7):
                c_map_rigetti.append([i + m, i + 1 + m])

                if i == 6:
                    c_map_rigetti.append([0 + m, 7 + m])

            if j != 0:
                c_map_rigetti.append([m - 6, m + 5])
                c_map_rigetti.append([m - 7, m + 6])

        for n in range(5):
            c_map_rigetti.append([n * 8 + 3, n * 8 + 5 * 8])
            c_map_rigetti.append([n * 8 + 4, n * 8 + 7 + 5 * 8])

        inverted = [[item[1], item[0]] for item in c_map_rigetti]
        c_map_rigetti = c_map_rigetti + inverted

    return c_map_rigetti


def get_google_c_map():
    """Returns a coupling map of the hardware layout scheme used by Google's Sycamore chip."""
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

    inverted = [[item[1], item[0]] for item in c_map_google]
    c_map_google = c_map_google + inverted

    return c_map_google


def handle_algorithm_level(
    qc: QuantumCircuit, num_qubits: int, save_png: bool, save_hist: bool
):
    """Handles the creation of the benchmark on the algorithm level.

    Keyword arguments:
    qc -- quantum circuit which shall be created
    num_qubits -- number of qubits
    save_png -- flag indicated whether to save schematic picture of quantum circuit
    save_hist -- flag indicated whether to simulate circuit and save its histogram

    Return values:
    filename_algo -- the filename of the created and saved benchmark
    depth -- circuit depth of created benchmark
    num_qubits -- number of qubits of generated circuit
    """
    filename_algo = qc.name + "_algorithm_" + str(num_qubits)
    if path.isfile("qpy_output/" + filename_algo + ".qpy"):
        filepath = "qpy_output/" + filename_algo + ".qpy"
        print(filepath + " already exists")
        with open(filepath, "rb") as fd:
            qc = qpy_serialization.load(fd)[0]
        depth = qc.depth()
    else:
        serialize_qc(qc, filename_algo)
        if save_png:
            save_circ(qc, filename_algo)
        if save_hist:
            sim_and_print_hist(qc, filename_algo)
        depth = qc.depth()

    return filename_algo, depth, num_qubits


def get_indep_level(
    qc: QuantumCircuit,
    num_qubits: int,
    save_png: bool,
    save_hist: bool,
    file_precheck: bool,
):
    """Handles the creation of the benchmark on the target-independent level.

    Keyword arguments:
    qc -- quantum circuit which the to be created benchmark circuit is based on
    num_qubits -- number of qubits
    save_png -- flag indicated whether to save schematic picture of quantum circuit
    save_hist -- flag indicated whether to simulate circuit and save its histogram
    file_precheck -- flag indicating whether to check whether the file already exists before creating it (again)

    Return values:
    filename_indep -- the filename of the created and saved benchmark
    depth -- circuit depth of created benchmark
    num_qubits -- number of qubits of generated circuit
    """

    filename_indep = qc.name + "_indep_" + str(num_qubits)
    qasm_output_folder = get_qasm_output_path()
    filepath = qasm_output_folder + filename_indep + ".qasm"
    if path.isfile(filepath) and file_precheck:
        print(filepath + " already exists")
        qc = QuantumCircuit.from_qasm_file(filepath)
        depth = qc.depth()
        return filename_indep, depth, num_qubits

    else:
        openqasm_gates = get_openqasm_gates()
        target_independent = transpile(
            qc, basis_gates=openqasm_gates, optimization_level=1
        )
        save_as_qasm(target_independent, filename_indep)
        if save_png:
            save_circ(target_independent, filename_indep)
        if save_hist:
            sim_and_print_hist(target_independent, filename_indep)

        depth = target_independent.depth()
        return filename_indep, depth, qc.num_qubits


def get_native_gates_level(
    qc: QuantumCircuit,
    gate_set: list,
    gate_set_name: str,
    opt_level: int,
    num_qubits: int,
    save_png: bool,
    save_hist: bool,
    file_precheck: bool,
):
    """Handles the creation of the benchmark on the target-dependent native gates level.

    Keyword arguments:
    qc -- quantum circuit which the to be created benchmark circuit is based on
    gate_set -- set of to be used gates
    gate_set_name -- name of this gate set
    opt_level -- optimization level
    num_qubits -- number of qubits
    save_png -- flag indicated whether to save schematic picture of quantum circuit
    save_hist -- flag indicated whether to simulate circuit and save its histogram
    file_precheck -- flag indicating whether to check whether the file already exists before creating it (again)

    Return values:
    filename_nativegates -- the filename of the created and saved benchmark
    depth -- circuit depth of created benchmark
    num_qubits/n_actual -- number of qubits of created benchmark
    """

    filename_nativegates = (
        qc.name
        + "_nativegates_"
        + gate_set_name
        + "_opt"
        + str(opt_level)
        + "_"
        + str(num_qubits)
    )

    qasm_output_folder = get_qasm_output_path()
    if (
        path.isfile(qasm_output_folder + filename_nativegates + ".qasm")
        and file_precheck
    ):
        print(qasm_output_folder + filename_nativegates + ".qasm" + " already exists")
        qc = QuantumCircuit.from_qasm_file(
            qasm_output_folder + filename_nativegates + ".qasm"
        )
        depth = qc.depth()
        return filename_nativegates, depth, num_qubits

    else:
        compiled_without_architecture = get_compiled_circuit_with_gateset(
            qc=qc, opt_level=opt_level, basis_gates=gate_set
        )
        n_actual = compiled_without_architecture.num_qubits
        filename_nativegates = (
            qc.name
            + "_nativegates_"
            + gate_set_name
            + "_opt"
            + str(opt_level)
            + "_"
            + str(n_actual)
        )
        save_as_qasm(
            compiled_without_architecture, filename_nativegates, gate_set, opt_level
        )
        if save_png:
            save_circ(compiled_without_architecture, filename_nativegates)
        if save_hist:
            sim_and_print_hist(compiled_without_architecture, filename_nativegates)

        depth = compiled_without_architecture.depth()
        return filename_nativegates, depth, n_actual


def get_mapped_level(
    qc: QuantumCircuit,
    gate_set: list,
    gate_set_name: str,
    opt_level: int,
    num_qubits: int,
    smallest_fitting_arch: bool,
    save_png: bool,
    save_hist: bool,
    file_precheck: bool,
):
    """Handles the creation of the benchmark on the target-dependent mapped level.

    Keyword arguments:
    qc -- quantum circuit which the to be created benchmark circuit is based on
    gate_set -- set of to be used gates
    gate_set_name -- name of this gate set
    opt_level -- optimization level
    num_qubits -- number of qubits
    smallest_fitting_arch -- flag indicating whether smallest fitting mapping scheme shall be used
    save_png -- flag indicated whether to save schematic picture of quantum circuit
    save_hist -- flag indicated whether to simulate circuit and save its histogram
    file_precheck -- flag indicating whether to check whether the file already exists before creating it (again)

    Return values:
    filename_mapped -- the filename of the created and saved benchmark
    depth -- circuit depth of created benchmark
    num_qubits -- number of qubits of generated circuit
    """

    c_map, backend_name, gate_set_name_mapped, c_map_found = select_c_map(
        gate_set_name, smallest_fitting_arch, num_qubits
    )

    if c_map_found:
        filename_mapped = (
            qc.name
            + "_mapped_"
            + gate_set_name_mapped
            + "_opt"
            + str(opt_level)
            + "_"
            + str(num_qubits)
        )
        qasm_output_folder = get_qasm_output_path()
        if (
            path.isfile(qasm_output_folder + filename_mapped + ".qasm")
            and file_precheck
        ):
            print(qasm_output_folder + filename_mapped + ".qasm" + " already exists")
            qc = QuantumCircuit.from_qasm_file(
                qasm_output_folder + filename_mapped + ".qasm"
            )
            depth = qc.depth()
        else:
            compiled_with_architecture = get_compiled_circuit_with_gateset(
                qc=qc, opt_level=opt_level, basis_gates=gate_set, c_map=c_map
            )
            save_as_qasm(
                compiled_with_architecture,
                filename_mapped,
                gate_set,
                opt_level,
                True,
                c_map,
                gate_set_name_mapped + "-" + backend_name,
            )

            if save_png:
                save_circ(compiled_with_architecture, filename_mapped)
            if save_hist:
                sim_and_print_hist(compiled_with_architecture, filename_mapped)

            depth = compiled_with_architecture.depth()
        return filename_mapped, depth, num_qubits
    else:
        return "", 0, 0


def select_c_map(gate_set_name: str, smallest_fitting_arch: bool, num_qubits: int):
    """Returns a suitable coupling map for input parameters

    Keyword arguments:
    gate_set_name -- name of used gate set
    smallest_fitting_arch -- flag indicating whether smallest fitting mapping scheme shall be used
    num_qubits -- number of qubits

    Return values:
    c_map -- coupling map for input parameters
    backend_name -- name of the hardware layout for the respective coupling map
    gate_set_name_mapped -- combination of gate_set_name and smallest_fitting_arch
    c_map_found -- indicator whether a suitable coupling map has been found
    """
    c_map_found = False
    c_map = []
    backend_name = ""
    gate_set_name_mapped = ""

    if gate_set_name == "rigetti":
        c_map_found = True
        if smallest_fitting_arch:
            if num_qubits <= 8:
                c_map = get_rigetti_c_map(1)
                backend_name = "8 qubits"
            elif num_qubits <= 16:
                c_map = get_rigetti_c_map(2)
                backend_name = "Aspen-3: 16 qubits"
            elif num_qubits <= 32:
                c_map = get_rigetti_c_map(4)
                backend_name = "Aspen-10: 32 qubits"
            elif num_qubits <= 40:
                c_map = get_rigetti_c_map(5)
                backend_name = "Aspen-11: 40 qubits"
            elif num_qubits <= 80:
                c_map = get_rigetti_c_map(10)
                backend_name = "Aspen-M-1: 80 qubits"
            else:
                c_map_found = False
            gate_set_name_mapped = gate_set_name + "-s"

        elif num_qubits <= 80:
            c_map = get_rigetti_c_map(10)
            backend_name = "Aspen-M-1: 80 qubits"
            gate_set_name_mapped = gate_set_name + "-b"
        else:
            c_map_found = False

    elif gate_set_name == "ibm":
        c_map_found = True
        if smallest_fitting_arch:
            if num_qubits <= 5:
                backend = FakeBogota()
                c_map = backend.configuration().coupling_map
                backend_name = backend.name()
            elif num_qubits <= 7:
                backend = FakeCasablanca()
                c_map = backend.configuration().coupling_map
                backend_name = backend.name()
            elif num_qubits <= 16:
                backend = FakeGuadalupe()
                c_map = backend.configuration().coupling_map
                backend_name = backend.name()
            elif num_qubits <= 27:
                backend = FakeMontreal()
                c_map = backend.configuration().coupling_map
                backend_name = backend.name()
            elif num_qubits <= 65:
                backend = FakeManhattan()
                c_map = backend.configuration().coupling_map
                backend_name = backend.name()
            elif num_qubits <= 127:
                c_map = get_cmap_imbq_washington()
                backend_name = "Washington"
            else:
                c_map_found = False
            gate_set_name_mapped = gate_set_name + "-s"

        elif num_qubits <= 127:
            c_map = get_cmap_imbq_washington()
            backend_name = "Washington"
            gate_set_name_mapped = gate_set_name + "-b"
        else:
            c_map_found = False

    if c_map_found:
        return c_map, backend_name, gate_set_name_mapped, c_map_found
    else:
        return None, "", "", False


def get_cmap_imbq_washington():
    """Returns the coupling map of the IBM-Q washington quantum computer."""
    c_map_ibmq_washington = [
        [0, 1],
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
        [125, 126],
    ]

    inverted = [[item[1], item[0]] for item in c_map_ibmq_washington]
    c_map_ibmq_washington = c_map_ibmq_washington + inverted
    return c_map_ibmq_washington


def get_openqasm_gates():
    """Returns a list of all quantum gates within the openQASM 2.0 standard header."""
    # according to https://github.com/Qiskit/qiskit-terra/blob/main/qiskit/qasm/libs/qelib1.inc
    gate_list = [
        "u3",
        "u2",
        "u1",
        "cx",
        "id",
        "u0",
        "u",
        "p",
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
        "sx",
        "sxdg",
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
        "cp",
        "cu3",
        "csx",
        "cu",
        "rxx",
        "rzz",
        "rccx",
        "rc3x",
        "c3x",
        "c3sqrtx",
        "c4x",
    ]
    return gate_list


def get_molecule(benchmark_instance_name: str):
    """Returns a Molecule object depending on the parameter value."""
    try:
        from qiskit_nature.drivers import Molecule
    except:
        print("Please install qiskit_nature.")
        return None
    m_1 = Molecule(
        geometry=[["Li", [0.0, 0.0, 0.0]], ["H", [0.0, 0.0, 2.5]]],
        charge=0,
        multiplicity=1,
    )
    m_2 = Molecule(
        geometry=[["H", [0.0, 0.0, 0.0]], ["H", [0.0, 0.0, 0.735]]],
        charge=0,
        multiplicity=1,
    )
    m_3 = Molecule(
        geometry=[
            ["O", [0.0, 0.0, 0.0]],
            ["H", [0.586, 0.757, 0.0]],
            ["H", [0.586, -0.757, 0.0]],
        ],
        charge=0,
        multiplicity=1,
    )
    instances = {"small": m_1, "medium": m_2, "large": m_3}

    return instances[benchmark_instance_name]
