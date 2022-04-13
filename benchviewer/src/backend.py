import pandas as pd
import os
import re
import uuid
import json
from zipfile import *

# All available benchmarks shown on our webpage are defined here
benchmarks = [
    {"name": "Amplitude Estimation (AE)", "id": "1", "filename": "ae"},
    {"name": "Deutsch-Jozsa", "id": "2", "filename": "dj"},
    {"name": "Graph State", "id": "3", "filename": "graphstate"},
    {"name": "GHZ State", "id": "4", "filename": "ghz"},
    {"name": "Grover's (no ancilla)", "id": "5", "filename": "grover-noancilla"},
    {"name": "Grover's (v-chain)", "id": "6", "filename": "grover-v-chain"},
    {
        "name": "Portfolio Optimization with QAOA",
        "id": "7",
        "filename": "portfolioqaoa",
    },
    {"name": "Portfolio Optimization with VQE", "id": "8", "filename": "portfoliovqe"},
    {
        "name": "Quantum Approximation Optimization Algorithm (QAOA)",
        "id": "9",
        "filename": "qaoa",
    },
    {"name": "Quantum Fourier Transformation (QFT)", "id": "10", "filename": "qft"},
    {"name": "QFT Entangled", "id": "11", "filename": "qftentangled"},
    {"name": "Quantum Generative Adversarial Network", "id": "12", "filename": "qgan"},
    {
        "name": "Quantum Phase Estimation (QPE) exact",
        "id": "13",
        "filename": "qpeexact",
    },
    {
        "name": "Quantum Phase Estimation (QPE) inexact",
        "id": "14",
        "filename": "qpeinexact",
    },
    {"name": "Quantum Walk (no ancilla)", "id": "15", "filename": "qwalk-noancilla"},
    {"name": "Quantum Walk (v-chain)", "id": "16", "filename": "qwalk-v-chain"},
    {"name": "Variational Quantum Eigensolver (VQE)", "id": "17", "filename": "vqe"},
    {
        "name": "Efficient SU2 ansatz with Random Parameters",
        "id": "18",
        "filename": "su2random",
    },
    {
        "name": "Real Amplitudes ansatz with Random Parameters",
        "id": "19",
        "filename": "realamprandom",
    },
    {
        "name": "Two Local ansatz with Random Parameters",
        "id": "20",
        "filename": "twolocalrandom",
    },
    {"name": "W State", "id": "21", "filename": "wstate"},
]

nonscalable_benchmarks = [
    {"name": "Excited State", "id": "22", "filename": "excitedstate"},
    {"name": "Ground State", "id": "23", "filename": "groundstate"},
    {"name": "HHL", "id": "24", "filename": "hhl"},
    {"name": "Pricing Call Option", "id": "25", "filename": "pricingcall"},
    {"name": "Pricing Put Option", "id": "26", "filename": "pricingput"},
    {"name": "Routing", "id": "27", "filename": "routing"},
    {"name": "Shor's", "id": "28", "filename": "shor"},
    {"name": "Travelling Salesman", "id": "29", "filename": "tsp"},
]

# Store the pandas dataframe as the database containing all available benchmarks
database = None


def get_opt_level(filename: str):
    """Extracts the optimization level based on a filename.

    Keyword arguments:
    filename -- filename of a benchmark

    Return values:
    num -- optimization level
    """

    pat = re.compile("opt[0-9]")
    m = pat.search(filename)
    if m:
        num = m.group()[-1:]
    else:
        num = -1
    return int(num)


def get_num_qubits(filename: str):
    """Extracts the number of qubits based on a filename.

    Keyword arguments:
    filename -- filename of a benchmark

    Return values:
    num -- optimization level
    """

    pat = re.compile("(\d+)\.")
    m = pat.search(filename)
    if m:
        num = m.group()[0:-1]
    else:
        num = -1
    return int(num)


def createDatabase(qasm_path: str):
    """Creates the database based on the provided directories.

    Keyword arguments:
    qasm_path -- directory containing all .qasm files

    Return values:
    database -- database containing all available benchmarks
    """
    rows_list = []
    for filename in os.listdir(qasm_path):
        if filename.endswith(".qasm"):
            parsed_data = parse_data(qasm_path, filename)
            rows_list.append(parsed_data)
            continue

    colnames = [
        "benchmark",
        "num_qubits",
        "native_gate_set",
        "algo_layer",
        "indep_layer",
        "nativegates_layer",
        "mapped_layer",
        "smallest_mapping",
        "biggest_mapping",
        "opt_level",
        "path",
    ]

    database = pd.DataFrame(rows_list, columns=colnames)
    database["num_qubits"] = database["num_qubits"].astype(int)
    database["opt_level"] = database["opt_level"].astype(int)
    database["benchmark"] = database["benchmark"].astype(str)
    return database


def parse_data(directory: str, filename: str):
    """Extracts the optimization level based on a filename.

    Keyword arguments:
    directory -- location of file
    filename -- name of file

    Return values:
    parsed_data -- parsed data extracted from filename
    """
    benchmark = filename.split("_")[0].lower()
    num_qubits = get_num_qubits(filename)
    algorithm_flag = "algorithm" in filename
    indep_flag = "indep" in filename
    nativegates_flag = "nativegates" in filename
    mapped_flag = "mapped" in filename
    smallest_mapping = False
    biggest_mapping = False
    opt_level = get_opt_level(filename)
    path = os.path.join(directory, filename)
    gate_set = False
    if "ibm" in filename:
        gate_set = "ibm"
    elif "rigetti" in filename:
        gate_set = "rigetti"
    if "ibm-s" in filename or "rigetti-s" in filename:
        smallest_mapping = True
    elif "ibm-b" in filename or "rigetti-b" in filename:
        biggest_mapping = True
    parsed_data = [
        benchmark,
        num_qubits,
        gate_set,
        algorithm_flag,
        indep_flag,
        nativegates_flag,
        mapped_flag,
        smallest_mapping,
        biggest_mapping,
        opt_level,
        path,
    ]
    return parsed_data


def parseFilterCriteria(input_data):
    """Reformats the input_data such that it is easier to filter the database.

    Keyword arguments:
    input_data -- dictionaries of all selected benchmarks

    Return values:
    filter_list -- list of filter criteria for each selected benchmark
    algo_dicts -- dictionary to handle the algorithm level, since that one is not available as a downloadable file
    list(set(python_files_list)) -- list of all python files needed to generated the algorithm level
    """
    algo_dicts = []
    python_files_list = []

    filter_list = []
    for key, value in input_data.items():
        if "selectBench_" + str(key) not in value.keys():
            continue
        min_qubits = -1
        max_qubits = -1
        algorithm_flag = False
        indep_flag = False
        nativegates_flag = False
        mapped_flag = False
        smallest_mapping = False
        biggest_mapping = False
        gate_set_ibm = False
        gate_set_rigetti = False
        opt_levels = []
        if int(key) > 0 and int(key) <= len(benchmarks):
            name = benchmarks[int(key) - 1]["filename"]
        elif int(key) > 0 and int(key) <= len(benchmarks) + len(nonscalable_benchmarks):
            name = nonscalable_benchmarks[int(key) - 1 - len(benchmarks)]["filename"]
        for key, value in value.items():
            if "minQubits" in key:
                min_qubits = value
            if "maxQubits" in key:
                max_qubits = value
            if "algorithmLevel" in key and value:
                algorithm_flag = True
            if "indepLevel" in key and value:
                indep_flag = True
            elif "nativeGatesLevel" in key and value:
                nativegates_flag = True
            elif "mappedLevel" in key and value:
                mapped_flag = True

            if "ibm" in key:
                gate_set_ibm = True
            if "rigetti" in key:
                gate_set_rigetti = True
            if "optlevel0" in key:
                opt_levels.append(0)
            if "optlevel1" in key:
                opt_levels.append(1)
            if "optlevel2" in key:
                opt_levels.append(2)
            if "optlevel3" in key:
                opt_levels.append(3)
            if "smallest_arch" in key:
                smallest_mapping = True
            if "biggest_arch" in key:
                biggest_mapping = True

        if sum([algorithm_flag, indep_flag, nativegates_flag, mapped_flag]) == 0:
            continue

        filter_list.append(
            [
                name,
                min_qubits,
                max_qubits,
                gate_set_ibm,
                gate_set_rigetti,
                algorithm_flag,
                indep_flag,
                nativegates_flag,
                mapped_flag,
                smallest_mapping,
                biggest_mapping,
                opt_levels,
            ]
        )

        if algorithm_flag:
            if min_qubits != -1 and max_qubits != -1:
                tmp_dict = {
                    "name": name,
                    "min_qubits": min_qubits,
                    "max_qubits": max_qubits,
                }
            else:
                config_file_path = "../config.json"
                with open(config_file_path, "r") as jsonfile:
                    cfg = json.load(jsonfile)
                for benchmark_config in cfg["benchmarks"]:
                    if name == benchmark_config["name"]:
                        tmp_dict = benchmark_config
                        del tmp_dict["include"]
                        break

            algo_dicts.append(tmp_dict)
            # python_files_list.append(name.split("-")[0])
            python_files_list.append("./static/files/algo_level.txt")

    return filter_list, algo_dicts, list(set(python_files_list))


def filterDatabase(filterCriteria, database):
    """Filters the database according to the filter criteria.

    Keyword arguments:
    filterCriteria -- list of all filter criteria
    database -- database containing all available benchmarks

    Return values:
    db_filtered["path"].to_list() -- list of all file paths of the selected benchmark files
    """
    colnames = [
        "benchmark",
        "num_qubits",
        "native_gate_set",
        "algo_layer",
        "indep_layer",
        "nativegates_layer",
        "mapped_layer",
        "smallest_mapping",
        "biggest_mapping",
        "opt_level",
        "path",
    ]
    db_filtered = pd.DataFrame(columns=colnames)
    if len(database) == 0:
        return []
    # for each line of input (benchmark)
    for line in filterCriteria:
        benchmark = line[0]
        min_qubits = int(line[1])
        max_qubits = int(line[2])
        gate_set_ibm = line[3]
        gate_set_rigetti = line[4]
        indep_flag = line[6]
        nativegates_flag = line[7]
        mapped_flag = line[8]
        smallest_mapping = line[9]
        biggest_mapping = line[10]
        opt_levels = line[11]

        # filter for benchmark name
        db1 = database.loc[(database["benchmark"] == benchmark)]

        # filter for qubit range and stepsize (prob. set of relevant numbers and then filter)
        if min_qubits != -1 and max_qubits != -1:
            db2 = db1.loc[
                (database["num_qubits"] >= min_qubits)
                & (database["num_qubits"] <= max_qubits)
            ]
        else:
            db2 = db1
        # Algo Layer
        # if (algo_flag):
        # db3 = db2.loc[(database["algo_layer"])]
        # db_filtered = pd.concat([db_filtered, db3])
        # T-indep layer
        if indep_flag:
            db4 = db2.loc[(database["indep_layer"])]
            # db4_tmp = db2.loc[(database["indep_layer"])]
            # db4_total = pd.DataFrame(columns=colnames)
            # for opt_level in opt_levels:
            #    db_tmp = db4_tmp.loc[(db4_tmp["opt_level"] == opt_level)]
            #    db4_total = pd.concat([db4_total, db_tmp])
            db_filtered = pd.concat([db_filtered, db4])
        # Native Gates
        if nativegates_flag:
            db5_tmp = db2.loc[(database["nativegates_layer"])]
            db5_total = pd.DataFrame(columns=colnames)
            for opt_level in opt_levels:
                if gate_set_ibm:  # IBM
                    db_tmp = db5_tmp.loc[
                        (db5_tmp["native_gate_set"] == "ibm")
                        & ((db5_tmp["opt_level"] == opt_level))
                    ]
                    db5_total = pd.concat([db5_total, db_tmp])
                if gate_set_rigetti:  # Rigetti
                    db_tmp = db5_tmp.loc[
                        (db5_tmp["native_gate_set"] == "rigetti")
                        & ((db5_tmp["opt_level"] == opt_level))
                    ]
                    db5_total = pd.concat([db5_total, db_tmp])
            db_filtered = pd.concat([db_filtered, db5_total])
        # Mapped Layer
        if mapped_flag:

            db6_total = pd.DataFrame(columns=colnames)
            for opt_level in opt_levels:
                if gate_set_ibm:  # IBM
                    if smallest_mapping:
                        db6_tmp = db2.loc[
                            (database["mapped_layer"])
                            & (database["smallest_mapping"] == True)
                        ]
                        db_tmp = db6_tmp.loc[
                            (db6_tmp["native_gate_set"] == "ibm")
                            & ((db6_tmp["opt_level"] == opt_level))
                        ]
                        db6_total = pd.concat([db6_total, db_tmp])
                    if biggest_mapping:
                        db6_tmp = db2.loc[
                            (database["mapped_layer"])
                            & (database["biggest_mapping"] == True)
                        ]
                        db_tmp = db6_tmp.loc[
                            (db6_tmp["native_gate_set"] == "ibm")
                            & ((db6_tmp["opt_level"] == opt_level))
                        ]
                        db6_total = pd.concat([db6_total, db_tmp])
                if gate_set_rigetti:  # Rigetti
                    if smallest_mapping:
                        db6_tmp = db2.loc[
                            (database["mapped_layer"])
                            & (database["smallest_mapping"] == True)
                        ]
                        db_tmp = db6_tmp.loc[
                            (db6_tmp["native_gate_set"] == "rigetti")
                            & ((db6_tmp["opt_level"] == opt_level))
                        ]
                        db6_total = pd.concat([db6_total, db_tmp])
                    if biggest_mapping:
                        db6_tmp = db2.loc[
                            (database["mapped_layer"])
                            & (database["biggest_mapping"] == True)
                        ]
                        db_tmp = db6_tmp.loc[
                            (db6_tmp["native_gate_set"] == "rigetti")
                            & ((db6_tmp["opt_level"] == opt_level))
                        ]
                        db6_total = pd.concat([db6_total, db_tmp])

            db_filtered = pd.concat([db_filtered, db6_total])
    return db_filtered["path"].to_list()


def generate_zip(paths: list, python_files_list=None):
    """Generates the zip file for the selected benchmarks.

    Keyword arguments:
    paths -- list of file paths for all selected benchmarks
    python_files_list -- list of all python files necessary to generate the benchmarks on the algorithm level

    Return values:
    directory -- directory path to temporary zip files
    filename -- zip file name
    """

    filename = str(uuid.uuid4()) + ".zip"

    with ZipFile("./static/files/zip_tmp/" + filename, "w") as zf:
        for individualFile in paths:
            zf.write(
                individualFile,
                arcname=individualFile.split("/")[-1],
                compress_type=ZIP_DEFLATED,
            )
        if python_files_list:
            zf.write(
                "./static/files/algo_level.txt",
                compress_type=ZIP_DEFLATED,
                arcname="algo_level.txt",
            )

        directory = "./static/files/zip_tmp/"
        return directory, filename


def get_selected_file_paths(prepared_data):
    """Extracts all file paths according to the prepared user's filter criteria.

    Keyword arguments:
    prepared_data -- user's filter criteria after preparation step

    Return values:
    filter_list -- list of filter criteria for each selected benchmark
    algo_dicts -- dictionary to handle the algorithm level, since that one is not available as a downloadable file
    python_files_list -- list of all python files needed to generated the algorithm level
    """
    filter_criteria, algo_dicts, python_files_list = parseFilterCriteria(prepared_data)
    if filter_criteria:
        file_paths = filterDatabase(filter_criteria, database)
        return file_paths, algo_dicts, python_files_list
    else:
        return False, False, False


def init_database():
    """Generates the database and saves it into a global variable."""
    qasm_path = r"./static/files/qasm_output"

    global database
    database = createDatabase(qasm_path)

    # add_min_max_qubit_number(database)


def prepareFormInput(formData):
    """Formats the formData extracted from the user's inputs such that each benchmark is stored in one dictionary.

    Keyword arguments:
    formData -- unformatted user's filter criterias

    Return values:
    sub_dicts -- dictionary of dictionaries representing the user's filter criteria
    """
    # Path form data into several dictionaries, one for each benchmark
    pat = re.compile(r"_\d+")
    sub_dicts = {}
    for k, v in formData.items():
        m = pat.search(k)
        if m:
            num = m.group()[1:]
            sub_dicts.setdefault(num, {})[k] = v
    if "0" in sub_dicts:
        del sub_dicts["0"]
    return sub_dicts


def add_min_max_qubit_number(database):
    for benchmark in benchmarks:
        max_val = database[database["benchmark"] == benchmark["filename"]][
            "num_qubits"
        ].max()
        benchmark["max_qubits"] = int(max_val)

        min_val = database[database["benchmark"] == benchmark["filename"]][
            "num_qubits"
        ].min()
        benchmark["min_qubits"] = int(min_val)
