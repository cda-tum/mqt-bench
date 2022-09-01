from __future__ import annotations

import os
import subprocess
from datetime import date

import networkx as nx
import numpy as np
from joblib import Parallel, delayed
from pytket import __version__ as __tket_version__
from qiskit import QuantumCircuit, __qiskit_version__
from qiskit.algorithms import EstimationProblem
from qiskit.test.mock import FakeMontreal, FakeWashington

qasm_path = "mqt/benchviewer/static/files/qasm_output/"


def set_qasm_output_path(new_path: str = "mqt/benchviewer/static/files/qasm_output/"):
    global qasm_path
    qasm_path = new_path


def get_qasm_output_path():
    """Returns the path where all .qasm files are stored."""
    return qasm_path


def get_examplary_max_cut_qp(n_nodes: int, degree: int = 2):
    """Returns a quadratic problem formulation of a max cut problem of a random graph.

    Keyword arguments:
    n_nodes -- number of graph nodes (and also number of qubits)
    degree -- edges per node
    """
    try:
        from qiskit_optimization.applications import Maxcut
    except Exception:

        print("Please install qiskit_optimization.")
        return None
    graph = nx.random_regular_graph(d=degree, n=n_nodes, seed=111)
    maxcut = Maxcut(graph)
    return maxcut.to_quadratic_program()


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


def get_ionq11_c_map():
    ionq11_c_map = []
    for i in range(0, 11):
        for j in range(0, 11):
            if i != j:
                ionq11_c_map.append([i, j])
    return ionq11_c_map


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


def save_as_qasm(
    qc_str: str,
    filename: str,
    gate_set: list = None,
    mapped: bool = False,
    c_map=None,
    target_directory: str = "",
):
    """Saves a quantum circuit as a qasm file.

    Keyword arguments:
    qc_str -- Quantum circuit to be stored as a string
    filename -- filename
    gate_set -- set of used gates
    mapped -- boolean indicating whether the quantum circuit is mapped to a specific hardware layout
    c_map -- coupling map of used hardware layout
    """

    if c_map is None:
        c_map = []

    if target_directory:
        qasm_output_folder = target_directory
    else:
        qasm_output_folder = get_qasm_output_path()

    filename = os.path.join(qasm_output_folder, filename) + ".qasm"
    with open(filename, "w") as f:
        f.write("// Benchmark was created by MQT Bench on " + str(date.today()) + "\n")
        f.write(
            "// For more information about MQT Bench, please visit https://www.cda.cit.tum.de/mqtbench/"
            + "\n"
        )
        f.write("// MQT Bench version: " + "0.1.0" + "\n")
        if "qiskit" in filename:
            f.write("// Qiskit version: " + str(__qiskit_version__) + "\n")
        elif "tket" in filename:
            f.write("// TKET version: " + str(__tket_version__) + "\n")

        if gate_set:
            f.write("// Used Gate Set: " + str(gate_set) + "\n")
        if mapped:
            f.write("// Coupling List: " + str(c_map) + "\n")
        f.write("\n")
        f.write(qc_str)
    f.close()
    return True


def get_cmap_oqc_lucy():
    """Returns the coupling map of the OQC Lucy quantum computer."""
    # source: https://github.com/aws/amazon-braket-examples/blob/main/examples/braket_features/Verbatim_Compilation.ipynb

    # Connections are NOT bidirectional, this is not an accident
    c_map_oqc_lucy = [[0, 1], [0, 7], [1, 2], [2, 3], [7, 6], [6, 5], [4, 3], [4, 5]]

    return c_map_oqc_lucy


def get_cmap_from_devicename(device: str):
    if device == "ibm_washington":
        return FakeWashington().configuration().coupling_map
    elif device == "ibm_montreal":
        return FakeMontreal().configuration().coupling_map
    elif device == "rigetti_aspen_m1":
        return get_rigetti_c_map(10)
    elif device == "oqc_lucy":
        return get_cmap_oqc_lucy()
    elif device == "ionq11":
        return get_ionq11_c_map()
    else:
        return False


def get_molecule(benchmark_instance_name: str):
    """Returns a Molecule object depending on the parameter value."""
    try:
        from qiskit_nature.drivers import Molecule
    except Exception:
        print("Please install qiskit_nature.")
        return None
    m_1 = Molecule(
        geometry=[["H", [0.0, 0.0, 0.0]], ["H", [0.0, 0.0, 0.735]]],
        charge=0,
        multiplicity=1,
    )
    m_2 = Molecule(
        geometry=[["Li", [0.0, 0.0, 0.0]], ["H", [0.0, 0.0, 2.5]]],
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


def postprocess_oqc_qasm_files():
    directory = get_qasm_output_path()
    Parallel(n_jobs=-1, verbose=100)(
        delayed(postprocess_single_oqc_file)(directory, filename)
        for filename in os.listdir(directory)
    )


def postprocess_single_oqc_file(directory: str, filename: str):

    f = os.path.join(directory, filename)
    if "oqc_lucy_qiskit" in f or "oqc_qiskit" in f:
        with open(f) as f:
            lines = f.readlines()
        new_name = os.path.join(directory, filename)
        with open(new_name, "w") as f:
            for line in lines:
                if not (
                    "gate rzx" in line.strip("\n") or "gate ecr" in line.strip("\n")
                ):
                    f.write(line)
                if "gate ecr" in line.strip("\n"):
                    f.write(
                        "gate rzx(param0) q0,q1 { h q1; cx q0,q1; rz(param0) q1; cx q0,q1; h q1; }\n"
                    )
                    f.write(
                        "gate ecr q0,q1 { rzx(pi/4) q0,q1; x q0; rzx(-pi/4) q0,q1; }\n"
                    )

        assert QuantumCircuit.from_qasm_file(new_name)
        print("New qasm file for: ", new_name)

    elif "oqc_lucy_tket" in f or "oqc_tket" in f:
        with open(f) as f:
            lines = f.readlines()
        new_name = os.path.join(directory, filename)
        with open(new_name, "w") as f:
            count = 0
            for line in lines:
                f.write(line)
                count += 1
                if count == 9:
                    f.write(
                        "gate rzx(param0) q0,q1 { h q1; cx q0,q1; rz(param0) q1; cx q0,q1; h q1; }\n"
                    )
                    f.write(
                        "gate ecr q0,q1 { rzx(pi/4) q0,q1; x q0; rzx(-pi/4) q0,q1; }\n"
                    )
        assert QuantumCircuit.from_qasm_file(new_name)


def create_zip_file():
    return subprocess.call(
        "zip -rj ./mqt/benchviewer/static/files/MQTBench_all.zip ./mqt/benchviewer/static/files/qasm_output/",
        shell=True,
    )
