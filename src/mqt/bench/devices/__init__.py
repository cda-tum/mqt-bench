from __future__ import annotations

# ruff: noqa: I001
from mqt.bench.devices.calibration import DeviceCalibration
from mqt.bench.devices.device import Device
from mqt.bench.devices.provider import Provider

from mqt.bench.devices.ibm import IBMProvider
from mqt.bench.devices.ionq import IonQProvider
from mqt.bench.devices.oqc import OQCProvider
from mqt.bench.devices.quantinuum import QuantinuumProvider
from mqt.bench.devices.rigetti import RigettiProvider


class NotFoundError(Exception):
    """Raised when a device or provider is not found within the available ones."""


def get_available_providers() -> list[Provider]:
    """
    Get a list of all available providers
    """
    return [IBMProvider(), IonQProvider(), OQCProvider(), RigettiProvider(), QuantinuumProvider()]


def get_available_provider_names() -> list[str]:
    """
    Get a list of all available provider names
    """
    return [prov.provider_name for prov in get_available_providers()]


def get_provider_by_name(provider_name: str) -> Provider:
    """
    Get a provider by its name

    Args:
        provider_name: the name of the provider
    """
    provider = None
    for prov in get_available_providers():
        if prov.provider_name == provider_name:
            provider = prov
            break

    if provider is None:
        msg = f"Provider '{provider_name}' not found among available providers."
        raise NotFoundError(msg)

    return provider


def get_available_devices(sanitize_device: bool = False) -> list[Device]:
    """
    Get a list of all available devices

    Args:
        sanitize_device: whether to sanitize the device calibration data
    """
    return [
        dev for prov in get_available_providers() for dev in prov.get_available_devices(sanitize_device=sanitize_device)
    ]


def get_available_device_names() -> list[str]:
    """
    Get a list of all available device names
    """
    return [name for prov in get_available_providers() for name in prov.get_available_device_names()]


def get_device_by_name(device_name: str) -> Device:
    """
    Get a device by its name

    Args:
        device_name: the name of the device
    """
    device = None
    for provider in get_available_providers():
        try:
            device = provider.get_device(device_name)
            break
        except ValueError:
            continue

    if device is None:
        msg = f"Device '{device_name}' not found among available providers."
        raise NotFoundError(msg)

    return device


__all__ = [
    "Provider",
    "Device",
    "DeviceCalibration",
    "IBMProvider",
    "IonQProvider",
    "OQCProvider",
    "RigettiProvider",
    "QuantinuumProvider",
    "get_available_providers",
    "get_available_provider_names",
    "get_provider_by_name",
    "get_available_devices",
    "get_available_device_names",
    "get_device_by_name",
]
