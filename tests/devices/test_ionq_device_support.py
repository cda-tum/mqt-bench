from __future__ import annotations

from mqt.bench.devices import IonQProvider


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
    assert isinstance(device.get_readout_fidelity(0), (float, int))
    assert all(isinstance(device.get_single_qubit_gate_fidelity(gate, 0), (float, int)) for gate in single_qubit_gates)
    assert all(isinstance(device.get_two_qubit_gate_fidelity(gate, 0, 1), (float, int)) for gate in two_qubit_gates)


def test_ionq_aria1_device() -> None:
    """
    Test the import of the IonQ Aria quantum computer.
    """
    device = IonQProvider.get_device("ionq_aria1")
    single_qubit_gates = device.get_single_qubit_gates()
    two_qubit_gates = device.get_two_qubit_gates()

    assert device.name == "ionq_aria1"
    assert device.num_qubits == 23
    assert all(isinstance(gate, str) for gate in single_qubit_gates)
    assert all(isinstance(gate, str) for gate in two_qubit_gates)
    assert isinstance(device.get_readout_fidelity(0), (float, int))
    assert all(isinstance(device.get_single_qubit_gate_fidelity(gate, 0), (float, int)) for gate in single_qubit_gates)
    assert all(isinstance(device.get_two_qubit_gate_fidelity(gate, 0, 1), (float, int)) for gate in two_qubit_gates)
