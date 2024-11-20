"""Module for native gatesets."""

from __future__ import annotations

from .devices import get_available_devices


def get_available_native_gatesets() -> dict[str, list[str]]:
    """Get a list of all available native gatesets."""
    native_gates_dict = {}
    for device in get_available_devices():
        native_gates_dict[device.gateset_name] = device.get_native_gates()
    # native_gates_dict["clifford+t"] = ["id", "h", "s", "cx", "t"]
    return native_gates_dict


def get_native_gateset_by_name(gateset_name: str) -> tuple[str, list[str]]:
    """Get a native gateset by its name.

    Arguments:
        gateset_name: the name of the gateset
    """
    items = get_available_native_gatesets()
    for tmp_name, tmp_gateset in items.items():
        if tmp_name == gateset_name:
            return tmp_name, tmp_gateset
    msg = f"Gateset {gateset_name} not found in available gatesets."
    raise RuntimeError(msg)
