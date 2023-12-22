from __future__ import annotations

from qiskit.providers.fake_provider import FakeMontreal, FakeMontrealV2

from mqt.bench.devices import IBMProvider


def test_import_v1_backend() -> None:
    """
    Test importing a Qiskit `BackendV1` object.
    """
    backend = FakeMontreal()
    device = IBMProvider.import_qiskit_backend(backend)
    single_qubit_gate = device.get_single_qubit_gates().pop()
    two_qubit_gate = device.get_two_qubit_gates().pop()

    assert device.name == backend.name()
    assert device.num_qubits == backend.configuration().n_qubits
    assert device.coupling_map == [[a, b] for a, b in backend.configuration().coupling_map]
    assert device.basis_gates == backend.configuration().basis_gates
    assert isinstance(single_qubit_gate, str)
    assert isinstance(two_qubit_gate, str)
    # assert isinstance(device.get_readout_duration(0), (float, int))
    assert isinstance(device.get_readout_fidelity(0), (float, int))
    # assert isinstance(device.get_single_qubit_gate_duration(single_qubit_gate, 0), (float, int))
    assert isinstance(device.get_single_qubit_gate_fidelity(single_qubit_gate, 0), (float, int))
    # assert isinstance(device.get_two_qubit_gate_duration(two_qubit_gate, 0, 1), (float, int))
    assert isinstance(device.get_two_qubit_gate_fidelity(two_qubit_gate, 0, 1), (float, int))


def test_import_v2_backend() -> None:
    """
    Test importing a Qiskit `BackendV2` object.
    """
    backend = FakeMontrealV2()
    device = IBMProvider.import_qiskit_backend(backend)
    single_qubit_gate = device.get_single_qubit_gates().pop()
    two_qubit_gate = device.get_two_qubit_gates().pop()

    assert device.name == backend.name
    assert device.num_qubits == backend.num_qubits
    assert device.coupling_map == backend.coupling_map.get_edges()
    assert device.basis_gates == backend.operation_names
    assert isinstance(single_qubit_gate, str)
    assert isinstance(two_qubit_gate, str)
    # assert isinstance(device.get_readout_duration(0), (float, int))
    assert isinstance(device.get_readout_fidelity(0), (float, int))
    # assert isinstance(device.get_single_qubit_gate_duration(single_qubit_gate, 0), (float, int))
    assert isinstance(device.get_single_qubit_gate_fidelity(single_qubit_gate, 0), (float, int))
    # assert isinstance(device.get_two_qubit_gate_duration(two_qubit_gate, 0, 1), (float, int))
    assert isinstance(device.get_two_qubit_gate_fidelity(two_qubit_gate, 0, 1), (float, int))


def test_get_ibm_washington_device() -> None:
    """
    Test getting the IBM Washington device.
    """
    device = IBMProvider.get_device("ibm_washington")
    single_qubit_gate = device.get_single_qubit_gates().pop()
    two_qubit_gate = device.get_two_qubit_gates().pop()

    assert device.name == "ibm_washington"
    assert device.num_qubits == 127
    assert isinstance(single_qubit_gate, str)
    assert isinstance(two_qubit_gate, str)
    # assert isinstance(device.get_readout_duration(0), (float, int))
    assert isinstance(device.get_readout_fidelity(0), (float, int))
    # assert isinstance(device.get_single_qubit_gate_duration(single_qubit_gate, 0), (float, int))
    assert isinstance(device.get_single_qubit_gate_fidelity(single_qubit_gate, 0), (float, int))
    # assert isinstance(device.get_two_qubit_gate_duration(two_qubit_gate, 0, 1), (float, int))
    assert isinstance(device.get_two_qubit_gate_fidelity(two_qubit_gate, 0, 1), (float, int))


def test_get_ibmq_montreal_device() -> None:
    """
    Test getting the IBM Montreal device.
    """
    device = IBMProvider.get_device("ibm_montreal")
    single_qubit_gate = device.get_single_qubit_gates().pop()
    two_qubit_gate = device.get_two_qubit_gates().pop()

    assert device.name == "ibm_montreal"
    assert device.num_qubits == 27
    assert isinstance(single_qubit_gate, str)
    assert isinstance(two_qubit_gate, str)
    # assert isinstance(device.get_readout_duration(0), (float, int))
    assert isinstance(device.get_readout_fidelity(0), (float, int))
    # assert isinstance(device.get_single_qubit_gate_duration(single_qubit_gate, 0), (float, int))
    assert isinstance(device.get_single_qubit_gate_fidelity(single_qubit_gate, 0), (float, int))
    # assert isinstance(device.get_two_qubit_gate_duration(two_qubit_gate, 0, 1), (float, int))
    assert isinstance(device.get_two_qubit_gate_fidelity(two_qubit_gate, 0, 1), (float, int))
