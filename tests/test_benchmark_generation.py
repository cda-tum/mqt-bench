"""Tests for the benchmark generation."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    import types
    from collections.abc import Callable

    from qiskit import QuantumCircuit


import pytest
from qiskit.qasm2 import LEGACY_CUSTOM_INSTRUCTIONS
from qiskit.qasm2 import load as load_qasm2
from qiskit.qasm3 import load as load_qasm3

from mqt.bench import utils
from mqt.bench.benchmark_generator import (
    BenchmarkGenerator,
    qiskit_helper,
    timeout_watcher,
    tket_helper,
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
    filename = "testfile"
    filepath = Path(output_path) / (filename + ".qasm")
    evaluate_benchmark_with_qasm_formats(
        qiskit_helper.get_indep_level, (qc, input_value, False, False, output_path, filename), output_path
    )

    res = qiskit_helper.get_indep_level(
        qc,
        input_value,
        file_precheck=True,
        return_qc=False,
        target_directory=output_path,
        target_filename=filename,
        qasm_format="qasm3",
    )
    assert res
    filepath.unlink()

    evaluate_benchmark_with_qasm_formats(
        tket_helper.get_indep_level, (qc, input_value, False, False, output_path, filename), output_path
    )

    res = tket_helper.get_indep_level(
        qc,
        input_value,
        file_precheck=True,
        return_qc=False,
        target_directory=output_path,
        target_filename=filename,
        qasm_format="qasm3",
    )
    assert res
    filepath.unlink()


def test_native_gates_level_qiskit(quantum_circuit: QuantumCircuit, output_path: str) -> None:
    """Test the native gates level for the Qiskit compiler."""
    native_gatesets = get_available_native_gatesets()
    filename = "testfile"
    filepath = Path(output_path) / (filename + ".qasm")
    opt_level = 0
    for gateset in native_gatesets:
        evaluate_benchmark_with_qasm_formats(
            qiskit_helper.get_native_gates_level,
            (quantum_circuit, gateset, quantum_circuit.num_qubits, 0, False, False, output_path, filename),
            output_path,
        )

        res = qiskit_helper.get_native_gates_level(
            quantum_circuit,
            gateset,
            quantum_circuit.num_qubits,
            opt_level,
            file_precheck=True,
            return_qc=False,
            target_directory=output_path,
            target_filename=filename,
            qasm_format="qasm3",
        )
        assert res
        filepath.unlink()


def test_native_gates_level_tket(quantum_circuit: QuantumCircuit, output_path: str) -> None:
    """Test the native gates level for the TKET compiler."""
    filename = "testfile"
    filepath = Path(output_path) / (filename + ".qasm")

    for gateset in get_available_native_gatesets():
        if gateset.gateset_name != "clifford+t":
            evaluate_benchmark_with_qasm_formats(
                tket_helper.get_native_gates_level,
                (quantum_circuit, gateset, quantum_circuit.num_qubits, False, False, output_path, filename),
                output_path,
            )

            res = tket_helper.get_native_gates_level(
                quantum_circuit,
                gateset,
                quantum_circuit.num_qubits,
                file_precheck=True,
                return_qc=False,
                target_directory=output_path,
                target_filename=filename,
                qasm_format="qasm3",
            )
            assert res
            filepath.unlink()
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
    filename = "testfile"
    filepath = Path(output_path) / (filename + ".qasm")
    for device in get_available_devices():
        if device.num_qubits >= quantum_circuit.num_qubits:
            evaluate_benchmark_with_qasm_formats(
                qiskit_helper.get_mapped_level,
                (quantum_circuit, quantum_circuit.num_qubits, device, 0, False, False, output_path, filename),
                output_path,
            )

            res = qiskit_helper.get_mapped_level(
                quantum_circuit,
                quantum_circuit.num_qubits,
                device,
                opt_level=0,
                file_precheck=True,
                return_qc=False,
                target_directory=output_path,
                target_filename=filename,
                qasm_format="qasm3",
            )
            assert res
            filepath.unlink()


def test_mapped_level_tket(quantum_circuit: QuantumCircuit, output_path: str) -> None:
    """Test the mapped level for the TKET compiler."""
    filename = "testfile"
    filepath = Path(output_path) / (filename + ".qasm")
    for device in get_available_devices():
        if device.num_qubits >= quantum_circuit.num_qubits:
            evaluate_benchmark_with_qasm_formats(
                tket_helper.get_mapped_level,
                (quantum_circuit, quantum_circuit.num_qubits, device, False, False, output_path, filename),
                output_path,
            )

            res = tket_helper.get_mapped_level(
                quantum_circuit,
                quantum_circuit.num_qubits,
                device,
                file_precheck=True,
                return_qc=False,
                target_directory=output_path,
                target_filename=filename,
                qasm_format="qasm3",
            )
            assert res
            filepath.unlink()


def test_openqasm_gates() -> None:
    """Test the openqasm gates."""
    openqasm_gates = utils.get_openqasm_gates()
    num_openqasm_gates = 42
    assert len(openqasm_gates) == num_openqasm_gates


def test_dj_constant_oracle() -> None:
    """Test the creation of the DJ benchmark constant oracle."""
    qc = dj.create_circuit(5, False)
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


def evaluate_benchmark_with_qasm_formats(
    fct: Callable, args: list[int | QuantumCircuit | str | bool], output_path: str
) -> None:
    """Evaluate the benchmarks with different QASM formats."""
    for qasm_format in ["qasm2", "qasm3"]:
        res = fct(*args, qasm_format=qasm_format)
        assert res
        filepath = Path(output_path) / "testfile.qasm"
        if qasm_format == "qasm2":
            assert load_qasm2(filepath, custom_instructions=LEGACY_CUSTOM_INSTRUCTIONS)
        else:
            assert load_qasm3(filepath)


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

    with pytest.raises(ValueError, match="Length of hidden_string must be num_qubits - 1."):
        bv.create_circuit(3, hidden_string="wrong")
