from __future__ import annotations

import json
from typing import TYPE_CHECKING, TypedDict, cast

if TYPE_CHECKING:
    from pathlib import Path

from mqt.bench.devices import Device, DeviceCalibration, Provider

Fidelity = TypedDict("Fidelity", {"1q": float, "2q": float, "readout": float})
Timing = TypedDict("Timing", {"t1": float, "t2": float, "1q": float, "2q": float, "readout": float})


class IQMCalibration(TypedDict):
    """Class to store the calibration data of an IQM device.
    Follows https://docs.iqm.com/#tag/characterizations.
    """

    name: str
    basis_gates: list[str]
    connectivity: list[list[int]]
    fidelity: Fidelity
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
    def import_backend(cls, path: Path) -> Device:
        """Import an iqm backend as a Device object.

        Args:
            path: the path to the JSON file containing the calibration data.

        Returns: the Device object
        """
        with path.open() as json_file:
            iqm_calibration = cast(IQMCalibration, json.load(json_file))

        device = Device()
        device.name = iqm_calibration["name"]
        device.num_qubits = iqm_calibration["num_qubits"]
        device.basis_gates = iqm_calibration["basis_gates"]
        device.coupling_map = list(iqm_calibration["connectivity"])
        calibration = DeviceCalibration()
        for qubit in range(device.num_qubits):
            calibration.single_qubit_gate_fidelity[qubit] = dict.fromkeys(
                ["r"], 1. - iqm_calibration["error"]["1q"][str(qubit)]
            )
            calibration.single_qubit_gate_duration[qubit] = dict.fromkeys(
                ["r"], iqm_calibration["timing"]["1q"]
            )
            calibration.readout_fidelity[qubit] = iqm_calibration["error"]["readout"][str(qubit)]
            calibration.readout_duration[qubit] = iqm_calibration["timing"]["readout"]
            calibration.t1[qubit] = iqm_calibration["timing"]["t1"][str(qubit)]
            calibration.t2[qubit] = iqm_calibration["timing"]["t2"][str(qubit)]

        for qubit1, qubit2 in device.coupling_map:
            if (qubit1, qubit2) in calibration.two_qubit_gate_fidelity.keys():
                continue # Skip reverse direction
            calibration.two_qubit_gate_fidelity[(qubit1, qubit2)] = {"cz": 1. - iqm_calibration["error"]["2q"][str(qubit1) + '-' + str(qubit2)]}
            calibration.two_qubit_gate_duration[(qubit1, qubit2)] = {"cz": iqm_calibration["timing"]["2q"]}
            # Same values for the reverse direction
            calibration.two_qubit_gate_fidelity[(qubit2, qubit1)] = calibration.two_qubit_gate_fidelity[(qubit1, qubit2)]
            calibration.two_qubit_gate_duration[(qubit2, qubit1)] = calibration.two_qubit_gate_duration[(qubit1, qubit2)]
        
        device.calibration = calibration
        return device
