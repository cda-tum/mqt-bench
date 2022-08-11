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

    for filename in zip_file.namelist():
        if filename.endswith(".qasm"):
            parsed_data = parse_data(filename)
            rows_list.append(parsed_data)
            continue

    colnames = [
        "benchmark",
        "num_qubits",
        "indep_flag",
        "nativegates_flag",
        "mapped_flag",
        "compiler",
        "compiler_settings",
        "gate_set",
        "target_device",
        "path",
    ]

    database = pd.DataFrame(rows_list, columns=colnames)
    database["num_qubits"] = database["num_qubits"].astype(int)
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


def get_tket_settings(filename: str):
    if "line" in filename:
        return "line"
    elif "graph" in filename:
        return "graph"


def get_gate_set(filename: str):
    if "oqc" in filename:
        return "oqc"
    elif "ionq" in filename:
        return "ionq"
    elif "ibm" in filename:
        return "ibm"
    elif "rigetti" in filename:
        return "rigetti"


def get_target_device(filename: str):
    if "ibm_washington" in filename:
        return "ibm_washington"
    elif "ibm_montreal" in filename:
        return "ibm_montreal"
    elif "rigetti_aspen_m1" in filename:
        return "rigetti_aspen_m1"
    elif "ionq11" in filename:
        return "ionq11"
    elif "oqc_lucy" in filename:
        return "oqc_lucy"


def get_compiler_and_settings(filename: str):
    if "qiskit" in filename:
        return ("qiskit", get_opt_level(filename))
    elif "tket" in filename:
        return ("tket", get_tket_settings(filename))


def parse_data(filename: str):
    """Extracts the necessary information from a given filename.

    Keyword arguments:
    filename -- name of file

    Return values:
    parsed_data -- parsed data extracted from filename
    """
    benchmark = filename.split("_")[0].lower()
    num_qubits = get_num_qubits(filename)
    indep_flag = "indep" in filename
    nativegates_flag = "nativegates" in filename
    mapped_flag = "mapped" in filename
    compiler, compiler_settings = get_compiler_and_settings(filename)
    gate_set = get_gate_set(filename)
    target_device = get_target_device(filename)

    path = os.path.join(filename)
    parsed_data = [
        benchmark,
        num_qubits,
        indep_flag,
        nativegates_flag,
        mapped_flag,
        compiler,
        compiler_settings,
        gate_set,
        target_device,
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
        "indep_flag",
        "nativegates_flag",
        "mapped_flag",
        "compiler",
        "compiler_settings",
        "gate_set",
        "target_device",
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

    for identifier in indices_benchmarks:
        if int(identifier) > 0 and int(identifier) <= len(benchmarks):
            name = benchmarks[int(identifier) - 1]["filename"]

            db_tmp = database.loc[
                (database["num_qubits"] >= min_qubits)
                & (database["num_qubits"] <= max_qubits)
                & (database["benchmark"] == name)
            ]
        elif int(identifier) > 0 and int(identifier) <= len(benchmarks) + len(
            nonscalable_benchmarks
        ):
            name = nonscalable_benchmarks[int(identifier) - 1 - len(benchmarks)][
                "filename"
            ]

            db_tmp = database.loc[database["benchmark"] == name]
        else:
            print("FAIL")

        if indep_qiskit_compiler:
            db_tmp1 = db_tmp.loc[
                (db_tmp["indep_flag"] == True) & (db_tmp["compiler"] == "qiskit")
            ]
            db_filtered = pd.concat([db_filtered, db_tmp1])

        if indep_tket_compiler:
            db_tmp2 = db_tmp.loc[
                (db_tmp["indep_flag"] == True) & (db_tmp["compiler"] == "tket")
            ]
            db_filtered = pd.concat([db_filtered, db_tmp2])

        if nativegates_qiskit_compiler:
            for gate_set in native_gatesets:
                for opt_lvl in native_qiskit_opt_lvls:
                    db_tmp3 = db_tmp.loc[
                        (db_tmp["nativegates_flag"] == True)
                        & (db_tmp["gate_set"] == gate_set)
                        & (db_tmp["compiler"] == "qiskit")
                        & (db_tmp["compiler_settings"] == opt_lvl)
                    ]
                    db_filtered = pd.concat([db_filtered, db_tmp3])

        if nativegates_tket_compiler:
            for gate_set in native_gatesets:
                db_tmp4 = db_tmp.loc[
                    (db_tmp["nativegates_flag"] == True)
                    & (db_tmp["gate_set"] == gate_set)
                    & (db_tmp["compiler"] == "tket")
                ]
                db_filtered = pd.concat([db_filtered, db_tmp4])

        if mapped_qiskit_compiler:
            for opt_lvl in native_qiskit_opt_lvls:
                for device in mapped_devices:
                    db_tmp5 = db_tmp.loc[
                        (db_tmp["mapped_flag"] == True)
                        & (db_tmp["target_device"] == device)
                        & (db_tmp["compiler"] == "qiskit")
                        & (db_tmp["compiler_settings"] == opt_lvl)
                    ]
                    db_filtered = pd.concat([db_filtered, db_tmp5])

        if mapped_tket_compiler:
            for placement in mapped_tket_placements:
                for device in mapped_devices:
                    db_tmp6 = db_tmp.loc[
                        (db_tmp["mapped_flag"] == True)
                        & (db_tmp["target_device"] == device)
                        & (db_tmp["compiler"] == "tket")
                        & (db_tmp["compiler_settings"] == placement)
                    ]
                    db_filtered = pd.concat([db_filtered, db_tmp6])

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

    # print("benchmarks: ", num_benchmarks)
    # print("indep compiler: ", indep_qiskit_compiler, indep_tket_compiler)
    # print("native compiler: ", nativegates_qiskit_compiler, nativegates_tket_compiler)
    # print("native compiler settings qiskit: ", native_qiskit_opt_lvls)
    # print("native compiler gatesets: ", native_gatesets)
    # print("mapped compiler: ", mapped_qiskit_compiler, mapped_tket_compiler)
    # print("mapped compiler settings qiskit: ", mapped_qiskit_opt_lvls)
    # print("mapped compiler settings tket: ", mapped_tket_placements)
    # print("mapped devices: ", mapped_devices)

    res = (
        (int(min_qubits), int(max_qubits)),
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
