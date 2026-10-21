# Copyright (c) 2023 - 2026 Chair for Design Automation, TUM
# Copyright (c) 2025 - 2026 Munich Quantum Software Company GmbH
# All rights reserved.
#
# SPDX-License-Identifier: MIT
#
# Licensed under the MIT License

"""Test AQT target capabilities and compilation."""

from mqt.bench import get_benchmark
from mqt.bench.benchmark_generation import BenchmarkLevel
from mqt.bench.targets.devices import get_device
from mqt.bench.targets.gatesets import get_target_for_gateset


def test_aqt_target() -> None:
    """IBEX exposes all ordered RXX pairs and virtual RZ gates."""
    target = get_device("aqt_ibex_12")
    assert target.num_qubits == 12
    assert set(target.operation_names) == {"r", "rz", "rxx", "measure"}
    assert len(target["rxx"]) == 12 * 11
    assert all(props.duration == 0 and props.error == 0 for props in target["rz"].values())
    for level, model in [
        (BenchmarkLevel.NATIVEGATES, get_target_for_gateset("aqt", 3)),
        (BenchmarkLevel.MAPPED, target),
    ]:
        circuit = get_benchmark("ghz", level, 3, target=model)
        assert set(circuit.count_ops()) <= set(model.operation_names) | {"barrier"}
