"""Tests for the benchmark generation and evaluation."""

from __future__ import annotations

import json
import pickle
import sys
from pathlib import Path
from typing import TYPE_CHECKING

import pytket
from qiskit.qasm2 import dump

if TYPE_CHECKING:  # pragma: no cover
    import types

import pytest
from pytket.extensions.qiskit import tk_to_qiskit
from qiskit import QuantumCircuit

from mqt.bench import (
    BenchmarkGenerator,
    CompilerSettings,
    QiskitSettings,
    TKETSettings,
    evaluation,
    get_benchmark,
    qiskit_helper,
    timeout_watcher,
    tket_helper,
    utils,
)
from mqt.bench.benchmarks import (
    ae,
    dj,
    ghz,
    graphstate,
    groundstate,
    grover,
    portfolioqaoa,
    portfoliovqe,
    pricingcall,
    pricingput,
    qaoa,
    qft,
    qftentangled,
    qnn,
    qpeexact,
    qpeinexact,
    qwalk,
    random,
    realamprandom,
    routing,
    shor,
    su2random,
    tsp,
    twolocalrandom,
    vqe,
    wstate,
)
from mqt.bench.devices import IBMProvider, OQCProvider, get_available_providers, get_provider_by_name


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


@pytest.mark.parametrize(
    ("benchmark", "input_value", "scalable"),
    [
        (ae, 3, True),
        (ghz, 2, True),  # the generated GHZ benchmarks are later used in test_benchviewer.py::test_streaming_zip
        (dj, 3, True),
        (graphstate, 3, True),
        (grover, 3, False),
        (qaoa, 3, True),
        (qft, 3, True),
        (qftentangled, 3, True),
        (qnn, 3, True),
        (qpeexact, 3, True),
        (qpeinexact, 3, True),
        (tsp, 3, False),
        (qwalk, 3, False),
        (vqe, 3, True),
        (random, 3, True),
        (realamprandom, 3, True),
        (su2random, 3, True),
        (twolocalrandom, 3, True),
        (wstate, 3, True),
        (portfolioqaoa, 3, True),
        (shor, 3, False),
        (portfoliovqe, 3, True),
        (pricingcall, 3, False),
        (pricingput, 3, False),
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
    res = qiskit_helper.get_indep_level(
        qc,
        input_value,
        file_precheck=False,
        return_qc=False,
        target_directory=output_path,
    )
    assert res
    res = qiskit_helper.get_indep_level(
        qc,
        input_value,
        file_precheck=True,
        return_qc=False,
        target_directory=output_path,
    )
    assert res

    res = tket_helper.get_indep_level(
        qc,
        input_value,
        file_precheck=False,
        return_qc=False,
        target_directory=output_path,
    )
    assert res
    res = tket_helper.get_indep_level(
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
        (tsp, 3, False),
        (qwalk, 3, False),
        (vqe, 3, True),
        (random, 3, True),
        (realamprandom, 3, True),
        (su2random, 3, True),
        (twolocalrandom, 3, True),
        (wstate, 3, True),
        (portfolioqaoa, 3, True),
        (portfoliovqe, 3, True),
        (pricingcall, 3, False),
        (pricingput, 3, False),
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
        res = qiskit_helper.get_native_gates_level(
            qc,
            provider,
            qc.num_qubits,
            opt_level,
            file_precheck=False,
            return_qc=False,
            target_directory=output_path,
        )
        assert res
        res = qiskit_helper.get_native_gates_level(
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
                res = qiskit_helper.get_mapped_level(
                    qc,
                    qc.num_qubits,
                    device,
                    opt_level,
                    file_precheck=False,
                    return_qc=False,
                    target_directory=output_path,
                )
                assert res
                res = qiskit_helper.get_mapped_level(
                    qc,
                    qc.num_qubits,
                    device,
                    opt_level,
                    file_precheck=True,
                    return_qc=False,
                    target_directory=output_path,
                )
                assert res

    for provider in providers:
        res = tket_helper.get_native_gates_level(
            qc,
            provider,
            qc.num_qubits,
            file_precheck=False,
            return_qc=False,
            target_directory=output_path,
        )
        assert res
        res = tket_helper.get_native_gates_level(
            qc,
            provider,
            qc.num_qubits,
            file_precheck=True,
            return_qc=False,
            target_directory=output_path,
        )
        assert res

        for device in provider.get_available_devices():
            # Creating the circuit on target-dependent: mapped level qiskit
            if device.num_qubits >= qc.num_qubits:
                res = tket_helper.get_mapped_level(
                    qc,
                    qc.num_qubits,
                    device,
                    True,
                    file_precheck=False,
                    return_qc=False,
                    target_directory=output_path,
                )
                assert res
                res = tket_helper.get_mapped_level(
                    qc,
                    qc.num_qubits,
                    device,
                    False,
                    file_precheck=True,
                    return_qc=False,
                    target_directory=output_path,
                )
                assert res


def test_get_default_evaluation_output_path() -> None:
    """Test the default evaluation output path."""
    path = utils.get_default_evaluation_output_path()
    assert Path(path).exists()


def test_openqasm_gates() -> None:
    """Test the openqasm gates."""
    openqasm_gates = utils.get_openqasm_gates()
    num_openqasm_gates = 42
    assert len(openqasm_gates) == num_openqasm_gates


def test_dj_constant_oracle() -> None:
    """Test the creation of the DJ benchmark constant oracle."""
    qc = dj.create_circuit(5, False)
    assert qc.depth() > 0


def test_routing() -> None:
    """Test the creation of the routing benchmark."""
    qc = routing.create_circuit(4, 2)
    assert qc.depth() > 0


def test_unidirectional_coupling_map() -> None:
    """Test the unidirectional coupling map for the OQC Lucy device."""
    qc = get_benchmark(
        benchmark_name="dj",
        level="mapped",
        circuit_size=3,
        compiler="tket",
        compiler_settings=CompilerSettings(tket=TKETSettings(placement="graphplacement")),
        provider_name="oqc",
        device_name="oqc_lucy",
    )
    # check that all gates in the circuit are in the coupling map
    cmap = utils.convert_cmap_to_tuple_list(OQCProvider.get_device("oqc_lucy").coupling_map)
    assert qc.valid_connectivity(arch=pytket.architecture.Architecture(cmap), directed=True)


@pytest.mark.parametrize(
    (
        "benchmark_name",
        "level",
        "circuit_size",
        "benchmark_instance_name",
        "compiler",
        "compiler_settings",
        "provider_name",
        "device_name",
    ),
    [
        (
            "dj",
            "alg",
            5,
            None,
            "qiskit",
            None,
            "",
            "",
        ),
        (
            "wstate",
            0,
            6,
            None,
            "tket",
            None,
            "",
            "",
        ),
        (
            "ghz",
            "indep",
            5,
            None,
            "qiskit",
            None,
            "",
            "",
        ),
        (
            "graphstate",
            1,
            4,
            None,
            "qiskit",
            None,
            "",
            "",
        ),
        (
            "graphstate",
            1,
            4,
            None,
            "tket",
            None,
            "",
            "",
        ),
        (
            "dj",
            "nativegates",
            5,
            None,
            "qiskit",
            CompilerSettings(qiskit=QiskitSettings(optimization_level=2)),
            "ionq",
            "",
        ),
        (
            "dj",
            "nativegates",
            5,
            None,
            "qiskit",
            CompilerSettings(qiskit=QiskitSettings(optimization_level=2)),
            "ibm",
            "",
        ),
        (
            "dj",
            "nativegates",
            5,
            None,
            "qiskit",
            CompilerSettings(qiskit=QiskitSettings(optimization_level=2)),
            "rigetti",
            "rigetti_aspen_m3",
        ),
        (
            "dj",
            "nativegates",
            5,
            None,
            "qiskit",
            CompilerSettings(qiskit=QiskitSettings(optimization_level=2)),
            "oqc",
            "oqc_lucy",
        ),
        (
            "qft",
            2,
            6,
            None,
            "qiskit",
            CompilerSettings(qiskit=QiskitSettings(optimization_level=3)),
            "ionq",
            "ionq_harmony1",
        ),
        (
            "qft",
            2,
            6,
            None,
            "qiskit",
            CompilerSettings(qiskit=QiskitSettings(optimization_level=3)),
            "ibm",
            "ibm_montreal",
        ),
        ("qft", 2, 6, None, "tket", None, "rigetti", "rigetti_aspen_m3"),
        (
            "qft",
            2,
            6,
            None,
            "tket",
            None,
            "oqc",
            "oqc_lucy",
        ),
        (
            "qpeexact",
            "mapped",
            5,
            None,
            "qiskit",
            CompilerSettings(qiskit=QiskitSettings(optimization_level=1)),
            "ibm",
            "ibm_washington",
        ),
        (
            "qpeexact",
            "mapped",
            5,
            None,
            "qiskit",
            CompilerSettings(qiskit=QiskitSettings(optimization_level=1)),
            "ibm",
            "ibm_montreal",
        ),
        (
            "qpeexact",
            "mapped",
            5,
            None,
            "qiskit",
            CompilerSettings(qiskit=QiskitSettings(optimization_level=1)),
            "rigetti",
            "rigetti_aspen_m3",
        ),
        (
            "qpeexact",
            "mapped",
            5,
            None,
            "qiskit",
            CompilerSettings(qiskit=QiskitSettings(optimization_level=1)),
            "ionq",
            "ionq_harmony",
        ),
        (
            "qpeexact",
            "mapped",
            5,
            None,
            "qiskit",
            CompilerSettings(qiskit=QiskitSettings(optimization_level=1)),
            "ionq",
            "ionq_aria1",
        ),
        (
            "qpeexact",
            "mapped",
            5,
            None,
            "qiskit",
            CompilerSettings(qiskit=QiskitSettings(optimization_level=2)),
            "ionq",
            "ionq_aria1",
        ),
        (
            "qpeexact",
            "mapped",
            5,
            None,
            "qiskit",
            CompilerSettings(qiskit=QiskitSettings(optimization_level=1)),
            "oqc",
            "oqc_lucy",
        ),
        (
            "qpeinexact",
            3,
            4,
            None,
            "qiskit",
            CompilerSettings(qiskit=QiskitSettings(optimization_level=1)),
            "ibm",
            "ibm_washington",
        ),
        (
            "qpeinexact",
            3,
            4,
            None,
            "tket",
            CompilerSettings(tket=TKETSettings(placement="lineplacement")),
            "ibm",
            "ibm_washington",
        ),
        (
            "qpeinexact",
            3,
            4,
            None,
            "qiskit",
            CompilerSettings(qiskit=QiskitSettings(optimization_level=1)),
            "ibm",
            "ibm_montreal",
        ),
        (
            "qpeinexact",
            3,
            4,
            None,
            "tket",
            CompilerSettings(tket=TKETSettings(placement="graphplacement")),
            "ibm",
            "ibm_montreal",
        ),
        (
            "qpeinexact",
            3,
            4,
            None,
            "qiskit",
            CompilerSettings(qiskit=QiskitSettings(optimization_level=1)),
            "rigetti",
            "rigetti_aspen_m3",
        ),
        (
            "qpeinexact",
            3,
            4,
            None,
            "tket",
            CompilerSettings(tket=TKETSettings(placement="lineplacement")),
            "rigetti",
            "rigetti_aspen_m3",
        ),
        (
            "qpeinexact",
            3,
            4,
            None,
            "qiskit",
            CompilerSettings(qiskit=QiskitSettings(optimization_level=1)),
            "oqc",
            "oqc_lucy",
        ),
        (
            "qpeinexact",
            3,
            4,
            None,
            "tket",
            CompilerSettings(tket=TKETSettings(placement="graphplacement")),
            "oqc",
            "oqc_lucy",
        ),
        (
            "qpeinexact",
            3,
            4,
            None,
            "tket",
            CompilerSettings(tket=TKETSettings(placement="graphplacement")),
            "quantinuum",
            "quantinuum_h2",
        ),
        (
            "qpeinexact",
            3,
            4,
            None,
            "qiskit",
            CompilerSettings(qiskit=QiskitSettings(optimization_level=2)),
            "quantinuum",
            "quantinuum_h2",
        ),
        (
            "grover-noancilla",
            "alg",
            5,
            None,
            "qiskit",
            None,
            "",
            "",
        ),
        (
            "qwalk-noancilla",
            "alg",
            5,
            None,
            "qiskit",
            None,
            "",
            "",
        ),
        (
            "grover-v-chain",
            "alg",
            5,
            None,
            "qiskit",
            None,
            "",
            "",
        ),
        (
            "qwalk-v-chain",
            "alg",
            5,
            None,
            "qiskit",
            None,
            "",
            "",
        ),
        (
            "shor",
            "alg",
            None,
            "xsmall",
            "qiskit",
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
    compiler: str,
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
        compiler,
        compiler_settings,
        provider_name,
        device_name,
    )
    assert qc.depth() > 0
    if provider_name and "oqc" not in provider_name:
        if compiler == "tket":
            qc = tk_to_qiskit(qc)
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
            "qiskit",
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
            "qiskit",
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
            "qiskit",
            CompilerSettings(qiskit=QiskitSettings(optimization_level=1)),
            "rigetti",
            "rigetti_aspen_m3",
        )

    match = "Selected compiler must be in"
    with pytest.raises(ValueError, match=match):
        get_benchmark(
            "qpeexact",
            1,
            3,
            None,
            "wrong_compiler",
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
            "qiskit",
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
            "qiskit",
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
            "qiskit",
            CompilerSettings(qiskit=QiskitSettings(optimization_level=1)),
            "rigetti",
            "wrong_device",
        )


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

    evaluation.create_statistics(source_directory=Path(output_path), target_directory=Path(output_path))

    with (Path(output_path) / "evaluation_data.pkl").open("rb") as f:
        res_dicts = pickle.load(f)
    assert len(res_dicts) > 0


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
    res = qiskit_helper.get_mapped_level(
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

    filename = "ae_test_tket"
    qc = get_benchmark("ae", abstraction_level, 7)
    assert qc
    res = tket_helper.get_mapped_level(
        qc,
        qc.num_qubits,
        IBMProvider.get_device("ibm_washington"),
        False,
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

    tket_helper.get_native_gates_level(
        qc,
        OQCProvider(),
        qc.num_qubits,
        file_precheck=False,
        return_qc=False,
        target_directory=directory,
        target_filename=filename,
    )

    assert QuantumCircuit.from_qasm_file(str(path))
    path.unlink()

    directory = "."
    filename = "ghz_oqc2"
    path = Path(directory) / Path(filename).with_suffix(".qasm")
    tket_helper.get_mapped_level(
        qc,
        qc.num_qubits,
        OQCProvider().get_device("oqc_lucy"),
        lineplacement=False,
        file_precheck=False,
        return_qc=False,
        target_directory=directory,
        target_filename=filename,
    )
    assert QuantumCircuit.from_qasm_file(str(path))
    path.unlink()
    directory = "."
    filename = "ghz_oqc3"
    path = Path(directory) / Path(filename).with_suffix(".qasm")
    qiskit_helper.get_native_gates_level(
        qc,
        OQCProvider(),
        qc.num_qubits,
        opt_level=1,
        file_precheck=False,
        return_qc=False,
        target_directory=directory,
        target_filename=filename,
    )
    assert QuantumCircuit.from_qasm_file(str(path))
    path.unlink()
    directory = "."
    filename = "ghz_oqc4"
    path = Path(directory) / Path(filename).with_suffix(".qasm")
    qiskit_helper.get_mapped_level(
        qc,
        qc.num_qubits,
        OQCProvider().get_device("oqc_lucy"),
        opt_level=1,
        file_precheck=False,
        return_qc=False,
        target_directory=directory,
        target_filename=filename,
    )

    assert QuantumCircuit.from_qasm_file(str(path))
    path.unlink()


def test_evaluate_qasm_file() -> None:
    """Test the evaluation of a qasm file."""
    qc = get_benchmark("dj", 1, 5)
    filename = "test_5.qasm"
    with Path(filename).open("w", encoding="locale") as f:
        dump(qc, f)
    path = Path(filename)
    res = evaluation.evaluate_qasm_file(filename)
    assert type(res) is evaluation.EvaluationResult
    path.unlink()

    res = evaluation.evaluate_qasm_file("invalid_path.qasm")
    assert type(res) is evaluation.EvaluationResult
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
    assert evaluation.count_occurrences(sample_filenames, search_str) == expected_val


@pytest.mark.parametrize(
    ("compiler", "expected_val"),
    [
        ("qiskit", [10, 54, 79, 9, 38, 5, 88, 3, 23]),
        ("tket", [93, 2, 2]),
    ],
)
def test_count_qubit_numbers_per_compiler(compiler: str, expected_val: list[int], sample_filenames: list[str]) -> None:
    """Test the count_qubit_numbers_per_compiler function."""
    assert evaluation.count_qubit_numbers_per_compiler(sample_filenames, compiler) == expected_val


def test_calc_supermarq_features() -> None:
    """Test the calculation of the supermarq features."""
    ghz_qc = get_benchmark("ghz", 1, 5)
    ghz_features = utils.calc_supermarq_features(ghz_qc)
    assert ghz_features.program_communication == 0.4
    assert ghz_features.entanglement_ratio == 0.8
    assert ghz_features.critical_depth == 1.0
    assert ghz_features.parallelism == 0.0

    empty_qc = QuantumCircuit(2)
    empty_features = utils.calc_supermarq_features(empty_qc)
    assert empty_features.parallelism == 0.0
    assert empty_features.entanglement_ratio == 0.0
    assert empty_features.critical_depth == 0.0
    assert empty_features.program_communication == 0.0

    dense_qc = QuantumCircuit(2)
    dense_qc.h([0, 1])
    dense_features = utils.calc_supermarq_features(dense_qc)
    assert dense_features.parallelism == 1.0
    assert dense_features.entanglement_ratio == 0.0
    assert dense_features.critical_depth == 0.0
    assert dense_features.program_communication == 0.0

    regular_qc = get_benchmark("vqe", 1, 5)
    regular_features = utils.calc_supermarq_features(regular_qc)
    assert 0 < regular_features.parallelism < 1
    assert 0 < regular_features.entanglement_ratio < 1
    assert 0 < regular_features.critical_depth < 1
    assert 0 < regular_features.program_communication < 1
    assert 0 < regular_features.liveness < 1


def test_benchmark_generator() -> None:
    """Test the BenchmarkGenerator class."""
    generator = BenchmarkGenerator(qasm_output_path="test")
    assert generator.qasm_output_path == "test"
    assert generator.timeout > 0
    assert generator.cfg is not None


# This function is used to test the timeout watchers and needs two parameters since those values are logged when a timeout occurs.
def endless_loop(arg1: SampleObject, run_forever: bool) -> bool:  # noqa: ARG001
    """Endless loop necessary for testing the timeout watcher."""
    while run_forever:
        pass
    return True


class SampleObject:
    """Sample object for testing the timeout watcher."""

    def __init__(self, name: str) -> None:
        """Initialize the sample object."""
        self.name = name


def test_timeout_watchers() -> None:
    """Test the timeout watcher."""
    timeout = 1
    if sys.platform == "win32":
        with pytest.warns(RuntimeWarning, match="Timeout is not supported on Windows."):
            timeout_watcher(endless_loop, timeout, [SampleObject("test"), False])
    else:
        assert not timeout_watcher(endless_loop, timeout, [SampleObject("test"), True])
        assert timeout_watcher(endless_loop, timeout, [SampleObject("test"), False])


def test_get_module_for_benchmark() -> None:
    """Test the get_module_for_benchmark function."""
    for benchmark in utils.get_supported_benchmarks():
        assert utils.get_module_for_benchmark(benchmark.split("-")[0]) is not None


def test_benchmark_helper_shor() -> None:
    """Testing the Shor benchmarks."""
    shor_instances = ["xsmall", "small", "medium", "large", "xlarge"]
    for elem in shor_instances:
        res_shor = shor.get_instance(elem)
        assert res_shor


@pytest.mark.skipif(
    sys.platform == "win32",
    reason="PySCF is not available on Windows.",
)
def test_benchmark_groundstate_non_windows() -> None:
    """Testing the Groundstate benchmarks."""
    groundstate_instances = ["small", "medium", "large"]
    for elem in groundstate_instances:
        res_groundstate = groundstate.get_molecule(elem)
        assert res_groundstate

    qc = groundstate.create_circuit("small")
    assert qc.depth() > 0


@pytest.mark.skipif(
    sys.platform != "win32",
    reason="Windows-specific test.",
)
def test_benchmark_groundstate_windows() -> None:
    """Testing the Groundstate benchmarks on Windows."""
    with pytest.raises(ImportError, match=r"PySCF is not installed"):
        groundstate.create_circuit("small")


def test_tket_mapped_circuit_qubit_number() -> None:
    """Test the number of qubits in the tket-mapped circuit."""
    qc = get_benchmark("ghz", 1, 5)
    res = tket_helper.get_mapped_level(
        qc,
        qc.num_qubits,
        IBMProvider().get_device("ibm_washington"),
        True,
        file_precheck=False,
        return_qc=True,
    )
    assert isinstance(res, pytket.Circuit)
    assert res.n_qubits == 127
