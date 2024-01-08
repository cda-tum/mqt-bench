from __future__ import annotations

import json
from typing import TYPE_CHECKING, TypedDict, cast

if TYPE_CHECKING:
    from pathlib import Path

from mqt.bench.devices import Device, DeviceCalibration, Provider


class QubitProperties(TypedDict):
    """
    Class to store the properties of a single qubit.
    """

    T1: float
    T2: float
    fRB: float
    fRO: float
    qubit: float


class Coupling(TypedDict):
    """
    Class to store the connectivity of a two-qubit gate.
    """

    control_qubit: float
    target_qubit: float


class TwoQubitProperties(TypedDict):
    """
    Class to store the properties of a two-qubit gate.
    """

    coupling: Coupling
    fCX: float


class Properties(TypedDict):
    """
    Class to store the properties of a device.
    """

    one_qubit: dict[str, QubitProperties]
    two_qubit: dict[str, TwoQubitProperties]


class OQCCalibration(TypedDict):
    """
    Class to store the calibration data of an OQC device.
    """

    name: str
    basis_gates: list[str]
    num_qubits: int
    connectivity: list[list[int]]
    properties: Properties


class OQCProvider(Provider):
    """
    Class to manage OQC devices
    """

    provider_name = "oqc"

    @classmethod
    def get_available_device_names(cls) -> list[str]:
        """
        Get the names of all available OQC devices.
        """
        return ["oqc_lucy"]  # NOTE: update when adding new devices

    @classmethod
    def get_native_gates(cls) -> list[str]:
        """
        Get a list of provider specific native gates.
        """
        return ["rz", "sx", "x", "ecr", "measure", "barrier"]  # lucy

    @classmethod
    def import_backend(cls, path: Path) -> Device:
        """
        Import an OQC backend.
        Args:
            path: the path to the JSON file containing the calibration data

        Returns: the Device object
        """
        with path.open() as json_file:
            oqc_calibration = cast(OQCCalibration, json.load(json_file))

        device = Device()
        device.name = oqc_calibration["name"]
        device.num_qubits = oqc_calibration["num_qubits"]
        device.basis_gates = oqc_calibration["basis_gates"]
        device.coupling_map = list(oqc_calibration["connectivity"])

        calibration = DeviceCalibration()
        for qubit in range(device.num_qubits):
            calibration.single_qubit_gate_fidelity[qubit] = {
                gate: oqc_calibration["properties"]["one_qubit"][str(qubit)]["fRB"] for gate in ["rz", "sx", "x"]
            }
            calibration.readout_fidelity[qubit] = oqc_calibration["properties"]["one_qubit"][str(qubit)]["fRO"]
            calibration.t1[qubit] = oqc_calibration["properties"]["one_qubit"][str(qubit)]["T1"]
            calibration.t2[qubit] = oqc_calibration["properties"]["one_qubit"][str(qubit)]["T2"]

        for qubit1, qubit2 in device.coupling_map:
            calibration.two_qubit_gate_fidelity[(qubit1, qubit2)] = {
                gate: oqc_calibration["properties"]["two_qubit"][f"{qubit1}-{qubit2}"]["fCX"] for gate in ["ecr"]
            }
        device.calibration = calibration
        return device
