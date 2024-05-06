"""Evaluation of qasm files."""

from __future__ import annotations

import pickle
from dataclasses import dataclass
from pathlib import Path

from joblib import Parallel, delayed
from qiskit import QuantumCircuit

from mqt.bench import utils


def create_statistics(source_directory: Path | None = None, target_directory: Path | None = None) -> None:
    """Create statistics for the qasm files in the source_directory and save them in the target_directory."""
    if source_directory is None:
        source_directory = Path(utils.get_default_qasm_output_path())
    if target_directory is None:
        target_directory = Path(utils.get_default_evaluation_output_path())
    source_circuits_list = [file for file in source_directory.iterdir() if file.suffix == ".qasm"]
    res_dicts = Parallel(n_jobs=-1, verbose=100)(
        delayed(evaluate_qasm_file)(str(filename)) for filename in source_circuits_list
    )
    with (target_directory / "evaluation_data.pkl").open("wb") as f:
        pickle.dump(res_dicts, f)


@dataclass
class EvaluationResult:
    """Data class for the evaluation results of a qasm file."""

    filename: str
    num_qubits: int
    depth: int
    num_gates: int
    num_multiple_qubit_gates: int
    supermarq_features: utils.SupermarqFeatures


def evaluate_qasm_file(filename: str) -> EvaluationResult | None:
    """Evaluate a qasm file and return the results."""
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
    """Count the occurrences of a search string in a list of filenames."""
    return sum(search_str in filename for filename in filenames)


def count_qubit_numbers_per_compiler(filenames: list[str], compiler: str) -> list[int]:
    """Count the number of qubits per compiler for a list of filenames."""
    return [int(str(filename).split("_")[-1].split(".")[0]) for filename in filenames if compiler in filename]
