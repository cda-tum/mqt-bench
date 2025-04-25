"""Tests for the benchmark generation."""

from __future__ import annotations

import builtins
import io
from datetime import date
from importlib import metadata
from pathlib import Path
from typing import TYPE_CHECKING, NoReturn

if TYPE_CHECKING:  # pragma: no cover
    import types

from enum import Enum

import pytest
from qiskit import QuantumCircuit, qpy
from qiskit.qasm3 import load as load_qasm3

from mqt.bench.benchmark_generation import (
    CompilerSettings,
    QiskitSettings,
    generate_filename,
    get_alg_level,
    get_benchmark,
    get_indep_level,
    get_mapped_level,
    get_module_for_benchmark,
    get_native_gates_level,
    get_openqasm_gates,
    get_supported_benchmarks,
)
from mqt.bench.benchmarks import (
    ae,
    bv,
    dj,
    ghz,
    graphstate,
    grover,
    qaoa,
    qft,
    qftentangled,
    qnn,
    qpeexact,
    qpeinexact,
    quarkcardinality,
    quarkcopula,
    qwalk,
    randomcircuit,
    shor,
    vqerealamprandom,
    vqesu2random,
    vqetwolocalrandom,
    wstate,
)
from mqt.bench.devices import IBMProvider, OQCProvider, get_available_providers, get_provider_by_name
from mqt.bench.output import (
    MQTBenchExporterError,
    OutputFormat,
    __qiskit_version__,
    generate_header,
    save_circuit,
    write_circuit,
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
        "ghz_nativegates_rigetti_opt3_54.qasm",
        "ae_indep_93.qasm",
        "wstate_nativegates_rigetti_opt0_79.qasm",
        "ae_mapped_ibm_montreal_opt1_9.qasm",
        "ae_mapped_ibm_washington_opt0_38.qasm",
        "ae_mapped_oqc_lucy_opt0_5.qasm",
        "ae_mapped_ibm_washington_opt2_88.qasm",
        "qnn_mapped_ionq_harmony_opt3_3.qasm",
        "qnn_mapped_oqc_lucy_2.qasm",
        "qaoa_mapped_quantinuum_h2_graph_2.qasm",
        "dj_mapped_quantinuum_h2_opt3_23.qasm",
    ]


@pytest.mark.parametrize(
    ("benchmark", "input_value", "scalable"),
    [
        (ae, 3, True),
        (bv, 3, True),
        (ghz, 2, True),
        (dj, 3, True),
        (graphstate, 3, True),
        (grover, 3, False),
        (qaoa, 3, True),
        (qft, 3, True),
        (qftentangled, 3, True),
        (qnn, 3, True),
        (qpeexact, 3, True),
        (qpeinexact, 3, True),
        (quarkcardinality, 3, True),
        (quarkcopula, 3, True),
        (qwalk, 3, False),
        (randomcircuit, 3, True),
        (vqerealamprandom, 3, True),
        (vqesu2random, 3, True),
        (vqetwolocalrandom, 3, True),
        (wstate, 3, True),
        # (shor, 3, False),
    ],
)
def test_quantumcircuit_alg_level(
    benchmark: types.ModuleType, input_value: int, scalable: bool, output_path: str
) -> None:
    """Test the creation of the algorithm level benchmarks for the benchmarks."""
    qc = benchmark.create_circuit(input_value)
    if scalable:
        assert qc.num_qubits == input_value
    assert benchmark.__name__.split(".")[-1] in qc.name
    filename = "testfile"
    filepath = Path(output_path) / (filename + ".qasm")
    res = get_alg_level(qc, input_value, False, False, output_path, filename)
    assert res
    assert load_qasm3(filepath)

    res = get_alg_level(
        qc,
        input_value,
        file_precheck=True,
        return_qc=False,
        target_directory=output_path,
        target_filename=filename,
        output_format=OutputFormat.QASM3,
    )
    assert res
    assert load_qasm3(filepath)
    filepath.unlink()

    res = get_alg_level(
        qc,
        input_value,
        file_precheck=True,
        return_qc=True,
    )
    assert res.num_qubits >= input_value

    with pytest.raises(
        ValueError, match=r"'qasm2' is not supported for the algorithm level; please use e.g. 'qasm3' or 'qpy'."
    ):
        get_alg_level(qc, input_value, False, False, output_path, filename, output_format=OutputFormat.QASM2)


@pytest.mark.parametrize(
    ("benchmark", "input_value", "scalable"),
    [
        (ae, 3, True),
        (bv, 3, True),
        (ghz, 2, True),
        (dj, 3, True),
        (graphstate, 3, True),
        (grover, 3, False),
        (qaoa, 3, True),
        (qft, 3, True),
        (qftentangled, 3, True),
        (qnn, 3, True),
        (qpeexact, 3, True),
        (qpeinexact, 3, True),
        (qwalk, 3, False),
        (randomcircuit, 3, True),
        (vqerealamprandom, 3, True),
        (vqesu2random, 3, True),
        (vqetwolocalrandom, 3, True),
        (wstate, 3, True),
        (shor, 3, False),
    ],
)
def test_quantumcircuit_indep_level(
    benchmark: types.ModuleType, input_value: int, scalable: bool, output_path: str
) -> None:
    """Test the creation of the independent level benchmarks for the benchmarks."""
    if benchmark in (grover, qwalk):
        qc = benchmark.create_circuit(input_value, ancillary_mode="noancilla")
    else:
        qc = benchmark.create_circuit(input_value)

    if scalable:
        assert qc.num_qubits == input_value
    assert benchmark.__name__.split(".")[-1] in qc.name
    res = get_indep_level(
        qc,
        input_value,
        file_precheck=False,
        return_qc=False,
        target_directory=output_path,
    )
    assert res
    res = get_indep_level(
        qc,
        input_value,
        file_precheck=True,
        return_qc=False,
        target_directory=output_path,
    )
    assert res


@pytest.mark.parametrize(
    ("benchmark", "input_value", "scalable"),
    [
        (ae, 3, True),
        (bv, 3, True),
        (ghz, 3, True),
        (dj, 3, True),
        (graphstate, 3, True),
        (grover, 3, False),
        (qaoa, 3, True),
        (qft, 3, True),
        (qftentangled, 3, True),
        (qnn, 3, True),
        (qpeexact, 3, True),
        (qpeinexact, 3, True),
        (qwalk, 3, False),
        (randomcircuit, 3, True),
        (vqerealamprandom, 3, True),
        (vqesu2random, 3, True),
        (vqetwolocalrandom, 3, True),
        (wstate, 3, True),
    ],
)
def test_quantumcircuit_native_and_mapped_levels(
    benchmark: types.ModuleType, input_value: int, scalable: bool, output_path: str
) -> None:
    """Test the creation of the native and mapped level benchmarks for the benchmarks."""
    if benchmark in (grover, qwalk):
        qc = benchmark.create_circuit(input_value, ancillary_mode="noancilla")
    else:
        qc = benchmark.create_circuit(input_value)

    assert isinstance(qc, QuantumCircuit)
    if scalable:
        assert qc.num_qubits == input_value

    providers = get_available_providers()
    for provider in providers:
        opt_level = 1
        res = get_native_gates_level(
            qc,
            provider,
            qc.num_qubits,
            opt_level,
            file_precheck=False,
            return_qc=False,
            target_directory=output_path,
        )
        assert res
        res = get_native_gates_level(
            qc,
            provider,
            qc.num_qubits,
            opt_level,
            file_precheck=True,
            return_qc=False,
            target_directory=output_path,
        )
        assert res

        provider.get_native_gates()
        for device in provider.get_available_devices():
            # Creating the circuit on target-dependent: mapped level qiskit
            if device.num_qubits >= qc.num_qubits:
                res = get_mapped_level(
                    qc,
                    qc.num_qubits,
                    device,
                    opt_level,
                    file_precheck=False,
                    return_qc=False,
                    target_directory=output_path,
                )
                assert res
                res = get_mapped_level(
                    qc,
                    qc.num_qubits,
                    device,
                    opt_level,
                    file_precheck=True,
                    return_qc=False,
                    target_directory=output_path,
                )
                assert res


def test_openqasm_gates() -> None:
    """Test the openqasm gates."""
    openqasm_gates = get_openqasm_gates()
    num_openqasm_gates = 42
    assert len(openqasm_gates) == num_openqasm_gates


def test_bv() -> None:
    """Test the creation of the BV benchmark."""
    qc = bv.create_circuit(3)
    assert qc.depth() > 0
    assert qc.num_qubits == 3
    assert "bv" in qc.name

    qc = bv.create_circuit(3, dynamic=True)
    assert qc.depth() > 0
    assert qc.num_qubits == 3
    assert "bv" in qc.name

    with pytest.raises(ValueError, match=r"Length of hidden_string must be num_qubits - 1."):
        bv.create_circuit(3, hidden_string="wrong")


def test_dj_constant_oracle() -> None:
    """Test the creation of the DJ benchmark constant oracle."""
    qc = dj.create_circuit(5, False)
    assert qc.depth() > 0


@pytest.mark.parametrize(
    (
        "benchmark_name",
        "level",
        "circuit_size",
        "benchmark_instance_name",
        "compiler_settings",
        "provider_name",
        "device_name",
    ),
    [
        (
            "dj",
            "alg",
            3,
            None,
            None,
            "",
            "",
        ),
        (
            "wstate",
            0,
            3,
            None,
            None,
            "",
            "",
        ),
        (
            "ghz",
            "indep",
            3,
            None,
            None,
            "",
            "",
        ),
        (
            "graphstate",
            1,
            3,
            None,
            None,
            "",
            "",
        ),
        (
            "dj",
            "nativegates",
            3,
            None,
            CompilerSettings(qiskit=QiskitSettings(optimization_level=2)),
            "ionq",
            "",
        ),
        (
            "dj",
            "nativegates",
            3,
            None,
            CompilerSettings(qiskit=QiskitSettings(optimization_level=2)),
            "ibm",
            "",
        ),
        (
            "dj",
            "nativegates",
            3,
            None,
            CompilerSettings(qiskit=QiskitSettings(optimization_level=2)),
            "rigetti",
            "rigetti_aspen_m3",
        ),
        (
            "dj",
            "nativegates",
            3,
            None,
            CompilerSettings(qiskit=QiskitSettings(optimization_level=2)),
            "oqc",
            "oqc_lucy",
        ),
        (
            "qft",
            2,
            3,
            None,
            CompilerSettings(qiskit=QiskitSettings(optimization_level=3)),
            "ionq",
            "ionq_harmony1",
        ),
        (
            "qft",
            2,
            3,
            None,
            CompilerSettings(qiskit=QiskitSettings(optimization_level=3)),
            "ibm",
            "ibm_montreal",
        ),
        ("qft", 2, 6, None, None, "rigetti", "rigetti_aspen_m3"),
        (
            "qft",
            2,
            3,
            None,
            None,
            "oqc",
            "oqc_lucy",
        ),
        (
            "qpeexact",
            "mapped",
            3,
            None,
            CompilerSettings(qiskit=QiskitSettings(optimization_level=1)),
            "ibm",
            "ibm_washington",
        ),
        (
            "qpeexact",
            "mapped",
            3,
            None,
            CompilerSettings(qiskit=QiskitSettings(optimization_level=1)),
            "ibm",
            "ibm_montreal",
        ),
        (
            "qpeexact",
            "mapped",
            3,
            None,
            CompilerSettings(qiskit=QiskitSettings(optimization_level=1)),
            "rigetti",
            "rigetti_aspen_m3",
        ),
        (
            "qpeexact",
            "mapped",
            3,
            None,
            CompilerSettings(qiskit=QiskitSettings(optimization_level=1)),
            "ionq",
            "ionq_harmony",
        ),
        (
            "qpeexact",
            "mapped",
            3,
            None,
            CompilerSettings(qiskit=QiskitSettings(optimization_level=1)),
            "ionq",
            "ionq_aria1",
        ),
        (
            "qpeexact",
            "mapped",
            3,
            None,
            CompilerSettings(qiskit=QiskitSettings(optimization_level=2)),
            "ionq",
            "ionq_aria1",
        ),
        (
            "qpeexact",
            "mapped",
            3,
            None,
            CompilerSettings(qiskit=QiskitSettings(optimization_level=1)),
            "oqc",
            "oqc_lucy",
        ),
        (
            "qpeinexact",
            3,
            3,
            None,
            CompilerSettings(qiskit=QiskitSettings(optimization_level=1)),
            "ibm",
            "ibm_washington",
        ),
        (
            "qpeinexact",
            3,
            3,
            None,
            CompilerSettings(qiskit=QiskitSettings(optimization_level=1)),
            "ibm",
            "ibm_montreal",
        ),
        (
            "qpeinexact",
            3,
            3,
            None,
            CompilerSettings(qiskit=QiskitSettings(optimization_level=1)),
            "rigetti",
            "rigetti_aspen_m3",
        ),
        (
            "qpeinexact",
            3,
            3,
            None,
            CompilerSettings(qiskit=QiskitSettings(optimization_level=1)),
            "oqc",
            "oqc_lucy",
        ),
        (
            "qpeinexact",
            3,
            3,
            None,
            CompilerSettings(qiskit=QiskitSettings(optimization_level=2)),
            "quantinuum",
            "quantinuum_h2",
        ),
        (
            "grover-noancilla",
            "alg",
            3,
            None,
            None,
            "",
            "",
        ),
        (
            "qwalk-noancilla",
            "alg",
            3,
            None,
            None,
            "",
            "",
        ),
        (
            "grover-v-chain",
            "alg",
            3,
            None,
            None,
            "",
            "",
        ),
        (
            "qwalk-v-chain",
            "alg",
            3,
            None,
            None,
            "",
            "",
        ),
        (
            "shor",
            "alg",
            None,
            "xsmall",
            None,
            "",
            "",
        ),
    ],
)
def test_get_benchmark(
    benchmark_name: str,
    level: str | int,
    circuit_size: int | None,
    benchmark_instance_name: str | None,
    compiler_settings: CompilerSettings | None,
    provider_name: str,
    device_name: str,
) -> None:
    """Test the creation of the benchmarks using the get_benchmark method."""
    qc = get_benchmark(
        benchmark_name,
        level,
        circuit_size,
        benchmark_instance_name,
        compiler_settings,
        provider_name,
        device_name,
    )
    assert qc.depth() > 0
    if provider_name and "oqc" not in provider_name:
        assert isinstance(qc, QuantumCircuit)
        for qc_instruction in qc.data:
            instruction = qc_instruction.operation
            gate_type = instruction.name
            provider = get_provider_by_name(provider_name)
            assert gate_type in provider.get_native_gates() or gate_type == "barrier"


def test_get_benchmark_faulty_parameters() -> None:
    """Test the get_benchmark method with faulty parameters."""
    match = "Selected benchmark is not supported. Valid benchmarks are"
    with pytest.raises(ValueError, match=match):
        get_benchmark("wrong_name", 2, 6)
    match = "Selected level must be in"
    with pytest.raises(ValueError, match=match):
        get_benchmark(  # type: ignore[call-overload]
            "qpeexact",
            8,
            "wrong_size",
            None,
            CompilerSettings(qiskit=QiskitSettings(optimization_level=1)),
            "rigetti",
            "rigetti_aspen_m3",
        )
    match = "circuit_size must be None or int for this benchmark."
    with pytest.raises(ValueError, match=match):
        get_benchmark(
            "dj",
            1,
            -1,
            None,
            CompilerSettings(qiskit=QiskitSettings(optimization_level=1)),
            "rigetti",
            "rigetti_aspen_m3",
        )

    match = "benchmark_instance_name must be defined for this benchmark."
    with pytest.raises(ValueError, match=match):
        get_benchmark(  # type: ignore[call-overload]
            "shor",
            1,
            3,
            2,
            CompilerSettings(qiskit=QiskitSettings(optimization_level=1)),
            "rigetti",
            "rigetti_aspen_m3",
        )

    match = "compiler_settings must be of type CompilerSettings or None"
    with pytest.raises(ValueError, match=match):
        get_benchmark(  # type: ignore[call-overload]
            "qpeexact",
            1,
            3,
            None,
            "wrong_compiler_settings",
            "rigetti",
            "rigetti_aspen_m3",
        )
    match = "Selected provider_name must be in"
    with pytest.raises(ValueError, match=match):
        get_benchmark(
            "qpeexact",
            2,
            3,
            None,
            CompilerSettings(qiskit=QiskitSettings(optimization_level=1)),
            "wrong_gateset",
            "rigetti_aspen_m3",
        )
    match = "Selected device_name must be in"
    with pytest.raises(ValueError, match=match):
        get_benchmark(
            "qpeexact",
            3,
            3,
            None,
            CompilerSettings(qiskit=QiskitSettings(optimization_level=1)),
            "rigetti",
            "wrong_device",
        )


def test_configure_end(output_path: str) -> None:
    """Removes all temporarily created files while testing."""
    # delete all files in the test directory and the directory itself
    for f in Path(output_path).iterdir():
        f.unlink()
    Path(output_path).rmdir()


@pytest.mark.parametrize(
    "abstraction_level",
    [
        (1),
        (2),
        (3),
    ],
)
def test_saving_qasm_to_alternative_location_with_alternative_filename(
    abstraction_level: int,
) -> None:
    """Test saving the qasm file to an alternative location with an alternative filename."""
    directory = "."
    filename = "ae_test_qiskit"
    qc = get_benchmark("ae", abstraction_level, 5)
    assert qc
    res = get_mapped_level(
        qc,
        qc.num_qubits,
        IBMProvider.get_device("ibm_washington"),
        1,
        False,
        False,
        directory,
        filename,
    )
    assert res
    path = Path(directory) / Path(filename).with_suffix(".qasm")
    assert path.is_file()
    path.unlink()


def test_oqc_benchmarks() -> None:
    """Test the creation of benchmarks for the OQC devices."""
    qc = get_benchmark("ghz", 1, 5)
    directory = "."
    filename = "ghz_oqc"
    path = Path(directory) / Path(filename).with_suffix(".qasm")

    get_native_gates_level(
        qc,
        OQCProvider(),
        qc.num_qubits,
        opt_level=1,
        file_precheck=False,
        return_qc=False,
        target_directory=directory,
        target_filename=filename,
        output_format=OutputFormat.QASM2,
    )
    assert QuantumCircuit.from_qasm_file(str(path))
    path.unlink()
    directory = "."
    filename = "ghz_oqc2"
    path = Path(directory) / Path(filename).with_suffix(".qasm")
    get_mapped_level(
        qc,
        qc.num_qubits,
        OQCProvider().get_device("oqc_lucy"),
        opt_level=1,
        file_precheck=False,
        return_qc=False,
        target_directory=directory,
        target_filename=filename,
        output_format=OutputFormat.QASM2,
    )

    assert QuantumCircuit.from_qasm_file(str(path))
    path.unlink()


def test_get_module_for_benchmark() -> None:
    """Test the get_module_for_benchmark function."""
    for benchmark in get_supported_benchmarks():
        assert get_module_for_benchmark(benchmark.split("-")[0]) is not None


def test_benchmark_helper_shor() -> None:
    """Testing the Shor benchmarks."""
    shor_instances = ["xsmall", "small", "medium", "large", "xlarge"]
    for elem in shor_instances:
        res_shor = shor.get_instance(elem)
        assert res_shor


def test_validate_input() -> None:
    """Test the _validate_input() method for various edge cases."""
    # Case 1: to_be_factored_number (N) < 3.
    with pytest.raises(ValueError, match=r"N must have value >= 3, was 2"):
        shor.create_circuit(2, 2)

    # Case 2: a < 2.
    with pytest.raises(ValueError, match=r"a must have value >= 2, was 1"):
        shor.create_circuit(15, 1)

    # Case 3: N is even (and thus not odd).
    with pytest.raises(ValueError, match=r"The input needs to be an odd integer greater than 1."):
        shor.create_circuit(4, 3)

    # Case 4: a >= N.
    with pytest.raises(ValueError, match=r"The integer a needs to satisfy a < N and gcd\(a, N\) = 1."):
        shor.create_circuit(15, 15)

    # Case 5: gcd(a, N) != 1 (for example, N=15 and a=6, since gcd(15,6)=3).
    with pytest.raises(ValueError, match=r"The integer a needs to satisfy a < N and gcd\(a, N\) = 1."):
        shor.create_circuit(15, 6)

    # Case 6: Valid input (should not raise any exception).
    try:
        shor.create_circuit(15, 2)
    except ValueError as e:
        pytest.fail(f"Unexpected ValueError raised for valid input: {e}")


def test_create_ae_circuit_with_invalid_qubit_number() -> None:
    """Testing the minimum number of qubits in the amplitude estimation circuit."""
    with pytest.raises(ValueError, match=r"Number of qubits must be at least 2 \(1 evaluation \+ 1 target\)."):
        get_benchmark("ae", 1, 1)


@pytest.mark.parametrize(
    ("level", "expected"),
    [
        ("alg", "ghz_alg_5"),
        ("indep", "ghz_indep_5"),
        ("nativegates", "ghz_nativegates_ibm_opt2_5"),
        ("mapped", "ghz_mapped_ibm_washington_opt2_5"),
    ],
)
def test_generate_filename(level: str, expected: str) -> None:
    """Test the generation of a filename."""
    filename = generate_filename(
        benchmark_name="ghz",
        level=level,
        num_qubits=5,
        provider_name="ibm",
        device_name="ibm_washington",
        opt_level=2,
    )
    assert filename == expected


@pytest.fixture(autouse=True)
def temp_dir(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Ensure all files go into a temporary directory."""
    monkeypatch.chdir(tmp_path)
    return tmp_path


def test_generate_header_minimal(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test the generation of a minimal header."""
    monkeypatch.setattr(metadata, "version", lambda _: "9.9.9")
    hdr = generate_header(OutputFormat.QASM3)
    lines = hdr.splitlines()
    # first line has today's date
    assert lines[0] == f"// Benchmark created by MQT Bench on {date.today()}"
    # contains the fixed info lines
    assert "// For more info: https://www.cda.cit.tum.de/mqtbench/" in hdr
    assert "// MQT Bench version: 9.9.9" in hdr
    assert f"// Qiskit version: {__qiskit_version__}" in hdr
    assert f"// Output format: {OutputFormat.QASM3.value}" in hdr
    # no gate_set or mapping lines when omitted
    assert "// Used gate set:" not in hdr
    assert "// Coupling map:" not in hdr


def test_generate_header_with_options(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test the generation of a header with options."""
    monkeypatch.setattr(metadata, "version", lambda _: "0.1.0")
    gates = ["x", "cx", "h"]
    cmap = [[0, 1], [1, 2]]
    hdr = generate_header(OutputFormat.QASM2, gate_set=gates, c_map=cmap)

    assert f"// Used gate set: {gates}" in hdr
    assert f"// Coupling map: {cmap}" in hdr


def test_generate_header_pkg_not_installed(monkeypatch: pytest.MonkeyPatch) -> None:
    """metadata.version raises PackageNotFoundError."""
    monkeypatch.setattr(
        metadata,
        "version",
        lambda _pkg: (_ for _ in ()).throw(MQTBenchExporterError("boom")),
    )
    with pytest.raises(MQTBenchExporterError) as exc:
        generate_header(OutputFormat.QASM2)

    msg = str(exc.value)
    assert "not installed" in msg.lower()
    assert "mqt.bench" in msg


@pytest.mark.parametrize("fmt", [OutputFormat.QASM2, OutputFormat.QASM3])
def test_write_circuit_qasm(tmp_path: Path, fmt: OutputFormat) -> None:
    """Test writing a QASM circuit."""
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)

    out = tmp_path / "test.qasm"
    write_circuit(qc, out, fmt=fmt)

    text = out.read_text().splitlines()
    # header lines at top
    assert text[0].startswith("// Benchmark created by MQT Bench on")
    # QASM body present
    assert any(line.startswith("h ") for line in text), "H gate should appear"
    assert any(line.startswith("cx ") for line in text), "CX gate should appear"


def test_write_circuit_qpy(tmp_path: Path) -> None:
    """Test writing a QPY circuit with header embedded in metadata."""
    qc = QuantumCircuit(1)
    qc.x(0)
    out = tmp_path / "test.qpy"
    write_circuit(qc, out, fmt=OutputFormat.QPY)

    data = out.read_bytes()
    assert data.startswith(b"QISKIT"), "QPY file must start with the QISKIT magic"

    with out.open("rb") as fd:
        loaded = list(qpy.load(fd))
    assert len(loaded) == 1
    circ = loaded[0]
    assert isinstance(circ, QuantumCircuit)

    header = circ.metadata["mqt_bench"]
    assert header.startswith(f"// Benchmark created by MQT Bench on {date.today()}")
    assert "// MQT Bench version:" in header
    assert "// Output format: qpy" in header


def test_write_circuit_io_error(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Simulate I/O error while writing."""
    qc = QuantumCircuit(1)
    qc.h(0)

    out = tmp_path / "readonly.qasm"

    # Monkey-patch builtins.open to throw OSError on any attempt to open for writing
    def fake_open(*args: str, **kwargs: str) -> NoReturn:
        msg = "disk full"
        raise OSError(msg)

    monkeypatch.setattr(Path, "open", fake_open)
    monkeypatch.setattr(metadata, "version", lambda _: "0.1.0")

    with pytest.raises(MQTBenchExporterError) as exc:
        write_circuit(qc, out, fmt=OutputFormat.QASM2)

    msg = str(exc.value)
    assert "failed to write qasm2 file" in msg.lower()
    assert "disk full" in msg.lower()

    # restore Path.open so other tests continue unharmed
    monkeypatch.setattr(Path, "open", builtins.open)


def test_write_circuit_unsupported_format(tmp_path: Path) -> None:
    """Requesting an unsupported format should raise."""

    class FakeFormat(str, Enum):
        FAKE = "fake"

    qc = QuantumCircuit(1)

    with pytest.raises(MQTBenchExporterError) as exc:
        write_circuit(qc, tmp_path / "foo.fake", fmt=FakeFormat.FAKE)  # type: ignore[arg-type]

    msg = str(exc.value)
    assert "unsupported output format" in msg.lower()
    assert "fake" in msg.lower()


def test_save_circuit_success(tmp_path: Path) -> None:
    """Happy-path save."""
    qc = QuantumCircuit(1)
    qc.h(0)

    assert save_circuit(qc, "foo", OutputFormat.QASM2, target_directory=str(tmp_path))
    assert (tmp_path / "foo.qasm").exists()

    assert save_circuit(qc, "bar", OutputFormat.QPY, target_directory=str(tmp_path))
    assert (tmp_path / "bar.qpy").exists()


def test_save_circuit_write_error(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """save_circuit returns False when write_circuit fails."""
    qc = QuantumCircuit(1)
    qc.h(0)

    monkeypatch.setattr(
        "mqt.bench.output.write_circuit",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(MQTBenchExporterError("boom")),
    )

    ok = save_circuit(qc, "baz", OutputFormat.QASM3, target_directory=str(tmp_path))
    assert ok is False


@pytest.mark.parametrize("fmt", [OutputFormat.QASM2, OutputFormat.QASM3])
def test_write_circuit_qasm_to_text_stream(fmt: OutputFormat) -> None:
    """Test writing a QASM circuit to a text stream."""
    qc = QuantumCircuit(2)
    qc.cx(0, 1)

    buf = io.StringIO()
    write_circuit(qc, buf, fmt=fmt)

    text = buf.getvalue().splitlines()
    assert text[0].startswith("// Benchmark created by MQT Bench on")
    assert any("cx" in line for line in text)


def test_write_circuit_qpy_to_binary_stream() -> None:
    """Test writing a QPY circuit to a binary stream."""
    qc = QuantumCircuit(1)
    qc.x(0)

    buf = io.BytesIO()
    write_circuit(qc, buf, fmt=OutputFormat.QPY)

    buf.seek(0)
    magic = buf.read(6)
    assert magic == b"QISKIT"


def test_stream_mode_mismatch_raises() -> None:
    """Test that stream mode mismatch raises an error."""
    qc = QuantumCircuit(1)

    # Binary stream + QASM → error
    with pytest.raises(MQTBenchExporterError):
        write_circuit(qc, io.BytesIO(), fmt=OutputFormat.QASM3)

    # Text stream + QPY → error
    with pytest.raises(MQTBenchExporterError):
        write_circuit(qc, io.StringIO(), fmt=OutputFormat.QPY)
