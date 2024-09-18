"""Test the IBMProvider class and the IBM Washington and IBM Montreal devices."""

from __future__ import annotations

import pytest
from qiskit_ibm_runtime.fake_provider import FakeMontrealV2

from mqt.bench.devices import IBMProvider


def test_ibm_provider_methods() -> None:
    """Test the methods of the IBMProvider class."""
    assert IBMProvider.get_available_device_names() == ["ibm_washington", "ibm_montreal"]
    assert IBMProvider.get_available_basis_gates() == [["id", "rz", "sx", "x", "cx", "measure", "barrier"]]
    assert IBMProvider.get_native_gates() == ["id", "rz", "sx", "x", "cx", "measure", "barrier"]
    assert IBMProvider.get_max_qubits() == 127
    with pytest.raises(ValueError, match="Device ibm_unknown not found."):
        IBMProvider.get_device("ibm_unknown")


def test_import_v2_backend() -> None:
    """Test importing a Qiskit `BackendV2` object."""
    backend = FakeMontrealV2()
    device = IBMProvider.import_qiskit_backend(backend)
    single_qubit_gates = device.get_single_qubit_gates()
    two_qubit_gates = device.get_two_qubit_gates()

    assert device.name == backend.name
    assert device.num_qubits == backend.num_qubits
    assert device.coupling_map == backend.coupling_map.get_edges()
    assert device.basis_gates == backend.operation_names

    assert all(gate in ["id", "rz", "sx", "x", "cx", "measure", "barrier"] for gate in single_qubit_gates)
    assert all(gate == "cx" for gate in two_qubit_gates)

    for q in range(device.num_qubits):
        assert 0 <= device.get_readout_fidelity(q) <= 1
        assert device.get_readout_duration(q) >= 0
        if device.calibration is not None:
            assert device.calibration.get_t1(q) >= 0
            assert device.calibration.get_t2(q) >= 0

        for gate in single_qubit_gates:
            assert 0 <= device.get_single_qubit_gate_fidelity(gate, q) <= 1
            assert device.get_single_qubit_gate_duration(gate, q) >= 0
            if device.calibration is not None:
                assert 0 <= device.calibration.compute_average_single_qubit_gate_fidelity(gate) <= 1
                assert device.calibration.compute_average_single_qubit_gate_duration(gate) >= 0

    for q0, q1 in device.coupling_map:
        for gate in two_qubit_gates:
            assert 0 <= device.get_two_qubit_gate_fidelity(gate, q0, q1) <= 1
            assert device.get_two_qubit_gate_duration(gate, q0, q1) >= 0
            if device.calibration is not None:
                assert 0 <= device.calibration.compute_average_two_qubit_gate_fidelity(gate) <= 1
                assert device.calibration.compute_average_two_qubit_gate_duration(gate) >= 0

    if device.calibration is not None:
        assert 0 <= device.calibration.compute_average_readout_fidelity() <= 1
        assert device.calibration.compute_average_readout_duration() >= 0


def test_get_ibm_washington_device() -> None:
    """Test getting the IBM Washington device."""
    device = IBMProvider.get_device("ibm_washington")
    single_qubit_gates = device.get_single_qubit_gates()
    two_qubit_gates = device.get_two_qubit_gates()

    assert device.name == "ibm_washington"
    assert device.num_qubits == 127

    assert all(gate in ["id", "rz", "sx", "x", "cx", "measure", "barrier"] for gate in single_qubit_gates)
    assert all(gate == "cx" for gate in two_qubit_gates)

    for q in range(device.num_qubits):
        assert 0 <= device.get_readout_fidelity(q) <= 1
        assert device.get_readout_duration(q) >= 0

        for gate in single_qubit_gates:
            assert 0 <= device.get_single_qubit_gate_fidelity(gate, q) <= 1
            with pytest.raises(ValueError, match="Single-qubit gate duration values not available."):
                device.get_single_qubit_gate_duration(gate, q)

    for q0, q1 in device.coupling_map:
        for gate in two_qubit_gates:
            assert 0 <= device.get_two_qubit_gate_fidelity(gate, q0, q1) <= 1
            assert device.get_two_qubit_gate_duration(gate, q0, q1) >= 0


def test_get_ibmq_montreal_device() -> None:
    """Test getting the IBM Montreal device."""
    device = IBMProvider.get_device("ibm_montreal")
    single_qubit_gates = device.get_single_qubit_gates()
    two_qubit_gates = device.get_two_qubit_gates()

    assert device.name == "ibm_montreal"
    assert device.num_qubits == 27

    assert all(gate in ["id", "rz", "sx", "x", "cx", "measure", "barrier"] for gate in single_qubit_gates)
    assert all(gate == "cx" for gate in two_qubit_gates)

    for q in range(device.num_qubits):
        assert 0 <= device.get_readout_fidelity(q) <= 1
        assert device.get_readout_duration(q) >= 0

        for gate in single_qubit_gates:
            assert 0 <= device.get_single_qubit_gate_fidelity(gate, q) <= 1
            with pytest.raises(ValueError, match="Single-qubit gate duration values not available."):
                device.get_single_qubit_gate_duration(gate, q)
    for q0, q1 in device.coupling_map:
        for gate in two_qubit_gates:
            assert 0 <= device.get_two_qubit_gate_fidelity(gate, q0, q1) <= 1
            assert device.get_two_qubit_gate_duration(gate, q0, q1) >= 0
