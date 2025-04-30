# Copyright (c) 2023 - 2025 Chair for Design Automation, TUM
# Copyright (c) 2025 Munich Quantum Software Company GmbH
# All rights reserved.
#
# SPDX-License-Identifier: MIT
#
# Licensed under the MIT License

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
    available_gatesets = []
    for device in get_available_devices():
        if device.gateset not in available_gatesets:
            available_gatesets.append(device.gateset)
    return available_gatesets


def get_native_gateset_by_name(gateset_name: str) -> Gateset:
    """Get a native gateset by its name.

    Arguments:
        gateset_name: the name of the gateset
    """
    for gateset in get_available_native_gatesets():
        if gateset.gateset_name == gateset_name:
            return gateset
    msg = f"Gateset {gateset_name} not found in available gatesets."
    raise ValueError(msg)
