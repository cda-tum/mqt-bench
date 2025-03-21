"""Test the RigettiProvider class and the Rigetti Aspen-M3 device."""

from __future__ import annotations

import re

import pytest

from mqt.bench.devices import RigettiProvider


def test_rigetti_provider_methods() -> None:
    """Test the methods of the RigettiProvider class."""
    assert RigettiProvider.get_available_device_names() == ["rigetti_aspen_m3"]
    assert RigettiProvider.get_available_basis_gates() == [["rx", "rz", "cz", "cp", "xx_plus_yy", "measure", "barrier"]]
    assert RigettiProvider.get_native_gates() == ["rx", "rz", "cz", "cp", "xx_plus_yy", "measure", "barrier"]
    assert RigettiProvider.get_max_qubits() == 79


def test_rigetti_aspen_m3_device() -> None:
    """Test the import of the Rigetti Aspen-M3 quantum computer."""
    device = RigettiProvider.get_device("rigetti_aspen_m3")
    single_qubit_gates = device.get_single_qubit_gates()
    two_qubit_gates = device.get_two_qubit_gates()

    assert device.name == "rigetti_aspen_m3"
    assert device.num_qubits == 79

    assert all(gate in ["rx", "rz", "measure", "barrier"] for gate in single_qubit_gates)
    assert all(gate in ["cz", "cp", "xx_plus_yy"] for gate in two_qubit_gates)

    for q in range(device.num_qubits):
        assert 0 <= device.get_readout_fidelity(q) <= 1
        with pytest.raises(ValueError, match=re.escape("Readout duration values not available.")):
            device.get_readout_duration(q)

        for gate in single_qubit_gates:
            assert 0 <= device.get_single_qubit_gate_fidelity(gate, q) <= 1
            with pytest.raises(ValueError, match=re.escape("Single-qubit gate duration values not available.")):
                device.get_single_qubit_gate_duration(gate, q)

    for q0, q1 in device.coupling_map:
        for gate in two_qubit_gates:
            assert 0 <= device.get_two_qubit_gate_fidelity(gate, q0, q1) <= 1
            with pytest.raises(ValueError, match=re.escape("Two-qubit gate duration values not available.")):
                device.get_two_qubit_gate_duration(gate, q0, q1)
