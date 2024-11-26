"""Tests for the benchmark generation."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    import types

    from qiskit import QuantumCircuit

import pytest

from mqt.bench import utils
from mqt.bench.benchmark_generator import (
    BenchmarkGenerator,
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
    randomcircuit,
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
        (randomcircuit, 3, True),
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
    """Test the native gates level for the Qiskit compiler."""
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
    """Test the native gates level for the TKET compiler."""
    for gateset in get_available_native_gatesets():
        if gateset.gateset_name != "clifford+t":
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
    """Test the mapped level for the Qiskit compiler."""
    for device in get_available_devices():
        if device.num_qubits >= quantum_circuit.num_qubits:
            res = qiskit_helper.get_mapped_level(
                quantum_circuit,
                quantum_circuit.num_qubits,
                device,
                opt_level=0,
                file_precheck=False,
                return_qc=False,
                target_directory=output_path,
            )
            assert res
            res = qiskit_helper.get_mapped_level(
                quantum_circuit,
                quantum_circuit.num_qubits,
                device,
                opt_level=0,
                file_precheck=True,
                return_qc=False,
                target_directory=output_path,
            )
            assert res


def test_mapped_level_tket(quantum_circuit: QuantumCircuit, output_path: str) -> None:
    """Test the mapped level for the TKET compiler."""
    for device in get_available_devices():
        if device.num_qubits >= quantum_circuit.num_qubits:
            res = tket_helper.get_mapped_level(
                quantum_circuit,
                quantum_circuit.num_qubits,
                device,
                file_precheck=False,
                return_qc=False,
                target_directory=output_path,
            )
            assert res
            res = tket_helper.get_mapped_level(
                quantum_circuit,
                quantum_circuit.num_qubits,
                device,
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


def test_configure_end(output_path: str) -> None:
    """Removes all temporarily created files while testing."""
    # delete all files in the test directory and the directory itself
    for f in Path(output_path).iterdir():
        f.unlink()
    Path(output_path).rmdir()


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
