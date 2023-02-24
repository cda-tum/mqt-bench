from __future__ import annotations

import pickle
import sys
from pathlib import Path
from typing import TYPE_CHECKING, TypedDict

from joblib import Parallel, delayed
from mqt.bench import utils
from qiskit import QuantumCircuit

if TYPE_CHECKING or sys.version_info >= (3, 10, 0):  # pragma: no cover
    from importlib import resources
else:
    import importlib_resources as resources


def create_statistics() -> None:
    source_circuits_list = [file for file in Path(utils.get_qasm_output_path()).iterdir() if file.suffix == ".qasm"]
    res_dicts = Parallel(n_jobs=-1, verbose=100)(
        delayed(evaluate_qasm_file)(str(filename)) for filename in source_circuits_list
    )
    target_dir = Path(resources.files("mqt.bench") / "evaluation/")
    with Path(target_dir / "evaluation_data.pkl").open("wb") as f:
        pickle.dump(res_dicts, f)


class EvaluationResult(TypedDict):
    filename: str
    num_qubits: int
    depth: int
    num_gates: int
    num_multiple_qubit_gates: int
    program_communication: float
    critical_depth: float
    entanglement_ratio: float
    parallelism: float
    liveness: float


def evaluate_qasm_file(filename: str) -> EvaluationResult:
    print(filename)
    qc = QuantumCircuit.from_qasm_file(filename)
    qc.remove_final_measurements(inplace=True)
    (program_communication, critical_depth, entanglement_ratio, parallelism, liveness) = utils.calc_supermarq_features(
        qc
    )
    return {
        "filename": filename,
        "num_qubits": int(str(filename).split("_")[-1].split(".")[0]),
        "depth": qc.depth(),
        "num_gates": sum(qc.count_ops().values()),
        "num_multiple_qubit_gates": qc.num_nonlocal_gates(),
        "program_communication": program_communication,
        "critical_depth": critical_depth,
        "entanglement_ratio": entanglement_ratio,
        "parallelism": parallelism,
        "liveness": liveness,
    }


def count_occurrences(filenames: list[str], search_str: str) -> int:
    return sum([search_str in filename for filename in filenames])


def count_qubit_numbers_per_compiler(filenames: list[str], compiler: str) -> list[int]:
    return [int(str(filename).split("_")[-1].split(".")[0]) for filename in filenames if compiler in filename]
