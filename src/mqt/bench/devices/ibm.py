"""Module to manage IBM devices."""

from __future__ import annotations

from typing import TYPE_CHECKING, cast

from qiskit_ibm_runtime.fake_provider import FakeMontrealV2, FakeWashingtonV2

from .calibration import DeviceCalibration
from .device import Device

if TYPE_CHECKING:
    from qiskit.providers import BackendV2
    from qiskit.transpiler import Target


def get_ibm_washington(sanitize_device: bool = False) -> Device:
    """Get the IBM Washington device."""
    dev = import_qiskit_backend(FakeWashingtonV2(), "ibm_washington", "ibm_falcon")
    if sanitize_device:
        dev.sanitize_device()
    return dev


def get_ibm_montreal(sanitize_device: bool = False) -> Device:
    """Get the IBM Montreal device."""
    dev = import_qiskit_backend(FakeMontrealV2(), "ibm_montreal", "ibm_falcon")
    if sanitize_device:
        dev.sanitize_device()
    return dev


def import_qiskit_backend(backend: BackendV2, name: str, architecture: str) -> Device:
    """Import device data from a Qiskit `Backend` object.

    Arguments:
        backend: the Qiskit `BackendV2` object.
        name: the name of the device
        architecture: the name of the architecture

    Returns: Collection of device data
    """
    device = Device()
    device.name = name
    device.gateset_name = architecture
    device.num_qubits = backend.num_qubits
    device.basis_gates = backend.operation_names
    device.coupling_map = backend.coupling_map
    device.calibration = import_target(backend.target)
    return device


def import_target(target: Target) -> DeviceCalibration:
    """Import calibration data from a Qiskit `Target` object.

    Arguments:
        target: the Qiskit `Target` object.

    Returns: Collection of calibration data
    """
    calibration = DeviceCalibration()
    num_qubits = len(target.qubit_properties)

    for qubit in range(num_qubits):
        qubit_props = target.qubit_properties[qubit]
        calibration.t1[qubit] = cast("float", qubit_props.t1)
        calibration.t2[qubit] = cast("float", qubit_props.t2)

    calibration.single_qubit_gate_fidelity = {qubit: {} for qubit in range(num_qubits)}
    calibration.single_qubit_gate_duration = {qubit: {} for qubit in range(num_qubits)}
    coupling_map = target.build_coupling_map().get_edges()
    calibration.two_qubit_gate_fidelity = {(qubit1, qubit2): {} for qubit1, qubit2 in coupling_map}
    calibration.two_qubit_gate_duration = {(qubit1, qubit2): {} for qubit1, qubit2 in coupling_map}
    for instruction, qargs in target.instructions:
        # Skip `reset` and `delay` gate as their error information is not exposed.
        if instruction.name == "reset" or instruction.name == "delay":
            continue

        instruction_props = target[instruction.name][qargs]
        error: float = instruction_props.error
        duration: float = instruction_props.duration
        qubit = qargs[0]
        if instruction.name == "measure":
            calibration.readout_fidelity[qubit] = 1 - error
            calibration.readout_duration[qubit] = duration
        elif len(qargs) == 1:
            calibration.single_qubit_gate_fidelity[qubit][instruction.name] = 1 - error
            calibration.single_qubit_gate_duration[qubit][instruction.name] = duration
        elif len(qargs) == 2:
            qubit1, qubit2 = qargs
            calibration.two_qubit_gate_fidelity[qubit1, qubit2][instruction.name] = 1 - error
            calibration.two_qubit_gate_duration[qubit1, qubit2][instruction.name] = duration

    return calibration
