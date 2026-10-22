# Copyright (c) 2023 - 2026 Chair for Design Automation, TUM
# Copyright (c) 2025 - 2026 Munich Quantum Software Company GmbH
# All rights reserved.
#
# SPDX-License-Identifier: MIT
#
# Licensed under the MIT License

"""Tests for QIR export with the optional MQT Core dependency."""

from __future__ import annotations

import io
from typing import TYPE_CHECKING, cast

import pytest
from qiskit import QuantumCircuit
from qiskit.circuit import Parameter

from mqt.bench import BenchmarkLevel, get_benchmark
from mqt.bench.output import MQTBenchExporterError, OutputFormat, save_circuit, write_circuit
from mqt.bench.targets import get_device

if TYPE_CHECKING:
    from pathlib import Path
    from typing import Literal

    from pytest_console_scripts import ScriptRunner

pytest.importorskip("mqt.core.mlir")


@pytest.mark.parametrize("fmt", [OutputFormat.QIR, OutputFormat.LLVM, OutputFormat.QIR_BITCODE])
@pytest.mark.parametrize("profile", ["base", "adaptive"])
def test_qir_export(fmt: OutputFormat, profile: Literal["base", "adaptive"], tmp_path: Path) -> None:
    """Text and bitcode preserve classical measurement order through streams and files."""
    from mqt.core.qdmi import ProgramFormat  # ruff:ignore[import-outside-top-level]
    from mqt.core.qdmi.builtin_driver import open_device  # ruff:ignore[import-outside-top-level]

    circuit = QuantumCircuit(2, 2, metadata={"user": 42})
    circuit.x(0)
    circuit.measure([0, 1], [1, 0])
    original = circuit.copy()
    binary = fmt is OutputFormat.QIR_BITCODE
    stream = io.BytesIO() if binary else io.StringIO()
    write_circuit(circuit, stream, BenchmarkLevel.ALG, fmt, qir_profile=profile)
    assert circuit == original
    assert circuit.metadata == original.metadata
    assert save_circuit(circuit, "qir", BenchmarkLevel.ALG, fmt, target_directory=str(tmp_path), qir_profile=profile)
    path = tmp_path / ("qir.bc" if binary else "qir.ll")
    data = path.read_bytes() if binary else path.read_text()
    assert data == stream.getvalue()
    if isinstance(data, str):
        assert data.startswith("; Benchmark created by MQT Bench")
        assert "; QIR exporter: MQT Core " in data
        assert f'"qir_profiles"="{profile}_profile"' in data
    else:
        assert data.startswith(b"BC\xc0\xde")

    device = open_device("mqt.ddsim.default")
    program_format = getattr(ProgramFormat, f"QIR_{profile.upper()}_{'MODULE' if binary else 'STRING'}")
    job = device.submit_job(data, program_format, 8)
    assert job.wait()
    assert job.get_counts() == {"10": 8}


def test_qir_feedback_and_export_errors(tmp_path: Path) -> None:
    """Adaptive export handles feedback; failed lowering leaves an existing file intact."""
    from mqt.core.qdmi import ProgramFormat  # ruff:ignore[import-outside-top-level]
    from mqt.core.qdmi.builtin_driver import open_device  # ruff:ignore[import-outside-top-level]

    circuit = QuantumCircuit(2, 2)
    circuit.x(0)
    circuit.measure(0, 0)
    with circuit.if_test((circuit.clbits[0], True)):
        circuit.x(1)
    circuit.measure(1, 1)
    stream = io.StringIO()
    write_circuit(circuit, stream, BenchmarkLevel.ALG, OutputFormat.QIR, qir_profile="adaptive")
    device = open_device("mqt.ddsim.default")
    job = device.submit_job(stream.getvalue(), ProgramFormat.QIR_ADAPTIVE_STRING, 8)
    assert job.wait()
    assert job.get_counts() == {"11": 8}

    path = tmp_path / "existing.ll"
    path.write_text("existing output")
    with pytest.raises(MQTBenchExporterError, match="Unknown QIR profile"):
        write_circuit(
            circuit,
            path,
            BenchmarkLevel.ALG,
            OutputFormat.QIR,
            qir_profile=cast('Literal["base", "adaptive"]', "invalid"),
        )
    with pytest.raises(MQTBenchExporterError, match="base profile"):
        write_circuit(circuit, path, BenchmarkLevel.ALG, OutputFormat.QIR)
    assert path.read_text() == "existing output"
    circuit.rx(Parameter("theta"), 0)
    with pytest.raises(MQTBenchExporterError, match="requires bound parameters"):
        write_circuit(circuit, path, BenchmarkLevel.ALG, OutputFormat.QIR, qir_profile="adaptive")
    assert path.read_text() == "existing output"


@pytest.mark.parametrize("fmt", [OutputFormat.QIR, OutputFormat.LLVM, OutputFormat.QIR_BITCODE])
def test_qir_stream_mode(fmt: OutputFormat) -> None:
    """Reject text/bitcode stream mismatches before writing output."""
    stream = io.StringIO() if fmt is OutputFormat.QIR_BITCODE else io.BytesIO()
    with pytest.raises(MQTBenchExporterError, match="requires a"):
        write_circuit(QuantumCircuit(1), stream, BenchmarkLevel.ALG, fmt)
    assert not stream.getvalue()


@pytest.mark.parametrize("fmt", ["qir", "llvm", "qir-bitcode"])
@pytest.mark.parametrize("save", [False, True])
def test_qir_cli(fmt: str, save: bool, script_runner: ScriptRunner, tmp_path: Path) -> None:
    """The CLI prints LLVM text or writes text/bitcode with the requested profile."""
    result = script_runner.run([
        "mqt-bench",
        "--algorithm",
        "ghz_dynamic",
        "--num-qubits",
        "3",
        "--level",
        "indep",
        "--compiler",
        "mqt",
        "--compiler-seed",
        "17",
        "--mapping-trials",
        "2",
        "--output-format",
        fmt,
        "--qir-profile",
        "adaptive",
        "--target-directory",
        str(tmp_path),
        *(["--save"] if save else []),
    ])
    assert result.success
    if fmt == "qir-bitcode":
        path = tmp_path / "ghz_dynamic_indep_mqt_3.bc"
        assert path.read_bytes().startswith(b"BC\xc0\xde")
        assert result.stdout.strip() == str(path)
    else:
        if save:
            path = tmp_path / "ghz_dynamic_indep_mqt_3.ll"
            text = path.read_text()
            assert result.stdout.strip() == str(path)
        else:
            text = result.stdout
            assert not list(tmp_path.glob("*.ll"))
        assert text.startswith("; Benchmark created by MQT Bench")
        assert "; Compiler: mqt " in text
        assert '"qir_profiles"="adaptive_profile"' in text


@pytest.mark.parametrize("fmt", [OutputFormat.QIR, OutputFormat.QIR_BITCODE])
def test_qir_io_failure(fmt: OutputFormat, tmp_path: Path) -> None:
    """QIR export reports file and stream failures through the exporter API."""
    circuit = QuantumCircuit(1)
    circuit.x(0)
    path = tmp_path / "missing" / f"circuit.{fmt.extension()}"
    with pytest.raises(MQTBenchExporterError, match="Failed to write") as exc:
        write_circuit(circuit, path, BenchmarkLevel.ALG, fmt)
    assert isinstance(exc.value.__cause__, FileNotFoundError)
    assert not path.exists()
    stream = io.BytesIO() if fmt is OutputFormat.QIR_BITCODE else io.StringIO()
    stream.close()
    with pytest.raises(MQTBenchExporterError, match="Failed to write") as exc:
        write_circuit(circuit, stream, BenchmarkLevel.ALG, fmt)
    assert isinstance(exc.value.__cause__, ValueError)


@pytest.mark.parametrize("compiler", ["qiskit", "mqt"])
@pytest.mark.parametrize("level", [BenchmarkLevel.NATIVEGATES, BenchmarkLevel.MAPPED])
def test_qir_compiled_circuit(compiler: Literal["qiskit", "mqt"], level: BenchmarkLevel) -> None:
    """Export native and mapped circuits from either compiler with measurement order intact."""
    from mqt.core.qdmi import ProgramFormat  # ruff:ignore[import-outside-top-level]
    from mqt.core.qdmi.builtin_driver import open_device  # ruff:ignore[import-outside-top-level]

    source = QuantumCircuit(2, 2)
    source.x(0)
    source.measure([0, 1], [1, 0])
    target = get_device("iqm_crystal_5")
    circuit = get_benchmark(source, level, target=target, compiler=compiler)
    original = circuit.copy()
    stream = io.StringIO()
    write_circuit(circuit, stream, level, OutputFormat.QIR, target)
    assert circuit == original
    assert circuit.layout == original.layout
    assert circuit.metadata == original.metadata
    device = open_device("mqt.ddsim.default")
    job = device.submit_job(stream.getvalue(), ProgramFormat.QIR_BASE_STRING, 8)
    assert job.wait()
    assert job.get_counts() == {"10": 8}
