"""MQT Bench.

This file is part of the MQT Bench Benchmark library released under the MIT license.
See README.md or go to https://github.com/cda-tum/mqt-bench for more information.
"""

from __future__ import annotations

from .calibration import DeviceCalibration
from .device import Device, NoCalibrationDevice
from .ibm import get_ibm_montreal, get_ibm_torino, get_ibm_washington
from .ionq import get_ionq_aria1, get_ionq_harmony
from .iqm import get_iqm_adonis, get_iqm_apollo
from .oqc import get_oqc_lucy
from .quantinuum import get_quantinuum_h2
from .rigetti import get_rigetti_aspen_m3


def get_available_devices() -> list[NoCalibrationDevice]:
    """Get a list of all available devices."""
    return [
        NoCalibrationDevice(
            "ibm_montreal", "ibm_falcon", ["delay", "measure", "reset", "x", "rz", "sx", "cx", "id"], get_ibm_montreal
        ),
        NoCalibrationDevice(
            "ibm_washington",
            "ibm_falcon",
            ["cx", "rz", "measure", "delay", "x", "reset", "sx", "id"],
            get_ibm_washington,
        ),
        NoCalibrationDevice(
            "ibm_torino",
            "ibm_heron_r1",
            ["cz", "id", "delay", "measure", "reset", "rz", "sx", "x", "if_else", "for_loop", "switch_case"],
            get_ibm_torino,
        ),
        NoCalibrationDevice("ionq_aria1", "ionq", ["rxx", "rz", "ry", "rx", "measure", "barrier"], get_ionq_aria1),
        NoCalibrationDevice("ionq_harmony", "ionq", ["rxx", "rz", "ry", "rx", "measure", "barrier"], get_ionq_harmony),
        NoCalibrationDevice("iqm_adonis", "iqm", ["r", "cz", "measure", "barrier"], get_iqm_adonis),
        NoCalibrationDevice("iqm_apollo", "iqm", ["r", "cz", "measure", "barrier"], get_iqm_apollo),
        NoCalibrationDevice("oqc_lucy", "oqc", ["rz", "sx", "x", "ecr", "measure", "barrier"], get_oqc_lucy),
        NoCalibrationDevice(
            "quantinuum_h2", "quantinuum", ["rzz", "rz", "ry", "rx", "measure", "barrier"], get_quantinuum_h2
        ),
        NoCalibrationDevice(
            "rigetti_aspen_m3",
            "rigetti",
            ["rx", "rz", "cz", "cp", "xx_plus_yy", "measure", "barrier"],
            get_rigetti_aspen_m3,
        ),
    ]


def get_available_device_names() -> list[str]:
    """Get a list of all available device names."""
    return [device.name for device in get_available_devices()]


def get_device_by_name(device_name: str, sanitize_device: bool = False) -> Device:
    """Get a device by its name.

    Arguments:
        device_name: the name of the device
        sanitize_device: whether to sanitize the device's calibration data
    """
    for device in get_available_devices():
        if device.name == device_name:
            return device.constructor(sanitize_device)

    msg = f"Device {device_name} not found in available devices."
    raise ValueError(msg)


__all__ = [
    "Device",
    "DeviceCalibration",
    "get_available_device_names",
    "get_available_devices",
    "get_device_by_name",
]


def get_available_native_gatesets() -> list[tuple[str, list[str]]]:
    """Get a list of all available native gatesets."""
    return [(device.gateset_name, device.gateset) for device in get_available_devices()]
    # available_gatesets.append(("clifford+t", ["id", "h", "s", "cx", "t"]))


def get_native_gateset_by_name(gateset_name: str) -> tuple[str, list[str]]:
    """Get a native gateset by its name.

    Arguments:
        gateset_name: the name of the gateset
    """
    for tmp_name, tmp_gateset in get_available_native_gatesets():
        if tmp_name == gateset_name:
            return tmp_name, tmp_gateset
    msg = f"Gateset {gateset_name} not found in available gatesets."
    raise ValueError(msg)
