"""MQT Bench.

This file is part of the MQT Bench Benchmark library released under the MIT license.
See README.md or go to https://github.com/cda-tum/mqt-bench for more information.
"""

from __future__ import annotations

from .calibration import DeviceCalibration
from .device import Device, Gateset
from .ibm import IBMMontreal, IBMTorino, IBMWashington
from .ionq import IonQAria1, IonQHarmony
from .iqm import IQMAdonis, IQMApollo
from .oqc import OQCLucy
from .quantinuum import QuantinuumH2
from .rigetti import RigettiAspenM3


def get_available_devices() -> list[Device]:
    """Get a list of all available devices."""
    return [
        IBMTorino(),
        IBMMontreal(),
        IBMWashington(),
        IonQAria1(),
        IonQHarmony(),
        IQMAdonis(),
        IQMApollo(),
        OQCLucy(),
        QuantinuumH2(),
        RigettiAspenM3(),
    ]


def get_available_device_names() -> list[str]:
    """Get a list of all available device names."""
    return [device.name for device in get_available_devices()]


def get_device_by_name(device_name: str) -> Device:
    """Get a device by its name.

    Arguments:
        device_name: the name of the device
        sanitize_device: whether to sanitize the device's calibration data
    """
    for device in get_available_devices():
        if device.name == device_name:
            return device

    msg = f"Device {device_name} not found in available devices."
    raise ValueError(msg)


__all__ = [
    "Device",
    "DeviceCalibration",
    "Gateset",
    "get_available_device_names",
    "get_available_devices",
    "get_device_by_name",
]


def get_available_native_gatesets() -> list[Gateset]:
    """Get a list of all available native gatesets."""
    available_gatesets = [device.gateset for device in get_available_devices()]
    available_gatesets.append(
        Gateset(
            "clifford+t",
            ["s", "sdg", "t", "tdg", "z", "h", "cx"],
        )
    )
    return available_gatesets


def get_native_gateset_by_name(desired_gateset_name: str) -> Gateset:
    """Get a native gateset by its name.

    Arguments:
        desired_gateset_name: the name of the gateset
    """
    for gateset in get_available_native_gatesets():
        if gateset.gateset_name == desired_gateset_name:
            return gateset
    msg = f"Gateset {desired_gateset_name} not found in available gatesets."
    raise ValueError(msg)
