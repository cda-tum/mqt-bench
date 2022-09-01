from __future__ import annotations

from qiskit import AncillaRegister, QuantumCircuit, QuantumRegister


def create_circuit(
    n: int,
    depth: int = 3,
    coin_state_preparation: QuantumCircuit = None,
    ancillary_mode: str = "noancilla",
):
    """Returns a quantum circuit implementing the Quantum Walk algorithm.

    Keyword arguments:
    num_qubits -- number of qubits of the returned quantum circuit
    depth -- number of quantum steps
    coin_state_preparation -- optional quantum circuit for state preparation
    ancillary_mode -- defining the decomposition scheme
    """

    n = n - 1  # because one qubit is needed for the coin
    coin = QuantumRegister(1, "coin")
    node = QuantumRegister(n, "node")

    n_anc = 0
    if ancillary_mode == "recursion" and n > 3:
        n_anc = 1
    if (ancillary_mode == "v-chain" or ancillary_mode == "v-chain-dirty") and n > 2:
        n_anc = n - 2

    if n_anc == 0:
        qc = QuantumCircuit(node, coin, name="qwalk")

        # coin state preparation
        if coin_state_preparation is not None:
            qc.append(coin_state_preparation, coin[:])

        for _ in range(depth):
            # Hadamard coin operator
            qc.h(coin)

            # controlled increment
            for i in range(0, n - 1):
                qc.mcx(coin[:] + node[i + 1 :], node[i], mode=ancillary_mode)
            qc.cx(coin, node[n - 1])

            # controlled decrement
            qc.x(coin)
            qc.x(node[1:])
            for i in range(0, n - 1):
                qc.mcx(coin[:] + node[i + 1 :], node[i], mode=ancillary_mode)
            qc.cx(coin, node[n - 1])
            qc.x(node[1:])
            qc.x(coin)
    else:
        anc = AncillaRegister(n_anc, "anc")
        qc = QuantumCircuit(node, coin, anc, name="qwalk")

        # coin state preparation
        if coin_state_preparation is not None:
            qc.append(coin_state_preparation, coin[:])

        for _ in range(depth):
            # Hadamard coin operator
            qc.h(coin)

            # controlled increment
            for i in range(0, n - 1):
                qc.mcx(
                    coin[:] + node[i + 1 :],
                    node[i],
                    mode=ancillary_mode,
                    ancilla_qubits=anc[:],
                )
            qc.cx(coin, node[n - 1])

            # controlled decrement
            qc.x(coin)
            qc.x(node[1:])
            for i in range(0, n - 1):
                qc.mcx(
                    coin[:] + node[i + 1 :],
                    node[i],
                    mode=ancillary_mode,
                    ancilla_qubits=anc[:],
                )
            qc.cx(coin, node[n - 1])
            qc.x(node[1:])
            qc.x(coin)

    qc.measure_all()

    return qc
