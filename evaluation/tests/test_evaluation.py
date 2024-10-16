"""Tests for the benchmark evaluation."""

from __future__ import annotations

import json
import pickle
from pathlib import Path

import pytest
from qiskit.qasm2 import dump

from mqt.bench import utils
from mqt.bench.benchmark_generator import BenchmarkGenerator, get_benchmark
from mqt.bench.evaluation import (
    EvaluationResult,
    count_occurrences,
    count_qubit_numbers_per_compiler,
    create_statistics,
    evaluate_qasm_file,
)


@pytest.fixture
def output_path() -> str:
    """Fixture to create the output path for the tests."""
    output_path = Path("./tests/test_output/")
    output_path.mkdir(parents=True, exist_ok=True)
    return str(output_path)


@pytest.fixture
def sample_filenames() -> list[str]:
    """Fixture to return a list of sample filenames."""
    return [
        "ae_indep_qiskit_10.qasm",
        "ghz_nativegates_rigetti_qiskit_opt3_54.qasm",
        "ae_indep_tket_93.qasm",
        "wstate_nativegates_rigetti_qiskit_opt0_79.qasm",
        "ae_mapped_ibm_montreal_qiskit_opt1_9.qasm",
        "ae_mapped_ibm_washington_qiskit_opt0_38.qasm",
        "ae_mapped_oqc_lucy_qiskit_opt0_5.qasm",
        "ae_mapped_ibm_washington_qiskit_opt2_88.qasm",
        "qnn_mapped_ionq_harmony_qiskit_opt3_3.qasm",
        "qnn_mapped_oqc_lucy_tket_line_2.qasm",
        "qaoa_mapped_quantinuum_h2_tket_graph_2.qasm",
        "dj_mapped_quantinuum_h2_qiskit_opt3_23.qasm",
    ]


def test_get_default_evaluation_output_path() -> None:
    """Test the default evaluation output path."""
    path = utils.get_default_evaluation_output_path()
    assert Path(path).exists()


def test_create_benchmarks_from_config_and_evaluation(output_path: str) -> None:
    """Test the creation of benchmarks from a configuration file and the evaluation of the created benchmarks."""
    config = {
        "timeout": 1,
        "benchmarks": [
            {
                "name": "ghz",
                "include": True,
                "min_qubits": 20,
                "max_qubits": 21,
                "stepsize": 1,
                "precheck_possible": True,
            },
            {
                "name": "graphstate",
                "include": True,
                "min_qubits": 20,
                "max_qubits": 21,
                "stepsize": 1,
                "precheck_possible": True,
            },
        ],
    }
    file = Path("test_config.json")
    with file.open("w") as f:
        json.dump(config, f)

    generator = BenchmarkGenerator(cfg_path=str(file), qasm_output_path=output_path)
    generator.create_benchmarks_from_config(num_jobs=-1)
    file.unlink()

    create_statistics(source_directory=Path(output_path), target_directory=Path(output_path))

    with (Path(output_path) / "evaluation_data.pkl").open("rb") as f:
        res_dicts = pickle.load(f)
    assert len(res_dicts) > 0


def test_evaluate_qasm_file() -> None:
    """Test the evaluation of a qasm file."""
    qc = get_benchmark("dj", 1, 5)
    filename = "test_5.qasm"
    with Path(filename).open("w", encoding="locale") as f:
        dump(qc, f)
    path = Path(filename)
    res = evaluate_qasm_file(filename)
    assert type(res) is EvaluationResult
    path.unlink()

    res = evaluate_qasm_file("invalid_path.qasm")
    assert type(res) is EvaluationResult
    assert res.num_qubits == -1
    assert res.depth == -1
    assert res.num_gates == -1
    assert res.num_multiple_qubit_gates == -1
    assert res.supermarq_features == utils.SupermarqFeatures(-1.0, -1.0, -1.0, -1.0, -1.0)


@pytest.mark.parametrize(
    ("search_str", "expected_val"),
    [
        ("qiskit", 9),
        ("tket", 3),
        ("nativegates", 2),
        ("indep", 2),
        ("mapped", 8),
        ("mapped_ibm_washington", 2),
        ("mapped_ibm_montreal", 1),
        ("mapped_oqc_lucy", 2),
        ("mapped_rigetti_aspen_m3", 0),
        ("mapped_ionq_harmony", 1),
    ],
)
def test_count_occurrences(search_str: str, expected_val: int, sample_filenames: list[str]) -> None:
    """Test the count_occurrences function."""
    assert count_occurrences(sample_filenames, search_str) == expected_val


@pytest.mark.parametrize(
    ("compiler", "expected_val"),
    [
        ("qiskit", [10, 54, 79, 9, 38, 5, 88, 3, 23]),
        ("tket", [93, 2, 2]),
    ],
)
def test_count_qubit_numbers_per_compiler(compiler: str, expected_val: list[int], sample_filenames: list[str]) -> None:
    """Test the count_qubit_numbers_per_compiler function."""
    assert count_qubit_numbers_per_compiler(sample_filenames, compiler) == expected_val
