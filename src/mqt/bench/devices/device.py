# Copyright (c) 2023 - 2025 Chair for Design Automation, TUM
# Copyright (c) 2025 Munich Quantum Software Company GmbH
# All rights reserved.
#
# SPDX-License-Identifier: MIT
#
# Licensed under the MIT License

"""Device class for representing quantum devices."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .calibration import DeviceCalibration


@dataclass
class Gateset:
    """A class to represent a set of native gates."""

    name: str
    gates: list[str]


@dataclass
class Device(ABC):
    """A class to represent a (generic) quantum device.

    Attributes:
        name: name of the device
        num_qubits: number of qubits
        gateset: gateset of the device
        coupling_map: coupling map of the device's qubits
        calibration: calibration information for the device
    """

    name: str = ""
    gateset: Gateset = field(default_factory=Gateset)  # type: ignore[arg-type]
    num_qubits: int = 0
    coupling_map: list[list[int]] = field(default_factory=list)
    calibration: DeviceCalibration | None = None

    @abstractmethod
    def read_calibration(self) -> None:
        """Read the calibration data for the device."""

    def get_single_qubit_gate_fidelity(self, gate_type: str, qubit: int) -> float:
        """Get the single-qubit fidelity for a given gate type and qubit.

        Arguments:
        gate_type: name of the gate
        qubit: index of the qubit
        """
        self.check_calibration()

        assert self.calibration is not None

        if gate_type not in self.gateset.gates:
            msg = f"Gate {gate_type} not supported by device {self.name}."
            raise ValueError(msg)

        return self.calibration.get_single_qubit_gate_fidelity(gate_type, qubit)

    def check_calibration(self) -> None:
        """Check if the calibration data is read and do so if that was not the case."""
        if self.calibration is None:
            self.read_calibration()

    def get_single_qubit_gate_duration(self, gate_type: str, qubit: int) -> float:
        """Get the single-qubit gate duration for a given gate type and qubit.

        Arguments:
        gate_type: name of the gate
        qubit: index of the qubit
        """
        self.check_calibration()
        assert self.calibration is not None

        if gate_type not in self.gateset.gates:
            msg = f"Gate {gate_type} not supported by device {self.name}."
            raise ValueError(msg)

        return self.calibration.get_single_qubit_gate_duration(gate_type, qubit)

    def get_two_qubit_gate_fidelity(self, gate_type: str, qubit1: int, qubit2: int) -> float:
        """Get the two-qubit fidelity for a given gate type and qubit pair.

        Arguments:
        gate_type: name of the gate
        qubit1: index of the first qubit
        qubit2: index of the second qubit
        """
        self.check_calibration()
        assert self.calibration is not None

        if gate_type not in self.gateset.gates:
            msg = f"Gate {gate_type} not supported by device {self.name}."
            raise ValueError(msg)

        return self.calibration.get_two_qubit_gate_fidelity(gate_type, qubit1, qubit2)

    def get_two_qubit_gate_duration(self, gate_type: str, qubit1: int, qubit2: int) -> float:
        """Get the two-qubit gate duration for a given gate type and qubit pair.

        Arguments:
        gate_type: name of the gate
        qubit1: index of the first qubit
        qubit2: index of the second qubit
        """
        self.check_calibration()
        assert self.calibration is not None

        if gate_type not in self.gateset.gates:
            msg = f"Gate {gate_type} not supported by device {self.name}."
            raise ValueError(msg)

        return self.calibration.get_two_qubit_gate_duration(gate_type, qubit1, qubit2)

    def get_readout_fidelity(self, qubit: int) -> float:
        """Get the readout fidelity for a given qubit.

        Arguments:
        qubit: index of the qubit
        """
        self.check_calibration()
        assert self.calibration is not None

        return self.calibration.get_readout_fidelity(qubit)

    def get_readout_duration(self, qubit: int) -> float:
        """Get the readout duration for a given qubit.

        Arguments:
        qubit: index of the qubit
        """
        self.check_calibration()
        assert self.calibration is not None

        return self.calibration.get_readout_duration(qubit)

    def get_single_qubit_gates(self) -> set[str]:
        """Get the set of single-qubit gates supported by the device.

        Returns:
        list of single-qubit gates
        """
        self.check_calibration()
        assert self.calibration is not None
        return {gate for qubit in range(self.num_qubits) for gate in self.calibration.single_qubit_gate_fidelity[qubit]}

    def get_two_qubit_gates(self) -> set[str]:
        """Get the set of two-qubit gates supported by the device.

        Returns:
        list of two-qubit gates
        """
        self.check_calibration()
        assert self.calibration is not None
        return {
            gate
            for qubit1, qubit2 in self.coupling_map
            for gate in self.calibration.two_qubit_gate_fidelity[qubit1, qubit2]
        }

    def sanitize_device(self) -> None:
        """Tries to sanitize the device information so that it produces the least amount of problems when used.

        It is assumed that any edge, where the average two-qubit gate fidelity is 0, is not a valid edge.
        Thus, such edges are removed from the coupling map.

        It is ensured that
         * all single-qubit gates have fidelity data for all qubits in the device
         * all two-qubit gates have fidelity data for all qubit pairs in the coupling map.
        This is accomplished by substituting the missing fidelity data with the average fidelity for the gate.
        """
        self.check_calibration()
        assert self.calibration is not None

        # ensure that all single-qubit gates have fidelity data for all qubits in the coupling map
        for gate in self.get_single_qubit_gates():
            avg_fidelity = self.calibration.compute_average_single_qubit_gate_fidelity(gate)
            for qubit in range(self.num_qubits):
                if (
                    gate not in self.calibration.single_qubit_gate_fidelity[qubit]
                    or self.calibration.single_qubit_gate_fidelity[qubit][gate] == 0
                ):
                    self.calibration.single_qubit_gate_fidelity[qubit][gate] = avg_fidelity

        # remove any edge from the coupling map that has a fidelity of 0 for all gates (see ibm_washington)
        self.coupling_map = [
            list(edge)
            for edge in self.coupling_map
            if all(fidelity != 0 for fidelity in self.calibration.two_qubit_gate_fidelity[tuple(edge)].values())
        ]
        # remove the according fidelity data for edges that are not in the edited coupling map any more
        self.calibration.two_qubit_gate_fidelity = {
            tuple(edge): self.calibration.two_qubit_gate_fidelity[tuple(edge)] for edge in self.coupling_map
        }

        # ensure that all two-qubit gates have fidelity data for all edges in the coupling map
        for gate in self.get_two_qubit_gates():
            avg_fidelity = self.calibration.compute_average_two_qubit_gate_fidelity(gate)
            for edge in self.coupling_map:
                if (
                    gate not in self.calibration.two_qubit_gate_fidelity[tuple(edge)]
                    or self.calibration.two_qubit_gate_fidelity[tuple(edge)][gate] == 0
                ):
                    self.calibration.two_qubit_gate_fidelity[tuple(edge)][gate] = avg_fidelity
