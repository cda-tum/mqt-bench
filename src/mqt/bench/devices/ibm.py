"""Module to manage IBM devices."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING, TypedDict, cast

# Conditional import for type hinting and other imports
if TYPE_CHECKING:
    from qiskit.providers import BackendV2
    from qiskit.providers.models import BackendProperties
    from qiskit.transpiler import Target

# Conditional import for importlib resources based on Python version
from importlib import resources

from qiskit_ibm_runtime import QiskitRuntimeService

from .calibration import DeviceCalibration
from .device import Device
from .provider import Provider


class QubitPropertiesIBM(TypedDict):
    """Class to store the properties of a single qubit for IBMProvider."""

    T1: float  # us
    T2: float  # us
    eRO: float
    tRO: float  # ns
    eID: float
    eSX: float
    eX: float
    eCX: dict[str, float]
    tCX: dict[str, float]  # ns


class QubitPropertiesOpenAccess(TypedDict):
    """Class to store the properties of a single qubit for IBMOpenAccessProvider."""

    T1: float  # us
    T2: float  # us
    eRO: float
    tRO: float  # ns
    eID: float
    eSX: float
    eX: float
    eECR: dict[str, float]
    tECR: dict[str, float]  # ns


class IBMCalibration(TypedDict):
    """Class to store the calibration data of an IBM device."""

    name: str
    basis_gates: list[str]
    num_qubits: int
    connectivity: list[list[int]]
    properties: dict[str, QubitPropertiesIBM]


class IBMOpenAccessCalibration(TypedDict):
    """Class to store the calibration data of an open-access IBM device."""

    name: str
    basis_gates: list[str]
    num_qubits: int
    connectivity: list[list[int]]
    properties: dict[str, QubitPropertiesOpenAccess]


class BaseIBMProvider:
    """Base class for IBM providers with shared functionality."""

    @classmethod
    def import_backend_properties(cls, backend_properties: BackendProperties) -> DeviceCalibration:
        """Import calibration data from a Qiskit `BackendProperties` object."""
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
                    calibration.two_qubit_gate_fidelity[qubit1, qubit2] = {}
                calibration.two_qubit_gate_fidelity[qubit1, qubit2][gate.gate] = 1 - error

                if (qubit1, qubit2) not in calibration.two_qubit_gate_duration:
                    calibration.two_qubit_gate_duration[qubit1, qubit2] = {}
                calibration.two_qubit_gate_duration[qubit1, qubit2][gate.gate] = duration

        return calibration

    @classmethod
    def import_target(cls, target: Target) -> DeviceCalibration:
        """Import calibration data from a Qiskit `Target` object."""
        calibration = DeviceCalibration()
        num_qubits = len(target.qubit_properties)

        for qubit in range(num_qubits):
            qubit_props = target.qubit_properties[qubit]
            calibration.t1[qubit] = cast(float, qubit_props.t1)
            calibration.t2[qubit] = cast(float, qubit_props.t2)

        calibration.single_qubit_gate_fidelity = {qubit: {} for qubit in range(num_qubits)}
        calibration.single_qubit_gate_duration = {qubit: {} for qubit in range(num_qubits)}
        coupling_map = target.build_coupling_map().get_edges()

        # Initialize an empty list to hold the transformed connectivity
        connectivity: list[list[int]] = []

        # Loop over each tuple in the coupling map
        for a, b in coupling_map:
            # Add both directions for each connection
            connectivity.extend(([a, b], [b, a]))

        # Now connectivity is in the desired format
        coupling_map = connectivity

        calibration.two_qubit_gate_fidelity = {(qubit1, qubit2): {} for qubit1, qubit2 in coupling_map}
        calibration.two_qubit_gate_duration = {(qubit1, qubit2): {} for qubit1, qubit2 in coupling_map}
        for instruction, qargs in target.instructions:
            if instruction.name in ["reset", "delay"]:
                continue

            # Skip control flow operations like ForLoopOp, IfElseOp, SwitchCaseOp, etc.
            try:
                instruction_props = target[instruction.name][qargs]
                error: float = instruction_props.error
                duration: float = instruction_props.duration
            except KeyError:
                print(f"Instruction {instruction.name} not found in target.")
                continue

            qubit = qargs[0]
            if instruction.name == "measure":
                calibration.readout_fidelity[qubit] = 1 - error
                calibration.readout_duration[qubit] = duration
            elif len(qargs) == 1:
                calibration.single_qubit_gate_fidelity[qubit][instruction.name] = 1 - error
                calibration.single_qubit_gate_duration[qubit][instruction.name] = duration
            elif len(qargs) == 2:
                qubit1, qubit2 = qargs
                if (qubit1, qubit2) not in calibration.two_qubit_gate_fidelity:
                    calibration.two_qubit_gate_fidelity[qubit1, qubit2] = {}
                if (qubit2, qubit1) not in calibration.two_qubit_gate_fidelity:
                    calibration.two_qubit_gate_fidelity[qubit2, qubit1] = {}

                calibration.two_qubit_gate_fidelity[qubit1, qubit2][instruction.name] = 1 - error
                calibration.two_qubit_gate_fidelity[qubit2, qubit1][instruction.name] = 1 - error

                if (qubit1, qubit2) not in calibration.two_qubit_gate_duration:
                    calibration.two_qubit_gate_duration[qubit1, qubit2] = {}
                if (qubit2, qubit1) not in calibration.two_qubit_gate_duration:
                    calibration.two_qubit_gate_duration[qubit2, qubit1] = {}

                calibration.two_qubit_gate_duration[qubit1, qubit2][instruction.name] = duration
                calibration.two_qubit_gate_duration[qubit2, qubit1][instruction.name] = duration

        return calibration


class IBMProvider(Provider, BaseIBMProvider):
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
    def import_backend(cls, name: str) -> Device:
        """Import an IBM backend.

        Arguments:
            name (str): The name of the IBM backend whose calibration data needs to be imported.
                          This name will be used to locate the corresponding JSON calibration file.

        Returns:
              Device: An instance of `Device`, loaded with the calibration data from the JSON file.
        """
        # Assuming 'name' is already defined
        ref = resources.files("mqt.bench") / "calibration_files" / f"{name}_calibration.json"

        with resources.as_file(ref) as json_path, json_path.open() as json_file:
            # Load the JSON data and cast it to QuantinuumCalibration
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
            calibration.readout_duration[qubit] = ibm_calibration["properties"][str(qubit)]["tRO"] * 1e-9
            calibration.t1[qubit] = ibm_calibration["properties"][str(qubit)]["T1"] * 1e-6
            calibration.t2[qubit] = ibm_calibration["properties"][str(qubit)]["T2"] * 1e-6

        for qubit1, qubit2 in device.coupling_map:
            edge = f"{qubit1}_{qubit2}"
            error = ibm_calibration["properties"][str(qubit1)]["eCX"][edge]
            calibration.two_qubit_gate_fidelity[qubit1, qubit2] = {"cx": 1 - error}
            duration = ibm_calibration["properties"][str(qubit1)]["tCX"][edge] * 1e-9
            calibration.two_qubit_gate_duration[qubit1, qubit2] = {"cx": duration}

        device.calibration = calibration
        return device

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
        device.calibration = cls.import_target(backend.target)
        return device


class IBMOpenAccessProvider(Provider, BaseIBMProvider):
    """Class to manage open-access IBM devices."""

    provider_name = "ibm_open_access"

    @classmethod
    def get_available_device_names(cls) -> list[str]:
        """Get the names of all available open-access IBM devices."""
        return ["ibm_kyiv", "ibm_brisbane", "ibm_sherbrooke"]  # NOTE: update when adding new devices

    @classmethod
    def get_native_gates(cls) -> list[str]:
        """Get a list of provider specific native gates."""
        return ["id", "rz", "sx", "x", "ecr", "measure", "barrier"]  # ibm_kyiv, ibm_brisbane, ibm_sherbrooke

    @classmethod
    def import_backend(cls, name: str) -> Device:
        """Import an IBM backend.

        Arguments:
            name: the name of the backend.

        Returns: the Device object
        """
        service = QiskitRuntimeService(instance="ibm-q/open/main")
        backend = service.backend(name)

        device = Device()
        device.name = backend.name
        device.num_qubits = backend.num_qubits

        gates = backend.basis_gates.copy()
        gates.append("measure")  # Add the 'measure' gate
        gates.append("barrier")  # Add the 'barrier' gate

        device.basis_gates = gates

        # Initialize an empty list to hold the transformed connectivity
        connectivity: list[list[int]] = []

        # Loop over each tuple in the coupling map
        for a, b in backend.coupling_map:
            # Add both directions for each connection
            connectivity.extend(([a, b], [b, a]))

        # Now connectivity is in the desired format
        device.coupling_map = connectivity

        device.calibration = cls.import_target(backend.target)

        return device
