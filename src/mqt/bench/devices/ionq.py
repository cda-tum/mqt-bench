# Copyright (c) 2023 - 2025 Chair for Design Automation, TUM
# Copyright (c) 2025 Munich Quantum Software Company GmbH
# All rights reserved.
#
# SPDX-License-Identifier: MIT
#
# Licensed under the MIT License

"""IonQ devices."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING, TypedDict, cast

from .calibration import DeviceCalibration, get_device_calibration_path
from .device import Device, Gateset

if TYPE_CHECKING:
    from pathlib import Path


class IonQDevice(Device):
    """IonQ device."""

    def __init__(self, calibration_path: Path) -> None:
        """Initialize the IonQ device."""
        with calibration_path.open() as json_file:
            self.ionq_calibration = cast("IonQCalibration", json.load(json_file))
        self.calibration = None

        self.name = self.ionq_calibration["name"]
        self.gateset = Gateset("ionq", self.ionq_calibration["basis_gates"])
        self.num_qubits = self.ionq_calibration["num_qubits"]
        self.coupling_map = list(self.ionq_calibration["connectivity"])

    def read_calibration(self) -> None:
        """Read the calibration data for the device."""
        calibration = DeviceCalibration()
        for qubit in range(self.num_qubits):
            calibration.single_qubit_gate_fidelity[qubit] = dict.fromkeys(
                ["ry", "rx"], self.ionq_calibration["fidelity"]["1q"]["mean"]
            )
            calibration.single_qubit_gate_fidelity[qubit]["rz"] = 1  # rz is always perfect
            calibration.single_qubit_gate_duration[qubit] = dict.fromkeys(
                ["ry", "rx"], self.ionq_calibration["timing"]["1q"]
            )
            calibration.single_qubit_gate_duration[qubit]["rz"] = 0  # rz is always instantaneous
            calibration.readout_fidelity[qubit] = self.ionq_calibration["fidelity"]["spam"]["mean"]
            calibration.readout_duration[qubit] = self.ionq_calibration["timing"]["readout"]
            calibration.t1[qubit] = self.ionq_calibration["timing"]["t1"]
            calibration.t2[qubit] = self.ionq_calibration["timing"]["t2"]

        for qubit1, qubit2 in self.coupling_map:
            calibration.two_qubit_gate_fidelity[qubit1, qubit2] = {
                "rxx": self.ionq_calibration["fidelity"]["2q"]["mean"]
            }
            calibration.two_qubit_gate_duration[qubit1, qubit2] = {"rxx": self.ionq_calibration["timing"]["2q"]}
        self.calibration = calibration


class IonQHarmony(IonQDevice):
    """IonQ Harmony device."""

    def __init__(self) -> None:
        """Initialize the IonQ Harmony device."""
        super().__init__(get_device_calibration_path("ionq_harmony"))


class IonQAria1(IonQDevice):
    """IonQ Aria1 device."""

    def __init__(self) -> None:
        """Initialize the IonQ Aria1 device."""
        super().__init__(get_device_calibration_path("ionq_aria1"))


class Statistics(TypedDict):
    """Class to store the statistics of a gate or measurement."""

    mean: float


Fidelity = TypedDict("Fidelity", {"1q": Statistics, "2q": Statistics, "spam": Statistics})
Timing = TypedDict("Timing", {"t1": float, "t2": float, "1q": float, "2q": float, "readout": float, "reset": float})


class IonQCalibration(TypedDict):
    """Class to store the calibration data of an IonQ device. Follows https://docs.ionq.com/#tag/characterizations."""

    name: str
    basis_gates: list[str]
    connectivity: list[list[int]]
    fidelity: Fidelity
    num_qubits: int
    timing: Timing
