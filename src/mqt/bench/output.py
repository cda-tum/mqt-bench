"""Utility functions for the MQT Bench module."""

from __future__ import annotations

from datetime import date
from importlib import metadata
from pathlib import Path

from qiskit import QuantumCircuit
from qiskit import __version__ as __qiskit_version__
from qiskit.qasm2 import dumps as dumps2
from qiskit.qasm3 import dumps as dumps3


def save_as_qasm(
    qc: QuantumCircuit,
    filename: str,
    output_format: str = "qasm2",
    gate_set: list[str] | None = None,
    mapped: bool = False,
    c_map: list[list[int]] | None = None,
    target_directory: str = "",
) -> bool:
    """Saves a quantum circuit as a qasm file.

    Arguments:
        qc: Quantum circuit to be stored as a string
        filename: filename
        output_format: qasm format (qasm2 or qasm3)
        gate_set: set of used gates
        mapped: boolean indicating whether the quantum circuit is mapped to a specific hardware layout
        c_map: coupling map of used hardware layout
        target_directory: directory where the qasm file is stored
    """
    if c_map is None:
        c_map = []

    file = Path(target_directory, filename + ".qasm")

    if output_format == "qasm2":
        qc_str = dumps2(qc)
    elif output_format == "qasm3":
        qc_str = dumps3(qc)
    else:
        msg = f"Unknown qasm format: {output_format}"
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
