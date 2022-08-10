import pandas as pd
import os
import re
import json
import io
from zipfile import ZipFile, ZIP_DEFLATED
from pathlib import Path
from typing import List, Iterable

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
    {"name": "W-State", "id": "21", "filename": "wstate"},
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
database: pd.DataFrame = None
MQTBENCH_ALL_ZIP: ZipFile = None


def get_opt_level(filename: str):
    """Extracts the optimization level based on a filename.

    Keyword arguments:
    filename -- filename of a benchmark

    Return values:
    num -- optimization level
    """

    pat = re.compile(r"opt\d")
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

    pat = re.compile(r"(\d+)\.")
    m = pat.search(filename)
    if m:
        num = m.group()[0:-1]
    else:
        num = -1
    return int(num)


def createDatabase(zip_file: ZipFile):
    """Creates the database based on the provided directories.

    Keyword arguments:
    qasm_path -- zip containing all .qasm files

    Return values:
    database -- database containing all available benchmarks
    """
    rows_list = []
    # for filename in os.listdir(qasm_path):
    for filename in zip_file.namelist():
        if filename.endswith(".qasm"):
            parsed_data = parse_data(filename)
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


def read_mqtbench_all_zip():
    global MQTBENCH_ALL_ZIP
    huge_zip = Path("./static/files/qasm_output/MQTBench_all.zip")
    print("Reading in {} ({} bytes) ...".format(huge_zip.name, huge_zip.stat().st_size))
    with huge_zip.open("rb") as zf:
        bytes = io.BytesIO(zf.read())
        MQTBENCH_ALL_ZIP = ZipFile(bytes, mode="r")
    print("files: {}".format(len(MQTBENCH_ALL_ZIP.namelist())))


def parse_data(filename: str):
    """Extracts the necessary information from a given filename.

    Keyword arguments:
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
    path = os.path.join(filename)
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

    (
        (min_qubits, max_qubits),
        indices_benchmarks,
        (indep_qiskit_compiler, indep_tket_compiler),
        (
            (nativegates_qiskit_compiler, nativegates_tket_compiler),
            native_qiskit_opt_lvls,
            native_gatesets,
        ),
        (
            (mapped_qiskit_compiler, mapped_tket_compiler),
            (mapped_qiskit_opt_lvls, mapped_tket_placements),
            mapped_devices,
        ),
    ) = filterCriteria

    db_tmp = database.loc[
        (database["num_qubits"] >= min_qubits)
        & (database["num_qubits"] <= max_qubits)
        ]

    if indep_qiskit_compiler:
        #db_filtered = pd.concat([db_filtered, dbxyz])
    if indep_tket_compiler:
        #db_filtered = pd.concat([db_filtered, dbxyz])

    if nativegates_qiskit_compiler:
        #consider
        #native_qiskit_opt_lvls,
        #native_gatesets,

    if nativegates_tket_compiler:

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


class NoSeekBytesIO:
    def __init__(self, fp: io.BytesIO):
        self.fp = fp
        self.deleted_offset = 0

    def write(self, b):
        return self.fp.write(b)

    def tell(self):
        return self.deleted_offset + self.fp.tell()

    def hidden_tell(self):
        return self.fp.tell()

    def seekable(self):
        return False

    def hidden_seek(self, offset, start_point=io.SEEK_SET):
        return self.fp.seek(offset, start_point)

    def truncate_and_remember_offset(self, size):
        self.deleted_offset += self.fp.tell()
        self.fp.seek(0)
        return self.fp.truncate(size)

    def get_value(self):
        return self.fp.getvalue()

    def close(self):
        return self.fp.close()

    def read(self):
        return self.fp.read()

    def flush(self):
        return self.fp.flush()


def generate_zip_ephemeral_chunks(
    filenames: List[str], python_files_list: bool = False
) -> Iterable[bytes]:
    """Generates the zip file for the selected benchmarks and returns a generator of the chunks.

    Keyword arguments:
    paths -- list of file paths for all selected benchmarks
    python_files_list -- list of all python files necessary to generate the benchmarks on the algorithm level

    Return values:
        Generator of bytes to send to the browser
    """
    global MQTBENCH_ALL_ZIP
    fileobj = NoSeekBytesIO(io.BytesIO())

    paths: List[Path] = [Path(name) for name in filenames]
    if python_files_list:
        paths.append(Path("./static/files/algo_level.txt"))

    with ZipFile(fileobj, mode="w") as zf:
        for individualFile in paths:
            # zf.write(
            #     individualFile,
            #     arcname=individualFile.name,
            #     compress_type=ZIP_DEFLATED,
            #     compresslevel=1
            # )
            zf.writestr(
                individualFile.name,
                data=MQTBENCH_ALL_ZIP.read(individualFile.name),
                compress_type=ZIP_DEFLATED,
                compresslevel=1,
            )
            fileobj.hidden_seek(0)
            yield fileobj.read()
            fileobj.truncate_and_remember_offset(0)

    fileobj.hidden_seek(0)
    yield fileobj.read()
    fileobj.close()


def get_selected_file_paths(prepared_data):
    """Extracts all file paths according to the prepared user's filter criteria.

    Keyword arguments:
    prepared_data -- user's filter criteria after preparation step

    Return values:
    filter_list -- list of filter criteria for each selected benchmark
    algo_dicts -- dictionary to handle the algorithm level, since that one is not available as a downloadable file
    python_files_list -- list of all python files needed to generated the algorithm level
    """

    if prepared_data:
        file_paths = filterDatabase(prepared_data, database)
        return file_paths
    else:
        return False


def init_database():
    """Generates the database and saves it into a global variable."""
    global database

    assert MQTBENCH_ALL_ZIP is not None

    print("Creating data base...")
    database = createDatabase(MQTBENCH_ALL_ZIP)
    print("rows: {}".format(len(database)))
    print("... done")


def prepareFormInput(formData):
    """Formats the formData extracted from the user's inputs."""

    min_qubits = -1
    max_qubits = -1
    indep_qiskit_compiler = False
    indep_tket_compiler = False
    nativegates_qiskit_compiler = False
    nativegates_tket_compiler = False
    native_qiskit_opt_lvls = []
    native_gatesets = []
    mapped_qiskit_compiler = False
    mapped_tket_compiler = False
    mapped_qiskit_opt_lvls = []
    mapped_tket_placements = []
    mapped_devices = []

    pat = re.compile(r"_\d+")
    num_benchmarks = []
    for k, v in formData.items():
        m = pat.search(k)
        if m:
            num = m.group()[1:]
            num_benchmarks.append(num)

        if "minQubits" in k:
            min_qubits = v
        if "maxQubits" in k:
            max_qubits = v
        if "indep_qiskit_compiler" in k:
            indep_qiskit_compiler = True
        if "indep_tket_compiler" in k:
            indep_tket_compiler = True

        if "nativegates_qiskit_compiler" in k:
            nativegates_qiskit_compiler = True
        if "nativegates_tket_compiler" in k:
            nativegates_tket_compiler = True
        if "nativegates_qiskit_compiler_opt0" in k:
            native_qiskit_opt_lvls.append(0)
        if "nativegates_qiskit_compiler_opt1" in k:
            native_qiskit_opt_lvls.append(1)
        if "nativegates_qiskit_compiler_opt2" in k:
            native_qiskit_opt_lvls.append(2)
        if "nativegates_qiskit_compiler_opt3" in k:
            native_qiskit_opt_lvls.append(3)

        if "nativegates_ibm" in k:
            native_gatesets.append("ibm")
        if "nativegates_rigetti" in k:
            native_gatesets.append("rigetti")
        if "nativegates_oqc" in k:
            native_gatesets.append("oqc")
        if "nativegates_ionq" in k:
            native_gatesets.append("ionq")

        if "mapped_qiskit_compiler" in k:
            mapped_qiskit_compiler = True
        if "mapped_tket_compiler" in k:
            mapped_tket_compiler = True
        if "mapped_qiskit_compiler_opt0" in k:
            mapped_qiskit_opt_lvls.append(0)
        if "mapped_qiskit_compiler_opt1" in k:
            mapped_qiskit_opt_lvls.append(1)
        if "mapped_qiskit_compiler_opt2" in k:
            mapped_qiskit_opt_lvls.append(2)
        if "mapped_qiskit_compiler_opt3" in k:
            mapped_qiskit_opt_lvls.append(3)

        if "mapped_tket_compiler_graph" in k:
            mapped_tket_placements.append("graph")
        if "mapped_tket_compiler_line" in k:
            mapped_tket_placements.append("line")

        if "device_ibm_montreal" in k:
            mapped_devices.append("ibm_montreal")
        if "device_ibm_washington" in k:
            mapped_devices.append("ibm_washington")
        if "device_rigetti_aspen_m1" in k:
            mapped_devices.append("rigetti_aspen_m1")
        if "device_oqc_lucy" in k:
            mapped_devices.append("oqc_lucy")
        if "device_ionq_ionq11" in k:
            mapped_devices.append("ionq11")

    print("benchmarks: ", num_benchmarks)
    print("indep compiler: ", indep_qiskit_compiler, indep_tket_compiler)
    print("native compiler: ", nativegates_qiskit_compiler, nativegates_tket_compiler)
    print("native compiler settings qiskit: ", native_qiskit_opt_lvls)
    print("native compiler gatesets: ", native_gatesets)
    print("mapped compiler: ", mapped_qiskit_compiler, mapped_tket_compiler)
    print("mapped compiler settings qiskit: ", mapped_qiskit_opt_lvls)
    print("mapped compiler settings tket: ", mapped_tket_placements)
    print("mapped devices: ", mapped_devices)

    res = (
        (min_qubits, max_qubits),
        num_benchmarks,
        (indep_qiskit_compiler, indep_tket_compiler),
        (
            (nativegates_qiskit_compiler, nativegates_tket_compiler),
            native_qiskit_opt_lvls,
            native_gatesets,
        ),
        (
            (mapped_qiskit_compiler, mapped_tket_compiler),
            (mapped_qiskit_opt_lvls, mapped_tket_placements),
            mapped_devices,
        ),
    )
    print("Overall Result: ", res)
    return res


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
