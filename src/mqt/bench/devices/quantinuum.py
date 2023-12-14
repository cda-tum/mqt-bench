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


class QuantinuumCalibration(TypedDict):
    """
    Class to store the calibration data of an Quantinuum device.
    Follows https://docs.quantinuum.com/#tag/characterizations
    """

    machine: str
    connectivity: list[list[int]]
    date: int
    fidelity: Fidelity
    qubits: int
    timing: Timing


class QuantinuumProvider(Provider):
    """
    Class to manage Quantinuum devices.
    """

    provider_name = "quantinuum"

    @classmethod
    def get_available_device_names(cls) -> list[str]:
        """
        Get the names of all available Quantinuum devices.
        """
        return ["quantinuum_h2"]

    @classmethod
    def get_max_qubits(cls) -> int:
        """
        Get the maximum number of qubits of all available Quantinuum devices.
        """
        return 32

    @classmethod
    def import_backend(cls, path: Path) -> Device:
        """
        Import an Quantinuum backend as a Device object.
        Args:
            path: the path to the JSON file containing the calibration data

        Returns: the Device object
        """
        with path.open() as json_file:
            quantinuum_calibration = cast(QuantinuumCalibration, json.load(json_file))

        device = Device()
        device.name = quantinuum_calibration["machine"]
        device.num_qubits = quantinuum_calibration["qubits"]
        device.basis_gates = ["rxx", "rz", "ry", "rx", "measure", "barrier"]
        device.coupling_map = [[a, b] for a, b in quantinuum_calibration["connectivity"]] + [
            [b, a] for a, b in quantinuum_calibration["connectivity"]
        ]
        calibration = DeviceCalibration()
        for qubit in range(device.num_qubits):
            calibration.single_qubit_gate_fidelity[qubit] = {
                gate: quantinuum_calibration["fidelity"]["1q"]["mean"] for gate in ["ry", "rx"]
            }
            calibration.single_qubit_gate_fidelity[qubit]["rz"] = 1  # rz is always perfect
            calibration.single_qubit_gate_duration[qubit] = {
                gate: quantinuum_calibration["timing"]["1q"] for gate in ["ry", "rx"]
            }
            calibration.single_qubit_gate_duration[qubit]["rz"] = 0  # rz is always instantaneous
            calibration.readout_fidelity[qubit] = quantinuum_calibration["fidelity"]["spam"]["mean"]
            calibration.readout_duration[qubit] = quantinuum_calibration["timing"]["readout"]
            calibration.t1[qubit] = quantinuum_calibration["timing"]["t1"]
            calibration.t2[qubit] = quantinuum_calibration["timing"]["t2"]

        for qubit1, qubit2 in device.coupling_map:
            calibration.two_qubit_gate_fidelity[(qubit1, qubit2)] = {"rxx": quantinuum_calibration["fidelity"]["2q"]["mean"]}
            calibration.two_qubit_gate_duration[(qubit1, qubit2)] = {"rxx": quantinuum_calibration["timing"]["2q"]}
        device.calibration = calibration
        return device
