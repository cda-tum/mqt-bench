"""Utility functions for the MQT Bench module."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from importlib import import_module, metadata, resources
from pathlib import Path
from typing import TYPE_CHECKING

import networkx as nx
import numpy as np
from qiskit import QuantumCircuit
from qiskit import __version__ as __qiskit_version__
from qiskit.converters import circuit_to_dag
from qiskit.qasm2 import dumps as dumps2
from qiskit.qasm3 import dumps as dumps3

if TYPE_CHECKING:  # pragma: no cover
    from types import ModuleType


@dataclass
class SupermarqFeatures:
    """Data class for the Supermarq features of a quantum circuit."""

    program_communication: float
    critical_depth: float
    entanglement_ratio: float
    parallelism: float
    liveness: float


def get_supported_benchmarks() -> list[str]:
    """Returns a list of all supported benchmarks."""
    return [
        "ae",
        "bv",
        "dj",
        "grover-noancilla",
        "grover-v-chain",
        "ghz",
        "graphstate",
        "qaoa",
        "qft",
        "qftentangled",
        "qnn",
        "qpeexact",
        "qpeinexact",
        "qwalk-noancilla",
        "qwalk-v-chain",
        "randomcircuit",
        "vqerealamprandom",
        "vqesu2random",
        "vqetwolocalrandom",
        "wstate",
        "shor",
    ]


def get_supported_levels() -> list[str | int]:
    """Returns a list of all supported benchmark levels."""
    return ["alg", "indep", "nativegates", "mapped", 0, 1, 2, 3]


def get_default_qasm_output_path() -> str:
    """Returns the path where all .qasm files are stored."""
    return str(resources.files("mqt.bench") / "viewer" / "static" / "files" / "qasm_output")


def get_default_evaluation_output_path() -> str:
    """Returns the path where all .qasm files are stored."""
    return str(resources.files("mqt.bench") / "evaluation")


def get_zip_folder_path() -> str:
    """Returns the path where the zip file is stored."""
    return str(resources.files("mqt.bench") / "viewer" / "static" / "files")


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
    qc: QuantumCircuit,
    filename: str,
    qasm_format: str = "qasm2",
    gate_set: list[str] | None = None,
    mapped: bool = False,
    c_map: list[list[int]] | None = None,
    target_directory: str = "",
) -> bool:
    """Saves a quantum circuit as a qasm file.

    Arguments:
        qc: Quantum circuit to be stored as a string
        filename: filename
        qasm_format: qasm format (qasm2 or qasm3)
        gate_set: set of used gates
        mapped: boolean indicating whether the quantum circuit is mapped to a specific hardware layout
        c_map: coupling map of used hardware layout
        target_directory: directory where the qasm file is stored
    """
    if c_map is None:
        c_map = []

    file = Path(target_directory, filename + ".qasm")

    if qasm_format == "qasm2":
        qc_str = dumps2(qc)
    elif qasm_format == "qasm3":
        qc_str = dumps3(qc)
    else:
        msg = f"Unknown qasm format: {qasm_format}"
        raise ValueError(msg)

    try:
        mqtbench_module_version = metadata.version("mqt.bench")
    except Exception:
        print("'mqt.bench' is most likely not installed. Please run 'pip install . or pip install mqt.bench'.")
        return False

    with file.open("w") as f:
        f.write("// Benchmark was created by MQT Bench on " + str(date.today()) + "\n")
        f.write("// For more information about MQT Bench, please visit https://www.cda.cit.tum.de/mqtbench/\n")
        f.write("// MQT Bench version: " + mqtbench_module_version + "\n")
        f.write("// Qiskit version: " + str(__qiskit_version__) + "\n")
        if gate_set:
            f.write("// Used Gate Set: " + str(gate_set) + "\n")
        if mapped:
            f.write("// Coupling List: " + str(c_map) + "\n")
        f.write("\n")
        f.write(qc_str)
    f.close()

    return True


def calc_supermarq_features(
    qc: QuantumCircuit,
) -> SupermarqFeatures:
    """Calculates the Supermarq features for a given quantum circuit. Code adapted from https://github.com/Infleqtion/client-superstaq/blob/91d947f8cc1d99f90dca58df5248d9016e4a5345/supermarq-benchmarks/supermarq/converters.py."""
    num_qubits = qc.num_qubits
    dag = circuit_to_dag(qc)
    dag.remove_all_ops_named("barrier")

    # Program communication = circuit's average qubit degree / degree of a complete graph.
    graph = nx.Graph()
    for op in dag.two_qubit_ops():
        q1, q2 = op.qargs
        graph.add_edge(qc.find_bit(q1).index, qc.find_bit(q2).index)
    degree_sum = sum(graph.degree(n) for n in graph.nodes)
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
    n_ed = sum(longest_paths[name] for name in {op.name for op in dag.two_qubit_ops()} if name in longest_paths)
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
    """Returns the module for a specific benchmark."""
    return import_module("mqt.bench.benchmarks." + benchmark_name)
