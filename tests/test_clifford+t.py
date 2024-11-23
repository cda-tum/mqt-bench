from mqt.bench import get_benchmark
from mqt.bench.devices import get_native_gateset_by_name

def test_cliffordT() -> None:
    qc = get_benchmark(
        benchmark_name="ghz",
        level="nativegates",
        circuit_size=3,
        compiler="qiskit",
        gateset="clifford+t",
    )

    for gate_type in qc.count_ops().keys():
        assert gate_type in get_native_gateset_by_name("clifford+t").gates or gate_type in {"measure", "barrier"}