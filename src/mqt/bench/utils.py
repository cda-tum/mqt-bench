from __future__ import annotations

import subprocess
import sys
from datetime import date
from pathlib import Path
from typing import TYPE_CHECKING, cast

if TYPE_CHECKING:  # pragma: no cover
    from types import ModuleType

from importlib import import_module

import networkx as nx
import numpy as np
from pytket import __version__ as __tket_version__
from qiskit import QuantumCircuit, __qiskit_version__
from qiskit.providers.fake_provider import FakeMontreal, FakeWashington
from qiskit_optimization.applications import Maxcut

if TYPE_CHECKING or sys.version_info >= (3, 10, 0):  # pragma: no cover
    from importlib import metadata, resources
else:
    import importlib_metadata as metadata
    import importlib_resources as resources

if TYPE_CHECKING:  # pragma: no cover
    from qiskit.circuit import QuantumRegister, Qubit
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


def get_supported_gatesets() -> list[str]:
    return ["ibm", "rigetti", "ionq", "oqc", "quantinuum"]


def get_default_qasm_output_path() -> str:
    """Returns the path where all .qasm files are stored."""
    return str(resources.files("mqt.benchviewer") / "static" / "files" / "qasm_output")


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


def get_rigetti_aspen_m2_map() -> list[list[int]]:
    """Returns a coupling map of Rigetti Aspen M2 chip."""
    c_map_rigetti = []
    for j in range(5):
        for i in range(7):
            c_map_rigetti.append([i + j * 8, i + 1 + j * 8])

            if i == 6:
                c_map_rigetti.append([0 + j * 8, 7 + j * 8])

        if j != 0:
            c_map_rigetti.append([j * 8 - 6, j * 8 + 5])
            c_map_rigetti.append([j * 8 - 7, j * 8 + 6])

    for j in range(5):
        m = 8 * j + 5 * 8
        for i in range(7):
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
    return c_map_rigetti + inverted


def get_fully_connected_cmap(num_qubits: int) -> list[list[int]]:
    return [[i, j] for i in range(num_qubits) for j in range(num_qubits) if i != j]


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

    if gate_set == ["rz", "sx", "x", "ecr", "measure"]:
        postprocess_single_oqc_file(str(file))
    return True


def get_cmap_oqc_lucy() -> list[list[int]]:
    """Returns the coupling map of the OQC Lucy quantum computer."""
    # source: https://github.com/aws/amazon-braket-examples/blob/main/examples/braket_features/Verbatim_Compilation.ipynb

    # Connections are NOT bidirectional, this is not an accident
    return [[0, 1], [0, 7], [1, 2], [2, 3], [7, 6], [6, 5], [4, 3], [4, 5]]


def get_cmap_from_devicename(device: str) -> list[list[int]]:
    c_map_functions = {
        "ibm_washington": FakeWashington,
        "ibm_montreal": FakeMontreal,
        "rigetti_aspen_m2": get_rigetti_aspen_m2_map,
        "oqc_lucy": get_cmap_oqc_lucy,
        "ionq_harmony": get_fully_connected_cmap,
        "ionq_aria1": get_fully_connected_cmap,
        "quantinuum_h2": get_fully_connected_cmap,
    }

    if device in c_map_functions:
        if device in ("ibm_washington", "ibm_montreal"):
            cmap = c_map_functions[device]().configuration().coupling_map
        elif device == "ionq_harmony":
            cmap = c_map_functions[device](11)
        elif device == "ionq_aria1":
            cmap = c_map_functions[device](25)
        elif device == "quantinuum_h2":
            cmap = c_map_functions[device](32)
        else:
            cmap = c_map_functions[device]()
        return cast(list[list[int]], cmap)
    error_msg = f"Device {device} is not supported."
    raise ValueError(error_msg)


def postprocess_single_oqc_file(filename: str) -> None:
    with Path(filename).open() as f:
        lines = f.readlines()
    with Path(filename).open("w") as f:
        for line in lines:
            if not ("gate rzx" in line.strip("\n") or "gate ecr" in line.strip("\n")):
                f.write(line)
            if 'include "qelib1.inc"' in line.strip("\n"):
                f.write("opaque ecr q0,q1;\n")


def create_zip_file() -> int:
    return subprocess.call(f"zip -rj {get_zip_file_path()} {get_default_qasm_output_path()}", shell=True)


def calc_qubit_index(qargs: list[Qubit], qregs: list[QuantumRegister], index: int) -> int:
    offset = 0
    for reg in qregs:
        if qargs[index] not in reg:
            offset += reg.size
        else:
            qubit_index: int = offset + reg.index(qargs[index])
            return qubit_index
    error_msg = f"Global qubit index for local qubit {index} index not found."
    raise ValueError(error_msg)


def calc_supermarq_features(
    qc: QuantumCircuit,
) -> SupermarqFeatures:
    connectivity_collection: list[list[int]] = []
    liveness_A_matrix = 0
    connectivity_collection = [[] for _ in range(qc.num_qubits)]

    for instruction, qargs, _ in qc.data:
        if instruction.name in ("barrier", "measure"):
            continue
        liveness_A_matrix += len(qargs)
        first_qubit = calc_qubit_index(qargs, qc.qregs, 0)
        all_indices = [first_qubit]
        if len(qargs) == 2:
            second_qubit = calc_qubit_index(qargs, qc.qregs, 1)
            all_indices.append(second_qubit)
        for qubit_index in all_indices:
            to_be_added_entries = all_indices.copy()
            to_be_added_entries.remove(int(qubit_index))
            connectivity_collection[int(qubit_index)].extend(to_be_added_entries)

    connectivity: list[int] = [len(set(connectivity_collection[i])) for i in range(qc.num_qubits)]

    count_ops = qc.count_ops()
    num_gates = sum(count_ops.values())
    # before subtracting the measure and barrier gates, check whether it is in the dict
    if "measure" in count_ops:
        num_gates -= count_ops.get("measure")
    if "barrier" in count_ops:
        num_gates -= count_ops.get("barrier")
    num_multiple_qubit_gates = qc.num_nonlocal_gates()
    depth = qc.depth(lambda x: x[0].name not in ("barrier", "measure"))
    program_communication = np.sum(connectivity) / (qc.num_qubits * (qc.num_qubits - 1))

    if num_multiple_qubit_gates == 0:
        critical_depth = 0.0
    else:
        critical_depth = (
            qc.depth(filter_function=lambda x: len(x[1]) > 1 and x[0].name != "barrier") / num_multiple_qubit_gates
        )

    entanglement_ratio = num_multiple_qubit_gates / num_gates
    assert num_multiple_qubit_gates <= num_gates

    parallelism = (num_gates / depth - 1) / (qc.num_qubits - 1)

    liveness = liveness_A_matrix / (depth * qc.num_qubits)

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


def get_compilation_paths() -> list[tuple[str, list[tuple[str, int]]]]:
    return [
        ("ibm", [("ibm_washington", 127), ("ibm_montreal", 27)]),
        ("rigetti", [("rigetti_aspen_m2", 80)]),
        ("ionq", [("ionq_harmony", 11), ("ionq_aria1", 25)]),
        ("oqc", [("oqc_lucy", 8)]),
        ("quantinuum", [("quantinuum_h2", 32)]),
    ]


def get_supported_devices() -> list[str]:
    return [
        "ibm_washington",
        "ibm_montreal",
        "rigetti_aspen_m2",
        "ionq_harmony",
        "ionq_aria1",
        "oqc_lucy",
        "quantinuum_h2",
    ]


def convert_cmap_to_tuple_list(c_map: list[list[int]]) -> list[tuple[int, int]]:
    return [(c[0], c[1]) for c in c_map]
