"""Tests for the get_benchmark method."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest
import pytket
from pytket.extensions.qiskit import tk_to_qiskit
from qiskit import QuantumCircuit

from mqt.bench import get_benchmark, utils
from mqt.bench.benchmark_generator import (
    CompilerSettings,
    QiskitSettings,
    qiskit_helper,
    tket_helper,
)
from mqt.bench.devices import (
    get_device_by_name,
    get_native_gateset_by_name,
)


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
        # Algorithm-level tests
        ("dj", "alg", 3, None, "qiskit", None, "", ""),
        ("wstate", 0, 3, None, "tket", None, "", ""),
        ("shor", "alg", None, "xsmall", "qiskit", None, "", ""),
        ("grover-noancilla", "alg", 3, None, "qiskit", None, "", ""),
        ("qwalk-v-chain", "alg", 3, None, "qiskit", None, "", ""),
        # Independent level tests
        ("ghz", "indep", 3, None, "qiskit", None, "", ""),
        ("graphstate", 1, 3, None, "qiskit", None, "", ""),
        ("graphstate", 1, 3, None, "tket", None, "", ""),
        # Native gates level tests
        (
            "dj",
            "nativegates",
            3,
            None,
            "qiskit",
            CompilerSettings(qiskit=QiskitSettings(optimization_level=0)),
            "ionq",
            "",
        ),
        ("qft", 2, 3, None, "tket", None, "rigetti", "rigetti_aspen_m3"),
        # Mapped level tests
        (
            "ghz",
            "mapped",
            3,
            None,
            "qiskit",
            CompilerSettings(qiskit=QiskitSettings(optimization_level=0)),
            "",
            "ibm_washington",
        ),
        ("ghz", 3, 3, None, "tket", None, "ibm_falcon", "ibm_montreal"),
        ("ghz", 3, 3, None, "qiskit", CompilerSettings(qiskit=QiskitSettings(optimization_level=0)), "", "ionq_aria1"),
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
            gateset = get_native_gateset_by_name(gateset_name)
            assert gate_type in gateset.gates or gate_type == "barrier"


@pytest.mark.skipif(
    sys.platform == "win32",
    reason="PySCF is not available on Windows.",
)
def test_get_benchmark_groundstate() -> None:
    """Test the Groundstate benchmark when not on Windows."""
    assert get_benchmark("groundstate", "alg", None, "small", "qiskit").depth() > 0


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


def test_unidirectional_coupling_map() -> None:
    """Test the unidirectional coupling map for the OQC Lucy device."""
    qc = get_benchmark(
        benchmark_name="dj",
        level="mapped",
        circuit_size=3,
        compiler="tket",
        gateset="oqc",
        device_name="oqc_lucy",
    )
    # check that all gates in the circuit are in the coupling map
    cmap = utils.convert_cmap_to_tuple_list(get_device_by_name("oqc_lucy").coupling_map)
    assert qc.valid_connectivity(arch=pytket.architecture.Architecture(cmap), directed=True)


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


def test_clifford_t() -> None:
    """Test the Clifford+T gateset."""
    qc = get_benchmark(
        benchmark_name="ghz",
        level="nativegates",
        circuit_size=3,
        compiler="qiskit",
        gateset="clifford+t",
    )

    for gate_type in qc.count_ops():
        assert gate_type in get_native_gateset_by_name("clifford+t").gates or gate_type in {"measure", "barrier"}

    with pytest.raises(
        ValueError, match=r"The gateset 'clifford\+t' is not supported by TKET. Please use Qiskit instead."
    ):
        get_benchmark(
            benchmark_name="ghz",
            level="nativegates",
            circuit_size=3,
            compiler="tket",
            gateset="clifford+t",
        )
