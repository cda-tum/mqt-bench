from __future__ import annotations

import sys
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING or sys.version_info >= (3, 10, 0):
    from importlib import resources
else:
    import importlib_resources as resources

if TYPE_CHECKING:
    from pathlib import Path

    from mqt.bench.devices import Device

from abc import ABC, abstractmethod


@dataclass
class Provider(ABC):
    """
    Abstract class for a quantum device provider.
    """

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """
        Get the name of the provider.
        """

    @classmethod
    def get_available_devices(cls, sanitize_device: bool = False) -> list[Device]:
        """
        Get a list of all available devices.

        Args:
            sanitize_device: whether to sanitize the device calibration data
        """
        return [cls.get_device(name, sanitize_device=sanitize_device) for name in cls.get_available_device_names()]

    @classmethod
    @abstractmethod
    def get_available_device_names(cls) -> list[str]:
        """
        Get a list of all available device names.
        """

    @classmethod
    @abstractmethod
    def get_native_gates(cls) -> list[str]:
        """
        Get a list of provider specific native gates.
        """

    @classmethod
    def get_available_basis_gates(cls) -> list[list[str]]:
        """
        Get a list of all available basis gates.
        """
        unique_basis_gates = {tuple(device.basis_gates) for device in cls.get_available_devices()}
        return [list(basis_gates) for basis_gates in unique_basis_gates]

    @classmethod
    def get_max_qubits(cls) -> int:
        """
        Get the maximum number of qubits offered by a device from the provider.
        """
        return max([device.num_qubits for device in cls.get_available_devices()])

    @classmethod
    @abstractmethod
    def import_backend(cls, path: Path) -> Device:
        """
        Import a device from a file containing calibration data.
        """

    @classmethod
    def get_device(cls, name: str, sanitize_device: bool = False) -> Device:
        """
        Get a device by name.

        Args:
            name: the name of the device
            sanitize_device: whether to sanitize the device calibration data
        """
        if name not in cls.get_available_device_names():
            msg = f"Device {name} not found."
            raise ValueError(msg)

        ref = resources.files("mqt.bench") / "calibration_files" / f"{name}_calibration.json"
        with resources.as_file(ref) as json_path:
            device = cls.import_backend(json_path)
            if sanitize_device:
                device.sanitize_device()
            return device
