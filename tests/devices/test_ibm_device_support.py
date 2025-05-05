# Copyright (c) 2023 - 2025 Chair for Design Automation, TUM
# Copyright (c) 2025 Munich Quantum Software Company GmbH
# All rights reserved.
#
# SPDX-License-Identifier: MIT
#
# Licensed under the MIT License

"""Test the IBMProvider class and the IBM Washington and IBM Montreal devices."""

from __future__ import annotations

from mqt.bench.devices import get_device_by_name


def test_get_ibmq_washington_device() -> None:
    """Test getting the IBM Washington device."""
    device = get_device_by_name("ibm_washington")
    single_qubit_gates = device.get_single_qubit_gates()
    two_qubit_gates = device.get_two_qubit_gates()

    assert device.name == "ibm_washington"
    assert device.num_qubits == 127

    assert all(gate in ["id", "rz", "sx", "x", "cx", "measure", "barrier"] for gate in single_qubit_gates)
    assert all(gate == "cx" for gate in two_qubit_gates)

    for q in range(device.num_qubits):
        assert 0 <= device.get_readout_fidelity(q) <= 1
        assert device.get_readout_duration(q) >= 0

        for gate in single_qubit_gates:
            assert 0 <= device.get_single_qubit_gate_fidelity(gate, q) <= 1
            assert device.get_single_qubit_gate_duration(gate, q) >= 0

    for q0, q1 in device.coupling_map:
        for gate in two_qubit_gates:
            assert 0 <= device.get_two_qubit_gate_fidelity(gate, q0, q1) <= 1
            assert device.get_two_qubit_gate_duration(gate, q0, q1) >= 0


def test_get_ibmq_montreal_device() -> None:
    """Test getting the IBM Montreal device."""
    device = get_device_by_name("ibm_montreal")
    single_qubit_gates = device.get_single_qubit_gates()
    two_qubit_gates = device.get_two_qubit_gates()

    assert device.name == "ibm_montreal"
    assert device.num_qubits == 27

    assert all(gate in ["id", "rz", "sx", "x", "cx", "measure", "barrier"] for gate in single_qubit_gates)
    assert all(gate == "cx" for gate in two_qubit_gates)

    for q in range(device.num_qubits):
        assert 0 <= device.get_readout_fidelity(q) <= 1
        assert device.get_readout_duration(q) >= 0

        for gate in single_qubit_gates:
            assert 0 <= device.get_single_qubit_gate_fidelity(gate, q) <= 1
            assert device.get_single_qubit_gate_duration(gate, q) >= 0
    for q0, q1 in device.coupling_map:
        for gate in two_qubit_gates:
            assert 0 <= device.get_two_qubit_gate_fidelity(gate, q0, q1) <= 1
            assert device.get_two_qubit_gate_duration(gate, q0, q1) >= 0
