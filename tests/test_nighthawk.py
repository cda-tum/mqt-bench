# Copyright (c) 2023 - 2026 Chair for Design Automation, TUM
# Copyright (c) 2025 - 2026 Munich Quantum Software Company GmbH
# All rights reserved.
#
# SPDX-License-Identifier: MIT
#
# Licensed under the MIT License

"""Test the Nighthawk grid and mapped compilation."""

from mqt.bench import get_benchmark
from mqt.bench.benchmark_generation import BenchmarkLevel
from mqt.bench.targets.devices import get_device
from mqt.bench.targets.gatesets import get_gateset


def test_nighthawk() -> None:
    """Nighthawk has 218 bidirectional grid edges and a CZ basis."""
    target = get_device("ibm_nighthawk_120")
    assert target.num_qubits == 120
    assert get_gateset("ibm_nighthawk") == get_gateset("ibm_heron")
    edges = set(target["cz"])
    expected = {(q, q + 1) for q in range(120) if q % 10 != 9}
    expected |= {(q, q + 10) for q in range(110)}
    expected |= {(b, a) for a, b in list(expected)}
    assert edges == expected
    circuit = get_benchmark("ghz", BenchmarkLevel.MAPPED, 3, target=target)
    assert circuit.num_qubits == 120
    for item in circuit.data:
        if item.operation.num_qubits == 2:
            assert tuple(circuit.find_bit(q).index for q in item.qubits) in edges
