"""Test the IonQProvider class and the IonQ devices."""

from __future__ import annotations

from mqt.bench.devices import IonQProvider


def test_ionq_provider_methods() -> None:
    """Test the methods of the IonQProvider class."""
    assert IonQProvider.get_available_device_names() == ["ionq_harmony", "ionq_aria1"]
    assert IonQProvider.get_available_basis_gates() == [["rxx", "rz", "ry", "rx", "measure", "barrier"]]
    assert IonQProvider.get_native_gates() == ["rxx", "rz", "ry", "rx", "measure", "barrier"]
    assert IonQProvider.get_max_qubits() == 25


def test_ionq_harmony_device() -> None:
    """Test the import of the IonQ Harmony quantum computer."""
    device = IonQProvider.get_device("ionq_harmony")
    single_qubit_gates = device.get_single_qubit_gates()
    two_qubit_gates = device.get_two_qubit_gates()

    assert device.name == "ionq_harmony"
    assert device.num_qubits == 11

    assert all(gate in ["rz", "ry", "rx", "measure", "barrier"] for gate in single_qubit_gates)
    assert all(gate == "rxx" for gate in two_qubit_gates)

    for q in range(device.num_qubits):
        assert 0 <= device.get_readout_fidelity(q) <= 1
        assert device.get_readout_duration(q) >= 0
        for gate in single_qubit_gates:
            assert 0 <= device.get_single_qubit_gate_fidelity(gate, q) <= 1
            assert device.get_single_qubit_gate_duration(gate, q) >= 0

    for q0, q1 in device.coupling_map:
        for gate in two_qubit_gates:
            assert 0 <= device.get_two_qubit_gate_fidelity(gate, q0, q1) <= 1
            assert device.get_two_qubit_gate_duration(gate, q0, q1) >= 0


def test_ionq_aria1_device() -> None:
    """Test the import of the IonQ Aria quantum computer."""
    device = IonQProvider.get_device("ionq_aria1")
    single_qubit_gates = device.get_single_qubit_gates()
    two_qubit_gates = device.get_two_qubit_gates()

    assert device.name == "ionq_aria1"
    assert device.num_qubits == 25

    assert all(gate in ["rz", "ry", "rx", "measure", "barrier"] for gate in single_qubit_gates)
    assert all(gate == "rxx" for gate in two_qubit_gates)

    for q in range(device.num_qubits):
        assert 0 <= device.get_readout_fidelity(q) <= 1
        assert device.get_readout_duration(q) >= 0
        for gate in single_qubit_gates:
            assert 0 <= device.get_single_qubit_gate_fidelity(gate, q) <= 1
            assert device.get_single_qubit_gate_duration(gate, q) >= 0

    for q0, q1 in device.coupling_map:
        for gate in two_qubit_gates:
            assert 0 <= device.get_two_qubit_gate_fidelity(gate, q0, q1) <= 1
            assert device.get_two_qubit_gate_duration(gate, q0, q1) >= 0
