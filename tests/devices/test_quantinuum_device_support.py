from __future__ import annotations

from mqt.bench.devices import QuantinuumProvider


def test_quantinuum_h2_device() -> None:
    """
    Test the import of the Quantinuum H2 quantum computer.
    """
    device = QuantinuumProvider.get_device("quantinuum_h2")
    assert device.name == "quantinuum_h2"
    assert device.num_qubits == 32
