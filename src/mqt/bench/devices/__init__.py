"""MQT Bench.

This file is part of the MQT Bench Benchmark library released under the MIT license.
See README.md or go to https://github.com/cda-tum/mqt-bench for more information.
"""

from __future__ import annotations

# ruff: noqa: I001
from .calibration import DeviceCalibration
from .device import Device


from .ibm import get_ibm_montreal, get_ibm_washington
from .ionq import get_ionq_aria1, get_ionq_harmony
from .iqm import get_iqm_adonis, get_iqm_apollo
from .oqc import get_oqc_lucy
from .quantinuum import get_quantinuum_h2
from .rigetti import get_rigetti_aspen_m3


def get_available_devices() -> list[Device]:
    """Get a list of all available devices."""
    return [
        get_ionq_harmony(),
        get_ionq_aria1(),
        get_iqm_adonis(),
        get_iqm_apollo(),
        get_ibm_washington(),
        get_ibm_montreal(),
        get_rigetti_aspen_m3(),
        get_quantinuum_h2(),
        get_oqc_lucy(),
    ]


def get_available_device_names() -> list[str]:
    """Get a list of all available device names."""
    return [device.name for device in get_available_devices()]


def get_device_by_name(device_name: str) -> Device:
    """Get a device by its name.

    Arguments:
        device_name: the name of the device
    """
    for device in get_available_devices():
        if device.name == device_name:
            return device

    msg = f"Device {device_name} not found in available devices."
    raise RuntimeError(msg)


__all__ = [
    "Device",
    "DeviceCalibration",
    "get_available_device_names",
    "get_available_devices",
    "get_device_by_name",
]
