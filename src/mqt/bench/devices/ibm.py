# Copyright (c) 2023 - 2025 Chair for Design Automation, TUM
# Copyright (c) 2025 Munich Quantum Software Company GmbH
# All rights reserved.
#
# SPDX-License-Identifier: MIT
#
# Licensed under the MIT License

"""Module to manage IBM devices."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, cast

from qiskit_ibm_runtime.fake_provider import FakeMontrealV2, FakeTorino, FakeWashingtonV2

from . import Gateset
from .calibration import DeviceCalibration
from .device import Device

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from qiskit.providers import BackendV2


class IBMDevice(Device):
    """IBM Washington device."""

    def __init__(self, backend: BackendV2, device_name: str, gateset_name: str) -> None:
        """Initialize the IBM device."""
        self.name = device_name
        self.gateset = Gateset(gateset_name, backend.operation_names)
        self.num_qubits = backend.num_qubits
        self.coupling_map = backend.coupling_map
        self.calibration = None
        self.target = backend.target

    def read_calibration(self) -> None:
        """Read the calibration data for the device."""
        calibration = DeviceCalibration()
        num_qubits = len(self.target.qubit_properties)

        for qubit in range(num_qubits):
            qubit_props = self.target.qubit_properties[qubit]
            calibration.t1[qubit] = cast("float", qubit_props.t1)
            calibration.t2[qubit] = cast("float", qubit_props.t2)

        calibration.single_qubit_gate_fidelity = {qubit: {} for qubit in range(num_qubits)}
        calibration.single_qubit_gate_duration = {qubit: {} for qubit in range(num_qubits)}
        coupling_map = self.target.build_coupling_map().get_edges()
        calibration.two_qubit_gate_fidelity = {(qubit1, qubit2): {} for qubit1, qubit2 in coupling_map}
        calibration.two_qubit_gate_duration = {(qubit1, qubit2): {} for qubit1, qubit2 in coupling_map}
        for instruction, qargs in self.target.instructions:
            if instruction.name == "reset" or instruction.name == "delay":
                continue
            # Skip control flow operations like ForLoopOp, IfElseOp, SwitchCaseOp, etc.
            try:
                instruction_props = self.target[instruction.name][qargs]
                error: float = instruction_props.error
                duration: float = instruction_props.duration
            except KeyError:
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
                calibration.two_qubit_gate_fidelity[qubit1, qubit2][instruction.name] = 1 - error
                calibration.two_qubit_gate_duration[qubit1, qubit2][instruction.name] = duration

        self.calibration = calibration


class IBMWashington(IBMDevice):
    """IBM Washington device."""

    def __init__(self) -> None:
        """Initialize the IBM Washington device."""
        super().__init__(backend=FakeWashingtonV2(), device_name="ibm_washington", gateset_name="ibm_falcon")


class IBMTorino(IBMDevice):
    """IBM Torino device."""

    def __init__(self) -> None:
        """Initialize the IBM Torino device."""
        super().__init__(backend=FakeTorino(), device_name="ibm_torino", gateset_name="ibm_heron_r1")


class IBMMontreal(IBMDevice):
    """IBM Montreal device."""

    def __init__(self) -> None:
        """Initialize the IBM Montreal device."""
        super().__init__(backend=FakeMontrealV2(), device_name="ibm_montreal", gateset_name="ibm_falcon")
