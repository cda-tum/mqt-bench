from __future__ import annotations

from mqt.bench.devices import OQCProvider


def test_oqc_lucy_device() -> None:
    """
    Test the import of the OQC Lucy quantum computer.
    """
    device = OQCProvider.get_device("oqc_lucy")
    single_qubit_gates = device.get_single_qubit_gates()
    two_qubit_gates = device.get_two_qubit_gates()

    assert device.name == "oqc_lucy"
    assert device.num_qubits == 8
    assert all(isinstance(gate, str) for gate in single_qubit_gates)
    assert all(isinstance(gate, str) for gate in two_qubit_gates)
    assert isinstance(device.get_readout_fidelity(0), (float, int))
    assert all(isinstance(device.get_single_qubit_gate_fidelity(gate, 0), (float, int)) for gate in single_qubit_gates)
    assert all(isinstance(device.get_two_qubit_gate_fidelity(gate, 0, 1), (float, int)) for gate in two_qubit_gates)
