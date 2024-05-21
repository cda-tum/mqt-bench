"""Test the IQMProvider class and the IonQ devices."""

from __future__ import annotations

import pytest

from mqt.bench.devices import IQMProvider


def test_iqm_provider_methods() -> None:
    """Test the methods of the IQMProvider class.

    - get_available_device_names
    - get_available_basis_gates
    - get_native_gates
    - get_max_qubits.
    """
    assert IQMProvider.get_available_device_names() == ["iqm_adonis", "iqm_apollo"]
    assert IQMProvider.get_available_basis_gates() == [["r", "cz", "measure", "barrier"]]
    assert IQMProvider.get_native_gates() == ["r", "cz", "measure", "barrier"]
    assert IQMProvider.get_max_qubits() == 20
    with pytest.raises(ValueError, match="Device iqm_unknown not found."):
        IQMProvider.get_device("iqm_unknown")


def test_get_iqm_apollo_device() -> None:
    """Test getting the IQM Apollo device."""
    device = IQMProvider.get_device("iqm_apollo")
    single_qubit_gates = device.get_single_qubit_gates()
    two_qubit_gates = device.get_two_qubit_gates()

    assert device.name == "iqm_apollo"
    assert device.num_qubits == 20

    assert all(gate in ["r", "measure", "barrier"] for gate in single_qubit_gates)
    assert all(gate == "cz" for gate in two_qubit_gates)

    for q in range(device.num_qubits):
        assert 0 <= device.get_readout_fidelity(q) <= 1
        assert device.get_readout_duration(q) > 0
        if device.calibration is not None:
            assert device.calibration.get_t1(q) > 0
            assert device.calibration.get_t2(q) > 0

        for gate in single_qubit_gates:
            assert 0 <= device.get_single_qubit_gate_fidelity(gate, q) <= 1
            assert device.get_single_qubit_gate_duration(gate, q) > 0
            if device.calibration is not None:
                assert 0 <= device.calibration.compute_average_single_qubit_gate_fidelity(gate) <= 1
                assert device.calibration.compute_average_single_qubit_gate_duration(gate) > 0

    for q0, q1 in device.coupling_map:
        for gate in two_qubit_gates:
            assert 0 <= device.get_two_qubit_gate_fidelity(gate, q0, q1) <= 1
            assert device.get_two_qubit_gate_duration(gate, q0, q1) > 0
            if device.calibration is not None:
                assert 0 <= device.calibration.compute_average_two_qubit_gate_fidelity(gate) <= 1
                assert device.calibration.compute_average_two_qubit_gate_duration(gate) > 0

    if device.calibration is not None:
        assert 0 <= device.calibration.compute_average_readout_fidelity() <= 1
        assert device.calibration.compute_average_readout_duration() > 0


def test_get_iqm_adonis_device() -> None:
    """Test getting the IQM Adonis device."""
    device = IQMProvider.get_device("iqm_adonis")
    single_qubit_gates = device.get_single_qubit_gates()
    two_qubit_gates = device.get_two_qubit_gates()

    assert device.name == "iqm_adonis"
    assert device.num_qubits == 5

    assert all(gate in ["r", "measure", "barrier"] for gate in single_qubit_gates)
    assert all(gate == "cz" for gate in two_qubit_gates)

    for q in range(device.num_qubits):
        assert 0 <= device.get_readout_fidelity(q) <= 1
        assert device.get_readout_duration(q) > 0
        if device.calibration is not None:
            assert device.calibration.get_t1(q) > 0
            assert device.calibration.get_t2(q) > 0

        for gate in single_qubit_gates:
            assert 0 <= device.get_single_qubit_gate_fidelity(gate, q) <= 1
            assert device.get_single_qubit_gate_duration(gate, q) > 0
            if device.calibration is not None:
                assert 0 <= device.calibration.compute_average_single_qubit_gate_fidelity(gate) <= 1
                assert device.calibration.compute_average_single_qubit_gate_duration(gate) > 0

    for q0, q1 in device.coupling_map:
        for gate in two_qubit_gates:
            assert 0 <= device.get_two_qubit_gate_fidelity(gate, q0, q1) <= 1
            assert device.get_two_qubit_gate_duration(gate, q0, q1) > 0
            if device.calibration is not None:
                assert 0 <= device.calibration.compute_average_two_qubit_gate_fidelity(gate) <= 1
                assert device.calibration.compute_average_two_qubit_gate_duration(gate) > 0

    if device.calibration is not None:
        assert 0 <= device.calibration.compute_average_readout_fidelity() <= 1
        assert device.calibration.compute_average_readout_duration() > 0
