# Copyright (c) 2023 - 2026 Chair for Design Automation, TUM
# Copyright (c) 2025 - 2026 Munich Quantum Software Company GmbH
# All rights reserved.
#
# SPDX-License-Identifier: MIT
#
# Licensed under the MIT License

"""Rigetti Cepheus architecture and deployment targets."""

from __future__ import annotations

from math import pi

from qiskit.circuit import Parameter
from qiskit.circuit.library import CZGate, Measure, RXGate, RZGate
from qiskit.transpiler import InstructionProperties, Target

from ._registry import register_device

CEPHEUS_PHYSICAL_QUBITS = (*range(8), *range(9, 108))
"""Provider qubit label for each MQT Bench wire in the 107-qubit snapshot."""


@register_device("rigetti_cepheus_108")
def get_rigetti_cepheus_108() -> Target:
    """Get the full 108-qubit Cepheus architecture with a 12-by-9 grid."""
    return _build_cepheus_target(name="rigetti_cepheus_108", physical_qubits=tuple(range(108)))


@register_device("rigetti_cepheus_107")
def get_rigetti_cepheus_107() -> Target:
    """Get the 2026-10-02 deployment snapshot, which excludes physical qubit 8."""
    return _build_cepheus_target(name="rigetti_cepheus_107", physical_qubits=CEPHEUS_PHYSICAL_QUBITS)


def _build_cepheus_target(*, name: str, physical_qubits: tuple[int, ...]) -> Target:
    """Build a Cepheus target with bidirectional CZ gates and no calibration."""
    num_qubits = len(physical_qubits)
    target = Target(num_qubits=num_qubits, description=name)
    oneq_props = {(q,): InstructionProperties() for q in range(num_qubits)}
    for name, angle in (("rxpi", pi), ("rxpidg", -pi), ("rxpi2", pi / 2), ("rxpi2dg", -pi / 2)):
        target.add_instruction(RXGate(angle), oneq_props, name=name)
    target.add_instruction(RZGate(Parameter("theta")), oneq_props)
    target.add_instruction(Measure(), oneq_props)
    target.add_instruction(
        CZGate(),
        {
            (i, j): InstructionProperties()
            for i, physical_i in enumerate(physical_qubits)
            for j, physical_j in enumerate(physical_qubits)
            if abs(physical_i - physical_j) == 9
            or (abs(physical_i - physical_j) == 1 and physical_i // 9 == physical_j // 9)
        },
    )
    return target
