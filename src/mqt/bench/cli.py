import argparse

from mqt.bench import QiskitSettings, TKETSettings, get_benchmark, CompilerSettings
from pytket import Circuit
from pytket.qasm import circuit_to_qasm_str
from qiskit import QuantumCircuit
from qiskit.qasm2 import dumps as qiskit_circuit_to_str


def main() -> None:
    """
    Invoke :func:`get_benchmark` exactly once with the specified arguments.

    The resulting QASM string is printed to the standard output stream;
    no other output is generated.
    """

    parser = argparse.ArgumentParser(description="Generate a single benchmark")
    parser.add_argument("--level", type=str,
                        help='Level to generate benchmarks for ("alg", "indep", "nativegates" or "mapped")',
                        required=True)
    parser.add_argument("--algorithm", type=str, help="Name of the benchmark", required=True)
    parser.add_argument("--num-qubits", type=int, help="Number of Qubits")
    parser.add_argument("--compiler", type=str, help="Name of the compiler")
    parser.add_argument("--qiskit-optimization-level", type=int, help="Qiskit compiler optimization level")
    parser.add_argument("--tket-placement", type=str, help="TKET placement")
    parser.add_argument("--native-gate-set", type=str, help="Name of the provider")
    parser.add_argument("--device", type=str, help="Name of the device")
    args = parser.parse_args()

    qiskit_settings: QiskitSettings | None = None
    if args.qiskit_optimization_level is not None:
        qiskit_settings = QiskitSettings(args.qiskit_optimization_level)

    tket_settings: TKETSettings | None = None
    if args.tket_placement is not None:
        tket_settings = TKETSettings(args.tket_placement)

    # Note: Assertions about argument validity are in get_benchmark()

    result = get_benchmark(
        benchmark_name=args.algorithm,
        level=args.level,
        circuit_size=args.num_qubits,
        compiler=args.compiler,
        compiler_settings=CompilerSettings(
            qiskit=qiskit_settings,
            tket=tket_settings,
        ),
        provider_name=args.native_gate_set,
        device_name=args.device,
    )

    if isinstance(result, QuantumCircuit):
        qasm_str = qiskit_circuit_to_str(result)
    elif isinstance(result, Circuit):
        qasm_str = circuit_to_qasm_str(result)
    else:
        raise TypeError(f"Got unknown circuit type from get_benchmark: {type(result)}")

    print(qasm_str)
