"""Tests for the device module."""

from __future__ import annotations

import re
from typing import cast

import pytest

from mqt.bench.devices import (
    Device,
    DeviceCalibration,
    NoCalibrationDevice,
    calibration,
    get_available_devices,
    get_device_by_name,
    get_native_gateset_by_name,
)


@pytest.mark.parametrize("device", get_available_devices(), ids=lambda device: cast(str, device.name))
def test_sanitized_devices(device: NoCalibrationDevice) -> None:
    """Test that all devices can be sanitized and provide complete fidelity data."""
    calibrated_device = device.constructor(sanitize_device=True)
    assert calibrated_device.calibration is not None
    for qubit in range(calibrated_device.num_qubits):
        assert qubit in calibrated_device.calibration.single_qubit_gate_fidelity
        for gate in calibrated_device.get_single_qubit_gates():
            assert gate in calibrated_device.calibration.single_qubit_gate_fidelity[qubit]
            assert calibrated_device.calibration.single_qubit_gate_fidelity[qubit][gate] > 0
        assert qubit in calibrated_device.calibration.readout_fidelity

    for qubit1, qubit2 in calibrated_device.coupling_map:
        assert (qubit1, qubit2) in calibrated_device.calibration.two_qubit_gate_fidelity
        for gate in calibrated_device.get_two_qubit_gates():
            assert gate in calibrated_device.calibration.two_qubit_gate_fidelity[qubit1, qubit2]
            assert calibrated_device.calibration.two_qubit_gate_fidelity[qubit1, qubit2][gate] > 0


def test_device_calibration_errors() -> None:
    """Test that all device calibration methods raise errors when no calibration data is available."""
    device = Device(name="test", num_qubits=1, basis_gates=[], coupling_map=[], calibration=None)

    # Test all methods with no calibration
    with pytest.raises(ValueError, match=re.escape("Calibration data not available for device test.")):
        device.get_single_qubit_gate_fidelity("gate1", 0)
    with pytest.raises(ValueError, match=re.escape("Calibration data not available for device test.")):
        device.get_single_qubit_gate_duration("gate1", 0)
    with pytest.raises(ValueError, match=re.escape("Calibration data not available for device test.")):
        device.get_two_qubit_gate_fidelity("gate2", 0, 1)
    with pytest.raises(ValueError, match=re.escape("Calibration data not available for device test.")):
        device.get_two_qubit_gate_duration("gate2", 0, 1)
    with pytest.raises(ValueError, match=re.escape("Calibration data not available for device test.")):
        device.get_readout_fidelity(0)
    with pytest.raises(ValueError, match=re.escape("Calibration data not available for device test.")):
        device.get_readout_duration(0)
    with pytest.raises(ValueError, match=re.escape("Calibration data not available for device test.")):
        device.sanitize_device()

    # Test all methods with missing calibration data
    device.calibration = DeviceCalibration()
    with pytest.raises(ValueError, match=re.escape("Gate gate1 not supported by device test.")):
        device.get_single_qubit_gate_fidelity("gate1", 0)
    with pytest.raises(ValueError, match=re.escape("Gate gate1 not supported by device test.")):
        device.get_single_qubit_gate_duration("gate1", 0)
    with pytest.raises(ValueError, match=re.escape("Gate gate2 not supported by device test.")):
        device.get_two_qubit_gate_fidelity("gate2", 0, 1)
    with pytest.raises(ValueError, match=re.escape("Gate gate2 not supported by device test.")):
        device.get_two_qubit_gate_duration("gate2", 0, 1)
    with pytest.raises(ValueError, match=re.escape("Readout fidelity values not available.")):
        device.get_readout_fidelity(0)
    with pytest.raises(ValueError, match=re.escape("Readout duration values not available.")):
        device.get_readout_duration(0)
    with pytest.raises(ValueError, match=re.escape("Single-qubit gate fidelity values not available.")):
        device.calibration.get_single_qubit_gate_fidelity("gate_type", 0)
    with pytest.raises(ValueError, match=re.escape("Single-qubit gate duration values not available.")):
        device.calibration.get_single_qubit_gate_duration("gate_type", 0)
    with pytest.raises(ValueError, match=re.escape("Two-qubit gate fidelity values not available.")):
        device.calibration.get_two_qubit_gate_fidelity("gate_type", 0, 1)
    with pytest.raises(ValueError, match=re.escape("Two-qubit gate duration values not available.")):
        device.calibration.get_two_qubit_gate_duration("gate_type", 0, 1)
    with pytest.raises(ValueError, match=re.escape("Readout fidelity values not available.")):
        device.calibration.get_readout_fidelity(0)
    with pytest.raises(ValueError, match=re.escape("Readout duration values not available.")):
        device.calibration.get_readout_duration(0)
    with pytest.raises(ValueError, match=re.escape("T1 values not available.")):
        device.calibration.get_t1(0)
    with pytest.raises(ValueError, match=re.escape("T2 values not available.")):
        device.calibration.get_t2(0)
    with pytest.raises(ValueError, match=re.escape("Single-qubit gate fidelity values not available.")):
        device.calibration.compute_average_single_qubit_gate_fidelity("gate")
    with pytest.raises(ValueError, match=re.escape("Single-qubit gate duration values not available.")):
        device.calibration.compute_average_single_qubit_gate_duration("gate")
    with pytest.raises(ValueError, match=re.escape("Two-qubit gate fidelity values not available.")):
        device.calibration.compute_average_two_qubit_gate_fidelity("gate")
    with pytest.raises(ValueError, match=re.escape("Two-qubit gate duration values not available.")):
        device.calibration.compute_average_two_qubit_gate_duration("gate")
    with pytest.raises(ValueError, match=re.escape("Readout fidelity values not available.")):
        device.calibration.compute_average_readout_fidelity()
    with pytest.raises(ValueError, match=re.escape("Readout duration values not available.")):
        device.calibration.compute_average_readout_duration()

    with pytest.raises(FileNotFoundError, match="Calibration file not found*"):
        calibration.get_device_calibration_path("test")

    actual_dev = get_device_by_name("ionq_aria1")
    qubit = 100
    gate_type = "wrong_gate"
    with pytest.raises(
        ValueError, match=f"Single-qubit fidelity for gate {gate_type} and qubit {qubit} not available."
    ):
        actual_dev.calibration.get_single_qubit_gate_fidelity(gate_type, qubit)
    with pytest.raises(
        ValueError, match=f"Single-qubit duration for gate {gate_type} and qubit {qubit} not available."
    ):
        actual_dev.calibration.get_single_qubit_gate_duration(gate_type, qubit)
    with pytest.raises(
        ValueError, match=f"Two-qubit fidelity for gate {gate_type} and qubits {qubit} and {qubit} not available."
    ):
        actual_dev.calibration.get_two_qubit_gate_fidelity(gate_type, qubit, qubit)
    with pytest.raises(
        ValueError, match=f"Two-qubit duration for gate {gate_type} and qubits {qubit} and {qubit} not available."
    ):
        actual_dev.calibration.get_two_qubit_gate_duration(gate_type, qubit, qubit)
    with pytest.raises(ValueError, match=f"Readout fidelity for qubit {qubit} not available."):
        actual_dev.calibration.get_readout_fidelity(qubit)
    with pytest.raises(ValueError, match=f"Readout duration for qubit {qubit} not available."):
        actual_dev.calibration.get_readout_duration(qubit)
    with pytest.raises(ValueError, match=f"T1 for qubit {qubit} not available."):
        actual_dev.calibration.get_t1(qubit)
    with pytest.raises(ValueError, match=f"T2 for qubit {qubit} not available."):
        actual_dev.calibration.get_t2(qubit)


def test_no_calibration_devices() -> None:
    """Test that no calibration devices have the same gate set as the calibrated ones."""
    for no_calibration_device in get_available_devices():
        assert set(no_calibration_device.gateset) == set(no_calibration_device.constructor().basis_gates)


def test_unsupported_device() -> None:
    """Test that unsupported devices raise errors."""
    with pytest.raises(ValueError, match="Device unsupported not found in available devices."):
        get_device_by_name("unsupported")
    with pytest.raises(ValueError, match="Gateset unsupported not found in available gatesets."):
        get_native_gateset_by_name("unsupported")
