"""Module to manage IBM devices."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING, TypedDict, cast

if TYPE_CHECKING:
    from pathlib import Path

    from qiskit.providers import BackendV2
    from qiskit.transpiler import Target


from mqt.bench.devices import Device, DeviceCalibration, Provider


class QubitProperties(TypedDict):
    """Class to store the properties of a single qubit."""

    T1: float  # us
    T2: float  # us
    eRO: float
    tRO: float  # ns
    eID: float
    eSX: float
    eX: float
    eCX: dict[str, float]
    tCX: dict[str, float]  # ns


class IBMCalibration(TypedDict):
    """Class to store the calibration data of an IBM device."""

    name: str
    basis_gates: list[str]
    num_qubits: int
    connectivity: list[list[int]]
    properties: dict[str, QubitProperties]


class IBMProvider(Provider):
    """Class to manage IBM devices."""

    provider_name = "ibm"

    @classmethod
    def get_available_device_names(cls) -> list[str]:
        """Get the names of all available IBM devices."""
        return ["ibm_washington", "ibm_montreal"]  # NOTE: update when adding new devices

    @classmethod
    def get_native_gates(cls) -> list[str]:
        """Get a list of provider specific native gates."""
        return ["id", "rz", "sx", "x", "cx", "measure", "barrier"]  # washington, montreal

    @classmethod
    def import_backend(cls, path: Path) -> Device:
        """Import an IBM backend.

        Arguments:
            path: the path to the JSON file containing the calibration data.

        Returns: the Device object
        """
        with path.open() as json_file:
            ibm_calibration = cast(IBMCalibration, json.load(json_file))

        device = Device()
        device.name = ibm_calibration["name"]
        device.num_qubits = ibm_calibration["num_qubits"]
        device.basis_gates = ibm_calibration["basis_gates"]
        device.coupling_map = list(ibm_calibration["connectivity"])

        calibration = DeviceCalibration()
        for qubit in range(device.num_qubits):
            calibration.single_qubit_gate_fidelity[qubit] = {
                "id": 1 - ibm_calibration["properties"][str(qubit)]["eID"],
                "rz": 1,  # rz is always perfect
                "sx": 1 - ibm_calibration["properties"][str(qubit)]["eSX"],
                "x": 1 - ibm_calibration["properties"][str(qubit)]["eX"],
            }
            calibration.readout_fidelity[qubit] = 1 - ibm_calibration["properties"][str(qubit)]["eRO"]
            # data in nanoseconds, convert to SI unit (seconds)
            calibration.readout_duration[qubit] = ibm_calibration["properties"][str(qubit)]["tRO"] * 1e-9
            # data in microseconds, convert to SI unit (seconds)
            calibration.t1[qubit] = ibm_calibration["properties"][str(qubit)]["T1"] * 1e-6
            calibration.t2[qubit] = ibm_calibration["properties"][str(qubit)]["T2"] * 1e-6

        for qubit1, qubit2 in device.coupling_map:
            edge = f"{qubit1}_{qubit2}"

            error = ibm_calibration["properties"][str(qubit1)]["eCX"][edge]
            calibration.two_qubit_gate_fidelity[qubit1, qubit2] = {"cx": 1 - error}

            # data in nanoseconds, convert to SI unit (seconds)
            duration = ibm_calibration["properties"][str(qubit1)]["tCX"][edge] * 1e-9
            calibration.two_qubit_gate_duration[qubit1, qubit2] = {"cx": duration}

        device.calibration = calibration
        return device

    @classmethod
    def __import_target(cls, target: Target) -> DeviceCalibration:
        """Import calibration data from a Qiskit `Target` object.

        Arguments:
            target: the Qiskit `Target` object.

        Returns: Collection of calibration data
        """
        calibration = DeviceCalibration()
        num_qubits = len(target.qubit_properties)

        for qubit in range(num_qubits):
            qubit_props = target.qubit_properties[qubit]
            calibration.t1[qubit] = cast(float, qubit_props.t1)
            calibration.t2[qubit] = cast(float, qubit_props.t2)

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

    @classmethod
    def import_qiskit_backend(cls, backend: BackendV2) -> Device:
        """Import device data from a Qiskit `Backend` object.

        Arguments:
            backend: the Qiskit `BackendV2` object.

        Returns: Collection of device data
        """
        device = Device()
        device.name = backend.name
        device.num_qubits = backend.num_qubits
        device.basis_gates = backend.operation_names
        device.coupling_map = backend.coupling_map.get_edges()
        device.calibration = cls.__import_target(backend.target)
        return device
