# Copyright (c) 2023 - 2025 Chair for Design Automation, TUM
# Copyright (c) 2025 Munich Quantum Software Company GmbH
# All rights reserved.
#
# SPDX-License-Identifier: MIT
#
# Licensed under the MIT License

"""Module to manage IQM devices."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING, TypedDict, cast

from .calibration import DeviceCalibration, get_device_calibration_path
from .device import Device, Gateset

if TYPE_CHECKING:
    from pathlib import Path


class IQMDevice(Device):
    """IQM device."""

    def __init__(self, calibration_path: Path) -> None:
        """Initialize the device."""
        with calibration_path.open() as json_file:
            self.iqm_calibration = cast("IQMCalibration", json.load(json_file))
        self.calibration = None

        self.name = self.iqm_calibration["name"]
        self.gateset = Gateset("iqm", self.iqm_calibration["basis_gates"])
        self.num_qubits = self.iqm_calibration["num_qubits"]
        self.coupling_map = list(self.iqm_calibration["connectivity"])

    def read_calibration(self) -> None:
        """Read the calibration data for the device."""
        calibration = DeviceCalibration()
        for qubit in range(self.num_qubits):
            calibration.single_qubit_gate_fidelity[qubit] = dict.fromkeys(
                ["r"], 1.0 - self.iqm_calibration["error"]["one_q"][str(qubit)]
            )
            calibration.single_qubit_gate_duration[qubit] = dict.fromkeys(
                ["r"],
                self.iqm_calibration["timing"]["one_q"] * 1e-9,  # ns to s
            )
            calibration.readout_fidelity[qubit] = 1.0 - self.iqm_calibration["error"]["readout"][str(qubit)]
            calibration.readout_duration[qubit] = self.iqm_calibration["timing"]["readout"] * 1e-9  # ns to s
            calibration.t1[qubit] = self.iqm_calibration["timing"]["t1"][str(qubit)] * 1e-9  # ns to s
            calibration.t2[qubit] = self.iqm_calibration["timing"]["t2"][str(qubit)] * 1e-9  # ns to s

        for qubit1, qubit2 in self.coupling_map:
            if (qubit1, qubit2) in calibration.two_qubit_gate_fidelity:
                continue  # Skip reverse direction
            calibration.two_qubit_gate_fidelity[qubit1, qubit2] = {
                "cz": 1.0 - self.iqm_calibration["error"]["two_q"][str(qubit1) + "-" + str(qubit2)]
            }
            calibration.two_qubit_gate_duration[qubit1, qubit2] = {
                "cz": self.iqm_calibration["timing"]["two_q"] * 1e-9  # ns to s
            }

            # Same values for the reverse direction
            calibration.two_qubit_gate_fidelity[qubit2, qubit1] = calibration.two_qubit_gate_fidelity[qubit1, qubit2]
            calibration.two_qubit_gate_duration[qubit2, qubit1] = calibration.two_qubit_gate_duration[qubit1, qubit2]

        self.calibration = calibration


class IQMAdonis(IQMDevice):
    """IQM Adonis device."""

    def __init__(self) -> None:
        """Initialize the IQM Adonis device."""
        super().__init__(get_device_calibration_path("iqm_adonis"))


class IQMApollo(IQMDevice):
    """IQM Apollo device."""

    def __init__(self) -> None:
        """Initialize the IQM Apollo device."""
        super().__init__(get_device_calibration_path("iqm_apollo"))


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
