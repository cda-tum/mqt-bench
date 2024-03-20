from __future__ import annotations

import subprocess
import sys
from datetime import date
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    from types import ModuleType

from importlib import import_module

import networkx as nx
import numpy as np
from pytket import __version__ as __tket_version__
from qiskit import QuantumCircuit
from qiskit import __version__ as __qiskit_version__
from qiskit.converters import circuit_to_dag
from qiskit_optimization.applications import Maxcut

from mqt.bench.devices import OQCProvider

if TYPE_CHECKING or sys.version_info >= (3, 10, 0):  # pragma: no cover
    from importlib import metadata, resources
else:
    import importlib_metadata as metadata
    import importlib_resources as resources

if TYPE_CHECKING:  # pragma: no cover
    from qiskit_optimization import QuadraticProgram

from dataclasses import dataclass


@dataclass
class SupermarqFeatures:
    program_communication: float
    critical_depth: float
    entanglement_ratio: float
    parallelism: float
    liveness: float


qasm_path = str(resources.files("mqt.benchviewer") / "static/files/qasm_output/")


def get_supported_benchmarks() -> list[str]:
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
        "qnn",
        "qpeexact",
        "qpeinexact",
        "qwalk-noancilla",
        "qwalk-v-chain",
        "random",
        "realamprandom",
        "su2random",
        "twolocalrandom",
        "vqe",
        "wstate",
        "shor",
        "pricingcall",
        "pricingput",
        "groundstate",
        "routing",
        "tsp",
    ]


def get_supported_levels() -> list[str | int]:
    return ["alg", "indep", "nativegates", "mapped", 0, 1, 2, 3]


def get_supported_compilers() -> list[str]:
    return ["qiskit", "tket"]


def get_default_config_path() -> str:
    return str(resources.files("mqt.bench") / "config.json")


def get_default_qasm_output_path() -> str:
    """Returns the path where all .qasm files are stored."""
    return str(resources.files("mqt.benchviewer") / "static" / "files" / "qasm_output")


def get_default_evaluation_output_path() -> str:
    """Returns the path where all .qasm files are stored."""
    return str(resources.files("mqt.bench") / "evaluation")


def get_zip_file_path() -> str:
    """Returns the path where the zip file is stored."""
    return str(resources.files("mqt.benchviewer") / "static/files/MQTBench_all.zip")


def get_examplary_max_cut_qp(n_nodes: int, degree: int = 2) -> QuadraticProgram:
    """Returns a quadratic problem formulation of a max cut problem of a random graph.

    Keyword arguments:
    n_nodes -- number of graph nodes (and also number of qubits)
    degree -- edges per node
    """
    graph = nx.random_regular_graph(d=degree, n=n_nodes, seed=111)
    maxcut = Maxcut(graph)
    return maxcut.to_quadratic_program()


def get_openqasm_gates() -> list[str]:
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
    gate_set: list[str] | None = None,
    mapped: bool = False,
    c_map: list[list[int]] | None = None,
    target_directory: str = "",
) -> bool:
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

    file = Path(target_directory, filename + ".qasm")

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

    if gate_set == OQCProvider.get_native_gates():
        postprocess_single_oqc_file(str(file))
    return True


def postprocess_single_oqc_file(filename: str) -> None:
    with Path(filename).open() as f:
        lines = f.readlines()
    with Path(filename).open("w") as f:
        for line in lines:
            if not ("gate rzx" in line.strip("\n") or "gate ecr" in line.strip("\n")):
                f.write(line)
            if 'include "qelib1.inc"' in line.strip("\n"):
                f.write("opaque ecr q0,q1;\n")


def create_zip_file(zip_path: str | None = None, qasm_path: str | None = None) -> int:
    if zip_path is None:
        zip_path = get_zip_file_path()
    if qasm_path is None:
        qasm_path = get_default_qasm_output_path()
    return subprocess.call(f"zip -rj {zip_path} {qasm_path}", shell=True)


def calc_supermarq_features(
    qc: QuantumCircuit,
) -> SupermarqFeatures:
    """Calculates the Supermarq features for a given quantum circuit. Code adapted from https://github.com/Infleqtion/client-superstaq/blob/91d947f8cc1d99f90dca58df5248d9016e4a5345/supermarq-benchmarks/supermarq/converters.py"""
    num_qubits = qc.num_qubits
    dag = circuit_to_dag(qc)
    dag.remove_all_ops_named("barrier")

    # Program communication = circuit's average qubit degree / degree of a complete graph.
    graph = nx.Graph()
    for op in dag.two_qubit_ops():
        q1, q2 = op.qargs
        graph.add_edge(qc.find_bit(q1).index, qc.find_bit(q2).index)
    degree_sum = sum([graph.degree(n) for n in graph.nodes])
    program_communication = degree_sum / (num_qubits * (num_qubits - 1)) if num_qubits > 1 else 0

    # Liveness feature = sum of all entries in the liveness matrix / (num_qubits * depth).
    activity_matrix = np.zeros((num_qubits, dag.depth()))
    for i, layer in enumerate(dag.layers()):
        for op in layer["partition"]:
            for qubit in op:
                activity_matrix[qc.find_bit(qubit).index, i] = 1
    liveness = np.sum(activity_matrix) / (num_qubits * dag.depth()) if dag.depth() > 0 else 0

    #  Parallelism feature = max((((# of gates / depth) -1) /(# of qubits -1)), 0).
    parallelism = (
        max(((len(dag.gate_nodes()) / dag.depth()) - 1) / (num_qubits - 1), 0)
        if num_qubits > 1 and dag.depth() > 0
        else 0
    )

    # Entanglement-ratio = ratio between # of 2-qubit gates and total number of gates in the circuit.
    entanglement_ratio = len(dag.two_qubit_ops()) / len(dag.gate_nodes()) if len(dag.gate_nodes()) > 0 else 0

    # Critical depth = # of 2-qubit gates along the critical path / total # of 2-qubit gates.
    longest_paths = dag.count_ops_longest_path()
    n_ed = sum([longest_paths[name] for name in {op.name for op in dag.two_qubit_ops()} if name in longest_paths])
    n_e = len(dag.two_qubit_ops())
    critical_depth = n_ed / n_e if n_e != 0 else 0

    assert 0 <= program_communication <= 1
    assert 0 <= critical_depth <= 1
    assert 0 <= entanglement_ratio <= 1
    assert 0 <= parallelism <= 1
    assert 0 <= liveness <= 1

    return SupermarqFeatures(
        program_communication,
        critical_depth,
        entanglement_ratio,
        parallelism,
        liveness,
    )


def get_module_for_benchmark(benchmark_name: str) -> ModuleType:
    if benchmark_name in ["portfolioqaoa", "portfoliovqe", "pricingcall", "pricingput"]:
        return import_module("mqt.bench.benchmarks.qiskit_application_finance." + benchmark_name)
    if benchmark_name == "qnn":
        return import_module("mqt.bench.benchmarks.qiskit_application_ml.qnn")
    if benchmark_name == "groundstate":
        return import_module("mqt.bench.benchmarks.qiskit_application_nature.groundstate")
    if benchmark_name == "routing":
        return import_module("mqt.bench.benchmarks.qiskit_application_optimization.routing")
    if benchmark_name == "tsp":
        return import_module("mqt.bench.benchmarks.qiskit_application_optimization.tsp")
    return import_module("mqt.bench.benchmarks." + benchmark_name)


def convert_cmap_to_tuple_list(c_map: list[list[int]]) -> list[tuple[int, int]]:
    return [(c[0], c[1]) for c in c_map]
