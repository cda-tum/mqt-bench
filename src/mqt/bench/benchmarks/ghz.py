# Copyright (c) 2023 - 2025 Chair for Design Automation, TUM
# Copyright (c) 2025 Munich Quantum Software Company GmbH
# All rights reserved.
#
# SPDX-License-Identifier: MIT
#
# Licensed under the MIT License

"""GHZ benchmark definition."""

from __future__ import annotations

from qiskit import QuantumCircuit, QuantumRegister


def create_circuit(num_qubits: int) -> QuantumCircuit:
    """Returns a quantum circuit implementing the GHZ state.

    Arguments:
        num_qubits: number of qubits of the returned quantum circuit
    """
    q = QuantumRegister(num_qubits, "q")
    qc = QuantumCircuit(q, name="ghz")
    qc.h(q[-1])
    for i in range(1, num_qubits):
        qc.cx(q[num_qubits - i], q[num_qubits - i - 1])
    qc.measure_all()

    return qc
