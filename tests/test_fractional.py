# Copyright (c) 2023 - 2026 Chair for Design Automation, TUM
# Copyright (c) 2025 - 2026 Munich Quantum Software Company GmbH
# All rights reserved.
#
# SPDX-License-Identifier: MIT
#
# Licensed under the MIT License

"""Test targets."""

from __future__ import annotations

from math import pi

import numpy as np
import pytest
from qiskit import QuantumCircuit
from qiskit.circuit import Parameter
from qiskit.circuit.library import RZZGate
from qiskit.quantum_info import Operator
from qiskit.transpiler import Target

from mqt.bench import BenchmarkLevel, get_benchmark
from mqt.bench.targets.devices import (
    get_device,
)
from mqt.bench.targets.gatesets import (
    get_target_for_gateset,
)


@pytest.mark.skipif(not hasattr(Target, "gate_has_angle_bounds"), reason="Fractional targets need Qiskit 2.2")
@pytest.mark.parametrize("level", [BenchmarkLevel.NATIVEGATES, BenchmarkLevel.MAPPED])
@pytest.mark.parametrize("angle", [-100.0, -np.pi, -0.37, 0.37, 2.4, 100.0])
def test_fractional_heron_qiskit(level: BenchmarkLevel, angle: float) -> None:
    """Fractional targets keep native RZZ angles within the hardware interval."""
    target = get_target_for_gateset("ibm_heron_fractional", 2)
    circuit = QuantumCircuit(2)
    circuit.rzz(angle, 0, 1)
    result = get_benchmark(circuit, level, target=target, random_parameters=False)
    assert all(
        target.instruction_supported(item.operation.name, parameters=item.operation.params) for item in result.data
    )
    assert np.allclose(Operator(result).data, Operator(circuit).data)
    assert result.count_ops().get("rzz", 0) <= 1


@pytest.mark.skipif(not hasattr(Target, "gate_has_angle_bounds"), reason="Fractional targets need Qiskit 2.2")
@pytest.mark.parametrize("level", [BenchmarkLevel.NATIVEGATES, BenchmarkLevel.MAPPED])
@pytest.mark.parametrize("gateset", ["ionq_forte", "rigetti"])
@pytest.mark.parametrize("angle", [-0.37, 2.4])
def test_native_aliases_preserve_angle_bounds(level: BenchmarkLevel, gateset: str, angle: float) -> None:
    """Native alias lowering retains bounds on other target gates."""
    target = get_target_for_gateset(gateset, 2)
    # Use a bounded entangler with the gate set's native single-qubit aliases.
    bounded = Target(num_qubits=2)
    for name in target.operation_names:
        operation = target.operation_from_name(name)
        if operation.num_qubits == 1:
            bounded.add_instruction(operation, name=name)
    bounded.add_instruction(RZZGate(Parameter("zz")), angle_bounds=[(0, pi / 2)])
    circuit = QuantumCircuit(2)
    circuit.rzz(angle, 0, 1)
    result = get_benchmark(circuit, level, target=bounded, random_parameters=False)
    assert all(
        bounded.instruction_supported(item.operation.name, parameters=item.operation.params) for item in result.data
    )
    assert all(
        bounded.supported_angle_bound("rzz", item.operation.params)
        for item in result.data
        if item.operation.name == "rzz"
    )
    np.testing.assert_allclose(Operator.from_circuit(result).data, Operator(circuit).data, atol=1e-12)


@pytest.mark.skipif(not hasattr(Target, "gate_has_angle_bounds"), reason="Fractional targets need Qiskit 2.2")
def test_fractional_heron_device() -> None:
    """Fractional gates share the Heron sites and couplings."""
    target = get_device("ibm_heron_156_fractional")
    assert target.num_qubits == 156
    assert target.qargs_for_operation_name("rx") == target.qargs_for_operation_name("sx")
    assert target.qargs_for_operation_name("rzz") == target.qargs_for_operation_name("cz")
    assert target.instruction_supported("rzz", (0, 1), parameters=[np.pi / 2])
    assert not target.instruction_supported("rzz", (0, 1), parameters=[-0.37])
