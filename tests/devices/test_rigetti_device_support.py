from __future__ import annotations

import pytest

from mqt.bench.devices import RigettiProvider


def test_rigetti_provider_methods() -> None:
    # Test get_available_device_names method
    assert RigettiProvider.get_available_device_names() == ["rigetti_aspen_m2"]

    # Test get_available_basis_gates method
    assert RigettiProvider.get_available_basis_gates() == [["rx", "rz", "cz", "cp", "xx_plus_yy", "measure", "barrier"]]

    # Test get_native_gates method
    assert RigettiProvider.get_native_gates() == ["rx", "rz", "cz", "cp", "xx_plus_yy", "measure", "barrier"]

    # Test get_max_qubits method
    assert RigettiProvider.get_max_qubits() == 80


def test_rigetti_aspen_m2_device() -> None:
    """
    Test the import of the Rigetti Aspen-M2 quantum computer.
    """
    device = RigettiProvider.get_device("rigetti_aspen_m2")
    single_qubit_gates = device.get_single_qubit_gates()
    two_qubit_gates = device.get_two_qubit_gates()

    assert device.name == "rigetti_aspen_m2"
    assert device.num_qubits == 80

    assert all(isinstance(gate, str) for gate in single_qubit_gates)
    assert all(isinstance(gate, str) for gate in two_qubit_gates)

    for q in range(device.num_qubits):
        assert isinstance(device.get_readout_fidelity(q), (float, int))
        with pytest.raises(ValueError, match="Readout duration values not available."):
            device.get_readout_duration(q)
        for gate in single_qubit_gates:
            assert isinstance(device.get_single_qubit_gate_fidelity(gate, q), (float, int))
            with pytest.raises(ValueError, match="Single-qubit gate duration values not available."):
                device.get_single_qubit_gate_duration(gate, q)

    for q0, q1 in device.coupling_map:
        for gate in two_qubit_gates:
            try:
                assert isinstance(device.get_two_qubit_gate_fidelity(gate, q0, q1), (float, int))
            except Exception:
                with pytest.raises(ValueError):  # noqa: PT011
                    device.get_two_qubit_gate_fidelity(gate, q0, q1)

            try:  # not all gates are available for all qubit pairs
                assert isinstance(device.get_two_qubit_gate_duration(gate, q0, q1), (float, int))
            except Exception:
                with pytest.raises(ValueError):  # noqa: PT011
                    device.get_two_qubit_gate_duration(gate, q0, q1)
