from __future__ import annotations

import json
from typing import TYPE_CHECKING, TypedDict, cast

if TYPE_CHECKING:
    from pathlib import Path

from mqt.bench.devices import Device, DeviceCalibration, Provider


class Statistics(TypedDict):
    mean: float


Fidelity = TypedDict("Fidelity", {"1q": Statistics, "2q": Statistics, "spam": Statistics})


class QuantinuumCalibration(TypedDict):
    """
    Class to store the calibration data of an Quantinuum device.
    Follows https://docs.quantinuum.com/#tag/characterizations
    """

    name: str
    basis_gates: list[str]
    connectivity: list[list[int]]
    fidelity: Fidelity
    num_qubits: int


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
        return ["quantinuum_h2"]  # NOTE: update when adding new devices

    @classmethod
    def get_native_gates(cls) -> list[str]:
        """
        Get a list of provider specific native gates.
        """
        return ["rzz", "rz", "ry", "rx", "measure", "barrier"]  # h2

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
        device.name = quantinuum_calibration["name"]
        device.num_qubits = quantinuum_calibration["num_qubits"]
        device.basis_gates = quantinuum_calibration["basis_gates"]
        device.coupling_map = list(quantinuum_calibration["connectivity"])
        calibration = DeviceCalibration()
        for qubit in range(device.num_qubits):
            calibration.single_qubit_gate_fidelity[qubit] = {
                gate: quantinuum_calibration["fidelity"]["1q"]["mean"] for gate in ["ry", "rx"]
            }
            calibration.single_qubit_gate_fidelity[qubit]["rz"] = 1  # rz is always perfect
            calibration.readout_fidelity[qubit] = quantinuum_calibration["fidelity"]["spam"]["mean"]

        for qubit1, qubit2 in device.coupling_map:
            calibration.two_qubit_gate_fidelity[(qubit1, qubit2)] = {
                "rzz": quantinuum_calibration["fidelity"]["2q"]["mean"]
            }
        device.calibration = calibration
        return device
