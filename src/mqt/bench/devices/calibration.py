from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class DeviceCalibration:
    """
    Calibration data for a (generic) device.

    Attributes
    single_qubit_gate_fidelity: single-qubit fidelity for each qubit and gate
    single_qubit_gate_duration: single-qubit gate duration for each qubit and gate
    two_qubit_gate_fidelity: two-qubit fidelity for each qubit pair and gate
    two_qubit_gate_duration: two-qubit gate duration for each qubit pair and gate
    readout_fidelity: readout fidelity for each qubit
    readout_duration: readout duration for each qubit
    t1: T1 time for each qubit
    t2: T2 time for each qubit
    frequency: frequency for each qubit
    """

    single_qubit_gate_fidelity: dict[int, dict[str, float]] = field(default_factory=dict)
    single_qubit_gate_duration: dict[int, dict[str, float]] = field(default_factory=dict)
    two_qubit_gate_fidelity: dict[tuple[int, ...], dict[str, float]] = field(default_factory=dict)
    two_qubit_gate_duration: dict[tuple[int, ...], dict[str, float]] = field(default_factory=dict)
    readout_fidelity: dict[int, float] = field(default_factory=dict)
    readout_duration: dict[int, float] = field(default_factory=dict)
    t1: dict[int, float] = field(default_factory=dict)
    t2: dict[int, float] = field(default_factory=dict)

    def get_single_qubit_gate_fidelity(self, gate_type: str, qubit: int) -> float:
        """
        Get the single-qubit fidelity for a given gate type and qubit.

        Args
        gate_type: name of the gate
        qubit: index of the qubit
        """
        if not self.single_qubit_gate_fidelity:
            msg = "Single-qubit gate fidelity values not available."
            raise ValueError(msg)

        try:
            return self.single_qubit_gate_fidelity[qubit][gate_type]
        except KeyError:
            msg = f"Single-qubit fidelity for gate {gate_type} and qubit {qubit} not available."
            raise ValueError(msg) from None

    def get_single_qubit_gate_duration(self, gate_type: str, qubit: int) -> float:
        """
        Get the single-qubit duration for a given gate type and qubit.

        Args
        gate_type: name of the gate
        qubit: index of the qubit
        """
        if not self.single_qubit_gate_duration:
            msg = "Single-qubit gate duration values not available."
            raise ValueError(msg)

        try:
            return self.single_qubit_gate_duration[qubit][gate_type]
        except KeyError:
            msg = f"Single-qubit duration for gate {gate_type} and qubit {qubit} not available."
            raise ValueError(msg) from None

    def get_two_qubit_gate_fidelity(self, gate_type: str, qubit1: int, qubit2: int) -> float:
        """
        Get the two-qubit fidelity for a given gate type and qubit pair.

        Args
        gate_type: name of the gate
        qubit1: index of the first qubit
        qubit2: index of the second qubit
        """
        if not self.two_qubit_gate_fidelity:
            msg = "Two-qubit gate fidelity values not available."
            raise ValueError(msg)

        try:
            return self.two_qubit_gate_fidelity[(qubit1, qubit2)][gate_type]
        except KeyError:
            msg = f"Two-qubit fidelity for gate {gate_type} and qubits {qubit1} and {qubit2} not available."
            raise ValueError(msg) from None

    def get_two_qubit_gate_duration(self, gate_type: str, qubit1: int, qubit2: int) -> float:
        """
        Get the two-qubit duration for a given gate type and qubit pair.

        Args
        gate_type: name of the gate
        qubit1: index of the first qubit
        qubit2: index of the second qubit
        """
        if not self.two_qubit_gate_duration:
            msg = "Two-qubit gate duration values not available."
            raise ValueError(msg)

        try:
            return self.two_qubit_gate_duration[(qubit1, qubit2)][gate_type]
        except KeyError:
            msg = f"Two-qubit duration for gate {gate_type} and qubits {qubit1} and {qubit2} not available."
            raise ValueError(msg) from None

    def get_readout_fidelity(self, qubit: int) -> float:
        """
        Get the readout fidelity for a given qubit.

        Args
        qubit: index of the qubit
        """
        if not self.readout_fidelity:
            msg = "Readout fidelity values not available."
            raise ValueError(msg)

        try:
            return self.readout_fidelity[qubit]
        except KeyError:
            msg = f"Readout fidelity for qubit {qubit} not available."
            raise ValueError(msg) from None

    def get_readout_duration(self, qubit: int) -> float:
        """
        Get the readout duration for a given qubit.

        Args
        qubit: index of the qubit
        """
        if not self.readout_duration:
            msg = "Readout duration values not available."
            raise ValueError(msg)

        try:
            return self.readout_duration[qubit]
        except KeyError:
            msg = f"Readout duration for qubit {qubit} not available."
            raise ValueError(msg) from None

    def get_t1(self, qubit: int) -> float:
        """
        Get the T1 time for a given qubit.

        Args
        qubit: index of the qubit
        """
        if not self.t1:
            msg = "T1 values not available."
            raise ValueError(msg)

        try:
            return self.t1[qubit]
        except KeyError:
            msg = f"T1 for qubit {qubit} not available."
            raise ValueError(msg) from None

    def get_t2(self, qubit: int) -> float:
        """
        Get the T2 time for a given qubit.

        Args
        qubit: index of the qubit
        """
        if not self.t2:
            msg = "T2 values not available."
            raise ValueError(msg)

        try:
            return self.t2[qubit]
        except KeyError:
            msg = f"T2 for qubit {qubit} not available."
            raise ValueError(msg) from None

    def compute_average_single_qubit_gate_fidelity(self, gate: str) -> float:
        """
        Compute the average single-qubit fidelity.
        """
        if not self.single_qubit_gate_fidelity:
            msg = "Single-qubit gate fidelity values not available."
            raise ValueError(msg)

        avg_single_qubit_gate_fidelity = 0.0
        entries = 0
        for fidelity in self.single_qubit_gate_fidelity.values():
            if gate in fidelity:
                avg_single_qubit_gate_fidelity += fidelity[gate]
                entries += 1
        return avg_single_qubit_gate_fidelity / entries

    def compute_average_single_qubit_gate_duration(self, gate: str) -> float:
        """
        Compute the average single-qubit duration.
        """
        if not self.single_qubit_gate_duration:
            msg = "Single-qubit gate duration values not available."
            raise ValueError(msg)

        avg_single_qubit_gate_duration = 0.0
        entries = 0
        for duration in self.single_qubit_gate_duration.values():
            if gate in duration:
                avg_single_qubit_gate_duration += duration[gate]
                entries += 1
        return avg_single_qubit_gate_duration / entries

    def compute_average_two_qubit_gate_fidelity(self, gate: str) -> float:
        """
        Compute the average two-qubit gate fidelity.
        """
        if not self.two_qubit_gate_fidelity:
            msg = "Two-qubit gate fidelity values not available."
            raise ValueError(msg)

        avg_two_qubit_gate_fidelity = 0.0
        entries = 0
        for fidelity in self.two_qubit_gate_fidelity.values():
            if gate in fidelity:
                avg_two_qubit_gate_fidelity += fidelity[gate]
                entries += 1
        return avg_two_qubit_gate_fidelity / entries

    def compute_average_two_qubit_gate_duration(self, gate: str) -> float:
        """
        Compute the average two-qubit duration.
        """
        if not self.two_qubit_gate_duration:
            msg = "Two-qubit gate duration values not available."
            raise ValueError(msg)

        avg_two_qubit_gate_duration = 0.0
        entries = 0
        for duration in self.two_qubit_gate_duration.values():
            if gate in duration:
                avg_two_qubit_gate_duration += duration[gate]
                entries += 1
        return avg_two_qubit_gate_duration / entries

    def compute_average_readout_fidelity(self) -> float:
        """
        Compute the average readout fidelity.
        """
        if not self.readout_fidelity:
            msg = "Readout fidelity values not available."
            raise ValueError(msg)

        return sum(self.readout_fidelity.values()) / len(self.readout_fidelity)

    def compute_average_readout_duration(self) -> float:
        """
        Compute the average readout duration.
        """
        if not self.readout_duration:
            msg = "Readout duration values not available."
            raise ValueError(msg)

        return sum(self.readout_duration.values()) / len(self.readout_duration)
