"""Tests for the CLI."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import pytest
from qiskit.qasm2 import dumps

from mqt.bench import CompilerSettings, QiskitSettings, get_benchmark

if TYPE_CHECKING:
    from pytest_console_scripts import ScriptRunner


# fmt: off
@pytest.mark.parametrize(
    ("args", "expected_output"),
    [
        ([
             "--level", "alg",
             "--algorithm", "ghz",
             "--num-qubits", "10",
         ], dumps(get_benchmark(level="alg", benchmark_name="ghz", circuit_size=10))),
        ([
             "--level", "alg",
             "--algorithm", "shor_xsmall",
             "--num-qubits", "10",
         ], "OPENQASM 2.0;"),  # Note: shor is non-deterministic, so just a basic sanity check
        ([
             "--level", "alg",
             "--algorithm", "ghz",
             "--num-qubits", "20",
         ], dumps(get_benchmark(level="alg", benchmark_name="ghz", circuit_size=20))),
        ([
             "--level", "indep",
             "--algorithm", "ghz",
             "--num-qubits", "20",
         ], dumps(get_benchmark(level="indep", benchmark_name="ghz", circuit_size=20))),
        ([
             "--level", "nativegates",
             "--algorithm", "ghz",
             "--num-qubits", "20",
             "--native-gate-set", "ibm",
         ], dumps(get_benchmark(level="nativegates", benchmark_name="ghz", circuit_size=20, provider_name="ibm"))),
        ([
             "--level", "mapped",
             "--algorithm", "ghz",
             "--num-qubits", "20",
             "--qiskit-optimization-level", "2",
             "--native-gate-set", "ibm",
             "--device", "ibm_montreal",
         ], dumps(get_benchmark(
            level="mapped",
            benchmark_name="ghz",
            circuit_size=20,
            compiler_settings=CompilerSettings(QiskitSettings(optimization_level=2)),
            provider_name="ibm",
            device_name="ibm_montreal",
        ))),
        ([
             "--level", "mapped",
             "--algorithm", "ghz",
             "--num-qubits", "20",
             "--qiskit-optimization-level", "2",
             "--device", "ibm_montreal",
         ], dumps(get_benchmark(
            level="mapped",
            benchmark_name="ghz",
            circuit_size=20,
            compiler_settings=CompilerSettings(QiskitSettings(optimization_level=2)),
            device_name="ibm_montreal",
        ))),
        (["--help"], "usage: mqt.bench.cli"),
    ],
)
def test_cli(args: list[str], expected_output: str, script_runner: ScriptRunner) -> None:
    """Test the CLI with different arguments."""
    ret = script_runner.run(["mqt.bench.cli", *args])
    assert ret.success
    assert expected_output in ret.stdout


# fmt: off
@pytest.mark.parametrize(
    ("args", "expected_output"),
    [
        ([], "usage: mqt.bench.cli"),
        (["asd"], "usage: mqt.bench.cli"),
        (["--benchmark", "ae"], "usage: mqt.bench.cli"),
        # Note: We don't care about the actual error messages in most cases
        ([
             "--level", "alg",
             "--algorithm", "not-a-valid-benchmark",
             "--num-qubits", "20",
         ], ""),
    ],
)
def test_cli_errors(args: list[str], expected_output: str, script_runner: ScriptRunner) -> None:
    """Test the CLI with different error cases."""
    ret = script_runner.run(["mqt.bench.cli", *args])
    assert not ret.success
    assert expected_output in ret.stderr


def test_cli_output_formats_and_save(tmp_path: Path, script_runner: ScriptRunner) -> None:
    """Test output formats and save functionality."""
    # Test QASM3 prints to stdout when not saving
    ret_qasm3 = script_runner.run([
        "mqt.bench.cli",
        "--level", "alg",
        "--algorithm", "ghz",
        "--num-qubits", "5",
        "--output-format", "qasm3",
    ])
    assert ret_qasm3.success
    # QASM3 header should appear and not relate to save
    assert "MQT Bench version:" in ret_qasm3.stdout
    assert "OPENQASM" in ret_qasm3.stdout

    # Test saving QPY to a file
    target_dir = str(tmp_path)
    target_file = "mybench"
    ret_qpy = script_runner.run([
        "mqt.bench.cli",
        "--level", "alg",
        "--algorithm", "ghz",
        "--num-qubits", "5",
        "--output-format", "qpy",
        "--save",
        "--target-directory", target_dir,
        "--target-filename", target_file,
    ])
    # File should exist
    assert ret_qpy.success
    # Should output the path to the saved file
    expected_path = str(Path(target_dir) / f"{target_file}.qpy")
    assert expected_path in ret_qpy.stdout
    # File should exist
    assert (tmp_path / f"{target_file}.qpy").is_file()
