from __future__ import annotations

from mqt.bench.devices import IonQProvider


def test_ionq_provider_methods() -> None:
    """
    Test the methods of the IonQProvider class:
    - get_available_device_names
    - get_available_basis_gates
    - get_native_gates
    - get_max_qubits
    """
    assert IonQProvider.get_available_device_names() == ["ionq_harmony", "ionq_aria1"]
    assert IonQProvider.get_available_basis_gates() == [["rxx", "rz", "ry", "rx", "measure", "barrier"]]
    assert IonQProvider.get_native_gates() == ["rxx", "rz", "ry", "rx", "measure", "barrier"]
    assert IonQProvider.get_max_qubits() == 25


def test_ionq_harmony_device() -> None:
    """
    Test the import of the IonQ Harmony quantum computer.
    """
    device = IonQProvider.get_device("ionq_harmony")
    single_qubit_gates = device.get_single_qubit_gates()
    two_qubit_gates = device.get_two_qubit_gates()

    assert device.name == "ionq_harmony"
    assert device.num_qubits == 11

    assert all(isinstance(gate, str) for gate in single_qubit_gates)
    assert all(isinstance(gate, str) for gate in two_qubit_gates)

    for q in range(device.num_qubits):
        assert isinstance(device.get_readout_fidelity(q), float | int)
        assert isinstance(device.get_readout_duration(q), float | int)
        for gate in single_qubit_gates:
            assert isinstance(device.get_single_qubit_gate_fidelity(gate, q), float | int)
            assert isinstance(device.get_single_qubit_gate_duration(gate, q), float | int)

    for q0, q1 in device.coupling_map:
        for gate in two_qubit_gates:
            assert isinstance(device.get_two_qubit_gate_fidelity(gate, q0, q1), float | int)
            assert isinstance(device.get_two_qubit_gate_duration(gate, q0, q1), float | int)


def test_ionq_aria1_device() -> None:
    """
    Test the import of the IonQ Aria quantum computer.
    """
    device = IonQProvider.get_device("ionq_aria1")
    single_qubit_gates = device.get_single_qubit_gates()
    two_qubit_gates = device.get_two_qubit_gates()

    assert device.name == "ionq_aria1"
    assert device.num_qubits == 25

    assert all(isinstance(gate, str) for gate in single_qubit_gates)
    assert all(isinstance(gate, str) for gate in two_qubit_gates)

    for q in range(device.num_qubits):
        assert isinstance(device.get_readout_fidelity(q), float | int)
        assert isinstance(device.get_readout_duration(q), float | int)
        for gate in single_qubit_gates:
            assert isinstance(device.get_single_qubit_gate_fidelity(gate, q), float | int)
            assert isinstance(device.get_single_qubit_gate_duration(gate, q), float | int)

    for q0, q1 in device.coupling_map:
        for gate in two_qubit_gates:
            assert isinstance(device.get_two_qubit_gate_fidelity(gate, q0, q1), float | int)
            assert isinstance(device.get_two_qubit_gate_duration(gate, q0, q1), float | int)
