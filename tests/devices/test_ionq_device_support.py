from __future__ import annotations

from mqt.bench.devices import IonQProvider


def test_ionq_harmony_device() -> None:
    """
    Test the import of the IonQ Harmony quantum computer.
    """
    device = IonQProvider.get_device("ionq_harmony")
    assert device.name == "ionq_harmony"
    assert device.num_qubits == 11


def test_ionq_aria1_device() -> None:
    """
    Test the import of the IonQ Aria quantum computer.
    """
    device = IonQProvider.get_device("ionq_aria1")
    assert device.name == "ionq_aria1"
    assert device.num_qubits == 23
