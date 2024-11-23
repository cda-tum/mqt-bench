"""Tests for the benchmark generation."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import TYPE_CHECKING

import pytket

if TYPE_CHECKING:  # pragma: no cover
    import types

import pytest
from pytket.extensions.qiskit import tk_to_qiskit
from qiskit import QuantumCircuit

from mqt.bench import utils
from mqt.bench.benchmark_generator import (
    BenchmarkGenerator,
    CompilerSettings,
    QiskitSettings,
    get_benchmark,
    qiskit_helper,
    timeout_watcher,
    tket_helper,
)
from mqt.bench.benchmarks import (
    ae,
    dj,
    ghz,
    graphstate,
    groundstate,
    grover,
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
    twolocalrandom,
    vqe,
    wstate,
)
from mqt.bench.devices import (
    get_available_devices,
    get_available_native_gatesets,
    get_device_by_name,
    get_native_gateset_by_name,
)


@pytest.fixture
def output_path() -> str:
    """Fixture to create the output path for the tests."""
    output_path = Path("./tests/test_output/")
    output_path.mkdir(parents=True, exist_ok=True)
    return str(output_path)


@pytest.fixture
def quantum_circuit() -> str:
    """Fixture to return a GHZ quantum circuit."""
    return ghz.create_circuit(3)


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
        (vqe, 3, True),
        (random, 3, True),
        (realamprandom, 3, True),
        (su2random, 3, True),
        (twolocalrandom, 3, True),
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


def test_native_gates_level_qiskit(quantum_circuit: QuantumCircuit, output_path: str) -> None:
    native_gatesets = get_available_native_gatesets()
    for gateset in native_gatesets:
        opt_level = 0
        res = qiskit_helper.get_native_gates_level(
            quantum_circuit,
            gateset,
            quantum_circuit.num_qubits,
            opt_level,
            file_precheck=False,
            return_qc=False,
            target_directory=output_path,
        )
        assert res
        res = qiskit_helper.get_native_gates_level(
            quantum_circuit,
            gateset,
            quantum_circuit.num_qubits,
            opt_level,
            file_precheck=True,
            return_qc=False,
            target_directory=output_path,
        )
        assert res


def test_native_gates_level_tket(quantum_circuit: QuantumCircuit, output_path: str) -> None:
    for gateset in get_available_native_gatesets():
        if gateset[0] != "clifford+t":
            res = tket_helper.get_native_gates_level(
                quantum_circuit,
                gateset,
                quantum_circuit.num_qubits,
                file_precheck=False,
                return_qc=False,
                target_directory=output_path,
            )
            assert res
            res = tket_helper.get_native_gates_level(
                quantum_circuit,
                gateset,
                quantum_circuit.num_qubits,
                file_precheck=True,
                return_qc=False,
                target_directory=output_path,
            )
            assert res
        else:
            with pytest.raises(
                ValueError, match=r"The gateset 'clifford\+t' is not supported by TKET. Please use Qiskit instead."
            ):
                tket_helper.get_native_gates_level(
                    quantum_circuit,
                    gateset,
                    quantum_circuit.num_qubits,
                    file_precheck=False,
                    return_qc=False,
                    target_directory=output_path,
                )


def test_mapped_level_qiskit(quantum_circuit: QuantumCircuit, output_path: str) -> None:
    for device in get_available_devices():
        calibrated_device = device.constructor()
        if calibrated_device.num_qubits >= quantum_circuit.num_qubits:
            res = qiskit_helper.get_mapped_level(
                quantum_circuit,
                quantum_circuit.num_qubits,
                calibrated_device,
                opt_level=0,
                file_precheck=False,
                return_qc=False,
                target_directory=output_path,
            )
            assert res
            res = qiskit_helper.get_mapped_level(
                quantum_circuit,
                quantum_circuit.num_qubits,
                calibrated_device,
                opt_level=0,
                file_precheck=True,
                return_qc=False,
                target_directory=output_path,
            )
            assert res


def test_mapped_level_tket(quantum_circuit: QuantumCircuit, output_path: str) -> None:
    for device in get_available_devices():
        calibrated_device = device.constructor()
        if calibrated_device.num_qubits >= quantum_circuit.num_qubits:
            res = tket_helper.get_mapped_level(
                quantum_circuit,
                quantum_circuit.num_qubits,
                calibrated_device,
                file_precheck=False,
                return_qc=False,
                target_directory=output_path,
            )
            assert res
            res = tket_helper.get_mapped_level(
                quantum_circuit,
                quantum_circuit.num_qubits,
                calibrated_device,
                file_precheck=True,
                return_qc=False,
                target_directory=output_path,
            )
            assert res


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
        gateset_name="oqc",
        device_name="oqc_lucy",
    )
    # check that all gates in the circuit are in the coupling map
    cmap = utils.convert_cmap_to_tuple_list(get_device_by_name("oqc_lucy").coupling_map)
    assert qc.valid_connectivity(arch=pytket.architecture.Architecture(cmap), directed=True)


@pytest.mark.parametrize(
    (
        "benchmark_name",
        "level",
        "circuit_size",
        "benchmark_instance_name",
        "compiler",
        "compiler_settings",
        "gateset_name",
        "device_name",
    ),
    [
        (
            "dj",
            "alg",
            3,
            None,
            "qiskit",
            None,
            "",
            "",
        ),
        (
            "wstate",
            0,
            3,
            None,
            "tket",
            None,
            "",
            "",
        ),
        (
            "ghz",
            "indep",
            3,
            None,
            "qiskit",
            None,
            "",
            "",
        ),
        (
            "graphstate",
            1,
            3,
            None,
            "qiskit",
            None,
            "",
            "",
        ),
        (
            "graphstate",
            1,
            3,
            None,
            "tket",
            None,
            "",
            "",
        ),
        (
            "dj",
            "nativegates",
            3,
            None,
            "qiskit",
            CompilerSettings(qiskit=QiskitSettings(optimization_level=2)),
            "ionq",
            "",
        ),
        (
            "qft",
            2,
            3,
            None,
            "qiskit",
            CompilerSettings(qiskit=QiskitSettings(optimization_level=3)),
            "ionq",
            "ionq_harmony1",
        ),
        ("qft", 2, 6, None, "tket", None, "rigetti", "rigetti_aspen_m3"),
        (
            "qpeexact",
            "mapped",
            3,
            None,
            "qiskit",
            CompilerSettings(qiskit=QiskitSettings(optimization_level=1)),
            "ibm_falcon",
            "ibm_washington",
        ),
        (
            "qpeexact",
            "mapped",
            3,
            None,
            "qiskit",
            CompilerSettings(qiskit=QiskitSettings(optimization_level=2)),
            "ionq",
            "ionq_aria1",
        ),
        (
            "qpeinexact",
            3,
            3,
            None,
            "tket",
            None,
            "ibm_falcon",
            "ibm_washington",
        ),
        (
            "qpeinexact",
            3,
            3,
            None,
            "qiskit",
            CompilerSettings(qiskit=QiskitSettings(optimization_level=1)),
            "ibm_falcon",
            "ibm_montreal",
        ),
        (
            "qpeinexact",
            3,
            3,
            None,
            "tket",
            None,
            "ibm_falcon",
            "ibm_montreal",
        ),
        (
            "qpeinexact",
            3,
            3,
            None,
            "qiskit",
            CompilerSettings(qiskit=QiskitSettings(optimization_level=1)),
            "rigetti",
            "rigetti_aspen_m3",
        ),
        (
            "qpeinexact",
            3,
            3,
            None,
            "tket",
            None,
            "rigetti",
            "rigetti_aspen_m3",
        ),
        (
            "grover-noancilla",
            "alg",
            3,
            None,
            "qiskit",
            None,
            "",
            "",
        ),
        (
            "qwalk-noancilla",
            "alg",
            3,
            None,
            "qiskit",
            None,
            "",
            "",
        ),
        (
            "qwalk-v-chain",
            "alg",
            3,
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
    gateset_name: str,
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
        gateset_name,
        device_name,
    )
    assert qc.depth() > 0
    if gateset_name and "oqc" not in gateset_name:
        if compiler == "tket":
            qc = tk_to_qiskit(qc, replace_implicit_swaps=False)
        assert isinstance(qc, QuantumCircuit)
        for qc_instruction in qc.data:
            instruction = qc_instruction.operation
            gate_type = instruction.name
            _, gateset = get_native_gateset_by_name(gateset_name)
            assert gate_type in gateset or gate_type == "barrier"


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
    match = "Gateset wrong_gateset not found in available gatesets."
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
        get_device_by_name("ibm_washington"),
        1,
        False,
        False,
        directory,
        filename,
    )
    assert res
    path = Path(directory) / Path(filename).with_suffix(".qasm")
    assert path.is_file()
    #  path.unlink()

    filename = "ae_test_tket"
    qc = get_benchmark("ae", abstraction_level, 7)
    assert qc
    res = tket_helper.get_mapped_level(
        qc,
        qc.num_qubits,
        get_device_by_name("ibm_washington"),
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
        get_native_gateset_by_name("oqc"),
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
        get_device_by_name("oqc_lucy"),
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
        get_native_gateset_by_name("oqc"),
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
        get_device_by_name("oqc_lucy"),
        opt_level=1,
        file_precheck=False,
        return_qc=False,
        target_directory=directory,
        target_filename=filename,
    )

    assert QuantumCircuit.from_qasm_file(str(path))
    path.unlink()


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
        get_device_by_name("ibm_washington"),
        file_precheck=False,
        return_qc=True,
    )
    assert isinstance(res, pytket.Circuit)
    assert res.n_qubits == 127
