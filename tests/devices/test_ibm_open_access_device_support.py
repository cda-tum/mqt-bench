"""Unit tests for IBM Open Access Device Support.

This module contains tests for the functionality of the IBMOpenAccessProvider class,
including importing backend data, retrieving device information, and verifying
calibration data.
"""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import mock_open, patch

import pytest

from mqt.bench.devices import Device, IBMOpenAccessProvider

def test_get_device_success() -> None:
    """Test successful retrieval of a device by name."""
    device = Device(name="ibm_test_device", num_qubits=3, basis_gates=["id", "rz", "x"], coupling_map=[[0, 1], [1, 2]])
    with (
        patch.object(IBMOpenAccessProvider, "import_backend", return_value=device),
        patch.object(IBMOpenAccessProvider, "get_device", return_value=device),
    ):
        retrieved_device = IBMOpenAccessProvider.get_device("ibm_test_device")
        assert retrieved_device.name == "ibm_test_device"
        assert retrieved_device.num_qubits == 3


def test_get_device_not_found() -> None:
    """Test retrieval of a device that does not exist."""
    with pytest.raises(ValueError, match="Device ibm_unknown not found."):
        IBMOpenAccessProvider.get_device("ibm_unknown")


def test_ibm_open_access_provider_methods() -> None:
    """Test various methods of the IBMOpenAccessProvider class."""
    assert IBMOpenAccessProvider.get_available_device_names() == ["ibm_kyiv", "ibm_brisbane", "ibm_sherbrooke"]
    assert IBMOpenAccessProvider.get_available_basis_gates() == [["ecr", "id", "rz", "sx", "x", "measure", "barrier"]]
    assert IBMOpenAccessProvider.get_native_gates() == ["id", "rz", "sx", "x", "ecr", "measure", "barrier"]
    assert IBMOpenAccessProvider.get_max_qubits() == 127
    with pytest.raises(ValueError, match="Device ibm_unknown not found."):
        IBMOpenAccessProvider.get_device("ibm_unknown")


def test_get_ibm_kyiv_device() -> None:
    """Test retrieving the IBM Kyiv device and its properties."""
    device = IBMOpenAccessProvider.get_device("ibm_kyiv")
    single_qubit_gates = device.get_single_qubit_gates()
    two_qubit_gates = device.get_two_qubit_gates()

    assert device.name == "ibm_kyiv"
    assert device.num_qubits == 127

    assert all(gate in ["ecr", "id", "rz", "sx", "x", "measure", "barrier"] for gate in single_qubit_gates)
    assert all(gate == "ecr" for gate in two_qubit_gates)

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


def test_get_ibm_brisbane_device() -> None:
    """Test retrieving the IBM Brisbane device and its properties."""
    device = IBMOpenAccessProvider.get_device("ibm_brisbane")
    single_qubit_gates = device.get_single_qubit_gates()
    two_qubit_gates = device.get_two_qubit_gates()

    assert device.name == "ibm_brisbane"
    assert device.num_qubits == 127

    assert all(gate in ["id", "rz", "sx", "x", "ecr", "measure", "barrier"] for gate in single_qubit_gates)
    assert all(gate == "ecr" for gate in two_qubit_gates)

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


def test_get_ibm_sherbrooke_device() -> None:
    """Test retrieving the IBM Sherbrooke device and its properties."""
    device = IBMOpenAccessProvider.get_device("ibm_sherbrooke")
    single_qubit_gates = device.get_single_qubit_gates()
    two_qubit_gates = device.get_two_qubit_gates()

    assert device.name == "ibm_sherbrooke"
    assert device.num_qubits == 127

    assert all(gate in ["id", "rz", "sx", "x", "ecr", "measure", "barrier"] for gate in single_qubit_gates)
    assert all(gate == "ecr" for gate in two_qubit_gates)

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
