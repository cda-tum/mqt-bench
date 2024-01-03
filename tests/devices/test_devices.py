from __future__ import annotations

from typing import cast

import pytest

from mqt.bench.devices import Device, DeviceCalibration, get_available_devices


@pytest.mark.parametrize(
    "device", get_available_devices(sanitize_device=True), ids=lambda device: cast(str, device.name)
)
def test_sanitized_devices(device: Device) -> None:
    """
    Test that all devices can be sanitized and provide complete fidelity data.
    """
    assert device.calibration is not None
    for qubit in range(device.num_qubits):
        assert qubit in device.calibration.single_qubit_gate_fidelity
        for gate in device.get_single_qubit_gates():
            assert gate in device.calibration.single_qubit_gate_fidelity[qubit]
            assert device.calibration.single_qubit_gate_fidelity[qubit][gate] > 0
        assert qubit in device.calibration.readout_fidelity

    for qubit1, qubit2 in device.coupling_map:
        assert (qubit1, qubit2) in device.calibration.two_qubit_gate_fidelity
        for gate in device.get_two_qubit_gates():
            assert gate in device.calibration.two_qubit_gate_fidelity[(qubit1, qubit2)]
            assert device.calibration.two_qubit_gate_fidelity[(qubit1, qubit2)][gate] > 0


def test_device_calibration_errors() -> None:
    """
    Test that all device calibration methods raise errors when no calibration data is available.
    """
    device = Device(name="test", num_qubits=1, basis_gates=[], coupling_map=[], calibration=None)

    # Test all methods with no calibration
    with pytest.raises(ValueError, match="Calibration data not available for device test."):
        device.get_single_qubit_gate_fidelity("gate1", 0)
    with pytest.raises(ValueError, match="Calibration data not available for device test."):
        device.get_single_qubit_gate_duration("gate1", 0)
    with pytest.raises(ValueError, match="Calibration data not available for device test."):
        device.get_two_qubit_gate_fidelity("gate2", 0, 1)
    with pytest.raises(ValueError, match="Calibration data not available for device test."):
        device.get_two_qubit_gate_duration("gate2", 0, 1)
    with pytest.raises(ValueError, match="Calibration data not available for device test."):
        device.get_readout_fidelity(0)
    with pytest.raises(ValueError, match="Calibration data not available for device test."):
        device.get_readout_duration(0)

    # Test all methods with missing calibration data
    device.calibration = DeviceCalibration()
    with pytest.raises(ValueError, match="Gate gate1 not supported by device test."):
        device.get_single_qubit_gate_fidelity("gate1", 0)
    with pytest.raises(ValueError, match="Gate gate1 not supported by device test."):
        device.get_single_qubit_gate_duration("gate1", 0)
    with pytest.raises(ValueError, match="Gate gate2 not supported by device test."):
        device.get_two_qubit_gate_fidelity("gate2", 0, 1)
    with pytest.raises(ValueError, match="Gate gate2 not supported by device test."):
        device.get_two_qubit_gate_duration("gate2", 0, 1)
    with pytest.raises(ValueError, match="Readout fidelity values not available."):
        device.get_readout_fidelity(0)
    with pytest.raises(ValueError, match="Readout duration values not available."):
        device.get_readout_duration(0)
