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
from qiskit.circuit import Gate, Parameter
from qiskit.circuit.library import CZGate, HGate, RXGate, RYGate, RZGate
from qiskit.quantum_info import Operator
from qiskit.transpiler import Target

from mqt.bench import BenchmarkLevel, get_benchmark
from mqt.bench.targets.devices import (
    get_device,
)
from mqt.bench.targets.devices.rigetti import CEPHEUS_PHYSICAL_QUBITS
from mqt.bench.targets.gatesets import (
    get_gateset,
    get_target_for_gateset,
)
from mqt.bench.targets.gatesets._compilation import prepare_target  # ruff:ignore[import-private-name]
from mqt.bench.targets.gatesets.ionq import GPI2Gate, GPIGate


@pytest.mark.parametrize("gateset", ["ionq_forte", "rigetti"])
@pytest.mark.parametrize("opt_level", [0, 2, 3])
@pytest.mark.parametrize("symbolic", [False, True])
def test_native_compilation_semantics(gateset: str, opt_level: int, *, symbolic: bool) -> None:
    """Each hardware family preserves the complete matrix and target constraints."""
    theta = Parameter("theta")
    circuit = QuantumCircuit(2)
    circuit.rx(theta if symbolic else 0.31, 0)
    circuit.h(1)
    circuit.u(0.43, -0.25, theta if symbolic else 0.16, 1)
    circuit.cx(0, 1)
    circuit.rz(-0.7, 0)
    target = get_target_for_gateset(gateset, 2)
    result = get_benchmark(
        circuit, BenchmarkLevel.NATIVEGATES, target=target, opt_level=opt_level, random_parameters=False
    )
    for instruction in result.data:
        assert target.instruction_supported(
            instruction.operation.name,
            qargs=tuple(result.find_bit(q).index for q in instruction.qubits),
            parameters=instruction.operation.params,
        )
    if symbolic:
        circuit = circuit.assign_parameters({theta: 0.37})
        result = result.assign_parameters({theta: 0.37})
    np.testing.assert_allclose(Operator.from_circuit(result).data, Operator(circuit).data, atol=1e-12)


@pytest.mark.parametrize(("gate_type", "angle", "phase"), [(GPIGate, pi, pi / 2), (GPI2Gate, pi / 2, 0)])
def test_ionq_radian_definition(gate_type: type[GPIGate | GPI2Gate], angle: float, phase: float) -> None:
    """Gate phases use radians and retain the GPI gate's global phase."""
    phi = Parameter("phi")
    circuit = QuantumCircuit(1)
    circuit.append(gate_type(phi), [0])
    reference = QuantumCircuit(1, global_phase=phase)
    reference.r(angle, 0.37, 0)
    np.testing.assert_allclose(
        Operator(circuit.assign_parameters({phi: 0.37})).data, Operator(reference).data, atol=1e-12
    )


def test_rigetti_fixed_rx_aliases() -> None:
    """All four fixed gates are standard RX capabilities with distinct names."""
    for target in (get_target_for_gateset("rigetti", 2), get_device("rigetti_cepheus_107")):
        for name, angle in (("rxpi", pi), ("rxpidg", -pi), ("rxpi2", pi / 2), ("rxpi2dg", -pi / 2)):
            operation = target.operation_from_name(name)
            assert isinstance(operation, RXGate)
            assert operation.params == [angle]
            assert target.instruction_supported(name, (0,), parameters=[angle])
            assert not target.instruction_supported(name, (0,), parameters=[0.123])


def test_cepheus_physical_labels() -> None:
    """Dense wires preserve the provider's sparse labels and grid edges."""
    target = get_device("rigetti_cepheus_107")
    assert len(CEPHEUS_PHYSICAL_QUBITS) == target.num_qubits == 107
    assert set(CEPHEUS_PHYSICAL_QUBITS) == set(range(108)) - {8}
    edges = {(CEPHEUS_PHYSICAL_QUBITS[i], CEPHEUS_PHYSICAL_QUBITS[j]) for i, j in target["cz"]}
    assert len(edges) == 386
    assert (0, 9) in edges
    assert (98, 107) in edges
    assert (7, 9) not in edges
    assert (17, 18) not in edges


def test_forte_virtual_z() -> None:
    """Forte supports arbitrary virtual Z rotations in the compiler model."""
    target = get_device("ionq_forte_36")
    assert target.instruction_supported("rz", (0,), parameters=[0.123])
    assert target["rz"][0,].duration == 0
    assert target["rz"][0,].error == 0
    assert "rz" in get_gateset("ionq_forte")


@pytest.mark.parametrize("gateset", ["rigetti", "ionq_forte"])
@pytest.mark.parametrize("angle", [pi / 2, -pi / 2, pi, -pi])
def test_fixed_rotation_uses_one_native_gate(gateset: str, angle: float) -> None:
    """Quarter and half turns need only one native gate besides virtual Z."""
    circuit = QuantumCircuit(2)
    circuit.rx(angle, 0)
    target = get_target_for_gateset(gateset, 2)
    result = get_benchmark(circuit, BenchmarkLevel.NATIVEGATES, target=target)
    assert sum(count for name, count in result.count_ops().items() if name != "rz") == 1
    np.testing.assert_allclose(Operator(result).data, Operator(circuit).data, atol=1e-12)


@pytest.mark.parametrize("gateset", ["rigetti", "ionq_forte"])
@pytest.mark.parametrize("level", [BenchmarkLevel.NATIVEGATES, BenchmarkLevel.MAPPED])
def test_native_output_can_be_controlled_and_recompiled(gateset: str, level: BenchmarkLevel) -> None:
    """Native definitions stay reusable outside their original target."""
    from qiskit import transpile  # ruff:ignore[import-outside-top-level]

    theta = Parameter("theta")
    circuit = QuantumCircuit(2)
    circuit.rx(theta, 0)
    circuit.h(1)
    circuit.cx(0, 1)
    target = get_target_for_gateset(gateset, 2)
    target.description = "custom target"
    result = get_benchmark(circuit, level, target=target, random_parameters=False)
    for value in [-0.37, 0.29]:
        bound = result.assign_parameters({theta: value})
        expected = Operator(bound).data
        recompiled = transpile(bound, basis_gates=["rz", "sx", "x", "cx"])
        np.testing.assert_allclose(Operator.from_circuit(recompiled).data, expected, atol=1e-12)
        np.testing.assert_allclose(
            Operator(bound.to_gate().control()).data,
            Operator(Operator(bound).to_instruction().control()).data,
            atol=1e-12,
        )


@pytest.mark.parametrize(
    ("name", "operation"),
    [
        ("rxpi2", RXGate(0.37)),
        ("rxpi2", RYGate(pi / 2)),
        ("gpi2", HGate()),
        ("gpi2", GPI2Gate(0.37)),
    ],
)
def test_native_gate_names_do_not_override_capabilities(name: str, operation: Gate) -> None:
    """A familiar alias must not change the declared gate or allowed angles."""
    target = Target(num_qubits=2)
    target.add_instruction(RZGate(Parameter("theta")))
    target.add_instruction(CZGate())
    target.add_instruction(operation, name=name)
    prepared, lowering = prepare_target(target, native=True)
    assert prepared.operation_from_name(name) == operation
    assert lowering is None
