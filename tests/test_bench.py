"""Tests for the benchmark generation."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    import types

import pytest
from qiskit import QuantumCircuit
from qiskit.qasm3 import load as load_qasm3

from mqt.bench import utils
from mqt.bench.benchmark_generation import (
    CompilerSettings,
    QiskitSettings,
    get_alg_level,
    get_benchmark,
    get_indep_level,
    get_mapped_level,
    get_native_gates_level,
    timeout_watcher,
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
    qwalk,
    randomcircuit,
    shor,
    vqerealamprandom,
    vqesu2random,
    vqetwolocalrandom,
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
        qasm_format="qasm3",
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
        ValueError, match=r"'qasm2' is not supported for the algorithm level, please use 'qasm3' instead."
    ):
        get_alg_level(qc, input_value, False, False, output_path, filename, qasm_format="qasm2")


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
    openqasm_gates = utils.get_openqasm_gates()
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
        qasm_format="qasm2",
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
        qasm_format="qasm2",
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
