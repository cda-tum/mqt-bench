"""Test the Clifford+T gateset."""

from __future__ import annotations

import pytest

from mqt.bench import get_benchmark
from mqt.bench.devices import get_native_gateset_by_name


def test_clifford_t() -> None:
    """Test the Clifford+T gateset."""
    qc = get_benchmark(
        benchmark_name="ghz",
        level="nativegates",
        circuit_size=3,
        compiler="qiskit",
        gateset="clifford+t",
    )

    for gate_type in qc.count_ops():
        assert gate_type in get_native_gateset_by_name("clifford+t").gates or gate_type in {"measure", "barrier"}

    with pytest.raises(
        ValueError, match=r"The gateset 'clifford\+t' is not supported by TKET. Please use Qiskit instead."
    ):
        get_benchmark(
            benchmark_name="ghz",
            level="nativegates",
            circuit_size=3,
            compiler="tket",
            gateset="clifford+t",
        )
