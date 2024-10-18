"""Module to manage IQM devices."""

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


class Infidelity(TypedDict):
    """Class to store the infidelity properties of a IQM device."""

    one_q: dict[str, float]
    two_q: dict[str, float]
    readout: dict[str, float]


class Timing(TypedDict):
    """Class to store the time properties of a IQM device."""

    t1: dict[str, float]
    t2: dict[str, float]
    one_q: float
    two_q: float
    readout: float


class IQMCalibration(TypedDict):
    """Class to store the calibration data of an IQM device.

    Follows https://docs.iqm.com/#tag/characterizations.
    """

    name: str
    basis_gates: list[str]
    connectivity: list[list[int]]
    error: Infidelity
    num_qubits: int
    timing: Timing


class IQMProvider(Provider):
    """Class to manage IQM devices."""

    provider_name = "iqm"

    @classmethod
    def get_available_device_names(cls) -> list[str]:
        """Get the names of all available IQM devices."""
        return ["iqm_adonis", "iqm_apollo"]  # NOTE: update when adding new devices

    @classmethod
    def get_native_gates(cls) -> list[str]:
        """Get a list of provider specific native gates."""
        return ["r", "cz", "measure", "barrier"]

    @classmethod
    def import_backend(cls, name: str) -> Device:
        """Import an iqm backend as a Device object.

        Arguments:
            name (str): The name of the iqm backend whose calibration data needs to be imported.
                            This name will be used to locate the corresponding JSON calibration file.

        Returns:
            Device: An instance of `Device`, loaded with the calibration data from the JSON file.
        """
        ref = resources.files("mqt.bench") / "calibration_files" / f"{name}_calibration.json"

        with resources.as_file(ref) as json_path, json_path.open() as json_file:
            # Load the JSON data and cast it to QuantinuumCalibration
            iqm_calibration = cast(IQMCalibration, json.load(json_file))

        device = Device()
        device.name = iqm_calibration["name"]
        device.num_qubits = iqm_calibration["num_qubits"]
        device.basis_gates = iqm_calibration["basis_gates"]
        device.coupling_map = list(iqm_calibration["connectivity"])
        calibration = DeviceCalibration()
        for qubit in range(device.num_qubits):
            calibration.single_qubit_gate_fidelity[qubit] = dict.fromkeys(
                ["r"], 1.0 - iqm_calibration["error"]["one_q"][str(qubit)]
            )
            calibration.single_qubit_gate_duration[qubit] = dict.fromkeys(
                ["r"],
                iqm_calibration["timing"]["one_q"] * 1e-9,  # ns to s
            )
            calibration.readout_fidelity[qubit] = 1.0 - iqm_calibration["error"]["readout"][str(qubit)]
            calibration.readout_duration[qubit] = iqm_calibration["timing"]["readout"] * 1e-9  # ns to s
            calibration.t1[qubit] = iqm_calibration["timing"]["t1"][str(qubit)] * 1e-9  # ns to s
            calibration.t2[qubit] = iqm_calibration["timing"]["t2"][str(qubit)] * 1e-9  # ns to s

        for qubit1, qubit2 in device.coupling_map:
            if (qubit1, qubit2) in calibration.two_qubit_gate_fidelity:
                continue  # Skip reverse direction
            calibration.two_qubit_gate_fidelity[qubit1, qubit2] = {
                "cz": 1.0 - iqm_calibration["error"]["two_q"][str(qubit1) + "-" + str(qubit2)]
            }
            calibration.two_qubit_gate_duration[qubit1, qubit2] = {
                "cz": iqm_calibration["timing"]["two_q"] * 1e-9  # ns to s
            }

            # Same values for the reverse direction
            calibration.two_qubit_gate_fidelity[qubit2, qubit1] = calibration.two_qubit_gate_fidelity[qubit1, qubit2]
            calibration.two_qubit_gate_duration[qubit2, qubit1] = calibration.two_qubit_gate_duration[qubit1, qubit2]

        device.calibration = calibration
        return device
