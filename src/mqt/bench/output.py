"""Output functions for the MQT Bench module."""

from __future__ import annotations

from datetime import date
from enum import Enum
from importlib import metadata
from pathlib import Path

from qiskit import QuantumCircuit
from qiskit import __version__ as __qiskit_version__
from qiskit.qasm2 import dumps as dumps2
from qiskit.qasm3 import dumps as dumps3
from qiskit.qpy import dump as dump_qpy


class OutputFormat(str, Enum):
    """Enumeration of supported output formats for circuit export."""

    QASM2 = "qasm2"
    QASM3 = "qasm3"
    QPY = "qpy"


class MQTBenchExporterError(Exception):
    """Custom exception for errors arising during MQT Bench exporting operations."""


def generate_header(
    fmt: OutputFormat,
    gate_set: list[str] | None = None,
    mapped: bool = False,
    c_map: list[list[int]] | None = None,
) -> str:
    """Generate a standardized header for MQT Bench outputs.

    Arguments:
        fmt: The chosen output format enum member.
        gate_set: Optional list of gate names used in the circuit.
        mapped: Whether the circuit was mapped to hardware.
        c_map: Optional coupling map of the hardware layout.

    Returns:
        A string containing the formatted header.
    """
    try:
        version = metadata.version("mqt.bench")
    except Exception:
        msg = "Could not retrieve 'mqt.bench' version. Is the package installed?"
        raise MQTBenchExporterError(msg) from None

    lines: list[str] = []
    lines.extend((
        f"// Benchmark created by MQT Bench on {date.today()}",
        "// For more info: https://www.cda.cit.tum.de/mqtbench/",
        f"// MQT Bench version: {version}",
        f"// Qiskit version: {__qiskit_version__}",
        f"// Output format: {fmt.value}",
    ))

    if gate_set:
        lines.append(f"// Used gate set: {gate_set}")
    if mapped:
        lines.append(f"// Coupling map: {c_map or []}")

    return "\n".join(lines) + "\n\n"


def write_circuit(
    qc: QuantumCircuit,
    file_path: Path,
    fmt: OutputFormat = OutputFormat.QASM2,
    gate_set: list[str] | None = None,
    mapped: bool = False,
    c_map: list[list[int]] | None = None,
) -> None:
    """Write the given quantum circuit to disk in the specified format, preceded by an MQT Bench header.

    Args:
        qc: The QuantumCircuit to export.
        file_path: Destination file path (including extension).
        fmt: Desired output format.
        gate_set: Optional gate set list.
        mapped: Whether the circuit is hardware-mapped.
        c_map: Optional coupling map.

    Raises:
        MQTBenchExporterError: On unsupported format or I/O errors.
    """
    header = generate_header(fmt, gate_set, mapped, c_map)

    # Choose write mode and serialization
    if fmt in (OutputFormat.QASM2, OutputFormat.QASM3):
        serial = dumps2(qc) if fmt == OutputFormat.QASM2 else dumps3(qc)
        try:
            with Path.open(file_path, "w", encoding="utf-8") as f:
                f.write(header)
                f.write(serial)
        except Exception as e:
            msg = f"Failed to write QASM file: {e}"
            raise MQTBenchExporterError(msg) from None

    elif fmt == OutputFormat.QPY:
        try:
            with Path.open(file_path, "wb") as f:
                f.write(header.encode("utf-8"))
                dump_qpy(qc, f)
        except Exception as e:
            msg = f"Failed to write QPY file: {e}"
            raise MQTBenchExporterError(msg) from None

    else:
        msg = f"Unsupported output format: {fmt}"
        raise MQTBenchExporterError(msg) from None


def save_circuit(
    qc: QuantumCircuit,
    filename: str,
    output_format: str = OutputFormat.QASM2.value,
    gate_set: list[str] | None = None,
    mapped: bool = False,
    c_map: list[list[int]] | None = None,
    target_directory: str = "",
) -> bool:
    """Public API to save a quantum circuit in various formats with MQT Bench header.

    Args:
        qc: Circuit to export.
        filename: Base filename without extension.
        output_format: One of the supported format values ('qasm2', 'qasm3', 'qpy').
        gate_set: Optional list of gate names.
        mapped: Hardware mapping flag.
        c_map: Optional coupling map.
        target_directory: Directory to place the output file.

    Returns:
        True on success, False otherwise.
    """
    try:
        fmt = OutputFormat(output_format)
    except ValueError:
        msg = f"Unknown output format: {output_format}"
        raise ValueError(msg) from None

    file_ext = "qasm" if fmt.value in (OutputFormat.QASM2.value, OutputFormat.QASM3.value) else fmt.value
    path = Path(target_directory) / f"{filename}.{file_ext}"
    try:
        write_circuit(qc, path, fmt, gate_set, mapped, c_map)
    except MQTBenchExporterError as e:
        print(e)
        return False

    return True
