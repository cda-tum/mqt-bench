# Copyright (c) 2023 - 2025 Chair for Design Automation, TUM
# Copyright (c) 2025 Munich Quantum Software Company GmbH
# All rights reserved.
#
# SPDX-License-Identifier: MIT
#
# Licensed under the MIT License

"""Module to manage OQC devices."""

from __future__ import annotations

import json
from typing import TypedDict, cast

from .calibration import DeviceCalibration, get_device_calibration_path
from .device import Device, Gateset


class OQCLucy(Device):
    """OQC Lucy device."""

    def __init__(self) -> None:
        """Initialize the OQC device."""
        with get_device_calibration_path("oqc_lucy").open() as json_file:
            self.oqc_calibration = cast("OQCCalibration", json.load(json_file))
        self.calibration = None

        self.name = self.oqc_calibration["name"]
        self.gateset = Gateset("oqc", self.oqc_calibration["basis_gates"])
        self.num_qubits = self.oqc_calibration["num_qubits"]
        self.coupling_map = list(self.oqc_calibration["connectivity"])

    def read_calibration(self) -> None:
        """Read the calibration data for the device."""
        calibration = DeviceCalibration()
        for qubit in range(self.num_qubits):
            calibration.single_qubit_gate_fidelity[qubit] = {
                gate: self.oqc_calibration["properties"]["one_qubit"][str(qubit)]["fRB"] for gate in ["rz", "sx", "x"]
            }
            calibration.readout_fidelity[qubit] = self.oqc_calibration["properties"]["one_qubit"][str(qubit)]["fRO"]
            # data in microseconds, convert to SI unit (seconds)
            calibration.t1[qubit] = self.oqc_calibration["properties"]["one_qubit"][str(qubit)]["T1"] * 1e-6
            calibration.t2[qubit] = self.oqc_calibration["properties"]["one_qubit"][str(qubit)]["T2"] * 1e-6

        for qubit1, qubit2 in self.coupling_map:
            calibration.two_qubit_gate_fidelity[qubit1, qubit2] = dict.fromkeys(
                ["ecr"], self.oqc_calibration["properties"]["two_qubit"][f"{qubit1}-{qubit2}"]["fECR"]
            )
        self.calibration = calibration


class QubitProperties(TypedDict):
    """Class to store the properties of a single qubit."""

    T1: float
    T2: float
    fRB: float
    fRO: float
    qubit: float


class Coupling(TypedDict):
    """Class to store the connectivity of a two-qubit gate."""

    control_qubit: float
    target_qubit: float


class TwoQubitProperties(TypedDict):
    """Class to store the properties of a two-qubit gate."""

    coupling: Coupling
    fECR: float


class Properties(TypedDict):
    """Class to store the properties of a device."""

    one_qubit: dict[str, QubitProperties]
    two_qubit: dict[str, TwoQubitProperties]


class OQCCalibration(TypedDict):
    """Class to store the calibration data of an OQC device."""

    name: str
    basis_gates: list[str]
    num_qubits: int
    connectivity: list[list[int]]
    properties: Properties
