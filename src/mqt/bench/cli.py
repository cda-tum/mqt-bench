"""Command-line interface for generating benchmarks."""

from __future__ import annotations

import argparse
import sys
from importlib import metadata
from pathlib import Path

from qiskit.qasm2 import dumps as qasm2_dumps
from qiskit.qasm3 import dumps as qasm3_dumps

from . import CompilerSettings, QiskitSettings, get_benchmark
from .output import OutputFormat, generate_header, save_circuit


class CustomArgumentParser(argparse.ArgumentParser):
    """Custom argument parser that includes version information in the help message."""

    def format_help(self) -> str:
        """Include version information in the help message."""
        help_message = super().format_help()
        version_info = (
            f"\nMQT Bench version: {metadata.version('mqt.bench')}\nQiskit version: {metadata.version('qiskit')}\n"
        )
        return help_message + version_info


def parse_benchmark_name_and_instance(algorithm: str) -> tuple[str, str | None]:
    """Parse an algorithm name like "shor_xlarge" into a benchmark and instance name."""
    if algorithm.startswith("shor_"):
        parts = algorithm.split("_", 1)
        return parts[0], parts[1]
    return algorithm, None


def main() -> None:
    """Generate a single benchmark and output in specified format."""
    parser = CustomArgumentParser(description="Generate a single benchmark")
    parser.add_argument(
        "--level",
        type=str,
        choices=["alg", "indep", "nativegates", "mapped"],
        help='Level to generate benchmarks for ("alg", "indep", "nativegates" or "mapped").',
        required=True,
    )
    parser.add_argument(
        "--algorithm",
        type=str,
        help="Name of the benchmark (e.g., 'grover-v-chain', 'shor_xsmall').",
        required=True,
    )
    parser.add_argument(
        "--num-qubits",
        type=int,
        help="Number of qubits for the benchmark.",
        required=True,
    )
    parser.add_argument(
        "--qiskit-optimization-level",
        type=int,
        help="Qiskit compiler optimization level (0-3).",
    )
    parser.add_argument(
        "--native-gate-set",
        type=str,
        help="Provider name for native gate set (e.g., 'ibm', 'rigetti').",
    )
    parser.add_argument(
        "--device",
        type=str,
        help="Device name for mapping stage (e.g., 'ibm_washington').",
    )
    parser.add_argument(
        "--output-format",
        type=str,
        choices=[fmt.value for fmt in OutputFormat],
        default=OutputFormat.QASM2.value,
        help="Output format: 'qasm2', 'qasm3', or 'qpy'.",
    )
    parser.add_argument(
        "--target-directory",
        type=str,
        default=".",
        help="Directory to save the output file (only used for 'qpy' or if --save is specified).",
    )
    parser.add_argument(
        "--target-filename",
        type=str,
        default="",
        help="Base filename (without extension) for saved output.",
    )
    parser.add_argument(
        "--save",
        action="store_true",
        help="If set, save the output to a file instead of printing to stdout (required for 'qpy').",
    )

    args = parser.parse_args()

    # Build Qiskit settings
    qiskit_settings = QiskitSettings()
    if args.qiskit_optimization_level is not None:
        qiskit_settings = QiskitSettings(args.qiskit_optimization_level)

    # Parse algorithm and optional instance
    benchmark_name, benchmark_instance = parse_benchmark_name_and_instance(args.algorithm)

    # Generate circuit
    circuit = get_benchmark(
        benchmark_name=benchmark_name,
        benchmark_instance_name=benchmark_instance,
        level=args.level,
        circuit_size=args.num_qubits,
        compiler_settings=CompilerSettings(qiskit=qiskit_settings),
        provider_name=args.native_gate_set or "ibm",
        device_name=args.device or "ibm_washington",
    )

    try:
        fmt = OutputFormat(args.output_format)
    except ValueError:
        msg = f"Unknown output format: {args.output_format}"
        raise ValueError(msg) from None

    # For QASM outputs, serialize and print
    if fmt in (OutputFormat.QASM2, OutputFormat.QASM3) and not args.save:
        header = generate_header(fmt)
        serial = qasm2_dumps(circuit) if fmt == OutputFormat.QASM2 else qasm3_dumps(circuit)
        sys.stdout.write(header)
        sys.stdout.write(serial)
        return

    # Otherwise, save to file
    filename = args.target_filename or f"{benchmark_name}_{args.level}_{args.num_qubits}_{fmt.value}"
    success = save_circuit(
        qc=circuit,
        filename=filename,
        output_format=str(fmt.value),
        target_directory=args.target_directory,
    )
    if not success:
        sys.exit(1)
    # Optionally, inform user of file location if saving
    if args.save or fmt == OutputFormat.QPY:
        ext = "qasm" if fmt in (OutputFormat.QASM2, OutputFormat.QASM3) else fmt.value
        path = Path(args.target_directory) / f"{filename}.{ext}"
        print(path)


if __name__ == "__main__":
    main()
