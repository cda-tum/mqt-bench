# Copyright (c) 2023 - 2025 Chair for Design Automation, TUM
# Copyright (c) 2025 Munich Quantum Software Company GmbH
# All rights reserved.
#
# SPDX-License-Identifier: MIT
#
# Licensed under the MIT License

"""Module to manage Quantinuum devices."""

from __future__ import annotations

import json
from typing import TypedDict, cast

from .calibration import DeviceCalibration, get_device_calibration_path
from .device import Device, Gateset


class QuantinuumH2(Device):
    """Quantinuum H2 device."""

    def __init__(self) -> None:
        """Initialize the Quantinuum device."""
        with get_device_calibration_path("quantinuum_h2").open() as json_file:
            self.quantinuum_calibration = cast("QuantinuumCalibration", json.load(json_file))
        self.calibration = None

        self.name = self.quantinuum_calibration["name"]
        self.gateset = Gateset("quantinuum", self.quantinuum_calibration["basis_gates"])
        self.num_qubits = self.quantinuum_calibration["num_qubits"]
        self.coupling_map = list(self.quantinuum_calibration["connectivity"])

    def read_calibration(self) -> None:
        """Read the calibration data for the device."""
        calibration = DeviceCalibration()
        for qubit in range(self.num_qubits):
            calibration.single_qubit_gate_fidelity[qubit] = dict.fromkeys(
                ["ry", "rx"], self.quantinuum_calibration["fidelity"]["1q"]["mean"]
            )
            calibration.single_qubit_gate_fidelity[qubit]["rz"] = 1  # rz is always perfect
            calibration.readout_fidelity[qubit] = self.quantinuum_calibration["fidelity"]["spam"]["mean"]

        for qubit1, qubit2 in self.coupling_map:
            calibration.two_qubit_gate_fidelity[qubit1, qubit2] = {
                "rzz": self.quantinuum_calibration["fidelity"]["2q"]["mean"]
            }
        self.calibration = calibration


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
