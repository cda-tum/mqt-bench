from __future__ import annotations

import pytest

from mqt.bench.devices import OQCProvider


def test_oqc_provider_methods() -> None:
    """
    Test the methods of the OQCrovider class:
    - get_available_device_names
    - get_available_basis_gates
    - get_native_gates
    - get_max_qubits
    """
    assert OQCProvider.get_available_device_names() == ["oqc_lucy"]
    assert OQCProvider.get_available_basis_gates() == [["rz", "sx", "x", "ecr", "measure", "barrier"]]
    assert OQCProvider.get_native_gates() == ["rz", "sx", "x", "ecr", "measure", "barrier"]
    assert OQCProvider.get_max_qubits() == 8


def test_oqc_lucy_device() -> None:
    """
    Test the import of the OQC Lucy quantum computer.
    """
    device = OQCProvider.get_device("oqc_lucy")
    single_qubit_gates = device.get_single_qubit_gates()
    two_qubit_gates = device.get_two_qubit_gates()

    assert device.name == "oqc_lucy"
    assert device.num_qubits == 8

    assert all(isinstance(gate, str) for gate in single_qubit_gates)
    assert all(isinstance(gate, str) for gate in two_qubit_gates)

    for q in range(device.num_qubits):
        assert isinstance(device.get_readout_fidelity(q), float | int)
        with pytest.raises(ValueError, match="Readout duration values not available."):
            device.get_readout_duration(q)
        for gate in single_qubit_gates:
            assert isinstance(device.get_single_qubit_gate_fidelity(gate, q), float | int)
            with pytest.raises(ValueError, match="Single-qubit gate duration values not available."):
                device.get_single_qubit_gate_duration(gate, q)

    for q0, q1 in device.coupling_map:
        for gate in two_qubit_gates:
            assert isinstance(device.get_two_qubit_gate_fidelity(gate, q0, q1), float | int)
            with pytest.raises(ValueError, match="Two-qubit gate duration values not available."):
                device.get_two_qubit_gate_duration(gate, q0, q1)
