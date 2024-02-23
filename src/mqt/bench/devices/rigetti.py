from __future__ import annotations

import json
import warnings
from typing import TYPE_CHECKING, TypedDict, cast

if TYPE_CHECKING:
    from pathlib import Path

from mqt.bench.devices import Device, DeviceCalibration, Provider


class QubitProperties(TypedDict):
    """
    Class to store the properties of a single qubit.
    """

    fActiveReset: float
    fRO: float
    f1QRB: float
    f1QRB_std_err: float
    f1Q_simultaneous_RB: float
    f1Q_simultaneous_RB_std_err: float
    T1: float
    T2: float


class TwoQubitProperties(TypedDict):
    """
    Class to store the properties of a two-qubit gate.
    """

    fCZ: float
    fCZ_std_err: float
    fCPHASE: float
    fCPHASE_std_err: float
    fXY: float
    fXY_std_err: float


Properties = TypedDict("Properties", {"1Q": dict[str, QubitProperties], "2Q": dict[str, TwoQubitProperties]})


class RigettiCalibration(TypedDict):
    """
    Class to store the calibration data of a Rigetti device.
    """

    name: str
    num_qubits: int
    basis_gates: list[str]
    connectivity: list[tuple[int, int]]
    properties: Properties


class RigettiProvider(Provider):
    """
    Class to manage Rigetti devices.
    """

    provider_name = "rigetti"

    @classmethod
    def get_available_device_names(cls) -> list[str]:
        """
        Get the names of all available Rigetti devices.
        """
        return ["rigetti_aspen_m3"]  # NOTE: update when adding new devices

    @classmethod
    def get_native_gates(cls) -> list[str]:
        """
        Get a list of provider specific native gates.
        """
        return ["rx", "rz", "cz", "cp", "xx_plus_yy", "measure", "barrier"]  # aspen_m3

    @classmethod
    def __from_rigetti_index(cls, rigetti_index: int) -> int:
        """
        Convert the Rigetti qubit index to a consecutive index.
        The Rigetti architectures consist of 8-qubit rings arranged in a two-dimensional grid.
        Each qubit is identified by a three digit number, where:
          * the first digit is the row index,
          * the second digit is the column index, and
          * the third digit is the ring index.

        Args:
            rigetti_index: the Rigetti qubit index

        Returns: the consecutive index
        """
        ring_size = 8
        columns = 5
        row = rigetti_index // 100
        column = (rigetti_index % 100) // 10
        ring = rigetti_index % 10
        qubit_indx = row * (ring_size * columns) + column * ring_size + ring
        # Account for missing qubit in Aspen-M3
        # rigetti_index: 136 = qubit_indx: 70
        if qubit_indx >= 70:
            qubit_indx = qubit_indx - 1
        return qubit_indx

    @classmethod
    def __to_rigetti_index(cls, index: int) -> int:
        """
        Convert the consecutive index to the Rigetti qubit index.
        Args:
            index: the consecutive index

        Returns: the Rigetti qubit index
        """
        # Account for missing qubit in Aspen-M3
        # rigetti_index: 136 = qubit_indx: 70
        if index >= 70:
            index = index + 1
        ring_size = 8
        columns = 5
        row = index // (ring_size * columns)
        column = (index % (ring_size * columns)) // ring_size
        ring = (index % (ring_size * columns)) % ring_size
        return row * 100 + column * 10 + ring

    @classmethod
    def import_backend(cls, path: Path) -> Device:
        """
        Import a Rigetti backend.
        Args:
            path: the path to the JSON file containing the calibration data

        Returns: the Device object
        """
        with path.open() as json_file:
            rigetti_calibration = cast(RigettiCalibration, json.load(json_file))

        device = Device()
        device.name = rigetti_calibration["name"]
        device.num_qubits = rigetti_calibration["num_qubits"]
        device.basis_gates = rigetti_calibration["basis_gates"]

        device.coupling_map = [
            [cls.__from_rigetti_index(a), cls.__from_rigetti_index(b)] for a, b in rigetti_calibration["connectivity"]
        ]

        calibration = DeviceCalibration()
        for qubit in range(device.num_qubits):
            rigetti_index = cls.__to_rigetti_index(qubit)
            calibration.single_qubit_gate_fidelity[qubit] = {
                gate: rigetti_calibration["properties"]["1Q"][str(rigetti_index)]["f1QRB"] for gate in ["rx", "rz"]
            }
            calibration.readout_fidelity[qubit] = rigetti_calibration["properties"]["1Q"][str(rigetti_index)]["fRO"]
            calibration.t1[qubit] = rigetti_calibration["properties"]["1Q"][str(rigetti_index)]["T1"]
            calibration.t2[qubit] = rigetti_calibration["properties"]["1Q"][str(rigetti_index)]["T2"]

        # Store the fidelity data of all two-qubit gates for averaging
        cz_lst, cp_lst, xx_plus_yy_lst = [], [], []
        msg = (
            "Rigetti device fidelity data is not available for some two-qubit gates."
            "The average value of the available gates will be used for the missing ones."
        )
        warnings.warn(msg, stacklevel=1)

        for qubit1, qubit2 in device.coupling_map:
            rigetti_index1 = cls.__to_rigetti_index(qubit1)
            rigetti_index2 = cls.__to_rigetti_index(qubit2)
            if qubit1 > qubit2:  # Rigetti calibration data is symmetric
                continue  # Reverse edge will be set later

            edge = f"{rigetti_index1}-{rigetti_index2}"
            fidelity = {}
            try:  # Collect the fidelity data if available and save in lst for averaging
                fidelity["cz"] = rigetti_calibration["properties"]["2Q"][edge]["fCZ"]
                cz_lst.append(fidelity["cz"])
            except KeyError:  # If not available, set to -1 to indicate missing
                fidelity["cz"] = -1.0
            try:
                fidelity["cp"] = rigetti_calibration["properties"]["2Q"][edge]["fCPHASE"]
                cp_lst.append(fidelity["cp"])
            except KeyError:
                fidelity["cp"] = -1.0
            try:
                fidelity["xx_plus_yy"] = rigetti_calibration["properties"]["2Q"][edge]["fXY"]
                xx_plus_yy_lst.append(fidelity["xx_plus_yy"])
            except KeyError:
                fidelity["xx_plus_yy"] = -1.0

            # Save the fidelity data for the two-qubit gate
            calibration.two_qubit_gate_fidelity[(qubit1, qubit2)] = fidelity

        # If there are missing values, use the average
        cz_avg = sum(cz_lst) / len(cz_lst)
        cp_avg = sum(cp_lst) / len(cp_lst)
        xx_plus_yy_avg = sum(xx_plus_yy_lst) / len(xx_plus_yy_lst)

        for qubit1, qubit2 in device.coupling_map:
            if qubit1 > qubit2:
                continue
            # Check if the fidelity data is missing (== -1) and set to average if so
            if calibration.two_qubit_gate_fidelity[(qubit1, qubit2)]["cz"] < 0:
                calibration.two_qubit_gate_fidelity[(qubit1, qubit2)]["cz"] = cz_avg
            if calibration.two_qubit_gate_fidelity[(qubit1, qubit2)]["cp"] < 0:
                calibration.two_qubit_gate_fidelity[(qubit1, qubit2)]["cp"] = cp_avg
            if calibration.two_qubit_gate_fidelity[(qubit1, qubit2)]["xx_plus_yy"] < 0:
                calibration.two_qubit_gate_fidelity[(qubit1, qubit2)]["xx_plus_yy"] = xx_plus_yy_avg

            # Rigetti calibration data is symmetric, set same values for reverse edge
            calibration.two_qubit_gate_fidelity[(qubit2, qubit1)] = calibration.two_qubit_gate_fidelity[
                (qubit1, qubit2)
            ]
        device.calibration = calibration
        return device
