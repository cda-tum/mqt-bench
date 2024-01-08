from __future__ import annotations

import json
from typing import TYPE_CHECKING, TypedDict, cast

if TYPE_CHECKING:
    from pathlib import Path

from mqt.bench.devices import Device, DeviceCalibration, Provider


class Statistics(TypedDict):
    mean: float


Fidelity = TypedDict("Fidelity", {"1q": Statistics, "2q": Statistics, "spam": Statistics})
Timing = TypedDict("Timing", {"t1": float, "t2": float, "1q": float, "2q": float, "readout": float, "reset": float})


class IonQCalibration(TypedDict):
    """
    Class to store the calibration data of an IonQ device.
    Follows https://docs.ionq.com/#tag/characterizations
    """

    name: str
    basis_gates: list[str]
    connectivity: list[list[int]]
    fidelity: Fidelity
    num_qubits: int
    timing: Timing


class IonQProvider(Provider):
    """
    Class to manage IonQ devices.
    """

    provider_name = "ionq"

    @classmethod
    def get_available_device_names(cls) -> list[str]:
        """
        Get the names of all available IonQ devices.
        """
        return ["ionq_harmony", "ionq_aria1"]  # NOTE: update when adding new devices

    @classmethod
    def get_native_gates(cls) -> list[str]:
        """
        Get a list of provider specific native gates.
        """
        return ["rxx", "rz", "ry", "rx", "measure", "barrier"]  # harmony, aria1

    @classmethod
    def import_backend(cls, path: Path) -> Device:
        """
        Import an IonQ backend as a Device object.
        Args:
            path: the path to the JSON file containing the calibration data

        Returns: the Device object
        """
        with path.open() as json_file:
            ionq_calibration = cast(IonQCalibration, json.load(json_file))

        device = Device()
        device.name = ionq_calibration["name"]
        device.num_qubits = ionq_calibration["num_qubits"]
        device.basis_gates = ionq_calibration["basis_gates"]
        device.coupling_map = list(ionq_calibration["connectivity"])
        calibration = DeviceCalibration()
        for qubit in range(device.num_qubits):
            calibration.single_qubit_gate_fidelity[qubit] = {
                gate: ionq_calibration["fidelity"]["1q"]["mean"] for gate in ["ry", "rx"]
            }
            calibration.single_qubit_gate_fidelity[qubit]["rz"] = 1  # rz is always perfect
            calibration.single_qubit_gate_duration[qubit] = {
                gate: ionq_calibration["timing"]["1q"] for gate in ["ry", "rx"]
            }
            calibration.single_qubit_gate_duration[qubit]["rz"] = 0  # rz is always instantaneous
            calibration.readout_fidelity[qubit] = ionq_calibration["fidelity"]["spam"]["mean"]
            calibration.readout_duration[qubit] = ionq_calibration["timing"]["readout"]
            calibration.t1[qubit] = ionq_calibration["timing"]["t1"]
            calibration.t2[qubit] = ionq_calibration["timing"]["t2"]

        for qubit1, qubit2 in device.coupling_map:
            calibration.two_qubit_gate_fidelity[(qubit1, qubit2)] = {"rxx": ionq_calibration["fidelity"]["2q"]["mean"]}
            calibration.two_qubit_gate_duration[(qubit1, qubit2)] = {"rxx": ionq_calibration["timing"]["2q"]}
        device.calibration = calibration
        return device
