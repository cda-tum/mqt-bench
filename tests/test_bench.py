from __future__ import annotations

from pathlib import Path

import pytest
from mqt.bench import get_benchmark, qiskit_helper, tket_helper, utils
from mqt.bench.benchmarks import (
    ae,
    dj,
    ghz,
    graphstate,
    groundstate,
    grover,
    hhl,
    portfolioqaoa,
    portfoliovqe,
    pricingcall,
    pricingput,
    qaoa,
    qft,
    qftentangled,
    qgan,
    qpeexact,
    qpeinexact,
    qwalk,
    realamprandom,
    routing,
    shor,
    su2random,
    tsp,
    twolocalrandom,
    vqe,
    wstate,
)
from pytket.extensions.qiskit import tk_to_qiskit
from qiskit import QuantumCircuit

test_qasm_output_path = "./test_output/"


def test_configure_begin():
    Path(test_qasm_output_path).mkdir(parents=True, exist_ok=True)
    utils.set_qasm_output_path(test_qasm_output_path)
    assert utils.get_qasm_output_path() == test_qasm_output_path


@pytest.mark.parametrize(
    ("benchmark", "input_value", "scalable"),
    [
        (ae, 8, True),
        (ghz, 5, True),
        (dj, 3, True),
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
    num_openqasm_gates = 42
    assert len(openqasm_gates) == num_openqasm_gates


def test_rigetti_cmap_generator():
    num_edges = 212
    assert len(utils.get_rigetti_aspen_m2_map()) == num_edges


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


def test_unidirectional_coupling_map():
    from pytket.architecture import Architecture

    qc = get_benchmark(
        benchmark_name="dj",
        level="mapped",
        circuit_size=3,
        compiler="tket",
        compiler_settings={"tket": {"placement": "graphplacement"}},
        gate_set_name="oqc",
        device_name="oqc_lucy",
    )
    # check that all gates in the circuit are in the coupling map
    assert qc.valid_connectivity(arch=Architecture(utils.get_cmap_oqc_lucy()), directed=True)


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
            assert gate_type in qiskit_helper.get_native_gates(gate_set_name) or gate_type == "barrier"


def test_configure_end():
    # delete all files in the test directory and the directory itself

    for f in Path(test_qasm_output_path).iterdir():
        f.unlink()
    Path(test_qasm_output_path).rmdir()
    utils.set_qasm_output_path()


# def test_benchmark_creation(monkeypatch):
#     import json
#
#     config = {
#         "timeout": 120,
#         "benchmarks": [
#             {
#                 "name": benchmark,
#                 "include": True,
#                 "min_qubits": 3,
#                 "max_qubits": 4,
#                 "stepsize": 1,
#                 "ancillary_mode": ["noancilla", "v-chain"],
#                 "instances": ["small"],
#                 "min_index": 1,
#                 "max_index": 2,
#                 "min_nodes": 2,
#                 "max_nodes": 3,
#                 "min_uncertainty": 2,
#                 "max_uncertainty": 3,
#             }
#             for benchmark in utils.get_supported_benchmarks()
#             if benchmark != "shor"
#         ],
#     }
#     with Path("test_config.json").open("w") as f:
#         json.dump(config, f)
#     monkeypatch.setattr("sys.argv", ["pytest", "--file-name", "test_config.json"])
#     generate()
#
#     benchmarks_path = utils.get_qasm_output_path()
#     assert len(list(Path(benchmarks_path).iterdir())) > 1000
#
#     Path("test_config.json").unlink()


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
):
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


def test_oqc_postprocessing():
    qc = get_benchmark("ghz", 1, 5)
    assert qc
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
