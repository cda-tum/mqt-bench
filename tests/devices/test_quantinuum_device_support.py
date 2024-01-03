from __future__ import annotations

from mqt.bench.devices import QuantinuumProvider


def test_quantinuum_h2_device() -> None:
    """
    Test the import of the Quantinuum H2 quantum computer.
    """
    device = QuantinuumProvider.get_device("quantinuum_h2")
    single_qubit_gates = device.get_single_qubit_gates()
    two_qubit_gates = device.get_two_qubit_gates()

    assert device.name == "quantinuum_h2"
    assert device.num_qubits == 32
    assert all(isinstance(gate, str) for gate in single_qubit_gates)
    assert all(isinstance(gate, str) for gate in two_qubit_gates)
    assert isinstance(device.get_readout_fidelity(0), (float, int))
    assert all(isinstance(device.get_single_qubit_gate_fidelity(gate, 0), (float, int)) for gate in single_qubit_gates)
    assert all(isinstance(device.get_two_qubit_gate_fidelity(gate, 0, 1), (float, int)) for gate in two_qubit_gates)
