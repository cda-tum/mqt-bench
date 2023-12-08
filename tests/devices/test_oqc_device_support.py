from mqt.bench.devices import OQCProvider


def test_oqc_lucy_device() -> None:
    """
    Test the import of the OQC Lucy quantum computer.
    """
    device = OQCProvider.get_device("lucy")
    assert device.name == "lucy"
    assert device.num_qubits == 8  # noqa: PLR2004
