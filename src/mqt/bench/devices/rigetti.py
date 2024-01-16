from __future__ import annotations

import json
from contextlib import suppress
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
        return ["rigetti_aspen_m2"]  # NOTE: update when adding new devices

    @classmethod
    def get_native_gates(cls) -> list[str]:
        """
        Get a list of provider specific native gates.
        """
        return ["rx", "rz", "cz", "cp", "xx_plus_yy", "measure", "barrier"]  # aspen_m2

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
        return row * (ring_size * columns) + column * ring_size + ring

    @classmethod
    def __to_rigetti_index(cls, index: int) -> int:
        """
        Convert the consecutive index to the Rigetti qubit index.
        Args:
            index: the consecutive index

        Returns: the Rigetti qubit index
        """
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

        for qubit1, qubit2 in device.coupling_map:
            rigetti_index1 = cls.__to_rigetti_index(qubit1)
            rigetti_index2 = cls.__to_rigetti_index(qubit2)
            if qubit1 > qubit2:
                continue

            edge = f"{rigetti_index1}-{rigetti_index2}"
            fidelity = {}
            with suppress(KeyError):
                fidelity["cz"] = rigetti_calibration["properties"]["2Q"][edge]["fCZ"]
            with suppress(KeyError):
                fidelity["cp"] = rigetti_calibration["properties"]["2Q"][edge]["fCPHASE"]
            with suppress(KeyError):
                fidelity["xx_plus_yy"] = rigetti_calibration["properties"]["2Q"][edge]["fXY"]
            calibration.two_qubit_gate_fidelity[(qubit1, qubit2)] = fidelity

            # Rigetti calibration data is symmetric
            calibration.two_qubit_gate_fidelity[(qubit2, qubit1)] = calibration.two_qubit_gate_fidelity[
                (qubit1, qubit2)
            ]
        device.calibration = calibration
        return device
