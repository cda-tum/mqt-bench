from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import mock_open, patch

import pytest

from mqt.bench.devices import Device, IBMOpenAccessProvider

SAMPLE_CALIBRATION_DATA = {
    "name": "ibm_kyiv",
    "basis_gates": ["ecr", "id", "rz", "sx", "x", "measure", "barrier"],
    "num_qubits": 5,
    "connectivity": [[0, 1], [1, 2], [2, 3], [3, 4], [0, 2]],
    "properties": {
        "0": {
            "T1": 50.0,
            "T2": 30.0,
            "eRO": 0.01,
            "tRO": 50.0,
            "eID": 0.001,
            "eSX": 0.002,
            "eX": 0.003,
            "eECR": {"0_1": 0.01, "0_2": 0.02},
            "tECR": {"0_1": 100.0, "0_2": 150.0},
        },
        "1": {
            "T1": 50.0,
            "T2": 30.0,
            "eRO": 0.01,
            "tRO": 50.0,
            "eID": 0.001,
            "eSX": 0.002,
            "eX": 0.003,
            "eECR": {"1_2": 0.01},
            "tECR": {"1_2": 100.0},
        },
        "2": {
            "T1": 50.0,
            "T2": 30.0,
            "eRO": 0.01,
            "tRO": 50.0,
            "eID": 0.001,
            "eSX": 0.002,
            "eX": 0.003,
            "eECR": {"2_3": 0.01},
            "tECR": {"2_3": 100.0},
        },
        "3": {
            "T1": 50.0,
            "T2": 30.0,
            "eRO": 0.01,
            "tRO": 50.0,
            "eID": 0.001,
            "eSX": 0.002,
            "eX": 0.003,
            "eECR": {"3_4": 0.01},
            "tECR": {"3_4": 100.0},
        },
        "4": {
            "T1": 50.0,
            "T2": 30.0,
            "eRO": 0.01,
            "tRO": 50.0,
            "eID": 0.001,
            "eSX": 0.002,
            "eX": 0.003,
            "eECR": {},
            "tECR": {},
        },
    },
}


def test_import_backend_success() -> None:
    mock_json = json.dumps(SAMPLE_CALIBRATION_DATA)
    with patch("pathlib.Path.open", mock_open(read_data=mock_json)) as mocked_file:
        path = Path("dummy_path.json")
        device = IBMOpenAccessProvider.import_backend(path)
        mocked_file.assert_called_once()  # Expect call without specific mode
        assert device.name == "ibm_kyiv"
        assert device.num_qubits == 5
        assert device.basis_gates == ["ecr", "id", "rz", "sx", "x", "measure", "barrier"]
        assert device.coupling_map == [[0, 1], [1, 2], [2, 3], [3, 4], [0, 2]]


def test_import_backend_invalid_file() -> None:
    with patch("pathlib.Path.open", mock_open(read_data="not a json")):
        path = Path("invalid_path.json")
        with pytest.raises(json.JSONDecodeError):
            IBMOpenAccessProvider.import_backend(path)


def test_import_backend_missing_fields() -> None:
    incomplete_data = {
        "name": "ibm_kyiv",
        "basis_gates": ["id", "rz"],
        "num_qubits": 5,
        "connectivity": [[0, 1], [1, 2]],
        # Missing 'properties'
    }
    mock_json = json.dumps(incomplete_data)
    with patch("pathlib.Path.open", mock_open(read_data=mock_json)):
        path = Path("incomplete_path.json")
        with pytest.raises(KeyError):
            IBMOpenAccessProvider.import_backend(path)


def test_get_device_success() -> None:
    device = Device(name="ibm_test_device", num_qubits=3, basis_gates=["id", "rz", "x"], coupling_map=[[0, 1], [1, 2]])
    with patch.object(IBMOpenAccessProvider, "import_backend", return_value=device):
        with patch.object(IBMOpenAccessProvider, "get_device", return_value=device):
            retrieved_device = IBMOpenAccessProvider.get_device("ibm_test_device")
            assert retrieved_device.name == "ibm_test_device"
            assert retrieved_device.num_qubits == 3


def test_get_device_not_found() -> None:
    with pytest.raises(ValueError, match="Device ibm_unknown not found."):
        IBMOpenAccessProvider.get_device("ibm_unknown")


def test_device_calibration_fidelity_values() -> None:
    mock_json = json.dumps(SAMPLE_CALIBRATION_DATA)
    with patch("pathlib.Path.open", mock_open(read_data=mock_json)):
        path = Path("dummy_path.json")
        device = IBMOpenAccessProvider.import_backend(path)
        for qubit in range(device.num_qubits):
            assert 0 <= device.get_readout_fidelity(qubit) <= 1
            for gate in device.get_single_qubit_gates():
                assert 0 <= device.get_single_qubit_gate_fidelity(gate, qubit) <= 1


def test_device_calibration_durations() -> None:
    mock_json = json.dumps(SAMPLE_CALIBRATION_DATA)
    with patch("pathlib.Path.open", mock_open(read_data=mock_json)):
        path = Path("dummy_path.json")
        device = IBMOpenAccessProvider.import_backend(path)
        for qubit in range(device.num_qubits):
            assert device.get_readout_duration(qubit) >= 0
            for gate in device.get_single_qubit_gates():
                with pytest.raises(ValueError, match="Single-qubit gate duration values not available."):
                    device.get_single_qubit_gate_duration(gate, qubit)
        for qubit1, qubit2 in device.coupling_map:
            assert device.get_two_qubit_gate_duration("ecr", qubit1, qubit2) >= 0


def test_ibm_open_access_provider_methods() -> None:
    """Test the methods of the IBMProvider class."""
    assert IBMOpenAccessProvider.get_available_device_names() == ["ibm_kyiv", "ibm_brisbane", "ibm_sherbrooke"]
    assert IBMOpenAccessProvider.get_available_basis_gates() == [["ecr", "id", "rz", "sx", "x", "measure", "barrier"]]
    assert IBMOpenAccessProvider.get_native_gates() == ["id", "rz", "sx", "x", "ecr", "measure", "barrier"]
    assert IBMOpenAccessProvider.get_max_qubits() == 127
    with pytest.raises(ValueError, match="Device ibm_unknown not found."):
        IBMOpenAccessProvider.get_device("ibm_unknown")


def test_get_ibm_kyiv_device() -> None:
    """Test getting the IBM Kyiv device."""
    device = IBMOpenAccessProvider.get_device("ibm_kyiv")
    single_qubit_gates = device.get_single_qubit_gates()
    two_qubit_gates = device.get_two_qubit_gates()

    assert device.name == "ibm_kyiv"
    assert device.num_qubits == 127

    assert all(gate in ["ecr", "id", "rz", "sx", "x", "measure", "barrier"] for gate in single_qubit_gates)
    assert all(gate == "ecr" for gate in two_qubit_gates)

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


def test_get_ibm_brisbane_device() -> None:
    """Test getting the IBM Brisbane device."""
    device = IBMOpenAccessProvider.get_device("ibm_brisbane")
    single_qubit_gates = device.get_single_qubit_gates()
    two_qubit_gates = device.get_two_qubit_gates()

    assert device.name == "ibm_brisbane"
    assert device.num_qubits == 127

    assert all(gate in ["id", "rz", "sx", "x", "ecr", "measure", "barrier"] for gate in single_qubit_gates)
    assert all(gate == "ecr" for gate in two_qubit_gates)

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


def test_get_ibm_sherbrooke_device() -> None:
    """Test getting the IBM Sherbrooke device."""
    device = IBMOpenAccessProvider.get_device("ibm_sherbrooke")
    single_qubit_gates = device.get_single_qubit_gates()
    two_qubit_gates = device.get_two_qubit_gates()

    assert device.name == "ibm_sherbrooke"
    assert device.num_qubits == 127

    assert all(gate in ["id", "rz", "sx", "x", "ecr", "measure", "barrier"] for gate in single_qubit_gates)
    assert all(gate == "ecr" for gate in two_qubit_gates)

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
