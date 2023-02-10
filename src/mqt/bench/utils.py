from __future__ import annotations

import subprocess
import sys
from datetime import date
from pathlib import Path
from typing import TYPE_CHECKING

import networkx as nx
import numpy as np
from pytket import __version__ as __tket_version__
from qiskit import QuantumCircuit, __qiskit_version__
from qiskit.algorithms import EstimationProblem
from qiskit.providers.fake_provider import FakeMontreal, FakeWashington

if TYPE_CHECKING or sys.version_info >= (3, 10, 0):  # pragma: no cover
    from importlib import metadata, resources
else:
    import importlib_metadata as metadata
    import importlib_resources as resources

qasm_path = str(resources.files("mqt.benchviewer") / "static/files/qasm_output/")


def get_supported_benchmarks():
    return [
        "ae",
        "dj",
        "grover-noancilla",
        "grover-v-chain",
        "ghz",
        "graphstate",
        "portfolioqaoa",
        "portfoliovqe",
        "qaoa",
        "qft",
        "qftentangled",
        "qgan",
        "qpeexact",
        "qpeinexact",
        "qwalk-noancilla",
        "qwalk-v-chain",
        "realamprandom",
        "su2random",
        "twolocalrandom",
        "vqe",
        "wstate",
        "shor",
        "hhl",
        "pricingcall",
        "pricingput",
        "groundstate",
        "routing",
        "tsp",
    ]


def get_supported_levels():
    return ["alg", "indep", "nativegates", "mapped", 0, 1, 2, 3]


def get_supported_compilers():
    return ["qiskit", "tket"]


def get_supported_gatesets():
    return ["ibm", "rigetti", "ionq", "oqc"]


def get_supported_devices():
    return ["ibm_washington", "ibm_montreal", "rigetti_aspen_m2", "ionq11", "oqc_lucy"]


def set_qasm_output_path(new_path: str | None = None):
    if new_path is None:
        new_path = str(resources.files("mqt.benchviewer") / "static/files/qasm_output/")

    global qasm_path
    qasm_path = new_path


def get_qasm_output_path():
    """Returns the path where all .qasm files are stored."""
    return qasm_path


def get_zip_file_path():
    """Returns the path where the zip file is stored."""
    return str(resources.files("mqt.benchviewer") / "static/files/MQTBench_all.zip")


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

    def __eq__(self, other):
        return isinstance(other, BernoulliQ) and self._theta_p == other._theta_p

    def power(self, power: float, _matrix_power: bool = True):
        # implement the efficient power of Q
        q_k = QuantumCircuit(1)
        q_k.ry(2 * power * self._theta_p, 0)
        return q_k


def get_estimation_problem():
    """Returns a estimation problem instance for a fixed p value."""

    p = 0.2

    a = BernoulliA(p)
    q = BernoulliQ(p)

    return EstimationProblem(
        state_preparation=a,  # A operator
        grover_operator=q,  # Q operator
        objective_qubits=[0],  # the "good" state Psi1 is identified as measuring |1> in qubit 0
    )


def get_rigetti_aspen_m2_map():
    """Returns a coupling map of Rigetti Aspen M2 chip."""
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
    return [
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

    qasm_output_folder = target_directory if target_directory else get_qasm_output_path()

    file = Path(qasm_output_folder, filename + ".qasm")

    try:
        mqtbench_module_version = metadata.version("mqt.bench")
    except Exception:
        print("'mqt.bench' is most likely not installed. Please run 'pip install . or pip install mqt.bench'.")
        return False

    with file.open("w") as f:
        f.write("// Benchmark was created by MQT Bench on " + str(date.today()) + "\n")
        f.write("// For more information about MQT Bench, please visit https://www.cda.cit.tum.de/mqtbench/\n")
        f.write("// MQT Bench version: " + mqtbench_module_version + "\n")
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

    if gate_set == ["rz", "sx", "x", "ecr", "measure"]:
        postprocess_single_oqc_file(str(file))
    return True


def get_cmap_oqc_lucy():
    """Returns the coupling map of the OQC Lucy quantum computer."""
    # source: https://github.com/aws/amazon-braket-examples/blob/main/examples/braket_features/Verbatim_Compilation.ipynb

    # Connections are NOT bidirectional, this is not an accident
    return [[0, 1], [0, 7], [1, 2], [2, 3], [7, 6], [6, 5], [4, 3], [4, 5]]


def get_cmap_from_devicename(device: str):
    if device == "ibm_washington":
        return FakeWashington().configuration().coupling_map
    if device == "ibm_montreal":
        return FakeMontreal().configuration().coupling_map
    if device == "rigetti_aspen_m2":
        return get_rigetti_aspen_m2_map()
    if device == "oqc_lucy":
        return get_cmap_oqc_lucy()
    if device == "ionq11":
        return get_ionq11_c_map()
    return False


def get_molecule(benchmark_instance_name: str):
    """Returns a Molecule object depending on the parameter value."""
    m_1 = ["H 0.0 0.0 0.0", "H 0.0 0.0 0.735"]
    m_2 = ["Li 0.0 0.0 0.0", "H 0.0 0.0 2.5"]
    m_3 = ["O 0.0 0.0 0.0", "H 0.586, 0.757, 0.0", "H 0.586, -0.757, 0.0"]
    instances = {"small": m_1, "medium": m_2, "large": m_3}

    return instances[benchmark_instance_name]


def postprocess_single_oqc_file(filename: str):
    with Path(filename).open() as f:
        lines = f.readlines()
    with Path(filename).open("w") as f:
        for line in lines:
            if not ("gate rzx" in line.strip("\n") or "gate ecr" in line.strip("\n")):
                f.write(line)
            if 'include "qelib1.inc"' in line.strip("\n"):
                f.write("opaque ecr q0,q1;\n")


def create_zip_file():
    return subprocess.call(f"zip -rj {get_zip_file_path()} {get_qasm_output_path()}", shell=True)
