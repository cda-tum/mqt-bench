"""Module to manage Quantinuum devices."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING, TypedDict, cast

from .calibration import DeviceCalibration, get_device_calibration_path
from .device import Device

if TYPE_CHECKING:
    from pathlib import Path


def get_quantinuum_h2(sanitize_device: bool = False) -> Device:
    """Get the Quantinuum H2 device."""
    dev = import_quantinuum_device(get_device_calibration_path("quantinuum_h2"))
    if sanitize_device:
        dev.sanitize_device()
    return dev


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


def import_quantinuum_device(path: Path) -> Device:
    """Import an Quantinuum backend as a Device object.

    Arguments:
        path: the path to the JSON file containing the calibration data.

    Returns:
        the Device object
    """
    with path.open() as json_file:
        quantinuum_calibration = cast("QuantinuumCalibration", json.load(json_file))

    device = Device()
    device.name = quantinuum_calibration["name"]
    device.gateset_name = "quantinuum"
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
        calibration.two_qubit_gate_fidelity[qubit1, qubit2] = {"rzz": quantinuum_calibration["fidelity"]["2q"]["mean"]}
    device.calibration = calibration
    return device
