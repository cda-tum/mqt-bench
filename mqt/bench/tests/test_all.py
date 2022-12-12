from __future__ import annotations

import os

import pytest
from pytket.extensions.qiskit import tk_to_qiskit
from qiskit import QuantumCircuit

from mqt.bench.benchmark_generator import get_benchmark
from mqt.bench.benchmarks import (
    ae,
    dj,
    ghz,
    graphstate,
    grover,
    hhl,
    qaoa,
    qft,
    qftentangled,
    qpeexact,
    qpeinexact,
    qwalk,
    realamprandom,
    shor,
    su2random,
    twolocalrandom,
    vqe,
    wstate,
)
from mqt.bench.benchmarks.qiskit_application_finance import (
    portfolioqaoa,
    portfoliovqe,
    pricingcall,
    pricingput,
)
from mqt.bench.benchmarks.qiskit_application_ml import qgan
from mqt.bench.benchmarks.qiskit_application_nature import groundstate
from mqt.bench.benchmarks.qiskit_application_optimization import routing, tsp
from mqt.bench.utils import qiskit_helper, tket_helper, utils


def test_configure_begin():
    test_qasm_output_path = "./test_output/"
    if not os.path.exists(test_qasm_output_path):
        os.mkdir(test_qasm_output_path)
    utils.set_qasm_output_path(test_qasm_output_path)
    assert utils.get_qasm_output_path() == test_qasm_output_path


@pytest.mark.parametrize(
    "benchmark, input_value, scalable",
    [
        (ae, 8, True),
        (ghz, 5, True),
        (dj, 5, True),
        (graphstate, 8, True),
        (grover, 5, False),
        (hhl, 2, False),
        (qaoa, 5, True),
        (qft, 8, True),
        (qftentangled, 8, True),
        (qpeexact, 8, True),
        (qpeinexact, 8, True),
        (tsp, 3, False),
        (qwalk, 5, False),
        (vqe, 5, True),
        (realamprandom, 9, True),
        (su2random, 7, True),
        (twolocalrandom, 8, True),
        (wstate, 8, True),
        (portfolioqaoa, 5, True),
        (shor, 9, False),
        (portfoliovqe, 5, True),
        (pricingcall, 5, False),
        (pricingput, 5, False),
        (qgan, 5, True),
    ],
)
def test_quantumcircuit_indep_level(benchmark, input_value, scalable):
    if benchmark in (grover, qwalk):
        qc = benchmark.create_circuit(input_value, ancillary_mode="noancilla")
    else:
        qc = benchmark.create_circuit(input_value)
    if scalable:
        assert qc.num_qubits == input_value
    res = qiskit_helper.get_indep_level(qc, input_value, file_precheck=False)
    assert res
    res = qiskit_helper.get_indep_level(qc, input_value, file_precheck=True)
    assert res

    res = tket_helper.get_indep_level(qc, input_value, file_precheck=False)
    assert res
    res = tket_helper.get_indep_level(qc, input_value, file_precheck=True)
    assert res


@pytest.mark.parametrize(
    "benchmark, input_value, scalable",
    [
        (ae, 8, True),
        (ghz, 5, True),
        (dj, 5, True),
        (graphstate, 8, True),
        (grover, 5, False),
        (qaoa, 5, True),
        (qft, 8, True),
        (qftentangled, 8, True),
        (qpeexact, 8, True),
        (qpeinexact, 8, True),
        (tsp, 3, False),
        (qwalk, 5, False),
        (vqe, 5, True),
        (realamprandom, 3, True),
        (su2random, 7, True),
        (twolocalrandom, 5, True),
        (wstate, 8, True),
        (portfolioqaoa, 5, True),
        (portfoliovqe, 5, True),
        (pricingcall, 5, False),
        (pricingput, 5, False),
        (qgan, 5, True),
    ],
)
def test_quantumcircuit_native_and_mapped_levels(benchmark, input_value, scalable):
    if benchmark in (grover, qwalk):
        qc = benchmark.create_circuit(input_value, ancillary_mode="noancilla")
    else:
        qc = benchmark.create_circuit(input_value)
    if scalable:
        assert qc.num_qubits == input_value

    compilation_paths = [
        ("ibm", [("ibm_washington", 127), ("ibm_montreal", 27)]),
        ("rigetti", [("rigetti_aspen_m2", 80)]),
        ("ionq", [("ionq11", 11)]),
        ("oqc", [("oqc_lucy", 8)]),
    ]
    for gate_set_name, devices in compilation_paths:
        opt_level = 1
        res = qiskit_helper.get_native_gates_level(
            qc,
            gate_set_name,
            qc.num_qubits,
            opt_level,
            file_precheck=False,
        )
        assert res
        res = qiskit_helper.get_native_gates_level(
            qc,
            gate_set_name,
            qc.num_qubits,
            opt_level,
            file_precheck=True,
        )
        assert res
        if gate_set_name != "ionq":
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
                    )
                    assert res
                    res = qiskit_helper.get_mapped_level(
                        qc,
                        gate_set_name,
                        qc.num_qubits,
                        device_name,
                        opt_level,
                        file_precheck=True,
                    )
                    assert res

    for gate_set_name, devices in compilation_paths:
        res = tket_helper.get_native_gates_level(
            qc,
            gate_set_name,
            qc.num_qubits,
            file_precheck=False,
        )
        assert res
        res = tket_helper.get_native_gates_level(
            qc,
            gate_set_name,
            qc.num_qubits,
            file_precheck=True,
        )
        assert res
        if gate_set_name != "ionq":
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
                    )
                    assert res
                    res = tket_helper.get_mapped_level(
                        qc,
                        gate_set_name,
                        qc.num_qubits,
                        device_name,
                        False,
                        file_precheck=True,
                    )
                    assert res


def test_openqasm_gates():
    openqasm_gates = utils.get_openqasm_gates()
    assert len(openqasm_gates) == 42


def test_rigetti_cmap_generator():
    assert len(utils.get_rigetti_aspen_m2_map()) == 212


def test_dj_constant_oracle():
    qc = dj.create_circuit(5, False)
    assert qc.depth() > 0


def test_groundstate():
    m = utils.get_molecule("small")
    qc = groundstate.create_circuit(m)
    assert qc.depth() > 0


def test_routing():
    qc = routing.create_circuit(4, 2)
    assert qc.depth() > 0


@pytest.mark.parametrize(
    "benchmark_name, level, circuit_size, benchmark_instance_name, compiler, compiler_settings, gate_set_name, device_name,",
    [
        (
            "dj",
            "alg",
            5,
            None,
            "qiskit",
            None,
            None,
            None,
        ),
        (
            "wstate",
            0,
            6,
            None,
            "tket",
            None,
            None,
            None,
        ),
        (
            "ghz",
            "indep",
            5,
            None,
            "qiskit",
            None,
            None,
            None,
        ),
        (
            "graphstate",
            1,
            4,
            None,
            "qiskit",
            None,
            None,
            None,
        ),
        (
            "graphstate",
            1,
            4,
            None,
            "tket",
            None,
            None,
            None,
        ),
        (
            "groundstate",
            1,
            4,
            "small",
            "qiskit",
            None,
            None,
            None,
        ),
        (
            "dj",
            "nativegates",
            5,
            None,
            "qiskit",
            {
                "qiskit": {"optimization_level": 2},
            },
            "ionq",
            None,
        ),
        (
            "dj",
            "nativegates",
            5,
            None,
            "qiskit",
            {
                "qiskit": {"optimization_level": 2},
            },
            "ibm",
            None,
        ),
        (
            "dj",
            "nativegates",
            5,
            None,
            "qiskit",
            {
                "qiskit": {"optimization_level": 2},
            },
            "rigetti",
            None,
        ),
        (
            "dj",
            "nativegates",
            5,
            None,
            "qiskit",
            {
                "qiskit": {"optimization_level": 2},
            },
            "oqc",
            None,
        ),
        (
            "qft",
            2,
            6,
            None,
            "qiskit",
            {
                "qiskit": {"optimization_level": 3},
            },
            "ionq",
            None,
        ),
        (
            "qft",
            2,
            6,
            None,
            "qiskit",
            {
                "qiskit": {"optimization_level": 3},
            },
            "ibm",
            None,
        ),
        (
            "qft",
            2,
            6,
            None,
            "tket",
            None,
            "rigetti",
            None,
        ),
        (
            "qft",
            2,
            6,
            None,
            "tket",
            None,
            "oqc",
            None,
        ),
        (
            "qpeexact",
            "mapped",
            5,
            None,
            "qiskit",
            {
                "qiskit": {"optimization_level": 1},
            },
            "ibm",
            "ibm_washington",
        ),
        (
            "qpeexact",
            "mapped",
            5,
            None,
            "qiskit",
            {
                "qiskit": {"optimization_level": 1},
            },
            "ibm",
            "ibm_montreal",
        ),
        (
            "qpeexact",
            "mapped",
            5,
            None,
            "qiskit",
            {
                "qiskit": {"optimization_level": 1},
            },
            "rigetti",
            "rigetti_aspen_m2",
        ),
        (
            "qpeexact",
            "mapped",
            5,
            None,
            "qiskit",
            {
                "qiskit": {"optimization_level": 1},
            },
            "ionq",
            "ionq11",
        ),
        (
            "qpeexact",
            "mapped",
            5,
            None,
            "qiskit",
            {
                "qiskit": {"optimization_level": 1},
            },
            "oqc",
            "oqc_lucy",
        ),
        (
            "qpeinexact",
            3,
            4,
            None,
            "qiskit",
            {
                "qiskit": {"optimization_level": 1},
            },
            "ibm",
            "ibm_washington",
        ),
        (
            "qpeinexact",
            3,
            4,
            None,
            "tket",
            {
                "tket": {"placement": "lineplacement"},
            },
            "ibm",
            "ibm_washington",
        ),
        (
            "qpeinexact",
            3,
            4,
            None,
            "qiskit",
            {
                "qiskit": {"optimization_level": 1},
            },
            "ibm",
            "ibm_montreal",
        ),
        (
            "qpeinexact",
            3,
            4,
            None,
            "tket",
            {
                "tket": {"placement": "graphplacement"},
            },
            "ibm",
            "ibm_montreal",
        ),
        (
            "qpeinexact",
            3,
            4,
            None,
            "qiskit",
            {
                "qiskit": {"optimization_level": 1},
            },
            "rigetti",
            "rigetti_aspen_m2",
        ),
        (
            "qpeinexact",
            3,
            4,
            None,
            "tket",
            {
                "tket": {"placement": "lineplacement"},
            },
            "rigetti",
            "rigetti_aspen_m2",
        ),
        (
            "qpeinexact",
            3,
            4,
            None,
            "qiskit",
            {
                "qiskit": {"optimization_level": 1},
            },
            "oqc",
            "oqc_lucy",
        ),
        (
            "qpeinexact",
            3,
            4,
            None,
            "tket",
            {
                "tket": {"placement": "graphplacement"},
            },
            "oqc",
            "oqc_lucy",
        ),
    ],
)
def test_get_benchmark(
    benchmark_name,
    level,
    circuit_size,
    benchmark_instance_name,
    compiler,
    compiler_settings,
    gate_set_name,
    device_name,
):

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
        for instruction, _qargs, _cargs in qc.data:
            gate_type = instruction.name
            assert (
                gate_type in qiskit_helper.get_native_gates(gate_set_name)
                or gate_type == "barrier"
            )


def test_configure_end():
    test_qasm_output_path = "./test_output/"
    for f in os.listdir(test_qasm_output_path):
        os.remove(os.path.join(test_qasm_output_path, f))
    os.rmdir(test_qasm_output_path)
    utils.set_qasm_output_path()


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
):
    directory = "."
    filename = "ae_test_qiskit"
    qc = get_benchmark("ae", abstraction_level, 5)
    assert qc
    res = qiskit_helper.get_mapped_level(
        qc, "ibm", qc.num_qubits, "ibm_washington", 1, False, False, directory, filename
    )
    assert res
    path = os.path.join(directory, filename) + ".qasm"
    assert os.path.isfile(path)
    os.remove(path)

    directory = "."
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
    path = os.path.join(directory, filename) + ".qasm"
    assert os.path.isfile(path)
    os.remove(path)


def test_oqc_postprocessing():
    qc = get_benchmark("ghz", 1, 5)
    assert qc
    directory = "."
    filename = "ghz_oqc"
    path = os.path.join(directory, filename) + ".qasm"

    tket_helper.get_native_gates_level(
        qc,
        "oqc",
        qc.num_qubits,
        file_precheck=False,
        return_qc=False,
        target_directory=directory,
        target_filename=filename,
    )
    assert QuantumCircuit.from_qasm_file(path)
    os.remove(path)

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
    assert QuantumCircuit.from_qasm_file(path)
    os.remove(path)

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
    assert QuantumCircuit.from_qasm_file(path)
    os.remove(path)

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
    assert QuantumCircuit.from_qasm_file(path)
    os.remove(path)
