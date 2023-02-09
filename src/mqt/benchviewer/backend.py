from __future__ import annotations

import io
import os
import re
import sys
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

import pandas as pd
import requests
from packaging import version
from tqdm import tqdm

if sys.version_info < (3, 10, 0):
    import importlib_metadata as metadata
else:
    from importlib import metadata

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Iterable


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
database: pd.DataFrame | None = None
MQTBENCH_ALL_ZIP: ZipFile | None = None


def get_opt_level(filename: str):
    """Extracts the optimization level based on a filename.

    Keyword arguments:
    filename -- filename of a benchmark

    Return values:
    num -- optimization level
    """

    pat = re.compile(r"opt\d")
    m = pat.search(filename)
    num = m.group()[-1:] if m else -1
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
    num = m.group()[0:-1] if m else -1
    return int(num)


def create_database(zip_file: ZipFile):
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


def handle_github_api_request(repo_url: str) -> requests.Response:
    # If the environment variable GITHUB_TOKEN is set, use it to authenticate to the GitHub API
    # to increase the rate limit from 60 to 5000 requests per hour per IP address.
    headers = None
    if "GITHUB_TOKEN" in os.environ:
        headers = {"Authorization": f"token {os.environ['GITHUB_TOKEN']}"}

    response = requests.get(f"https://api.github.com/repos/cda-tum/mqtbench/{repo_url}", headers=headers)
    success_code = 200
    if response.status_code == success_code:
        return response

    msg = (
        f"Request to GitHub API failed with status code {response.status_code}!\n"
        f"One reasons could be that the limit of 60 API calls per hour and IP address is exceeded.\n"
        f"If you want to increase the limit, set the environment variable GITHUB_TOKEN to a GitHub personal access token.\n"
        f"See https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token for more information."
    )
    raise RuntimeError(msg)


def read_mqtbench_all_zip(  # noqa: PLR0912
    skip_question: bool = False,
    target_location: str = None,
):
    huge_zip_path = Path(target_location) / "MQTBench_all.zip"

    try:
        mqtbench_module_version = metadata.version("mqt.bench")
    except Exception:
        print("'mqt.bench' is most likely not installed. Please run 'pip install . or pip install mqt.bench'.")
        return False

    print("Searching for local benchmarks...")
    if huge_zip_path.is_file() and len(ZipFile(huge_zip_path, "r").namelist()) != 0:
        print("... found.")
    else:
        print("No benchmarks found. Querying GitHub...")

        version_found = False
        available_versions = []
        for elem in handle_github_api_request("tags").json():
            available_versions.append(elem["name"])

        for possible_version in available_versions:
            if version.parse(mqtbench_module_version) >= version.parse(possible_version):
                response_json = handle_github_api_request(f"releases/tags/{possible_version}").json()
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
                            response = input("Would you like to downloaded the file? (Y/n)")
                        if skip_question or response.lower() == "y" or response == "":
                            handle_downloading_benchmarks(target_location, download_url)
                            break
            if version_found:
                break

        if not version_found:
            print("No suitable benchmarks found.")
            return False

    global MQTBENCH_ALL_ZIP
    with huge_zip_path.open("rb") as zf:
        zip_bytes = io.BytesIO(zf.read())
        MQTBENCH_ALL_ZIP = ZipFile(zip_bytes, mode="r")
    return True


def handle_downloading_benchmarks(target_location: str, download_url: str):
    print("Start downloading benchmarks...")

    r = requests.get(download_url)
    total_length = r.headers.get("content-length")
    total_length = int(total_length)
    fname = target_location + "/MQTBench_all.zip"

    Path(target_location).mkdir(parents=True, exist_ok=True)
    with Path(fname).open("wb") as f, tqdm(
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
    if "graph" in filename:
        return "graph"
    return None


def get_gate_set(filename: str):
    if "oqc" in filename:
        return "oqc"
    if "ionq" in filename:
        return "ionq"
    if "ibm" in filename:
        return "ibm"
    if "rigetti" in filename:
        return "rigetti"
    raise ValueError("Unknown gate set: " + filename)


def get_target_device(filename: str):
    if "ibm_washington" in filename:
        return "ibm_washington"
    if "ibm_montreal" in filename:
        return "ibm_montreal"
    if "rigetti_aspen" in filename:
        return "rigetti_aspen"
    if "ionq11" in filename:
        return "ionq11"
    if "oqc_lucy" in filename:
        return "oqc_lucy"
    raise ValueError("Unknown target device: " + filename)


def get_compiler_and_settings(filename: str):
    if "qiskit" in filename:
        return "qiskit", get_opt_level(filename)
    if "tket" in filename:
        return "tket", get_tket_settings(filename)
    raise ValueError("Unknown compiler: " + filename)


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
    gate_set = get_gate_set(filename) if nativegates_flag or mapped_flag else None
    target_device = get_target_device(filename) if mapped_flag else None

    return [
        benchmark,
        num_qubits,
        indep_flag,
        nativegates_flag,
        mapped_flag,
        compiler,
        compiler_settings,
        gate_set,
        target_device,
        filename,
    ]


def filter_database(filter_criteria: tuple, database: pd.DataFrame):  # noqa: PLR0912
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
    db_filtered["indep_flag"] = db_filtered["indep_flag"].astype(bool)
    db_filtered["nativegates_flag"] = db_filtered["nativegates_flag"].astype(bool)
    db_filtered["mapped_flag"] = db_filtered["mapped_flag"].astype(bool)
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
    ) = filter_criteria

    selected_scalable_benchmarks = []
    selected_nonscalable_benchmarks = []

    for identifier in indices_benchmarks:
        if 0 < int(identifier) <= len(benchmarks):
            name = benchmarks[int(identifier) - 1]["filename"]
            selected_scalable_benchmarks.append(name)

        elif 0 < int(identifier) <= len(benchmarks) + len(nonscalable_benchmarks):
            name = nonscalable_benchmarks[int(identifier) - 1 - len(benchmarks)]["filename"]
            selected_nonscalable_benchmarks.append(name)

    db_tmp = database.loc[
        (
            (database["num_qubits"] >= min_qubits)
            & (database["num_qubits"] <= max_qubits)
            & (database["benchmark"].isin(selected_scalable_benchmarks))
        )
        | (database["benchmark"].isin(selected_nonscalable_benchmarks))
    ]

    if indep_qiskit_compiler:
        db_tmp1 = db_tmp.loc[(db_tmp["indep_flag"]) & (db_tmp["compiler"] == "qiskit")]
        db_filtered = pd.concat([db_filtered, db_tmp1])

    if indep_tket_compiler:
        db_tmp2 = db_tmp.loc[(db_tmp["indep_flag"]) & (db_tmp["compiler"] == "tket")]
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
                (db_tmp["nativegates_flag"]) & (db_tmp["gate_set"] == gate_set) & (db_tmp["compiler"] == "tket")
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
    fileobj = NoSeekBytesIO(io.BytesIO())

    paths = [Path(name) for name in filenames]
    with ZipFile(fileobj, mode="w") as zf:
        for individual_file in paths:
            zf.writestr(
                individual_file.name,
                data=MQTBENCH_ALL_ZIP.read(individual_file.name),
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
        return filter_database(prepared_data, database)
    return False


def init_database():
    """Generates the database and saves it into a global variable."""
    global database

    assert MQTBENCH_ALL_ZIP is not None

    print("Initiating database...")
    database = create_database(MQTBENCH_ALL_ZIP)
    print(f"... done: {len(database)} benchmarks.")

    if not database.empty:
        return True

    print("Database initialization failed.")
    return False


def prepare_form_input(form_data: dict):  # noqa: PLR0912, PLR0915
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
    for k, v in form_data.items():
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
        if "device_rigetti_aspen" in k:
            mapped_devices.append("rigetti_aspen")
        if "device_oqc_lucy" in k:
            mapped_devices.append("oqc_lucy")
        if "device_ionq_ionq11" in k:
            mapped_devices.append("ionq11")

    return (
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
