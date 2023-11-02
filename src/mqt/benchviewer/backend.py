from __future__ import annotations

import io
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, cast
from zipfile import ZIP_DEFLATED, ZipFile

import pandas as pd
import requests
from packaging import version
from tqdm import tqdm

if TYPE_CHECKING or sys.version_info >= (3, 10, 0):  # pragma: no cover
    from importlib import metadata
else:
    import importlib_metadata as metadata


if TYPE_CHECKING:  # pragma: no cover
    from collections.abc import Iterable


@dataclass
class BenchmarkConfiguration:
    min_qubits: int
    max_qubits: int
    indices_benchmarks: list[int]
    indep_qiskit_compiler: bool
    indep_tket_compiler: bool
    nativegates_qiskit_compiler: bool
    nativegates_tket_compiler: bool
    mapped_qiskit_compiler: bool
    mapped_tket_compiler: bool
    native_qiskit_opt_lvls: list[int] | None = None
    native_gatesets: list[str] | None = None
    mapped_qiskit_opt_lvls: list[int] | None = None
    mapped_tket_placements: list[str] | None = None
    mapped_devices: list[str] | None = None


@dataclass
class ParsedBenchmarkName:
    benchmark: str
    num_qubits: int
    indep_flag: bool
    nativegates_flag: bool
    mapped_flag: bool
    compiler: str | int
    compiler_settings: str | int | None
    gate_set: str | None
    target_device: str | None
    filename: str


class Backend:
    def __init__(self) -> None:
        self.benchmarks = [
            {"name": "Amplitude Estimation (AE)", "id": "1", "filename": "ae"},
            {"name": "Deutsch-Jozsa", "id": "2", "filename": "dj"},
            {"name": "Graph State", "id": "3", "filename": "graphstate"},
            {"name": "GHZ State", "id": "4", "filename": "ghz"},
            {
                "name": "Grover's (no ancilla)",
                "id": "5",
                "filename": "grover-noancilla",
            },
            {"name": "Grover's (v-chain)", "id": "6", "filename": "grover-v-chain"},
            {
                "name": "Portfolio Optimization with QAOA",
                "id": "7",
                "filename": "portfolioqaoa",
            },
            {
                "name": "Portfolio Optimization with VQE",
                "id": "8",
                "filename": "portfoliovqe",
            },
            {
                "name": "Quantum Approximation Optimization Algorithm (QAOA)",
                "id": "9",
                "filename": "qaoa",
            },
            {
                "name": "Quantum Fourier Transformation (QFT)",
                "id": "10",
                "filename": "qft",
            },
            {"name": "QFT Entangled", "id": "11", "filename": "qftentangled"},
            {"name": "Quantum Neural Network (QNN)", "id": "12", "filename": "qnn"},
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
            {
                "name": "Quantum Walk (no ancilla)",
                "id": "15",
                "filename": "qwalk-noancilla",
            },
            {"name": "Quantum Walk (v-chain)", "id": "16", "filename": "qwalk-v-chain"},
            {"name": "Random Circuit", "id": "17", "filename": "random"},
            {
                "name": "Variational Quantum Eigensolver (VQE)",
                "id": "18",
                "filename": "vqe",
            },
            {
                "name": "Efficient SU2 ansatz with Random Parameters",
                "id": "19",
                "filename": "su2random",
            },
            {
                "name": "Real Amplitudes ansatz with Random Parameters",
                "id": "20",
                "filename": "realamprandom",
            },
            {
                "name": "Two Local ansatz with Random Parameters",
                "id": "21",
                "filename": "twolocalrandom",
            },
            {"name": "W-State", "id": "22", "filename": "wstate"},
        ]

        self.nonscalable_benchmarks = [
            {"name": "Ground State", "id": "23", "filename": "groundstate"},
            {"name": "Pricing Call Option", "id": "24", "filename": "pricingcall"},
            {"name": "Pricing Put Option", "id": "25", "filename": "pricingput"},
            {"name": "Routing", "id": "26", "filename": "routing"},
            {"name": "Shor's", "id": "27", "filename": "shor"},
            {"name": "Travelling Salesman", "id": "28", "filename": "tsp"},
        ]

        self.database: pd.DataFrame | None = None
        self.mqtbench_all_zip: ZipFile | None = None

    def filter_database(self, benchmark_config: BenchmarkConfiguration) -> list[str]:
        """Filters the database according to the filter criteria.

        Keyword arguments:
        filterCriteria -- list of all filter criteria
        database -- database containing all available benchmarks


        Return values:
        db_filtered["path"].to_list() -- list of all file paths of the selected benchmark files
        """
        colnames = list(ParsedBenchmarkName.__annotations__.keys())
        db_filtered = pd.DataFrame(columns=colnames)
        db_filtered["indep_flag"] = db_filtered["indep_flag"].astype(bool)
        db_filtered["nativegates_flag"] = db_filtered["nativegates_flag"].astype(bool)
        db_filtered["mapped_flag"] = db_filtered["mapped_flag"].astype(bool)
        if self.database is None or self.database.empty:
            return []

        selected_scalable_benchmarks = []
        selected_nonscalable_benchmarks = []

        for identifier in benchmark_config.indices_benchmarks:
            if 0 < identifier <= len(self.benchmarks):
                name = self.benchmarks[identifier - 1]["filename"]
                selected_scalable_benchmarks.append(name)

            elif 0 < identifier <= len(self.benchmarks) + len(self.nonscalable_benchmarks):
                name = self.nonscalable_benchmarks[identifier - 1 - len(self.benchmarks)]["filename"]
                selected_nonscalable_benchmarks.append(name)

        db_tmp = self.database.loc[
            (
                (self.database["num_qubits"] >= benchmark_config.min_qubits)
                & (self.database["num_qubits"] <= benchmark_config.max_qubits)
                & (self.database["benchmark"].isin(selected_scalable_benchmarks))
            )
            | (self.database["benchmark"].isin(selected_nonscalable_benchmarks))
        ]

        if benchmark_config.indep_qiskit_compiler:
            db_tmp1 = db_tmp.loc[(db_tmp["indep_flag"]) & (db_tmp["compiler"] == "qiskit")]
            db_filtered = pd.concat([db_filtered, db_tmp1])

        if benchmark_config.indep_tket_compiler:
            db_tmp2 = db_tmp.loc[(db_tmp["indep_flag"]) & (db_tmp["compiler"] == "tket")]
            db_filtered = pd.concat([db_filtered, db_tmp2])

        if (
            benchmark_config.nativegates_qiskit_compiler
            and benchmark_config.native_gatesets
            and benchmark_config.native_qiskit_opt_lvls
        ):
            for gate_set in benchmark_config.native_gatesets:
                for opt_lvl in benchmark_config.native_qiskit_opt_lvls:
                    db_tmp3 = db_tmp.loc[
                        (db_tmp["nativegates_flag"])
                        & (db_tmp["gate_set"] == gate_set)
                        & (db_tmp["compiler"] == "qiskit")
                        & (db_tmp["compiler_settings"] == opt_lvl)
                    ]
                    db_filtered = pd.concat([db_filtered, db_tmp3])

        if benchmark_config.nativegates_tket_compiler and benchmark_config.native_gatesets:
            for gate_set in benchmark_config.native_gatesets:
                db_tmp4 = db_tmp.loc[
                    (db_tmp["nativegates_flag"]) & (db_tmp["gate_set"] == gate_set) & (db_tmp["compiler"] == "tket")
                ]
                db_filtered = pd.concat([db_filtered, db_tmp4])

        if (
            benchmark_config.mapped_qiskit_compiler
            and benchmark_config.mapped_qiskit_opt_lvls
            and benchmark_config.mapped_devices
        ):
            for opt_lvl in benchmark_config.mapped_qiskit_opt_lvls:
                for device in benchmark_config.mapped_devices:
                    db_tmp5 = db_tmp.loc[
                        (db_tmp["mapped_flag"])
                        & (db_tmp["target_device"] == device)
                        & (db_tmp["compiler"] == "qiskit")
                        & (db_tmp["compiler_settings"] == opt_lvl)
                    ]
                    db_filtered = pd.concat([db_filtered, db_tmp5])

        if (
            benchmark_config.mapped_tket_compiler
            and benchmark_config.mapped_tket_placements
            and benchmark_config.mapped_devices
        ):
            for placement in benchmark_config.mapped_tket_placements:
                for device in benchmark_config.mapped_devices:
                    db_tmp6 = db_tmp.loc[
                        (db_tmp["mapped_flag"])
                        & (db_tmp["target_device"] == device)
                        & (db_tmp["compiler"] == "tket")
                        & (db_tmp["compiler_settings"] == placement)
                    ]
                    db_filtered = pd.concat([db_filtered, db_tmp6])

        return cast(list[str], db_filtered["filename"].to_list())

    def generate_zip_ephemeral_chunks(
        self,
        filenames: list[str],
    ) -> Iterable[bytes]:
        """Generates the zip file for the selected benchmarks and returns a generator of the chunks.

        Keyword arguments:
        paths -- list of file paths for all selected benchmarks

        Return values:
            Generator of bytes to send to the browser
        """
        fileobj = NoSeekBytesIO(io.BytesIO())

        with ZipFile(fileobj, mode="w") as zf:  # type: ignore[arg-type]
            for individual_file in filenames:
                individual_file_as_path = Path(individual_file)
                assert self.mqtbench_all_zip is not None
                zf.writestr(
                    individual_file_as_path.name,
                    data=self.mqtbench_all_zip.read(individual_file),
                    compress_type=ZIP_DEFLATED,
                    compresslevel=3,
                )
                fileobj.hidden_seek(0)
                yield fileobj.read()
                fileobj.truncate_and_remember_offset(0)

        fileobj.hidden_seek(0)
        yield fileobj.read()
        fileobj.close()

    def get_selected_file_paths(self, prepared_data: BenchmarkConfiguration) -> list[str]:
        """Extracts all file paths according to the prepared user's filter criteria.

        Keyword arguments:
        prepared_data -- user's filter criteria after preparation step

        Return values:
        file_paths -- list of filter criteria for each selected benchmark
        """
        return self.filter_database(prepared_data)

    def init_database(self) -> bool:
        """Generates the database and saves it into a global variable."""

        assert self.mqtbench_all_zip is not None

        print("Initiating database...")
        self.database = create_database(self.mqtbench_all_zip)
        print(f"... done: {len(self.database)} benchmarks.")

        if not self.database.empty:
            return True

        print("Database initialization failed.")
        return False

    def prepare_form_input(self, form_data: dict[str, str]) -> BenchmarkConfiguration:
        """Formats the formData extracted from the user's inputs."""
        min_qubits = 2
        max_qubits = 130
        indices_benchmarks = []
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

        for k, v in form_data.items():
            if "select" in k:
                found_benchmark_id = parse_benchmark_id_from_form_key(k)
                if found_benchmark_id:
                    indices_benchmarks.append(found_benchmark_id)
            min_qubits = int(v) if "minQubits" in k and v else min_qubits
            max_qubits = int(v) if "maxQubits" in k and v else max_qubits

            indep_qiskit_compiler = "indep_qiskit_compiler" in k or indep_qiskit_compiler
            indep_tket_compiler = "indep_tket_compiler" in k or indep_tket_compiler

            nativegates_qiskit_compiler = "nativegates_qiskit_compiler" in k or nativegates_qiskit_compiler
            nativegates_tket_compiler = "nativegates_tket_compiler" in k or nativegates_tket_compiler
            native_qiskit_opt_lvls.append(0) if "nativegates_qiskit_compiler_opt0" in k else None
            native_qiskit_opt_lvls.append(1) if "nativegates_qiskit_compiler_opt1" in k else None
            native_qiskit_opt_lvls.append(2) if "nativegates_qiskit_compiler_opt2" in k else None
            native_qiskit_opt_lvls.append(3) if "nativegates_qiskit_compiler_opt3" in k else None
            native_gatesets.append("ibm") if "nativegates_ibm" in k else None
            native_gatesets.append("rigetti") if "nativegates_rigetti" in k else None
            native_gatesets.append("oqc") if "nativegates_oqc" in k else None
            native_gatesets.append("ionq") if "nativegates_ionq" in k else None
            native_gatesets.append("quantinuum") if "nativegates_quantinuum" in k else None

            mapped_qiskit_compiler = "mapped_qiskit_compiler" in k or mapped_qiskit_compiler
            mapped_tket_compiler = "mapped_tket_compiler" in k or mapped_tket_compiler
            mapped_qiskit_opt_lvls.append(0) if "mapped_qiskit_compiler_opt0" in k else None
            mapped_qiskit_opt_lvls.append(1) if "mapped_qiskit_compiler_opt1" in k else None
            mapped_qiskit_opt_lvls.append(2) if "mapped_qiskit_compiler_opt2" in k else None
            mapped_qiskit_opt_lvls.append(3) if "mapped_qiskit_compiler_opt3" in k else None
            mapped_tket_placements.append("graph") if "mapped_tket_compiler_graph" in k else None
            mapped_tket_placements.append("line") if "mapped_tket_compiler_line" in k else None
            mapped_devices.append("ibm_montreal") if "device_ibm_montreal" in k else None
            mapped_devices.append("ibm_washington") if "device_ibm_washington" in k else None
            mapped_devices.append("rigetti_aspen_m2") if "device_rigetti_aspen_m2" in k else None
            mapped_devices.append("oqc_lucy") if "device_oqc_lucy" in k else None
            mapped_devices.append("ionq_harmony") if "device_ionq_harmony" in k else None
            mapped_devices.append("ionq_aria1") if "device_ionq_aria1" in k else None
            mapped_devices.append("quantinuum_h2") if "device_quantinuum_h2" in k else None

        return BenchmarkConfiguration(
            min_qubits=min_qubits,
            max_qubits=max_qubits,
            indices_benchmarks=indices_benchmarks,
            indep_qiskit_compiler=indep_qiskit_compiler,
            indep_tket_compiler=indep_tket_compiler,
            nativegates_qiskit_compiler=nativegates_qiskit_compiler,
            nativegates_tket_compiler=nativegates_tket_compiler,
            native_qiskit_opt_lvls=native_qiskit_opt_lvls,
            native_gatesets=native_gatesets,
            mapped_qiskit_compiler=mapped_qiskit_compiler,
            mapped_tket_compiler=mapped_tket_compiler,
            mapped_qiskit_opt_lvls=mapped_qiskit_opt_lvls,
            mapped_tket_placements=mapped_tket_placements,
            mapped_devices=mapped_devices,
        )

    def read_mqtbench_all_zip(
        self,
        target_location: str,
        skip_question: bool = False,
    ) -> bool:
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
            available_versions = [elem["name"] for elem in handle_github_api_request("tags").json()]

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
                            if skip_question or response.lower() == "y" or not response:
                                self.handle_downloading_benchmarks(target_location, download_url)
                                break
                if version_found:
                    break

            if not version_found:
                print("No suitable benchmarks found.")
                return False

        with huge_zip_path.open("rb") as zf:
            zip_bytes = io.BytesIO(zf.read())
            self.mqtbench_all_zip = ZipFile(zip_bytes, mode="r")
        return True

    def handle_downloading_benchmarks(self, target_location: str, download_url: str) -> None:
        print("Start downloading benchmarks...")

        r = requests.get(download_url, stream=True)

        content_length_response = r.headers.get("content-length")
        assert content_length_response is not None
        total_length = int(content_length_response)
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


def parse_data(filename: str) -> ParsedBenchmarkName:
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

    return ParsedBenchmarkName(
        benchmark=benchmark,
        num_qubits=num_qubits,
        indep_flag=indep_flag,
        nativegates_flag=nativegates_flag,
        mapped_flag=mapped_flag,
        compiler=compiler,
        compiler_settings=compiler_settings,
        gate_set=gate_set,
        target_device=target_device,
        filename=filename,
    )


class NoSeekBytesIO:
    def __init__(self, fp: io.BytesIO) -> None:
        self.fp = fp
        self.deleted_offset = 0

    def write(self, b: bytes) -> int:
        return self.fp.write(b)

    def tell(self) -> int:
        return self.deleted_offset + self.fp.tell()

    def hidden_tell(self) -> int:
        return self.fp.tell()

    def seekable(self) -> bool:
        return False

    def hidden_seek(self, offset: int, start_point: int = io.SEEK_SET) -> int:
        return self.fp.seek(offset, start_point)

    def truncate_and_remember_offset(self, size: int | None) -> int:
        self.deleted_offset += self.fp.tell()
        self.fp.seek(0)
        return self.fp.truncate(size)

    def get_value(self) -> bytes:
        return self.fp.getvalue()

    def close(self) -> None:
        return self.fp.close()

    def read(self) -> bytes:
        return self.fp.read()

    def flush(self) -> None:
        return self.fp.flush()


def parse_benchmark_id_from_form_key(k: str) -> int | bool:
    pat = re.compile(r"_\d+")
    m = pat.search(k)
    if m:
        return int(m.group()[1:])
    return False


def get_opt_level(filename: str) -> int:
    """Extracts the optimization level based on a filename.
    Keyword arguments:
    filename -- filename of a benchmark
    Return values:
    num -- optimization level
    """

    pat = re.compile(r"opt\d")
    m = pat.search(filename)
    num = m.group()[-1:] if m else -1
    return int(cast(str, num))


def get_num_qubits(filename: str) -> int:
    """Extracts the number of qubits based on a filename.
    Keyword arguments:
    filename -- filename of a benchmark
    Return values:
    num -- number of qubits
    """

    pat = re.compile(r"(\d+)\.")
    m = pat.search(filename)
    num = m.group()[0:-1] if m else -1
    return int(cast(str, num))


def get_tket_settings(filename: str) -> str | None:
    if "mapped" not in filename:
        return None
    if "line" in filename:
        return "line"
    if "graph" in filename:
        return "graph"
    error_msg = "Unknown tket settings in: " + filename
    raise ValueError(error_msg)


def get_gate_set(filename: str) -> str:
    if "oqc" in filename:
        return "oqc"
    if "ionq" in filename:
        return "ionq"
    if "ibm" in filename:
        return "ibm"
    if "rigetti" in filename:
        return "rigetti"
    if "quantinuum" in filename:
        return "quantinuum"
    raise ValueError("Unknown gate set: " + filename)


def get_target_device(filename: str) -> str:
    devices = [
        "ibm_washington",
        "ibm_montreal",
        "rigetti_aspen_m2",
        "ionq_harmony",
        "ionq_aria1",
        "oqc_lucy",
        "quantinuum_h2",
    ]
    if "ionq11" in filename:
        import warnings

        warnings.warn(
            "You are using a deprecated MQTBench version. Please re-install MQTBench or remove the MQTBench_all.zip file located at mqt/benchviewer/static/files/MQTBench_all.zip and re-start the server to download the latest benchmarks",
            DeprecationWarning,
            stacklevel=2,
        )
        return "ionq_harmony"
    for device in devices:
        if device in filename:
            return device
    raise ValueError("Unknown target device: " + filename)


def get_compiler_and_settings(filename: str) -> tuple[str, str | int | None]:
    if "qiskit" in filename:
        return "qiskit", get_opt_level(filename)
    if "tket" in filename:
        return "tket", get_tket_settings(filename)
    raise ValueError("Unknown compiler: " + filename)


def create_database(zip_file: ZipFile) -> pd.DataFrame:
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

    colnames = list(ParsedBenchmarkName.__annotations__.keys())

    database = pd.DataFrame(rows_list, columns=colnames)
    database["num_qubits"] = database["num_qubits"].astype(int)
    database["benchmark"] = database["benchmark"].astype(str)
    return database


def handle_downloading_benchmarks(target_location: str, download_url: str) -> None:
    print("Start downloading benchmarks...")

    r = requests.get(download_url)
    total_length = int(r.headers["content-length"])

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
