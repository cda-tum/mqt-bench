from __future__ import annotations

from mqt.bench.devices import RigettiProvider


def test_rigetti_aspen_m2_device() -> None:
    """
    Test the import of the Rigetti Aspen-M2 quantum computer.
    """
    device = RigettiProvider.get_device("rigetti_aspen_m2")
    assert device.name == "rigetti_aspen_m2"
    assert device.num_qubits == 80
