"""Test the IBMProvider class and the IBM Washington and IBM Montreal devices."""

from __future__ import annotations

import pytest

from mqt.bench.devices import IBMOpenAccessProvider


def test_ibm_open_access_provider_methods() -> None:
    """Test the methods of the IBMProvider class."""
    assert IBMOpenAccessProvider.get_available_device_names() == ["ibm_kyiv", "ibm_brisbane", "ibm_sherbrooke"]
    assert IBMOpenAccessProvider.get_available_basis_gates() == [["ecr", "id", "rz", "sx", "x", "measure", "barrier"]]
    assert IBMOpenAccessProvider.get_native_gates() == ["id", "rz", "sx", "x", "ecr", "measure", "barrier"]
    assert IBMOpenAccessProvider.get_max_qubits() == 127
    with pytest.raises(ValueError, match="Device ibm_unknown not found."):
        IBMOpenAccessProvider.get_device("ibm_unknown")


def test_get_ibm_kyiv_device() -> None:
    """Test getting the IBM Kyiv device."""
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
            with pytest.raises(ValueError, match="Single-qubit gate duration values not available."):
                device.get_single_qubit_gate_duration(gate, q)

    for q0, q1 in device.coupling_map:
        for gate in two_qubit_gates:
            assert 0 <= device.get_two_qubit_gate_fidelity(gate, q0, q1) <= 1
            assert device.get_two_qubit_gate_duration(gate, q0, q1) >= 0


def test_get_ibm_brisbane_device() -> None:
    """Test getting the IBM Brisbane device."""
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
            with pytest.raises(ValueError, match="Single-qubit gate duration values not available."):
                device.get_single_qubit_gate_duration(gate, q)
    for q0, q1 in device.coupling_map:
        for gate in two_qubit_gates:
            assert 0 <= device.get_two_qubit_gate_fidelity(gate, q0, q1) <= 1
            assert device.get_two_qubit_gate_duration(gate, q0, q1) >= 0


def test_get_ibm_sherbrooke_device() -> None:
    """Test getting the IBM Sherbrooke device."""
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
            with pytest.raises(ValueError, match="Single-qubit gate duration values not available."):
                device.get_single_qubit_gate_duration(gate, q)
    for q0, q1 in device.coupling_map:
        for gate in two_qubit_gates:
            assert 0 <= device.get_two_qubit_gate_fidelity(gate, q0, q1) <= 1
            assert device.get_two_qubit_gate_duration(gate, q0, q1) >= 0
