"""Test the quantinuum provider class and the Quantinuum H2 device."""

from __future__ import annotations

import pytest

from mqt.bench.devices import QuantinuumProvider


def test_quantinuum_provider_methods() -> None:
    """Test the methods of the QuantinuumProvider class."""
    assert QuantinuumProvider.get_available_device_names() == ["quantinuum_h2"]
    assert QuantinuumProvider.get_available_basis_gates() == [["rzz", "rz", "ry", "rx", "measure", "barrier"]]
    assert QuantinuumProvider.get_native_gates() == ["rzz", "rz", "ry", "rx", "measure", "barrier"]
    assert QuantinuumProvider.get_max_qubits() == 32


def test_quantinuum_h2_device() -> None:
    """Test the import of the Quantinuum H2 quantum computer."""
    device = QuantinuumProvider.get_device("quantinuum_h2")
    single_qubit_gates = device.get_single_qubit_gates()
    two_qubit_gates = device.get_two_qubit_gates()

    assert device.name == "quantinuum_h2"
    assert device.num_qubits == 32

    assert all(gate in ["rz", "ry", "rx", "measure", "barrier"] for gate in single_qubit_gates)
    assert all(gate == "rzz" for gate in two_qubit_gates)

    for q in range(device.num_qubits):
        assert 0 <= device.get_readout_fidelity(q) <= 1
        with pytest.raises(ValueError, match="Readout duration values not available."):
            device.get_readout_duration(q)

        for gate in single_qubit_gates:
            assert 0 <= device.get_single_qubit_gate_fidelity(gate, q) <= 1
            with pytest.raises(ValueError, match="Single-qubit gate duration values not available."):
                device.get_single_qubit_gate_duration(gate, q)

    for q0, q1 in device.coupling_map:
        for gate in two_qubit_gates:
            assert 0 <= device.get_two_qubit_gate_fidelity(gate, q0, q1) <= 1
            with pytest.raises(ValueError, match="Two-qubit gate duration values not available."):
                device.get_two_qubit_gate_duration(gate, q0, q1)
