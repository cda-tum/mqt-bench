from __future__ import annotations

import json
from pathlib import Path
from typing import TYPE_CHECKING

import pytket

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


@pytest.fixture()
def output_path() -> str:
    output_path = Path("./tests/test_output/")
    output_path.mkdir(parents=True, exist_ok=True)
    return str(output_path)


@pytest.fixture()
def sample_filenames() -> list[str]:
    return [
        "ae_indep_qiskit_10.qasm",
        "ghz_nativegates_rigetti_qiskit_opt3_54.qasm",
        "ae_indep_tket_93.qasm",
        "wstate_nativegates_rigetti_qiskit_opt0_79.qasm",
        "ae_mapped_ibm_montreal_qiskit_opt1_9.qasm",
        "ae_mapped_ibm_washington_qiskit_opt0_38.qasm",
        "ae_mapped_oqc_lucy_qiskit_opt0_5.qasm",
        "ae_mapped_rigetti_aspen_m2_qiskit_opt1_61.qasm",
        "ae_mapped_ibm_washington_qiskit_opt2_88.qasm",
        "qnn_mapped_ionq_harmony_qiskit_opt3_3.qasm",
        "qnn_mapped_oqc_lucy_tket_line_2.qasm",
        "qaoa_mapped_quantinuum_h2_tket_graph_2.qasm",
        "dj_mapped_quantinuum_h2_qiskit_opt3_23.qasm",
    ]


@pytest.mark.parametrize(
    ("benchmark", "input_value", "scalable"),
    [
        (ae, 8, True),
        (ghz, 5, True),
        (dj, 3, True),
        (graphstate, 8, True),
        (grover, 5, False),
        (qaoa, 5, True),
        (qft, 8, True),
        (qftentangled, 8, True),
        (qnn, 8, True),
        (qpeexact, 8, True),
        (qpeinexact, 8, True),
        (tsp, 3, False),
        (qwalk, 5, False),
        (vqe, 5, True),
        (random, 9, True),
        (realamprandom, 9, True),
        (su2random, 7, True),
        (twolocalrandom, 8, True),
        (wstate, 8, True),
        (portfolioqaoa, 5, True),
        (shor, 9, False),
        (portfoliovqe, 5, True),
        (pricingcall, 5, False),
        (pricingput, 5, False),
    ],
)
def test_quantumcircuit_indep_level(
    benchmark: types.ModuleType, input_value: int, scalable: bool, output_path: str
) -> None:
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
        (ae, 8, True),
        (ghz, 5, True),
        (dj, 3, True),
        (graphstate, 8, True),
        (grover, 5, False),
        (qaoa, 5, True),
        (qft, 8, True),
        (qftentangled, 8, True),
        (qnn, 5, True),
        (qpeexact, 8, True),
        (qpeinexact, 8, True),
        (tsp, 3, False),
        (qwalk, 5, False),
        (vqe, 5, True),
        (random, 9, True),
        (realamprandom, 3, True),
        (su2random, 7, True),
        (twolocalrandom, 5, True),
        (wstate, 8, True),
        (portfolioqaoa, 5, True),
        (portfoliovqe, 5, True),
        (pricingcall, 5, False),
        (pricingput, 5, False),
    ],
)
def test_quantumcircuit_native_and_mapped_levels(
    benchmark: types.ModuleType, input_value: int, scalable: bool, output_path: str
) -> None:
    if benchmark in (grover, qwalk):
        qc = benchmark.create_circuit(input_value, ancillary_mode="noancilla")
    else:
        qc = benchmark.create_circuit(input_value)

    assert isinstance(qc, QuantumCircuit)
    if scalable:
        assert qc.num_qubits == input_value

    compilation_paths = utils.get_compilation_paths()

    for gate_set_name, devices in compilation_paths:
        opt_level = 1
        res = qiskit_helper.get_native_gates_level(
            qc,
            gate_set_name,
            qc.num_qubits,
            opt_level,
            file_precheck=False,
            return_qc=False,
            target_directory=output_path,
        )
        assert res
        res = qiskit_helper.get_native_gates_level(
            qc,
            gate_set_name,
            qc.num_qubits,
            opt_level,
            file_precheck=True,
            return_qc=False,
            target_directory=output_path,
        )
        assert res

        for device_name, max_qubits in devices:
            # Creating the circuit on target-dependent: mapped level qiskit
            if max_qubits >= qc.num_qubits:
                res = qiskit_helper.get_mapped_level(
                    qc,
                    gate_set_name,
                    qc.num_qubits,
                    device_name,
                    opt_level,
                    file_precheck=False,
                    return_qc=False,
                    target_directory=output_path,
                )
                assert res
                res = qiskit_helper.get_mapped_level(
                    qc,
                    gate_set_name,
                    qc.num_qubits,
                    device_name,
                    opt_level,
                    file_precheck=True,
                    return_qc=False,
                    target_directory=output_path,
                )
                assert res

    for gate_set_name, devices in compilation_paths:
        res = tket_helper.get_native_gates_level(
            qc,
            gate_set_name,
            qc.num_qubits,
            file_precheck=False,
            return_qc=False,
            target_directory=output_path,
        )
        assert res
        res = tket_helper.get_native_gates_level(
            qc,
            gate_set_name,
            qc.num_qubits,
            file_precheck=True,
            return_qc=False,
            target_directory=output_path,
        )
        assert res
        for device_name, max_qubits in devices:
            # Creating the circuit on target-dependent: mapped level qiskit
            if max_qubits >= qc.num_qubits:
                res = tket_helper.get_mapped_level(
                    qc,
                    gate_set_name,
                    qc.num_qubits,
                    device_name,
                    True,
                    file_precheck=False,
                    return_qc=False,
                    target_directory=output_path,
                )
                assert res
                res = tket_helper.get_mapped_level(
                    qc,
                    gate_set_name,
                    qc.num_qubits,
                    device_name,
                    False,
                    file_precheck=True,
                    return_qc=False,
                    target_directory=output_path,
                )
                assert res


def test_openqasm_gates() -> None:
    openqasm_gates = utils.get_openqasm_gates()
    num_openqasm_gates = 42
    assert len(openqasm_gates) == num_openqasm_gates


def test_rigetti_cmap_generator() -> None:
    num_edges = 212
    assert len(utils.get_rigetti_aspen_m2_map()) == num_edges


def test_dj_constant_oracle() -> None:
    qc = dj.create_circuit(5, False)
    assert qc.depth() > 0


def test_groundstate() -> None:
    qc = groundstate.create_circuit("small")
    assert qc.depth() > 0


def test_routing() -> None:
    qc = routing.create_circuit(4, 2)
    assert qc.depth() > 0


def test_unidirectional_coupling_map() -> None:
    from pytket.architecture import Architecture

    qc = get_benchmark(
        benchmark_name="dj",
        level="mapped",
        circuit_size=3,
        compiler="tket",
        compiler_settings=CompilerSettings(tket=TKETSettings(placement="graphplacement")),
        gate_set_name="oqc",
        device_name="oqc_lucy",
    )
    # check that all gates in the circuit are in the coupling map
    cmap_converted = utils.convert_cmap_to_tuple_list(utils.get_cmap_oqc_lucy())
    assert qc.valid_connectivity(arch=Architecture(cmap_converted), directed=True)


@pytest.mark.parametrize(
    (
        "benchmark_name",
        "level",
        "circuit_size",
        "benchmark_instance_name",
        "compiler",
        "compiler_settings",
        "gate_set_name",
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
        ("groundstate", 1, 4, "small", "qiskit", None, "", ""),
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
            "rigetti_aspen_m2",
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
        ("qft", 2, 6, None, "tket", None, "rigetti", "rigetti_aspen_m2"),
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
            "rigetti_aspen_m2",
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
            "rigetti_aspen_m2",
        ),
        (
            "qpeinexact",
            3,
            4,
            None,
            "tket",
            CompilerSettings(tket=TKETSettings(placement="lineplacement")),
            "rigetti",
            "rigetti_aspen_m2",
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
    ],
)
def test_get_benchmark(
    benchmark_name: str,
    level: str | int,
    circuit_size: int | None,
    benchmark_instance_name: str | None,
    compiler: str,
    compiler_settings: CompilerSettings | None,
    gate_set_name: str,
    device_name: str,
) -> None:
    qc = get_benchmark(
        benchmark_name,
        level,
        circuit_size,
        benchmark_instance_name,
        compiler,
        compiler_settings,
        gate_set_name,
        device_name,
    )
    assert qc.depth() > 0
    if gate_set_name and "oqc" not in gate_set_name:
        if compiler == "tket":
            qc = tk_to_qiskit(qc)
        assert isinstance(qc, QuantumCircuit)
        for instruction, _qargs, _cargs in qc.data:
            gate_type = instruction.name
            assert gate_type in qiskit_helper.get_native_gates(gate_set_name) or gate_type == "barrier"


def test_get_benchmark_faulty_parameters() -> None:
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
            "rigetti_aspen_m2",
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
            "rigetti_aspen_m2",
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
            "rigetti_aspen_m2",
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
            "rigetti_aspen_m2",
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
            "rigetti_aspen_m2",
        )
    match = "Selected gate_set_name must be in"
    with pytest.raises(ValueError, match=match):
        get_benchmark(
            "qpeexact",
            2,
            3,
            None,
            "qiskit",
            CompilerSettings(qiskit=QiskitSettings(optimization_level=1)),
            "wrong_gateset",
            "rigetti_aspen_m2",
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


def test_create_benchmarks_from_config(output_path: str) -> None:
    config = {
        "timeout": 120,
        "benchmarks": [
            {
                "name": "ghz",
                "include": True,
                "min_qubits": 2,
                "max_qubits": 3,
                "stepsize": 1,
                "precheck_possible": True,
            },
        ],
    }
    file = Path("test_config.json")
    with file.open("w") as f:
        json.dump(config, f)

    generator = BenchmarkGenerator(cfg_path=str(file), qasm_output_path=output_path)
    generator.create_benchmarks_from_config(num_jobs=1)
    file.unlink()


def test_configure_end(output_path: str) -> None:
    # delete all files in the test directory and the directory itself
    for f in Path(output_path).iterdir():
        f.unlink()
    Path(output_path).rmdir()


def test_zip_creation() -> None:
    """Test the creation of the overall zip file."""
    retcode = utils.create_zip_file()
    assert retcode == 0

    zip_file = Path(utils.get_zip_file_path())
    assert zip_file.is_file()
    zip_file.unlink()


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
    directory = "."
    filename = "ae_test_qiskit"
    qc = get_benchmark("ae", abstraction_level, 5)
    assert qc
    res = qiskit_helper.get_mapped_level(
        qc, "ibm", qc.num_qubits, "ibm_washington", 1, False, False, directory, filename
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
        "ibm",
        qc.num_qubits,
        "ibm_washington",
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


def test_oqc_postprocessing() -> None:
    qc = get_benchmark("ghz", 1, 5)
    directory = "."
    filename = "ghz_oqc"
    path = Path(directory) / Path(filename).with_suffix(".qasm")

    tket_helper.get_native_gates_level(
        qc,
        "oqc",
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
        "oqc",
        qc.num_qubits,
        "oqc_lucy",
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
        "oqc",
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
        "oqc",
        qc.num_qubits,
        "oqc_lucy",
        opt_level=1,
        file_precheck=False,
        return_qc=False,
        target_directory=directory,
        target_filename=filename,
    )

    assert QuantumCircuit.from_qasm_file(str(path))
    path.unlink()


def test_evaluate_qasm_file() -> None:
    qc = get_benchmark("dj", 1, 5)
    filename = "test_5.qasm"
    qc.qasm(filename=filename)
    path = Path(filename)
    res = evaluation.evaluate_qasm_file(filename)
    assert type(res) == evaluation.EvaluationResult

    path.unlink()


@pytest.mark.parametrize(
    ("search_str", "expected_val"),
    [
        ("qiskit", 10),
        ("tket", 3),
        ("nativegates", 2),
        ("indep", 2),
        ("mapped", 9),
        ("mapped_ibm_washington", 2),
        ("mapped_ibm_montreal", 1),
        ("mapped_oqc_lucy", 2),
        ("mapped_rigetti_aspen_m2", 1),
        ("mapped_ionq_harmony", 1),
    ],
)
def test_count_occurrences(search_str: str, expected_val: int, sample_filenames: list[str]) -> None:
    assert evaluation.count_occurrences(sample_filenames, search_str) == expected_val


@pytest.mark.parametrize(
    ("compiler", "expected_val"),
    [
        ("qiskit", [10, 54, 79, 9, 38, 5, 61, 88, 3, 23]),
        ("tket", [93, 2, 2]),
    ],
)
def test_count_qubit_numbers_per_compiler(compiler: str, expected_val: list[int], sample_filenames: list[str]) -> None:
    assert evaluation.count_qubit_numbers_per_compiler(sample_filenames, compiler) == expected_val


def test_calc_supermarq_features() -> None:
    qc = get_benchmark("dj", 1, 5)
    features = utils.calc_supermarq_features(qc)
    assert type(features) == utils.SupermarqFeatures


def test_BenchmarkGenerator() -> None:
    generator = BenchmarkGenerator(qasm_output_path="test")
    assert generator.qasm_output_path == "test"
    assert generator.timeout > 0
    assert generator.cfg is not None


# This function is used to test the timeout watchers and needs two parameters since those values are logged when a timeout occurs.
def endless_loop(arg1: SampleObject, run_forever: bool) -> bool:  # noqa: ARG001
    while run_forever:
        pass
    return True


class SampleObject:
    def __init__(self, name: str):
        self.name = name


def test_timeout_watchers() -> None:
    timeout = 1
    assert not timeout_watcher(endless_loop, timeout, [SampleObject("test"), True])
    assert timeout_watcher(endless_loop, timeout, [SampleObject("test"), False])


def test_get_module_for_benchmark() -> None:
    for benchmark in utils.get_supported_benchmarks():
        assert utils.get_module_for_benchmark(benchmark.split("-")[0]) is not None


def test_benchmark_helper() -> None:
    shor_instances = ["xsmall", "small", "medium", "large", "xlarge"]
    for elem in shor_instances:
        res_shor = shor.get_instance(elem)
        assert res_shor
    groundstate_instances = ["small", "medium", "large"]
    for elem in groundstate_instances:
        res_groundstate = groundstate.get_molecule(elem)
        assert res_groundstate


def test_get_cmap_from_devicename() -> None:
    with pytest.raises(ValueError, match="Device wrong_name is not supported"):
        utils.get_cmap_from_devicename("wrong_name")


def test_tket_mapped_circuit_qubit_number() -> None:
    qc = get_benchmark("ghz", 1, 5)
    res = tket_helper.get_mapped_level(
        qc,
        "ibm",
        qc.num_qubits,
        "ibm_washington",
        True,
        file_precheck=False,
        return_qc=True,
    )
    assert isinstance(res, pytket.Circuit)
    assert res.n_qubits == 127
