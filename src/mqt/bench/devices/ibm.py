from __future__ import annotations

import json
from typing import TYPE_CHECKING, TypedDict, cast

if TYPE_CHECKING:
    from pathlib import Path

    from qiskit.providers.models import BackendProperties
    from qiskit.transpiler import Target

from qiskit.providers import BackendV1, BackendV2

from mqt.bench.devices import Device, DeviceCalibration, Provider


class QubitProperties(TypedDict):
    """
    Class to store the properties of a single qubit.
    """

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
    """
    Class to store the calibration data of an IBM device.
    """

    name: str
    basis_gates: list[str]
    num_qubits: int
    connectivity: list[list[int]]
    properties: dict[str, QubitProperties]


class IBMProvider(Provider):
    """
    Class to manage IBM devices.
    """

    provider_name = "ibm"

    @classmethod
    def get_available_device_names(cls) -> list[str]:
        """
        Get the names of all available IBM devices.
        """
        return ["ibm_washington", "ibm_montreal"]  # NOTE: update when adding new devices

    @classmethod
    def get_native_gates(cls) -> list[str]:
        """
        Get a list of provider specific native gates.
        """
        return ["id", "rz", "sx", "x", "cx", "measure", "barrier"]  # washington, montreal

    @classmethod
    def import_backend(cls, path: Path) -> Device:
        """
        Import an IBM backend.
        Args:
            path: the path to the JSON file containing the calibration data

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
            calibration.readout_duration[qubit] = ibm_calibration["properties"][str(qubit)]["tRO"]
            calibration.t1[qubit] = ibm_calibration["properties"][str(qubit)]["T1"]
            calibration.t2[qubit] = ibm_calibration["properties"][str(qubit)]["T2"]

        for qubit1, qubit2 in device.coupling_map:
            edge = f"{qubit1}_{qubit2}"

            error = ibm_calibration["properties"][str(qubit1)]["eCX"][edge]
            calibration.two_qubit_gate_fidelity[(qubit1, qubit2)] = {"cx": 1 - error}

            duration = ibm_calibration["properties"][str(qubit1)]["tCX"][edge]
            calibration.two_qubit_gate_duration[(qubit1, qubit2)] = {"cx": duration}

        device.calibration = calibration
        return device

    @classmethod
    def __import_backend_properties(cls, backend_properties: BackendProperties) -> DeviceCalibration:
        """
        Import calibration data from a Qiskit `BackendProperties` object.
        Args:
            backend_properties: the Qiskit `BackendProperties` object

        Returns: Collection of calibration data
        """
        calibration = DeviceCalibration()
        num_qubits = len(backend_properties.qubits)

        for qubit in range(num_qubits):
            calibration.t1[qubit] = cast(float, backend_properties.t1(qubit))
            calibration.t2[qubit] = cast(float, backend_properties.t2(qubit))
            calibration.readout_fidelity[qubit] = 1 - cast(float, backend_properties.readout_error(qubit))
            calibration.readout_duration[qubit] = cast(float, backend_properties.readout_length(qubit))

        calibration.single_qubit_gate_fidelity = {qubit: {} for qubit in range(num_qubits)}
        calibration.single_qubit_gate_duration = {qubit: {} for qubit in range(num_qubits)}
        for gate in backend_properties.gates:
            # Skip `reset` gate as its error information is not exposed.
            if gate.gate == "reset":
                continue

            error: float = backend_properties.gate_error(gate.gate, gate.qubits)
            duration: float = backend_properties.gate_length(gate.gate, gate.qubits)
            if len(gate.qubits) == 1:
                qubit = gate.qubits[0]
                calibration.single_qubit_gate_fidelity[qubit][gate.gate] = 1 - error
                calibration.single_qubit_gate_duration[qubit][gate.gate] = duration
            elif len(gate.qubits) == 2:
                qubit1, qubit2 = gate.qubits
                if (qubit1, qubit2) not in calibration.two_qubit_gate_fidelity:
                    calibration.two_qubit_gate_fidelity[(qubit1, qubit2)] = {}
                calibration.two_qubit_gate_fidelity[(qubit1, qubit2)][gate.gate] = 1 - error

                if (qubit1, qubit2) not in calibration.two_qubit_gate_duration:
                    calibration.two_qubit_gate_duration[(qubit1, qubit2)] = {}
                calibration.two_qubit_gate_duration[(qubit1, qubit2)][gate.gate] = duration

        return calibration

    @classmethod
    def __import_backend_v1(cls, backend: BackendV1) -> Device:
        """
        Import device data from a Qiskit `BackendV1` object.
        Args:
            backend: the Qiskit `BackendV1` object

        Returns: Collection of device data
        """
        device = Device()
        device.name = backend.name()
        device.num_qubits = backend.configuration().n_qubits
        device.basis_gates = backend.configuration().basis_gates
        device.coupling_map = list(backend.configuration().coupling_map)
        device.calibration = cls.__import_backend_properties(backend.properties())
        return device

    @classmethod
    def __import_target(cls, target: Target) -> DeviceCalibration:
        """
        Import calibration data from a Qiskit `Target` object.
        Args:
            target: the Qiskit `Target` object

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
                calibration.two_qubit_gate_fidelity[(qubit1, qubit2)][instruction.name] = 1 - error
                calibration.two_qubit_gate_duration[(qubit1, qubit2)][instruction.name] = duration

        return calibration

    @classmethod
    def __import_backend_v2(cls, backend: BackendV2) -> Device:
        """
        Import device data from a Qiskit `BackendV2` object.
        Args:
            backend: the Qiskit `BackendV2` object

        Returns: Collection of device data
        """
        device = Device()
        device.name = backend.name
        device.num_qubits = backend.num_qubits
        device.basis_gates = backend.operation_names
        device.coupling_map = backend.coupling_map.get_edges()
        device.calibration = cls.__import_target(backend.target)
        return device

    @classmethod
    def import_qiskit_backend(cls, backend: BackendV1 | BackendV2) -> Device:
        """
        Import device data from a Qiskit `Backend` object.
        Args:
            backend: the Qiskit `Backend` object

        Returns: Collection of device data
        """
        if isinstance(backend, BackendV1):
            return cls.__import_backend_v1(backend)
        if isinstance(backend, BackendV2):
            return cls.__import_backend_v2(backend)
        msg = f"Unsupported backend type {type(backend)}"
        raise TypeError(msg)
