from __future__ import annotations

from mqt.bench.devices import IonQProvider


def test_ionq_harmony_device() -> None:
    """
    Test the import of the IonQ Harmony quantum computer.
    """
    device = IonQProvider.get_device("ionq_harmony")
    single_qubit_gate = device.get_single_qubit_gates().pop()
    two_qubit_gate = device.get_two_qubit_gates().pop()

    assert device.name == "ionq_harmony"
    assert device.num_qubits == 11
    assert isinstance(single_qubit_gate, str)
    assert isinstance(two_qubit_gate, str)
    # assert isinstance(device.get_readout_duration(0), (float, int))
    assert isinstance(device.get_readout_fidelity(0), (float, int))
    # assert isinstance(device.get_single_qubit_gate_duration(single_qubit_gate, 0), (float, int))
    assert isinstance(device.get_single_qubit_gate_fidelity(single_qubit_gate, 0), (float, int))
    # assert isinstance(device.get_two_qubit_gate_duration(two_qubit_gate, 0, 1), (float, int))
    assert isinstance(device.get_two_qubit_gate_fidelity(two_qubit_gate, 0, 1), (float, int))


def test_ionq_aria1_device() -> None:
    """
    Test the import of the IonQ Aria quantum computer.
    """
    device = IonQProvider.get_device("ionq_aria1")
    single_qubit_gate = device.get_single_qubit_gates().pop()
    two_qubit_gate = device.get_two_qubit_gates().pop()

    assert device.name == "ionq_aria1"
    assert device.num_qubits == 23
    assert isinstance(single_qubit_gate, str)
    assert isinstance(two_qubit_gate, str)
    # assert isinstance(device.get_readout_duration(0), (float, int))
    assert isinstance(device.get_readout_fidelity(0), (float, int))
    # assert isinstance(device.get_single_qubit_gate_duration(single_qubit_gate, 0), (float, int))
    assert isinstance(device.get_single_qubit_gate_fidelity(single_qubit_gate, 0), (float, int))
    # assert isinstance(device.get_two_qubit_gate_duration(two_qubit_gate, 0, 1), (float, int))
    assert isinstance(device.get_two_qubit_gate_fidelity(two_qubit_gate, 0, 1), (float, int))
