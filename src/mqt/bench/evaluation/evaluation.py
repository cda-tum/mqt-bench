from __future__ import annotations

import pickle
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

from joblib import Parallel, delayed
from qiskit import QuantumCircuit

from mqt.bench import utils

if TYPE_CHECKING or sys.version_info >= (3, 10, 0):  # pragma: no cover
    from importlib import resources
else:
    import importlib_resources as resources


def create_statistics() -> None:
    source_circuits_list = [
        file for file in Path(utils.get_default_qasm_output_path()).iterdir() if file.suffix == ".qasm"
    ]
    res_dicts = Parallel(n_jobs=-1, verbose=100)(
        delayed(evaluate_qasm_file)(str(filename)) for filename in source_circuits_list
    )
    with (resources.files("mqt.bench") / "evaluation" / "evaluation_data.pkl").open("wb") as f:
        pickle.dump(res_dicts, f)


@dataclass
class EvaluationResult:
    filename: str
    num_qubits: int
    depth: int
    num_gates: int
    num_multiple_qubit_gates: int
    supermarq_features: utils.SupermarqFeatures


def evaluate_qasm_file(filename: str) -> EvaluationResult | None:
    try:
        qc = QuantumCircuit.from_qasm_file(filename)
    except Exception as e:
        print(f"Failed for {filename}: {e}")
        return EvaluationResult(
            filename=filename,
            num_qubits=-1,
            depth=-1,
            num_gates=-1,
            num_multiple_qubit_gates=-1,
            supermarq_features=utils.SupermarqFeatures(-1, -1, -1, -1, -1),
        )

    return EvaluationResult(
        filename=filename,
        num_qubits=int(str(filename).split("_")[-1].split(".")[0]),
        depth=qc.depth(),
        num_gates=sum(qc.count_ops().values()),
        num_multiple_qubit_gates=qc.num_nonlocal_gates(),
        supermarq_features=utils.calc_supermarq_features(qc),
    )


def count_occurrences(filenames: list[str], search_str: str) -> int:
    return sum([search_str in filename for filename in filenames])


def count_qubit_numbers_per_compiler(filenames: list[str], compiler: str) -> list[int]:
    return [int(str(filename).split("_")[-1].split(".")[0]) for filename in filenames if compiler in filename]
