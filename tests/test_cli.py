"""Tests for the CLI."""

from __future__ import annotations

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
             "--compiler", "qiskit",
         ], dumps(get_benchmark(level="indep", benchmark_name="ghz", circuit_size=20, compiler="qiskit"))),
        ([
             "--level", "mapped",
             "--algorithm", "ghz",
             "--num-qubits", "20",
             "--compiler", "qiskit",
             "--qiskit-optimization-level", "2",
             "--native-gate-set", "ibm",
             "--device", "ibm_montreal",
         ], dumps(get_benchmark(
            level="mapped",
            benchmark_name="ghz",
            circuit_size=20,
            compiler="qiskit",
            compiler_settings=CompilerSettings(QiskitSettings(optimization_level=2)),
            provider_name="ibm",
            device_name="ibm_montreal",
        ))),
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
             "--level", "indep",
             "--algorithm", "ghz",
             "--num-qubits", "20",
             # Missing compiler option
         ], ""),
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
