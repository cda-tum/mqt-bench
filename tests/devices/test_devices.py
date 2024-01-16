from __future__ import annotations

from typing import cast

import pytest

from mqt.bench.devices import (
    Device,
    DeviceCalibration,
    NotFoundError,
    get_available_devices,
    get_available_providers,
    get_provider_by_name,
)


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
    with pytest.raises(ValueError, match="Calibration data not available for device test."):
        device.sanitize_device()

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
    with pytest.raises(ValueError, match="Single-qubit gate fidelity values not available."):
        device.calibration.get_single_qubit_gate_fidelity("gate_type", 0)
    with pytest.raises(ValueError, match="Single-qubit gate duration values not available."):
        device.calibration.get_single_qubit_gate_duration("gate_type", 0)
    with pytest.raises(ValueError, match="Two-qubit gate fidelity values not available."):
        device.calibration.get_two_qubit_gate_fidelity("gate_type", 0, 1)
    with pytest.raises(ValueError, match="Two-qubit gate duration values not available."):
        device.calibration.get_two_qubit_gate_duration("gate_type", 0, 1)
    with pytest.raises(ValueError, match="Readout fidelity values not available."):
        device.calibration.get_readout_fidelity(0)
    with pytest.raises(ValueError, match="Readout duration values not available."):
        device.calibration.get_readout_duration(0)
    with pytest.raises(ValueError, match="T1 values not available."):
        device.calibration.get_t1(0)
    with pytest.raises(ValueError, match="T2 values not available."):
        device.calibration.get_t2(0)
    with pytest.raises(ValueError, match="Single-qubit gate fidelity values not available."):
        device.calibration.compute_average_single_qubit_gate_fidelity("gate")
    with pytest.raises(ValueError, match="Single-qubit gate duration values not available."):
        device.calibration.compute_average_single_qubit_gate_duration("gate")
    with pytest.raises(ValueError, match="Two-qubit gate fidelity values not available."):
        device.calibration.compute_average_two_qubit_gate_fidelity("gate")
    with pytest.raises(ValueError, match="Two-qubit gate duration values not available."):
        device.calibration.compute_average_two_qubit_gate_duration("gate")
    with pytest.raises(ValueError, match="Readout fidelity values not available."):
        device.calibration.compute_average_readout_fidelity()
    with pytest.raises(ValueError, match="Readout duration values not available."):
        device.calibration.compute_average_readout_duration()


def test_provider() -> None:
    """
    Test that all providers can be imported.
    """
    for provider in get_available_providers():
        assert provider.provider_name in ["ibm", "rigetti", "oqc", "ionq", "quantinuum"]

    with pytest.raises(NotFoundError, match="Provider 'test' not found among available providers."):
        get_provider_by_name("test")
