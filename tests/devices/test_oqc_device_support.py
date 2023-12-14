from __future__ import annotations

from mqt.bench.devices import OQCProvider


def test_oqc_lucy_device() -> None:
    """
    Test the import of the OQC Lucy quantum computer.
    """
    device = OQCProvider.get_device("oqc_lucy")
    assert device.name == "oqc_lucy"
    assert device.num_qubits == 8
