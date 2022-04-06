from benchviewer.src import backend

import pytest


@pytest.mark.parametrize(
    "filename, expected_res",
    [
        ("shor_15_4_nativegates_rigetti_opt0_18.qasm", 0),
        ("dj_mapped_ibm-s_opt3_103.qasm", 3),
        ("graphstate_nativegates_ibm_opt2_15.qasm", 2),
        ("grover-noancilla_nativegates_ibm_opt1_8.qasm", 1),
        ("HHL_t-indep_5.qasm", -1),
    ],
)
def test_get_opt_level(filename, expected_res):
    assert int(backend.get_opt_level(filename)) == expected_res


@pytest.mark.parametrize(
    "filename, expected_res",
    [
        ("shor_15_4_nativegates_rigetti_opt0_18.qasm", 18),
        ("dj_mapped_ibm-s_opt3_103.qasm", 103),
        ("graphstate_nativegates_ibm_opt2_15.qasm", 15),
        ("grover-noancilla_nativegates_ibm_opt1_8.qasm", 8),
        ("HHL_t-indep_a.qasm", -1),
    ],
)
def test_get_num_qubits(filename, expected_res):
    assert int(backend.get_num_qubits(filename)) == expected_res


@pytest.mark.parametrize(
    "directory, filename, expected_res",
    [
        (
            "../../static/qasm_output",
            "shor_15_4_nativegates_rigetti_opt0_18.qasm",
            [
                "shor",
                18,
                "rigetti",
                False,
                False,
                True,
                False,
                False,
                False,
                0,
                "../../static/qasm_output/shor_15_4_nativegates_rigetti_opt0_18.qasm",
            ],
        ),
        (
            "../../static/qasm_output",
            "dj_mapped_ibm-s_opt3_103.qasm",
            [
                "dj",
                103,
                "ibm",
                False,
                False,
                False,
                True,
                True,
                False,
                3,
                "../../static/qasm_output/dj_mapped_ibm-s_opt3_103.qasm",
            ],
        ),
        (
            "../../static/qasm_output",
            "dj_mapped_ibm-b_opt3_103.qasm",
            [
                "dj",
                103,
                "ibm",
                False,
                False,
                False,
                True,
                False,
                True,
                3,
                "../../static/qasm_output/dj_mapped_ibm-b_opt3_103.qasm",
            ],
        ),
        (
            "../../static/qasm_output",
            "grover-noancilla_nativegates_ibm_opt3_8.qasm",
            [
                "grover-noancilla",
                8,
                "ibm",
                False,
                False,
                True,
                False,
                False,
                False,
                3,
                "../../static/qasm_output/grover-noancilla_nativegates_ibm_opt3_8.qasm",
            ],
        ),
        (
            "../../static/qasm_output",
            "HHL_t-indep_5.qasm",
            [
                "hhl",
                5,
                False,
                False,
                True,
                False,
                False,
                False,
                False,
                -1,
                "../../static/qasm_output/HHL_t-indep_5.qasm",
            ],
        ),
    ],
)
def test_parse_data(directory, filename, expected_res):
    assert backend.parse_data(directory, filename) == expected_res


def test_prepareFormInput():
    form_data = dict(
        [
            ("selectBench_4", "GHZ State"),
            ("minQubits_4", "5"),
            ("maxQubits_4", "10"),
            ("indepLevel_4", "true"),
            ("selectBench_3", "Graph State"),
            ("minQubits_3", "5"),
            ("maxQubits_3", "20"),
            ("nativeGatesLevel_3", "true"),
            ("ibm_3", "ibm"),
            ("optlevel1_3", "1"),
            ("optlevel3_3", "3"),
            ("selectBench_21", "W State"),
            ("minQubits_21", "10"),
            ("maxQubits_21", "30"),
            ("mappedLevel_21", "true"),
            ("rigetti_21", "rigetti"),
            ("smallest_arch_21", "True"),
            ("optlevel0_21", "0"),
            ("optlevel2_21", "2"),
            ("selectBench_10", "Quantum Fourier Transformation (QFT)"),
            ("minQubits_10", "20"),
            ("maxQubits_10", "120"),
            ("nativeGatesLevel_10", "true"),
            ("mappedLevel_10", "true"),
            ("ibm_10", "ibm"),
            ("rigetti_10", "rigetti"),
            ("smallest_arch_10", "True"),
            ("biggest_arch_10", "True"),
            ("optlevel0_10", "0"),
            ("optlevel1_10", "1"),
            ("optlevel3_10", "3"),
            ("selectBench_11", "Entangled QFT"),
            ("minQubits_11", "100"),
            ("maxQubits_11", "110"),
            ("indepLevel_11", "true"),
            ("mappedLevel_11", "true"),
            ("biggest_arch_11", "True"),
            ("optlevel2_11", "2"),
            ("selectBench_13", "Quantum Phase Estimation (QPE) exact"),
            ("minQubits_13", "5"),
            ("maxQubits_13", "40"),
            ("algorithmLevel_13", "true"),
        ]
    )
    expected_res = {
        "3": {
            "selectBench_3": "Graph State",
            "minQubits_3": "5",
            "maxQubits_3": "20",
            "nativeGatesLevel_3": "true",
            "ibm_3": "ibm",
            "optlevel1_3": "1",
            "optlevel3_3": "3",
        },
        "4": {
            "selectBench_4": "GHZ State",
            "minQubits_4": "5",
            "maxQubits_4": "10",
            "indepLevel_4": "true",
        },
        "10": {
            "selectBench_10": "Quantum Fourier Transformation (QFT)",
            "minQubits_10": "20",
            "maxQubits_10": "120",
            "nativeGatesLevel_10": "true",
            "mappedLevel_10": "true",
            "ibm_10": "ibm",
            "rigetti_10": "rigetti",
            "smallest_arch_10": "True",
            "biggest_arch_10": "True",
            "optlevel0_10": "0",
            "optlevel1_10": "1",
            "optlevel3_10": "3",
        },
        "11": {
            "selectBench_11": "Entangled QFT",
            "minQubits_11": "100",
            "maxQubits_11": "110",
            "indepLevel_11": "true",
            "mappedLevel_11": "true",
            "biggest_arch_11": "True",
            "optlevel2_11": "2",
        },
        "13": {
            "selectBench_13": "Quantum Phase Estimation (QPE) exact",
            "minQubits_13": "5",
            "maxQubits_13": "40",
            "algorithmLevel_13": "true",
        },
        "21": {
            "selectBench_21": "W State",
            "minQubits_21": "10",
            "maxQubits_21": "30",
            "mappedLevel_21": "true",
            "rigetti_21": "rigetti",
            "smallest_arch_21": "True",
            "optlevel0_21": "0",
            "optlevel2_21": "2",
        },
    }
    assert backend.prepareFormInput(form_data) == expected_res


def test_parseFilterCriteria():
    input_data = dict(
        {
            "3": {
                "selectBench_3": "Graph State",
                "minQubits_3": "5",
                "maxQubits_3": "20",
                "nativeGatesLevel_3": "true",
                "ibm_3": "ibm",
                "optlevel1_3": "1",
                "optlevel3_3": "3",
            },
            "4": {
                "selectBench_4": "GHZ State",
                "minQubits_4": "5",
                "maxQubits_4": "10",
                "indepLevel_4": "true",
            },
            "10": {
                "selectBench_10": "Quantum Fourier Transformation (QFT)",
                "minQubits_10": "20",
                "maxQubits_10": "120",
                "nativeGatesLevel_10": "true",
                "mappedLevel_10": "true",
                "ibm_10": "ibm",
                "rigetti_10": "rigetti",
                "smallest_arch_10": "True",
                "biggest_arch_10": "True",
                "optlevel0_10": "0",
                "optlevel1_10": "1",
                "optlevel3_10": "3",
            },
            "11": {
                "selectBench_11": "Entangled QFT",
                "minQubits_11": "100",
                "maxQubits_11": "110",
                "indepLevel_11": "true",
                "mappedLevel_11": "true",
                "biggest_arch_11": "True",
                "optlevel2_11": "2",
            },
            "13": {
                "selectBench_13": "Quantum Phase Estimation (QPE) exact",
                "minQubits_13": "5",
                "maxQubits_13": "40",
                "algorithmLevel_13": "true",
            },
            "21": {
                "selectBench_21": "W State",
                "minQubits_21": "10",
                "maxQubits_21": "30",
                "mappedLevel_21": "true",
                "rigetti_21": "rigetti",
                "smallest_arch_21": "True",
                "optlevel0_21": "0",
                "optlevel2_21": "2",
            },
            "29": {
                "selectBench_29": "Travelling Salesman",
                "minQubits_29": "-1",
                "maxQubits_29": "-1",
                "indepLevel_29": "true",
            },
        }
    )
    expected_filter_criteria = [
        [
            "graphstate",
            "5",
            "20",
            True,
            False,
            False,
            False,
            True,
            False,
            False,
            False,
            [1, 3],
        ],
        ["ghz", "5", "10", False, False, False, True, False, False, False, False, []],
        [
            "qft",
            "20",
            "120",
            True,
            True,
            False,
            False,
            True,
            True,
            True,
            True,
            [0, 1, 3],
        ],
        [
            "qftentangled",
            "100",
            "110",
            False,
            False,
            False,
            True,
            False,
            True,
            False,
            True,
            [2],
        ],
        [
            "qpeexact",
            "5",
            "40",
            False,
            False,
            True,
            False,
            False,
            False,
            False,
            False,
            [],
        ],
        [
            "wstate",
            "10",
            "30",
            False,
            True,
            False,
            False,
            False,
            True,
            True,
            False,
            [0, 2],
        ],
        [
            "tsp",
            "-1",
            "-1",
            False,
            False,
            False,
            True,
            False,
            False,
            False,
            False,
            [],
        ],
    ]
    expected_python_files_list = ["./static/files/algo_level.txt"]

    assert backend.parseFilterCriteria(input_data) == (
        expected_filter_criteria,
        expected_python_files_list,
    )


def test_create_database():
    test_path = r"./benchviewer/static/files/test_output"
    import os

    cwd = os.getcwd()
    print(cwd)
    database = backend.createDatabase(test_path)
    assert len(database) == 30
    backend.database = database

    input_data = dict(
        {
            "4": {
                "selectBench_4": "GHZ State",
                "minQubits_4": "5",
                "maxQubits_4": "7",
                "indepLevel_4": "true",
            }
        }
    )
    res = backend.get_selected_file_paths(input_data)
    print(res)
    assert len(res[0]) == 1
    assert res[0][0] == test_path + "/" + "ghz_t-indep_5.qasm"

    input_data = dict(
        {
            "3": {
                "selectBench_3": "Graph State",
                "minQubits_3": "99",
                "maxQubits_3": "106",
                "nativeGatesLevel_3": "true",
                "ibm_3": "ibm",
                "optlevel1_3": "1",
                "optlevel2_3": "2",
            }
        }
    )
    res = backend.get_selected_file_paths(input_data)
    assert len(res[0]) == 2

    input_data = dict(
        {
            "3": {
                "selectBench_3": "Graph State",
                "minQubits_3": "99",
                "maxQubits_3": "106",
                "nativeGatesLevel_3": "true",
                "ibm_3": "ibm",
                "optlevel1_3": "1",
            }
        }
    )
    res = backend.get_selected_file_paths(input_data)
    assert len(res[0]) == 0

    input_data = dict(
        {
            "3": {
                "selectBench_3": "Graph State",
                "optlevel2_3": "2",
            }
        }
    )
    res = backend.get_selected_file_paths(input_data)
    assert res == (False, False, False)

    input_data = dict(
        {
            "10": {
                "selectBench_10": "Quantum Fourier Transformation (QFT)",
                "minQubits_10": "5",
                "maxQubits_10": "6",
                "mappedLevel_10": "true",
                "rigetti_10": "rigetti",
                "optlevel1_10": "1",
                "biggest_arch_10": "True",
            }
        }
    )
    res = backend.get_selected_file_paths(input_data)
    assert len(res[0]) == 1

    input_data = dict(
        {
            "10": {
                "selectBench_10": "Quantum Fourier Transformation (QFT)",
                "minQubits_10": "5",
                "maxQubits_10": "6",
                "mappedLevel_10": "true",
                "rigetti_10": "rigetti",
                "optlevel1_10": "1",
                "smallest_arch_10": "True",
                "biggest_arch_10": "True",
            }
        }
    )
    res = backend.get_selected_file_paths(input_data)
    assert len(res[0]) == 2

    input_data = dict(
        {
            "10": {
                "selectBench_10": "Quantum Fourier Transformation (QFT)",
                "minQubits_10": "5",
                "maxQubits_10": "6",
                "mappedLevel_10": "true",
                "ibm_10": "ibm",
                "rigetti_10": "rigetti",
                "optlevel1_10": "1",
                "smallest_arch_10": "True",
                "biggest_arch_10": "True",
            }
        }
    )
    res = backend.get_selected_file_paths(input_data)
    assert len(res[0]) == 4

    input_data = dict(
        {
            "10": {
                "selectBench_10": "Quantum Fourier Transformation (QFT)",
                "minQubits_10": "5",
                "maxQubits_10": "8",
                "nativeGatesLevel_10": "true",
                "mappedLevel_10": "true",
                "ibm_10": "ibm",
                "rigetti_10": "rigetti",
                "optlevel1_10": "1",
                "smallest_arch_10": "True",
                "biggest_arch_10": "True",
            }
        }
    )
    res = backend.get_selected_file_paths(input_data)
    assert len(res[0]) == 12

    input_data = dict(
        {
            "21": {
                "selectBench_21": "W State",
                "minQubits_21": "5",
                "maxQubits_21": "10",
                "mappedLevel_21": "true",
                "rigetti_21": "rigetti",
                "smallest_arch_21": "True",
                "optlevel0_21": "0",
            },
            "10": {
                "selectBench_10": "Quantum Fourier Transformation (QFT)",
                "minQubits_10": "5",
                "maxQubits_10": "8",
                "nativeGatesLevel_10": "true",
                "mappedLevel_10": "true",
                "ibm_10": "ibm",
                "rigetti_10": "rigetti",
                "optlevel1_10": "1",
                "smallest_arch_10": "True",
                "biggest_arch_10": "True",
            },
        }
    )
    res = backend.get_selected_file_paths(input_data)
    assert len(res[0]) == 14
