"""Command-line interface for generating benchmarks."""

from __future__ import annotations

import argparse
from importlib import metadata
from typing import cast

from qiskit.qasm2 import dumps as qiskit_circuit_to_str

from . import CompilerSettings, QiskitSettings, get_benchmark


class CustomArgumentParser(argparse.ArgumentParser):
    """Custom argument parser that includes version information in the help message."""

    def format_help(self) -> str:
        """Include version information in the help message."""
        help_message = super().format_help()
        version_info = (
            f"\nMQT Bench version: {metadata.version('mqt.bench')}\nQiskit version: {metadata.version('qiskit')}\n"
        )
        return help_message + version_info


def main() -> None:
    """Invoke :func:`get_benchmark` exactly once with the specified arguments.

    The resulting QASM string is printed to the standard output stream;
    no other output is generated.
    """
    parser = CustomArgumentParser(description="Generate a single benchmark")
    parser.add_argument(
        "--level",
        type=str,
        help='Level to generate benchmarks for ("alg", "indep", "nativegates" or "mapped")',
        required=True,
    )
    parser.add_argument("--algorithm", type=str, help="Name of the benchmark", required=True)
    parser.add_argument("--num-qubits", type=int, help="Number of Qubits", required=True)
    parser.add_argument("--qiskit-optimization-level", type=int, help="Qiskit compiler optimization level")
    parser.add_argument("--native-gate-set", type=str, help="Name of the provider")
    parser.add_argument("--device", type=str, help="Name of the device")
    args = parser.parse_args()

    qiskit_settings = QiskitSettings()
    if args.qiskit_optimization_level is not None:
        qiskit_settings = QiskitSettings(args.qiskit_optimization_level)

    # Note: Assertions about argument validity are in get_benchmark()

    # Temporary workaround to "get things working" with benchmark instances.
    # This special treatment should be removed as soon as instance handling has been refactored in get_benchmark().
    benchmark_name, benchmark_instance = parse_benchmark_name_and_instance(args.algorithm)

    result = get_benchmark(
        benchmark_name=benchmark_name,
        benchmark_instance_name=benchmark_instance,
        level=args.level,
        circuit_size=args.num_qubits,
        compiler_settings=CompilerSettings(
            qiskit=qiskit_settings,
        ),
        provider_name=args.native_gate_set,
        device_name=args.device,
    )
    print(qiskit_circuit_to_str(result))
    return


def parse_benchmark_name_and_instance(algorithm: str) -> tuple[str, str | None]:
    """Parse an algorithm name like "shor_xlarge" into a benchmark and instance name as expected by :func:`get_benchmark`."""
    if algorithm.startswith("shor_"):
        as_list = algorithm.split("_", 2)
        assert len(as_list) == 2
        return cast("tuple[str, str]", tuple(as_list))

    return algorithm, None
