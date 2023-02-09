from __future__ import annotations

import sys
from typing import TYPE_CHECKING
from zipfile import ZipFile

import pytest
from mqt.benchviewer import backend
from mqt.benchviewer.main import app, init

if TYPE_CHECKING or sys.version_info >= (3, 10, 0):
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
        ("HHL_indep_5.qasm", -1),
    ],
)
def test_get_opt_level(filename, expected_res):
    assert int(backend.get_opt_level(filename)) == expected_res


@pytest.mark.parametrize(
    ("filename", "expected_res"),
    [
        ("shor_15_4_nativegates_rigetti_qiskit_opt0_18.qasm", 18),
        ("dj_mapped_ibm_washington_qiskit_opt3_103.qasm", 103),
        ("graphstate_nativegates_ibm_qiskit_opt2_15.qasm", 15),
        ("grover-noancilla_nativegates_ibm_qiskit_opt1_8.qasm", 8),
        ("HHL_indep_5.qasm", 5),
    ],
)
def test_get_num_qubits(filename, expected_res):
    assert int(backend.get_num_qubits(filename)) == expected_res


@pytest.mark.parametrize(
    ("filename", "expected_res"),
    [
        (
            "shor_15_4_nativegates_rigetti_qiskit_opt0_18.qasm",
            [
                "shor",
                18,
                False,
                True,
                False,
                "qiskit",
                0,
                "rigetti",
                None,
                "shor_15_4_nativegates_rigetti_qiskit_opt0_18.qasm",
            ],
        ),
        (
            "dj_mapped_ibm_washington_qiskit_opt3_103.qasm",
            [
                "dj",
                103,
                False,
                False,
                True,
                "qiskit",
                3,
                "ibm",
                "ibm_washington",
                "dj_mapped_ibm_washington_qiskit_opt3_103.qasm",
            ],
        ),
        (
            "pricingcall_mapped_oqc_lucy_tket_line_5.qasm",
            [
                "pricingcall",
                5,
                False,
                False,
                True,
                "tket",
                "line",
                "oqc",
                "oqc_lucy",
                "pricingcall_mapped_oqc_lucy_tket_line_5.qasm",
            ],
        ),
        (
            "portfoliovqe_nativegates_ionq_qiskit_opt1_3.qasm",
            [
                "portfoliovqe",
                3,
                False,
                True,
                False,
                "qiskit",
                1,
                "ionq",
                None,
                "portfoliovqe_nativegates_ionq_qiskit_opt1_3.qasm",
            ],
        ),
        (
            "HHL_indep_qiskit_5.qasm",
            [
                "hhl",
                5,
                True,
                False,
                False,
                "qiskit",
                -1,
                None,
                None,
                "HHL_indep_qiskit_5.qasm",
            ],
        ),
    ],
)
def test_parse_data(filename, expected_res):
    assert backend.parse_data(filename) == expected_res


def test_prepare_form_input():
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
        "selectBench_12": "Quantum Generative Adversarial Network",
        "selectBench_13": "Quantum Phase Estimation (QPE) exact",
        "selectBench_14": "Quantum Phase Estimation (QPE) inexact",
        "selectBench_15": "Quantum Walk (no ancilla)",
        "selectBench_16": "Quantum Walk (v-chain)",
        "selectBench_17": "Variational Quantum Eigensolver (VQE)",
        "selectBench_18": "Efficient SU2 ansatz with Random Parameters",
        "selectBench_19": "Real Amplitudes ansatz with Random Parameters",
        "selectBench_20": "Two Local ansatz with Random Parameters",
        "selectBench_21": "W-State",
        "selectBench_22": "Ground State",
        "selectBench_23": "HHL",
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
        "device_ionq_ionq11": "true",
    }

    expected_res = (
        (75, 110),
        [
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "10",
            "11",
            "12",
            "13",
            "14",
            "15",
            "16",
            "17",
            "18",
            "19",
            "20",
            "21",
            "22",
            "23",
            "24",
            "25",
            "26",
            "27",
            "28",
        ],
        (True, True),
        ((True, True), [0, 1, 2, 3], ["ibm", "rigetti", "oqc", "ionq"]),
        (
            (True, True),
            ([0, 1, 2, 3], ["graph", "line"]),
            [
                "ibm_washington",
                "ibm_montreal",
                "rigetti_aspen",
                "oqc_lucy",
                "ionq11",
            ],
        ),
    )

    assert backend.prepare_form_input(form_data) == expected_res


benchviewer = resources.files("mqt.benchviewer")


def test_read_mqtbench_all_zip():
    with resources.as_file(benchviewer) as benchviewer_path:
        target_location = str(benchviewer_path / "static/files")
    assert backend.read_mqtbench_all_zip(skip_question=True, target_location=target_location)


def test_create_database():
    with resources.as_file(benchviewer) as benchviewer_path:
        zip_location = benchviewer_path / "static/files/MQTBench_all.zip"
    with ZipFile(zip_location, mode="r") as zf:
        database = backend.create_database(zf)
    assert len(database) > 0
    backend.database = database

    input_data = (
        (2, 5),
        ["4"],
        (True, False),
        ((False, False), [], []),
        ((False, False), ([], []), []),
    )
    res = backend.get_selected_file_paths(input_data)
    assert len(res) > 3

    input_data = (
        (110, 120),
        ["3"],
        (False, False),
        ((False, True), [], ["rigetti", "ionq"]),
        ((False, False), ([], []), []),
    )
    res = backend.get_selected_file_paths(input_data)
    assert len(res) > 15

    input_data = (
        (75, 110),
        ["2"],
        (False, False),
        ((False, False), [], ["rigetti", "ionq"]),
        ((True, True), ([1, 3], ["graph"]), ["ibm_washington", "rigetti_aspen_m2"]),
    )
    res = backend.get_selected_file_paths(input_data)
    assert len(res) > 20

    input_data = (
        (2, 5),
        ["23"],
        (True, True),
        ((True, False), [1, 3], ["rigetti", "ionq", "oqc", "ibm"]),
        (
            (True, True),
            ([1, 3], ["graph", "line"]),
            ["ibm_montreal", "rigetti_aspen", "ionq11", "ocq_lucy"],
        ),
    )
    res = backend.get_selected_file_paths(input_data)
    assert len(res) > 20

    input_data = (
        (2, 130),
        ["1"],
        (False, False),
        ((True, True), [], []),
        ((True, True), ([], []), []),
    )
    res = backend.get_selected_file_paths(input_data)
    assert res == []


def test_flask_server():
    with resources.as_file(benchviewer) as benchviewer_path:
        benchviewer_location = benchviewer_path
    target_location = str(benchviewer_location / "static/files")
    assert init(
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
