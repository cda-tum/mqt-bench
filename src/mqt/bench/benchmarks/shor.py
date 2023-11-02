# Code is based on Qiskit, therefore we have to add the following information:
# This code is part of Qiskit.
#
# (C) Copyright IBM 2019, 2022.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    from numpy.typing import NDArray
import math

import numpy as np
from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit import Gate, Instruction, ParameterVector
from qiskit.circuit.library import QFT
from qiskit.utils.validation import validate_min


def create_circuit(num_to_be_factorized: int, a: int = 2) -> QuantumCircuit:
    """Returns a quantum circuit implementing the Shor's algorithm.

    Keyword arguments:
    num_to_be_factorized -- number which shall be factorized
    a -- any integer that satisfies 1 < a < num_to_be_factorized and gcd(a, num_to_be_factorized) = 1
    """

    qc = Shor().construct_circuit(num_to_be_factorized, a)
    qc.measure_all()
    qc.name = "shor_" + str(num_to_be_factorized) + "_" + str(a)

    return qc


def get_instance(choice: str) -> list[int]:
    instances = {
        "xsmall": [9, 4],  # 18 qubits
        "small": [15, 4],  # 18 qubits
        "medium": [821, 4],  # 42 qubits
        "large": [11777, 4],  # 58 qubits
        "xlarge": [201209, 4],  # 74 qubits
    }
    return instances[choice]


class Shor:
    @staticmethod
    def _get_angles(a: int, n: int) -> NDArray[np.float_]:
        """Calculates the array of angles to be used in the addition in Fourier Space."""
        bits_little_endian = (bin(int(a))[2:].zfill(n))[::-1]

        angles = np.zeros(n)
        for i in range(n):
            for j in range(i + 1):
                k = i - j
                if bits_little_endian[j] == "1":
                    angles[i] += pow(2, -k)

        return angles * np.pi

    @staticmethod
    def _phi_add_gate(angles: NDArray[np.float_] | ParameterVector) -> Gate:
        """Gate that performs addition by a in Fourier Space."""
        circuit = QuantumCircuit(len(angles), name="phi_add_a")
        for i, angle in enumerate(angles):
            circuit.p(angle, i)
        return circuit.to_gate()

    def _double_controlled_phi_add_mod_N(
        self,
        angles: NDArray[np.float_] | ParameterVector,
        c_phi_add_N: Gate,
        iphi_add_N: Gate,
        qft: Gate,
        iqft: Gate,
    ) -> QuantumCircuit:
        """Creates a circuit which implements double-controlled modular addition by a."""
        ctrl_qreg = QuantumRegister(2, "ctrl")
        b_qreg = QuantumRegister(len(angles), "b")
        flag_qreg = QuantumRegister(1, "flag")

        circuit = QuantumCircuit(ctrl_qreg, b_qreg, flag_qreg, name="ccphi_add_a_mod_N")

        cc_phi_add_a = self._phi_add_gate(angles).control(2)
        cc_iphi_add_a = cc_phi_add_a.inverse()

        circuit.append(cc_phi_add_a, [*ctrl_qreg, *b_qreg])

        circuit.append(iphi_add_N, b_qreg)

        circuit.append(iqft, b_qreg)
        circuit.cx(b_qreg[-1], flag_qreg[0])
        circuit.append(qft, b_qreg)

        circuit.append(c_phi_add_N, [*flag_qreg, *b_qreg])

        circuit.append(cc_iphi_add_a, [*ctrl_qreg, *b_qreg])

        circuit.append(iqft, b_qreg)
        circuit.x(b_qreg[-1])
        circuit.cx(b_qreg[-1], flag_qreg[0])
        circuit.x(b_qreg[-1])
        circuit.append(qft, b_qreg)

        circuit.append(cc_phi_add_a, [*ctrl_qreg, *b_qreg])

        return circuit

    def _controlled_multiple_mod_N(
        self,
        n: int,
        N: int,
        a: int,
        c_phi_add_N: Gate,
        iphi_add_N: Gate,
        qft: Gate,
        iqft: Gate,
    ) -> Instruction:
        """Implements modular multiplication by a as an instruction."""
        ctrl_qreg = QuantumRegister(1, "ctrl")
        x_qreg = QuantumRegister(n, "x")
        b_qreg = QuantumRegister(n + 1, "b")
        flag_qreg = QuantumRegister(1, "flag")

        circuit = QuantumCircuit(ctrl_qreg, x_qreg, b_qreg, flag_qreg, name="cmult_a_mod_N")

        angle_params = ParameterVector("angles", length=n + 1)
        modulo_adder = self._double_controlled_phi_add_mod_N(angle_params, c_phi_add_N, iphi_add_N, qft, iqft)

        def append_adder(adder: QuantumCircuit, constant: int, idx: int) -> None:
            partial_constant = (pow(2, idx, N) * constant) % N
            angles = self._get_angles(partial_constant, n + 1)
            bound = adder.assign_parameters({angle_params: angles})
            circuit.append(bound, [*ctrl_qreg, x_qreg[idx], *b_qreg, *flag_qreg])

        circuit.append(qft, b_qreg)

        # perform controlled addition by a on the aux register in Fourier space
        for i in range(n):
            append_adder(modulo_adder, a, i)

        circuit.append(iqft, b_qreg)

        # perform controlled subtraction by a in Fourier space on both the aux and down register
        for i in range(n):
            circuit.cswap(ctrl_qreg, x_qreg[i], b_qreg[i])

        circuit.append(qft, b_qreg)

        a_inv = pow(a, -1, mod=N)

        modulo_adder_inv = modulo_adder.inverse()
        for i in reversed(range(n)):
            append_adder(modulo_adder_inv, a_inv, i)

        circuit.append(iqft, b_qreg)

        return circuit.to_instruction()

    def _power_mod_N(self, n: int, N: int, a: int) -> Instruction:
        """Implements modular exponentiation a^x as an instruction."""
        up_qreg = QuantumRegister(2 * n, name="up")
        down_qreg = QuantumRegister(n, name="down")
        aux_qreg = QuantumRegister(n + 2, name="aux")

        circuit = QuantumCircuit(up_qreg, down_qreg, aux_qreg, name=f"{a}^x mod {N}")

        qft = QFT(n + 1, do_swaps=False).to_gate()
        iqft = qft.inverse()

        # Create gates to perform addition/subtraction by N in Fourier Space
        phi_add_N = self._phi_add_gate(self._get_angles(N, n + 1))
        iphi_add_N = phi_add_N.inverse()
        c_phi_add_N = phi_add_N.control(1)

        # Apply the multiplication gates as showed in
        # the report in order to create the exponentiation
        for i in range(2 * n):
            partial_a = pow(a, pow(2, i), N)
            modulo_multiplier = self._controlled_multiple_mod_N(n, N, partial_a, c_phi_add_N, iphi_add_N, qft, iqft)
            circuit.append(modulo_multiplier, [up_qreg[i], *down_qreg, *aux_qreg])

        return circuit.to_instruction()

    @staticmethod
    def _validate_input(N: int, a: int) -> None:
        """Check parameters of the algorithm.

        Args:
            N: The odd integer to be factored, has a min. value of 3.
            a: Any integer that satisfies 1 < a < N and gcd(a, N) = 1.

        Raises:
            ValueError: Invalid input

        """
        validate_min("N", N, 3)
        validate_min("a", a, 2)

        if N < 1 or N % 2 == 0:
            msg = "The input needs to be an odd integer greater than 1."
            raise ValueError(msg)

        if a >= N or math.gcd(a, N) != 1:
            msg = "The integer a needs to satisfy a < N and gcd(a, N) = 1."
            raise ValueError(msg)

    def construct_circuit(self, N: int, a: int = 2) -> QuantumCircuit:
        """Construct quantum part of the algorithm.

        Args:
            N: The odd integer to be factored, has a min. value of 3.
            a: Any integer that satisfies 1 < a < N and gcd(a, N) = 1.

        Returns:
            Quantum circuit.

        """
        self._validate_input(N, a)

        # Get n value used in Shor's algorithm, to know how many qubits are used
        n = N.bit_length()

        # quantum register where the sequential QFT is performed
        up_qreg = QuantumRegister(2 * n, name="up")
        # quantum register where the multiplications are made
        down_qreg = QuantumRegister(n, name="down")
        # auxiliary quantum register used in addition and multiplication
        aux_qreg = QuantumRegister(n + 2, name="aux")

        # Create Quantum Circuit
        circuit = QuantumCircuit(up_qreg, down_qreg, aux_qreg, name=f"Shor(N={N}, a={a})")

        # Create maximal superposition in top register
        circuit.h(up_qreg)

        # Initialize down register to 1
        circuit.x(down_qreg[0])

        # Apply modulo exponentiation
        modulo_power = self._power_mod_N(n, N, a)
        circuit.append(modulo_power, circuit.qubits)

        # Apply inverse QFT
        iqft = QFT(len(up_qreg)).inverse().to_gate()
        circuit.append(iqft, up_qreg)
        return circuit
