from __future__ import annotations

from typing import cast

import pytest

from mqt.bench.devices import Device, get_available_devices


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
