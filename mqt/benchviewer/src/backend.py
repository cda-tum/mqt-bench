from __future__ import annotations

import io
import os
import re
import sys
from pathlib import Path
from typing import Iterable
from zipfile import ZIP_DEFLATED, ZipFile

import pandas as pd
import requests
from packaging import version
from tqdm import tqdm

if sys.version_info < (3, 10, 0):
    import importlib_metadata as metadata
else:
    from importlib import metadata


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
    {"name": "Ground State", "id": "22", "filename": "groundstate"},
    {"name": "HHL", "id": "23", "filename": "hhl"},
    {"name": "Pricing Call Option", "id": "24", "filename": "pricingcall"},
    {"name": "Pricing Put Option", "id": "25", "filename": "pricingput"},
    {"name": "Routing", "id": "26", "filename": "routing"},
    {"name": "Shor's", "id": "27", "filename": "shor"},
    {"name": "Travelling Salesman", "id": "28", "filename": "tsp"},
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


def read_mqtbench_all_zip(
    skip_question: bool = False,
    target_location: str = None,
):
    global MQTBENCH_ALL_ZIP
    huge_zip_path = Path(target_location + "/MQTBench_all.zip")

    try:
        mqtbench_module_version = metadata.version("mqt.bench")
    except Exception:
        print(
            "'mqt.bench' is most likely not installed. Please run 'pip install . or pip install mqt.bench'."
        )
        return False

    print("Searching for local benchmarks...")
    if (
        os.path.isfile(huge_zip_path)
        and len(ZipFile(huge_zip_path, "r").namelist()) != 0
    ):
        print("... found.")
    else:
        print("No benchmarks found. Querying GitHub...")

        version_found = False
        response = requests.get("https://api.github.com/repos/cda-tum/mqtbench/tags")
        available_versions = []
        for elem in response.json():
            available_versions.append(elem["name"])

        for possible_version in available_versions:
            if version.parse(mqtbench_module_version) >= version.parse(
                possible_version
            ):
                url = (
                    "https://api.github.com/repos/cda-tum/mqtbench/releases/tags/"
                    + possible_version
                )

                response = requests.get(url)
                if not response:
                    print(
                        "Suitable benchmarks cannot be downloaded since the GitHub API failed. "
                        "One reasons could be that the limit of 60 API calls per hour and IP address is exceeded."
                    )
                    return False

                response_json = response.json()
                if "assets" in response_json:
                    assets = response_json["assets"]
                elif "asset" in response_json:
                    assets = [response_json["asset"]]
                else:
                    assets = []

                for asset in assets:
                    if asset["name"] == "MQTBench_all.zip":
                        version_found = True

                    if version_found:
                        download_url = asset["browser_download_url"]
                        if not skip_question:
                            file_size = round((asset["size"]) / 2**20, 2)
                            print(
                                "Found 'MQTBench_all.zip' (Version {}, Size {} MB, Link: {})".format(
                                    possible_version,
                                    file_size,
                                    download_url,
                                )
                            )
                            response = input(
                                "Would you like to downloaded the file? (Y/n)"
                            )
                        if skip_question or response.lower() == "y" or response == "":
                            handle_downloading_benchmarks(target_location, download_url)
                            break
            if version_found:
                break

        if not version_found:
            print("No suitable benchmarks found.")
            return False

    with huge_zip_path.open("rb") as zf:
        bytes = io.BytesIO(zf.read())
        MQTBENCH_ALL_ZIP = ZipFile(bytes, mode="r")
    return True


def handle_downloading_benchmarks(target_location: str, download_url: str):
    print("Start downloading benchmarks...")

    r = requests.get(download_url)
    total_length = r.headers.get("content-length")
    total_length = int(total_length)
    fname = target_location + "/MQTBench_all.zip"

    if not os.path.isdir(target_location):
        os.makedirs(target_location)

    with open(fname, "wb") as f, tqdm(
        desc=fname,
        total=total_length,
        unit="iB",
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for data in r.iter_content(chunk_size=1024):
            size = f.write(data)
            bar.update(size)
    print(f"Download completed to {fname}. Server is starting now.")


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


def filterDatabase(filterCriteria: tuple, database: pd.DataFrame):
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
                (db_tmp["indep_flag"]) & (db_tmp["compiler"] == "qiskit")
            ]
            db_filtered = pd.concat([db_filtered, db_tmp1])

        if indep_tket_compiler:
            db_tmp2 = db_tmp.loc[
                (db_tmp["indep_flag"]) & (db_tmp["compiler"] == "tket")
            ]
            db_filtered = pd.concat([db_filtered, db_tmp2])

        if nativegates_qiskit_compiler:
            for gate_set in native_gatesets:
                for opt_lvl in native_qiskit_opt_lvls:
                    db_tmp3 = db_tmp.loc[
                        (db_tmp["nativegates_flag"])
                        & (db_tmp["gate_set"] == gate_set)
                        & (db_tmp["compiler"] == "qiskit")
                        & (db_tmp["compiler_settings"] == opt_lvl)
                    ]
                    db_filtered = pd.concat([db_filtered, db_tmp3])

        if nativegates_tket_compiler:
            for gate_set in native_gatesets:
                db_tmp4 = db_tmp.loc[
                    (db_tmp["nativegates_flag"])
                    & (db_tmp["gate_set"] == gate_set)
                    & (db_tmp["compiler"] == "tket")
                ]
                db_filtered = pd.concat([db_filtered, db_tmp4])

        if mapped_qiskit_compiler:
            for opt_lvl in mapped_qiskit_opt_lvls:
                for device in mapped_devices:
                    db_tmp5 = db_tmp.loc[
                        (db_tmp["mapped_flag"])
                        & (db_tmp["target_device"] == device)
                        & (db_tmp["compiler"] == "qiskit")
                        & (db_tmp["compiler_settings"] == opt_lvl)
                    ]
                    db_filtered = pd.concat([db_filtered, db_tmp5])

        if mapped_tket_compiler:
            for placement in mapped_tket_placements:
                for device in mapped_devices:
                    db_tmp6 = db_tmp.loc[
                        (db_tmp["mapped_flag"])
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
    filenames: list[str],
) -> Iterable[bytes]:
    """Generates the zip file for the selected benchmarks and returns a generator of the chunks.

    Keyword arguments:
    paths -- list of file paths for all selected benchmarks

    Return values:
        Generator of bytes to send to the browser
    """
    global MQTBENCH_ALL_ZIP
    fileobj = NoSeekBytesIO(io.BytesIO())

    paths: list[Path] = [Path(name) for name in filenames]

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
                compresslevel=3,
            )
            fileobj.hidden_seek(0)
            yield fileobj.read()
            fileobj.truncate_and_remember_offset(0)

    fileobj.hidden_seek(0)
    yield fileobj.read()
    fileobj.close()


def get_selected_file_paths(prepared_data: tuple):
    """Extracts all file paths according to the prepared user's filter criteria.

    Keyword arguments:
    prepared_data -- user's filter criteria after preparation step

    Return values:
    file_paths -- list of filter criteria for each selected benchmark
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

    print("Initiating database...")
    database = createDatabase(MQTBENCH_ALL_ZIP)
    print(f"... done: {len(database)} benchmarks.")

    if not database.empty:
        return True
    else:
        print("Database initialization failed.")
        return False


def prepareFormInput(formData: list):
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
            if min_qubits == "":
                min_qubits = 2

        if "maxQubits" in k:
            max_qubits = v
            if max_qubits == "":
                max_qubits = 130
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
    # print("Overall Result: ", res)
    return res
