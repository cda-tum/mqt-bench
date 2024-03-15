from __future__ import annotations

import pytest
from qiskit_ibm_runtime.fake_provider import FakeMontreal, FakeMontrealV2

from mqt.bench.devices import IBMProvider


def test_ibm_provider_methods() -> None:
    """
    Test the methods of the IBMProvider class:
    - get_available_device_names
    - get_available_basis_gates
    - get_native_gates
    - get_max_qubits
    """
    assert IBMProvider.get_available_device_names() == ["ibm_washington", "ibm_montreal"]
    assert IBMProvider.get_available_basis_gates() == [["id", "rz", "sx", "x", "cx", "measure", "barrier"]]
    assert IBMProvider.get_native_gates() == ["id", "rz", "sx", "x", "cx", "measure", "barrier"]
    assert IBMProvider.get_max_qubits() == 127
    with pytest.raises(ValueError, match="Device ibm_unknown not found."):
        IBMProvider.get_device("ibm_unknown")


def test_import_v1_backend() -> None:
    """
    Test importing a Qiskit `BackendV1` object.
    """
    backend = FakeMontreal()
    device = IBMProvider.import_qiskit_backend(backend)
    single_qubit_gates = device.get_single_qubit_gates()
    two_qubit_gates = device.get_two_qubit_gates()

    assert device.name == backend.name()
    assert device.num_qubits == backend.configuration().n_qubits
    assert device.coupling_map == [[a, b] for a, b in backend.configuration().coupling_map]
    assert device.basis_gates == backend.configuration().basis_gates

    assert all(isinstance(gate, str) for gate in single_qubit_gates)
    assert all(isinstance(gate, str) for gate in two_qubit_gates)

    for q in range(device.num_qubits):
        assert isinstance(device.get_readout_fidelity(q), float | int)
        assert isinstance(device.get_readout_duration(q), float | int)
        if device.calibration is not None:
            assert isinstance(device.calibration.get_t1(q), float | int)
            assert isinstance(device.calibration.get_t2(q), float | int)

        for gate in single_qubit_gates:
            assert isinstance(device.get_single_qubit_gate_fidelity(gate, q), float | int)
            assert isinstance(device.get_single_qubit_gate_duration(gate, q), float | int)
            if device.calibration is not None:
                assert isinstance(device.calibration.compute_average_single_qubit_gate_duration(gate), float | int)
                assert isinstance(device.calibration.compute_average_single_qubit_gate_fidelity(gate), float | int)

    for q0, q1 in device.coupling_map:
        for gate in two_qubit_gates:
            assert isinstance(device.get_two_qubit_gate_fidelity(gate, q0, q1), float | int)
            assert isinstance(device.get_two_qubit_gate_duration(gate, q0, q1), float | int)
            if device.calibration is not None:
                assert isinstance(device.calibration.compute_average_two_qubit_gate_duration(gate), float | int)
                assert isinstance(device.calibration.compute_average_two_qubit_gate_fidelity(gate), float | int)
    if device.calibration is not None:
        assert isinstance(device.calibration.compute_average_readout_fidelity(), float | int)
        assert isinstance(device.calibration.compute_average_readout_duration(), float | int)


def test_import_v2_backend() -> None:
    """
    Test importing a Qiskit `BackendV2` object.
    """
    backend = FakeMontrealV2()
    device = IBMProvider.import_qiskit_backend(backend)
    single_qubit_gates = device.get_single_qubit_gates()
    two_qubit_gates = device.get_two_qubit_gates()

    assert device.name == backend.name
    assert device.num_qubits == backend.num_qubits
    assert device.coupling_map == backend.coupling_map.get_edges()
    assert device.basis_gates == backend.operation_names

    assert all(isinstance(gate, str) for gate in single_qubit_gates)
    assert all(isinstance(gate, str) for gate in two_qubit_gates)

    for q in range(device.num_qubits):
        assert isinstance(device.get_readout_fidelity(q), float | int)
        assert isinstance(device.get_readout_duration(q), float | int)
        if device.calibration is not None:
            assert isinstance(device.calibration.get_t1(q), float | int)
            assert isinstance(device.calibration.get_t2(q), float | int)

        for gate in single_qubit_gates:
            assert isinstance(device.get_single_qubit_gate_fidelity(gate, q), float | int)
            assert isinstance(device.get_single_qubit_gate_duration(gate, q), float | int)
            if device.calibration is not None:
                assert isinstance(device.calibration.compute_average_single_qubit_gate_duration(gate), float | int)
                assert isinstance(device.calibration.compute_average_single_qubit_gate_fidelity(gate), float | int)

    for q0, q1 in device.coupling_map:
        for gate in two_qubit_gates:
            assert isinstance(device.get_two_qubit_gate_fidelity(gate, q0, q1), float | int)
            assert isinstance(device.get_two_qubit_gate_duration(gate, q0, q1), float | int)
            if device.calibration is not None:
                assert isinstance(device.calibration.compute_average_two_qubit_gate_duration(gate), float | int)
                assert isinstance(device.calibration.compute_average_two_qubit_gate_fidelity(gate), float | int)
    if device.calibration is not None:
        assert isinstance(device.calibration.compute_average_readout_fidelity(), float | int)
        assert isinstance(device.calibration.compute_average_readout_duration(), float | int)


def test_get_ibm_washington_device() -> None:
    """
    Test getting the IBM Washington device.
    """
    device = IBMProvider.get_device("ibm_washington")
    single_qubit_gates = device.get_single_qubit_gates()
    two_qubit_gates = device.get_two_qubit_gates()

    assert device.name == "ibm_washington"
    assert device.num_qubits == 127

    assert all(isinstance(gate, str) for gate in single_qubit_gates)
    assert all(isinstance(gate, str) for gate in two_qubit_gates)

    for q in range(device.num_qubits):
        assert isinstance(device.get_readout_fidelity(q), float | int)
        assert isinstance(device.get_readout_duration(q), float | int)
        for gate in single_qubit_gates:
            assert isinstance(device.get_single_qubit_gate_fidelity(gate, q), float | int)
            with pytest.raises(ValueError, match="Single-qubit gate duration values not available."):
                device.get_single_qubit_gate_duration(gate, q)

    for q0, q1 in device.coupling_map:
        for gate in two_qubit_gates:
            assert isinstance(device.get_two_qubit_gate_fidelity(gate, q0, q1), float | int)
            assert isinstance(device.get_two_qubit_gate_duration(gate, q0, q1), float | int)


def test_get_ibmq_montreal_device() -> None:
    """
    Test getting the IBM Montreal device.
    """
    device = IBMProvider.get_device("ibm_montreal")
    single_qubit_gates = device.get_single_qubit_gates()
    two_qubit_gates = device.get_two_qubit_gates()

    assert device.name == "ibm_montreal"
    assert device.num_qubits == 27

    assert all(isinstance(gate, str) for gate in single_qubit_gates)
    assert all(isinstance(gate, str) for gate in two_qubit_gates)

    for q in range(device.num_qubits):
        assert isinstance(device.get_readout_fidelity(q), float | int)
        assert isinstance(device.get_readout_duration(q), float | int)
        for gate in single_qubit_gates:
            assert isinstance(device.get_single_qubit_gate_fidelity(gate, q), float | int)
            with pytest.raises(ValueError, match="Single-qubit gate duration values not available."):
                device.get_single_qubit_gate_duration(gate, q)

    for q0, q1 in device.coupling_map:
        for gate in two_qubit_gates:
            assert isinstance(device.get_two_qubit_gate_fidelity(gate, q0, q1), float | int)
            assert isinstance(device.get_two_qubit_gate_duration(gate, q0, q1), float | int)


def test_import_unsupported_backend() -> None:
    with pytest.raises(TypeError, match="Unsupported backend type <class 'str'>"):
        IBMProvider.import_qiskit_backend("V3")
