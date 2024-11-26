"""Module to manage Quantinuum devices."""

from __future__ import annotations

import json
import sys
from typing import TYPE_CHECKING, TypedDict, cast

from .calibration import DeviceCalibration
from .device import Device
from .provider import Provider

if TYPE_CHECKING or sys.version_info >= (3, 10, 0):
    from importlib import resources
else:
    import importlib_resources as resources


class Statistics(TypedDict):
    """Class to store the statistics of a gate or measurement."""

    mean: float


Fidelity = TypedDict("Fidelity", {"1q": Statistics, "2q": Statistics, "spam": Statistics})


class QuantinuumCalibration(TypedDict):
    """Class to store the calibration data of a Quantinuum device. Follows https://docs.quantinuum.com/#tag/characterizations."""

    name: str
    basis_gates: list[str]
    connectivity: list[list[int]]
    fidelity: Fidelity
    num_qubits: int


class QuantinuumProvider(Provider):
    """Class to manage Quantinuum devices."""

    provider_name = "quantinuum"

    @classmethod
    def get_available_device_names(cls) -> list[str]:
        """Get the names of all available Quantinuum devices."""
        return ["quantinuum_h2"]  # NOTE: update when adding new devices

    @classmethod
    def get_native_gates(cls) -> list[str]:
        """Get a list of provider specific native gates."""
        return ["rzz", "rz", "ry", "rx", "measure", "barrier"]  # h2

    @classmethod
    def import_backend(cls, name: str) -> Device:
        """Import an Quantinuum backend as a Device object.

        Arguments:
            name (str): The name of the Quantinuum backend whose calibration data needs to be imported.
                            This name will be used to locate the corresponding JSON calibration file.

        Returns:
            Device: An instance of `Device`, loaded with the calibration data from the JSON file.
        """
        # Assuming 'name' is already defined
        ref = resources.files("mqt.bench") / "calibration_files" / f"{name}_calibration.json"

        with resources.as_file(ref) as json_path, json_path.open() as json_file:
            # Load the JSON data and cast it to QuantinuumCalibration
            quantinuum_calibration = cast(QuantinuumCalibration, json.load(json_file))

        device = Device()
        device.name = quantinuum_calibration["name"]
        device.num_qubits = quantinuum_calibration["num_qubits"]
        device.basis_gates = quantinuum_calibration["basis_gates"]
        device.coupling_map = list(quantinuum_calibration["connectivity"])
        calibration = DeviceCalibration()
        for qubit in range(device.num_qubits):
            calibration.single_qubit_gate_fidelity[qubit] = dict.fromkeys(
                ["ry", "rx"], quantinuum_calibration["fidelity"]["1q"]["mean"]
            )
            calibration.single_qubit_gate_fidelity[qubit]["rz"] = 1  # rz is always perfect
            calibration.readout_fidelity[qubit] = quantinuum_calibration["fidelity"]["spam"]["mean"]

        for qubit1, qubit2 in device.coupling_map:
            calibration.two_qubit_gate_fidelity[qubit1, qubit2] = {
                "rzz": quantinuum_calibration["fidelity"]["2q"]["mean"]
            }
        device.calibration = calibration
        return device
