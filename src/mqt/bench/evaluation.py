from __future__ import annotations

import pickle
import sys
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING or sys.version_info >= (3, 10, 0):  # pragma: no cover
    pass
else:
    pass

from pathlib import Path

import numpy as np
from joblib import Parallel, delayed
from mqt.bench import utils
from qiskit import QuantumCircuit, QuantumRegister
from qiskit.transpiler.passes import RemoveBarriers


def create_statistics_from_qasm_files():
    source_circuits_list = [file for file in Path(utils.get_qasm_output_path()).iterdir() if file.suffix == ".qasm"]

    res = Parallel(n_jobs=-1, verbose=100)(
        delayed(evaluate_qasm_file)(filename) for filename in source_circuits_list[:10000]
    )
    target_dir = Path("/Users/nils/Documents/repos/MQTBench/")
    with Path(target_dir / "evaluation_data.pkl").open("wb") as f:
        pickle.dump(res, f)


def evaluate_qasm_file(filename: str) -> tuple[str, int, int, int, int]:
    print(filename)
    qc = QuantumCircuit.from_qasm_file(filename)
    qc.remove_final_measurements(inplace=True)
    (program_communication, critical_depth, entanglement_ratio, parallelism, liveness) = calc_supermarq_features(qc)

    return (
        filename,
        qc.num_qubits,
        qc.depth(),
        sum(qc.count_ops().values()),
        qc.num_nonlocal_gates(),
        program_communication,
        critical_depth,
        entanglement_ratio,
        parallelism,
        liveness,
    )


def calc_qubit_index(qargs: list[Any], qregs: list[QuantumRegister], index: int) -> Any:
    offset = 0
    for reg in qregs:
        if qargs[index] not in reg:
            offset += reg.size
        else:
            qubit_index = offset + reg.index(qargs[index])
            return qubit_index
    error_msg = "Qubit not found."
    raise ValueError(error_msg)


def calc_supermarq_features(
    qc: QuantumCircuit,
) -> tuple[float, float, float, float, float]:
    qc = RemoveBarriers()(qc)
    connectivity_collection: list[list[int]] = []
    liveness_A_matrix = 0
    for _ in range(qc.num_qubits):
        connectivity_collection.append([])

    for _, qargs, _ in qc.data:
        liveness_A_matrix += len(qargs)
        first_qubit = calc_qubit_index(qargs, qc.qregs, 0)
        all_indices = [first_qubit]
        if len(qargs) == 2:
            second_qubit = calc_qubit_index(qargs, qc.qregs, 1)
            all_indices.append(second_qubit)
        for qubit_index in all_indices:
            to_be_added_entries = all_indices.copy()
            to_be_added_entries.remove(int(qubit_index))
            connectivity_collection[int(qubit_index)].extend(to_be_added_entries)

    connectivity: list[Any] = []
    for i in range(qc.num_qubits):
        connectivity.append([])
        connectivity[i] = len(set(connectivity_collection[i]))

    num_gates = sum(qc.count_ops().values())
    num_multiple_qubit_gates = qc.num_nonlocal_gates()
    depth = qc.depth()
    program_communication = np.sum(connectivity) / (qc.num_qubits * (qc.num_qubits - 1))

    if num_multiple_qubit_gates == 0:
        critical_depth = 0.0
    else:
        critical_depth = qc.depth(filter_function=lambda x: len(x[1]) > 1) / num_multiple_qubit_gates

    entanglement_ratio = num_multiple_qubit_gates / num_gates
    assert num_multiple_qubit_gates <= num_gates

    parallelism = (num_gates / depth - 1) / (qc.num_qubits - 1)

    liveness = liveness_A_matrix / (depth * qc.num_qubits)

    assert 0 <= program_communication <= 1
    assert 0 <= critical_depth <= 1
    assert 0 <= entanglement_ratio <= 1
    assert 0 <= parallelism <= 1
    assert 0 <= liveness <= 1

    return (
        program_communication,
        critical_depth,
        entanglement_ratio,
        parallelism,
        liveness,
    )


create_statistics_from_qasm_files()
