from __future__ import annotations

import sys
from typing import TYPE_CHECKING

import pytest

from mqt.benchviewer import Backend, BenchmarkConfiguration, Server, backend
from mqt.benchviewer.main import app

if TYPE_CHECKING or sys.version_info >= (3, 10, 0):  # pragma: no cover
    from importlib import resources
else:
    import importlib_resources as resources


@pytest.mark.parametrize(
    ("filename", "expected_res"),
    [
        ("shor_15_4_nativegates_rigetti_qiskit_opt0_18.qasm", 0),
        ("dj_mapped_ibm_washington_qiskit_opt3_103.qasm", 3),
        ("graphstate_nativegates_ibm_qiskit_opt2_15.qasm", 2),
        ("grover-noancilla_nativegates_ibm_qiskit_opt1_8.qasm", 1),
        ("random_indep_5.qasm", -1),
    ],
)
def test_get_opt_level(filename: str, expected_res: int) -> None:
    assert int(backend.get_opt_level(filename)) == expected_res


@pytest.mark.parametrize(
    ("filename", "expected_res"),
    [
        ("shor_15_4_nativegates_rigetti_qiskit_opt0_18.qasm", 18),
        ("dj_mapped_ibm_washington_qiskit_opt3_103.qasm", 103),
        ("graphstate_nativegates_ibm_qiskit_opt2_15.qasm", 15),
        ("grover-noancilla_nativegates_ibm_qiskit_opt1_8.qasm", 8),
        ("random_indep_5.qasm", 5),
    ],
)
def test_get_num_qubits(filename: str, expected_res: int) -> None:
    assert int(backend.get_num_qubits(filename)) == expected_res


@pytest.mark.parametrize(
    ("filename", "expected_res"),
    [
        (
            "shor_15_4_nativegates_rigetti_qiskit_opt0_18.qasm",
            backend.ParsedBenchmarkName(
                benchmark="shor",
                num_qubits=18,
                indep_flag=False,
                nativegates_flag=True,
                mapped_flag=False,
                compiler="qiskit",
                compiler_settings=0,
                gate_set="rigetti",
                target_device=None,
                filename="shor_15_4_nativegates_rigetti_qiskit_opt0_18.qasm",
            ),
        ),
        (
            "dj_mapped_ibm_washington_qiskit_opt3_103.qasm",
            backend.ParsedBenchmarkName(
                benchmark="dj",
                num_qubits=103,
                indep_flag=False,
                nativegates_flag=False,
                mapped_flag=True,
                compiler="qiskit",
                compiler_settings=3,
                gate_set="ibm",
                target_device="ibm_washington",
                filename="dj_mapped_ibm_washington_qiskit_opt3_103.qasm",
            ),
        ),
        (
            "pricingcall_mapped_oqc_lucy_tket_line_5.qasm",
            backend.ParsedBenchmarkName(
                benchmark="pricingcall",
                num_qubits=5,
                indep_flag=False,
                nativegates_flag=False,
                mapped_flag=True,
                compiler="tket",
                compiler_settings="line",
                gate_set="oqc",
                target_device="oqc_lucy",
                filename="pricingcall_mapped_oqc_lucy_tket_line_5.qasm",
            ),
        ),
        (
            "portfoliovqe_nativegates_ionq_qiskit_opt1_3.qasm",
            backend.ParsedBenchmarkName(
                benchmark="portfoliovqe",
                num_qubits=3,
                indep_flag=False,
                nativegates_flag=True,
                mapped_flag=False,
                compiler="qiskit",
                compiler_settings=1,
                gate_set="ionq",
                target_device=None,
                filename="portfoliovqe_nativegates_ionq_qiskit_opt1_3.qasm",
            ),
        ),
        (
            "random_indep_qiskit_5.qasm",
            backend.ParsedBenchmarkName(
                benchmark="random",
                num_qubits=5,
                indep_flag=True,
                nativegates_flag=False,
                mapped_flag=False,
                compiler="qiskit",
                compiler_settings=-1,
                gate_set=None,
                target_device=None,
                filename="random_indep_qiskit_5.qasm",
            ),
        ),
    ],
)
def test_parse_data(filename: str, expected_res: backend.ParsedBenchmarkName) -> None:
    assert backend.parse_data(filename) == expected_res


def test_prepare_form_input() -> None:
    form_data = {
        "all_benchmarks": "true",
        "minQubits": "75",
        "maxQubits": "110",
        "selectBench_1": "Amplitude Estimation (AE)",
        "selectBench_2": "Deutsch-Jozsa",
        "selectBench_3": "Graph State",
        "selectBench_4": "GHZ State",
        "selectBench_5": "Grover's (no ancilla)",
        "selectBench_6": "Grover's (v-chain)",
        "selectBench_7": "Portfolio Optimization with QAOA",
        "selectBench_8": "Portfolio Optimization with VQE",
        "selectBench_9": "Quantum Approximation Optimization Algorithm (QAOA)",
        "selectBench_10": "Quantum Fourier Transformation (QFT)",
        "selectBench_11": "QFT Entangled",
        "selectBench_12": "Quantum Neural Network (QNN)",
        "selectBench_13": "Quantum Phase Estimation (QPE) exact",
        "selectBench_14": "Quantum Phase Estimation (QPE) inexact",
        "selectBench_15": "Quantum Walk (no ancilla)",
        "selectBench_16": "Quantum Walk (v-chain)",
        "selectBench_17": "Random Circuit",
        "selectBench_18": "Variational Quantum Eigensolver (VQE)",
        "selectBench_19": "Efficient SU2 ansatz with Random Parameters",
        "selectBench_20": "Real Amplitudes ansatz with Random Parameters",
        "selectBench_21": "Two Local ansatz with Random Parameters",
        "selectBench_22": "W-State",
        "selectBench_23": "Ground State",
        "selectBench_24": "Pricing Call Option",
        "selectBench_25": "Pricing Put Option",
        "selectBench_26": "Routing",
        "selectBench_27": "Shor's",
        "selectBench_28": "Travelling Salesman",
        "indep_qiskit_compiler": "true",
        "indep_tket_compiler": "true",
        "nativegates_qiskit_compiler": "true",
        "nativegates_qiskit_compiler_opt0": "true",
        "nativegates_qiskit_compiler_opt1": "true",
        "nativegates_qiskit_compiler_opt2": "true",
        "nativegates_qiskit_compiler_opt3": "true",
        "nativegates_tket_compiler value=": "on",
        "nativegates_ibm": "true",
        "nativegates_rigetti": "true",
        "nativegates_oqc": "true",
        "nativegates_ionq": "true",
        "nativegates_quantinuum": "true",
        "mapped_qiskit_compiler": "true",
        "mapped_qiskit_compiler_opt0": "true",
        "mapped_qiskit_compiler_opt1": "true",
        "mapped_qiskit_compiler_opt2": "true",
        "mapped_qiskit_compiler_opt3": "true",
        "mapped_tket_compiler": "true",
        "mapped_tket_compiler_graph": "true",
        "mapped_tket_compiler_line": "true",
        "device_ibm_washington": "true",
        "device_ibm_montreal": "true",
        "device_rigetti_aspen_m2": "true",
        "device_oqc_lucy": "true",
        "device_ionq_harmony": "true",
        "device_ionq_aria1": "true",
        "device_quantinuum_h2": "true",
    }

    expected_res = BenchmarkConfiguration(
        min_qubits=75,
        max_qubits=110,
        indices_benchmarks=list(range(1, 29)),
        indep_qiskit_compiler=True,
        indep_tket_compiler=True,
        nativegates_qiskit_compiler=True,
        native_qiskit_opt_lvls=[0, 1, 2, 3],
        nativegates_tket_compiler=True,
        native_gatesets=["ibm", "rigetti", "oqc", "ionq", "quantinuum"],
        mapped_qiskit_compiler=True,
        mapped_qiskit_opt_lvls=[0, 1, 2, 3],
        mapped_tket_compiler=True,
        mapped_tket_placements=["graph", "line"],
        mapped_devices=[
            "ibm_washington",
            "ibm_montreal",
            "rigetti_aspen_m2",
            "oqc_lucy",
            "ionq_harmony",
            "ionq_aria1",
            "quantinuum_h2",
        ],
    )
    backend = Backend()
    assert backend.prepare_form_input(form_data) == expected_res

    form_data = {
        "all_benchmarks": "true",
        "minQubits": "75",
        "maxQubits": "110",
        "indep_qiskit_compiler": "true",
        "indep_tket_compiler": "true",
        "nativegates_qiskit_compiler": "true",
        "nativegates_qiskit_compiler_opt0": "true",
        "nativegates_qiskit_compiler_opt1": "true",
        "nativegates_qiskit_compiler_opt2": "true",
        "nativegates_qiskit_compiler_opt3": "true",
        "nativegates_tket_compiler value=": "on",
        "nativegates_ibm": "true",
        "nativegates_rigetti": "true",
        "nativegates_oqc": "true",
        "nativegates_ionq": "true",
        "nativegates_quantinuum": "true",
        "mapped_qiskit_compiler": "true",
        "mapped_qiskit_compiler_opt0": "true",
        "mapped_qiskit_compiler_opt1": "true",
        "mapped_qiskit_compiler_opt2": "true",
        "mapped_qiskit_compiler_opt3": "true",
        "mapped_tket_compiler": "true",
        "mapped_tket_compiler_graph": "true",
        "mapped_tket_compiler_line": "true",
        "device_ibm_washington": "true",
        "device_ibm_montreal": "true",
        "device_rigetti_aspen_m2": "true",
        "device_oqc_lucy": "true",
        "device_ionq_harmony": "true",
        "device_ionq_aria1": "true",
        "device_quantinuum_h2": "true",
    }
    expected_res = BenchmarkConfiguration(
        min_qubits=75,
        max_qubits=110,
        indices_benchmarks=[],
        indep_qiskit_compiler=True,
        indep_tket_compiler=True,
        nativegates_qiskit_compiler=True,
        native_qiskit_opt_lvls=[0, 1, 2, 3],
        nativegates_tket_compiler=True,
        native_gatesets=["ibm", "rigetti", "oqc", "ionq", "quantinuum"],
        mapped_qiskit_compiler=True,
        mapped_qiskit_opt_lvls=[0, 1, 2, 3],
        mapped_tket_compiler=True,
        mapped_tket_placements=["graph", "line"],
        mapped_devices=[
            "ibm_washington",
            "ibm_montreal",
            "rigetti_aspen_m2",
            "oqc_lucy",
            "ionq_harmony",
            "ionq_aria1",
            "quantinuum_h2",
        ],
    )
    backend = Backend()
    assert backend.prepare_form_input(form_data) == expected_res


benchviewer = resources.files("mqt.benchviewer")


def test_read_mqtbench_all_zip() -> None:
    backend = Backend()
    with resources.as_file(benchviewer) as benchviewer_path:
        target_location = str(benchviewer_path / "static/files")
    assert backend.read_mqtbench_all_zip(skip_question=True, target_location=target_location)


def test_create_database() -> None:
    backend = Backend()

    res_zip = backend.read_mqtbench_all_zip(
        skip_question=True,
        target_location=str(resources.files("mqt.benchviewer") / "static" / "files"),
    )
    assert res_zip

    assert backend.database is None
    backend.init_database()

    input_data = BenchmarkConfiguration(
        min_qubits=2,
        max_qubits=5,
        indices_benchmarks=[4],
        indep_qiskit_compiler=True,
        indep_tket_compiler=False,
        nativegates_qiskit_compiler=False,
        nativegates_tket_compiler=False,
        mapped_qiskit_compiler=False,
        mapped_tket_compiler=False,
    )

    res = backend.get_selected_file_paths(input_data)
    assert isinstance(res, list)
    assert len(res) > 3

    input_data = BenchmarkConfiguration(
        min_qubits=110,
        max_qubits=120,
        indices_benchmarks=[3],
        indep_qiskit_compiler=False,
        indep_tket_compiler=False,
        nativegates_qiskit_compiler=False,
        nativegates_tket_compiler=True,
        mapped_qiskit_compiler=False,
        mapped_tket_compiler=False,
        native_gatesets=["rigetti", "ionq"],
    )
    res = backend.get_selected_file_paths(input_data)
    assert isinstance(res, list)
    assert len(res) > 15

    input_data = BenchmarkConfiguration(
        min_qubits=75,
        max_qubits=110,
        indices_benchmarks=[2],
        indep_qiskit_compiler=False,
        indep_tket_compiler=False,
        nativegates_qiskit_compiler=False,
        nativegates_tket_compiler=False,
        mapped_qiskit_compiler=True,
        mapped_tket_compiler=True,
        native_gatesets=["rigetti", "ionq"],
        mapped_devices=["ibm_washington", "rigetti_aspen_m2"],
        mapped_tket_placements=["graph"],
    )
    res = backend.get_selected_file_paths(input_data)
    assert isinstance(res, list)
    assert len(res) > 20

    input_data = BenchmarkConfiguration(
        min_qubits=2,
        max_qubits=5,
        indices_benchmarks=[23],
        indep_qiskit_compiler=True,
        indep_tket_compiler=True,
        nativegates_qiskit_compiler=True,
        nativegates_tket_compiler=False,
        mapped_qiskit_compiler=True,
        mapped_tket_compiler=True,
        native_gatesets=["rigetti", "ionq", "oqc", "ibm", "quantinuum"],
        mapped_devices=[
            "ibm_montreal",
            "rigetti_aspen_m2",
            "ionq_harmony",
            "ionq_aria1",
            "ocq_lucy",
            "quantinuum_h2",
        ],
        mapped_tket_placements=["graph", "line"],
        native_qiskit_opt_lvls=[0, 3],
        mapped_qiskit_opt_lvls=[0, 3],
    )
    res = backend.get_selected_file_paths(input_data)
    assert isinstance(res, list)
    assert len(res) > 20

    input_data = BenchmarkConfiguration(
        min_qubits=2,
        max_qubits=130,
        indices_benchmarks=[1],
        indep_qiskit_compiler=False,
        indep_tket_compiler=False,
        nativegates_qiskit_compiler=True,
        nativegates_tket_compiler=True,
        mapped_qiskit_compiler=True,
        mapped_tket_compiler=True,
    )
    res = backend.get_selected_file_paths(input_data)
    assert isinstance(res, list)
    assert res == []


def test_streaming_zip() -> None:
    backend = Backend()
    backend.read_mqtbench_all_zip(
        skip_question=True,
        target_location=str(resources.files("mqt.benchviewer") / "static" / "files"),
    )
    res = backend.generate_zip_ephemeral_chunks(filenames=["ae_indep_qiskit_2.qasm", "ae_indep_qiskit_3.qasm"])
    assert list(res)

    with pytest.raises(KeyError):
        assert not list(backend.generate_zip_ephemeral_chunks(filenames=["not_existing_file.qasm"]))


def test_flask_server() -> None:
    with resources.as_file(benchviewer) as benchviewer_path:
        benchviewer_location = benchviewer_path
    target_location = str(benchviewer_location / "static/files")

    Server(
        skip_question=True,
        activate_logging=False,
        target_location=target_location,
    )

    paths_to_check = [
        "static/files/MQTBench_all.zip",
        "templates/benchmark_description.html",
        "templates/index.html",
        "templates/legal.html",
        "templates/description.html",
    ]
    for path in paths_to_check:
        assert (benchviewer_location / path).is_file()

    with app.test_client() as c:
        success_code = 200
        links_to_check = [
            "/mqtbench/index",
            "/mqtbench/download",
            "/mqtbench/legal",
            "/mqtbench/description",
            "/mqtbench/benchmark_description",
        ]
        for link in links_to_check:
            assert c.get(link).status_code == success_code
