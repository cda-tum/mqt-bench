from __future__ import annotations

from mqt.bench.devices import OQCProvider


def test_oqc_lucy_device() -> None:
    """
    Test the import of the OQC Lucy quantum computer.
    """
    device = OQCProvider.get_device("oqc_lucy")
    single_qubit_gate = device.get_single_qubit_gates().pop()
    two_qubit_gate = device.get_two_qubit_gates().pop()

    assert device.name == "oqc_lucy"
    assert device.num_qubits == 8
    assert isinstance(single_qubit_gate, str)
    assert isinstance(two_qubit_gate, str)
    # assert isinstance(device.get_readout_duration(0), (float, int))
    assert isinstance(device.get_readout_fidelity(0), (float, int))
    # assert isinstance(device.get_single_qubit_gate_duration(single_qubit_gate, 0), (float, int))
    assert isinstance(device.get_single_qubit_gate_fidelity(single_qubit_gate, 0), (float, int))
    # assert isinstance(device.get_two_qubit_gate_duration(two_qubit_gate, 0, 1), (float, int))
    assert isinstance(device.get_two_qubit_gate_fidelity(two_qubit_gate, 0, 1), (float, int))
