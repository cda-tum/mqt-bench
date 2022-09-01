from __future__ import annotations

import argparse
import importlib
import json
import signal
from os import mkdir, path

from joblib import Parallel, delayed
from qiskit import QuantumCircuit

from mqt.bench.benchmarks import hhl, shor
from mqt.bench.benchmarks.qiskit_application_finance import pricingcall, pricingput
from mqt.bench.benchmarks.qiskit_application_nature import groundstate
from mqt.bench.benchmarks.qiskit_application_optimization import routing, tsp
from mqt.bench.utils import qiskit_helper, tket_helper, utils


def init_module_paths():
    global benchmarks_module_paths_dict
    benchmarks_module_paths_dict = {
        "ae": "mqt.bench.benchmarks.ae",
        "dj": "mqt.bench.benchmarks.dj",
        "grover": "mqt.bench.benchmarks.grover",
        "ghz": "mqt.bench.benchmarks.ghz",
        "graphstate": "mqt.bench.benchmarks.graphstate",
        "portfolioqaoa": "mqt.bench.benchmarks.qiskit_application_finance.portfolioqaoa",
        "portfoliovqe": "mqt.bench.benchmarks.qiskit_application_finance.portfoliovqe",
        "qaoa": "mqt.bench.benchmarks.qaoa",
        "qft": "mqt.bench.benchmarks.qft",
        "qftentangled": "mqt.bench.benchmarks.qftentangled",
        "qgan": "mqt.bench.benchmarks.qiskit_application_ml.qgan",
        "qpeexact": "mqt.bench.benchmarks.qpeexact",
        "qpeinexact": "mqt.bench.benchmarks.qpeinexact",
        "qwalk": "mqt.bench.benchmarks.qwalk",
        "realamprandom": "mqt.bench.benchmarks.realamprandom",
        "su2random": "mqt.bench.benchmarks.su2random",
        "twolocalrandom": "mqt.bench.benchmarks.twolocalrandom",
        "vqe": "mqt.bench.benchmarks.vqe",
        "wstate": "mqt.bench.benchmarks.wstate",
    }


def create_benchmarks_from_config(cfg_path: str):
    init_module_paths()

    with open(cfg_path) as jsonfile:
        cfg = json.load(jsonfile)
        print("Read config successful")

    global timeout
    timeout = cfg["timeout"]

    global qasm_output_folder
    qasm_output_folder = utils.get_qasm_output_path()
    if not path.isdir(qasm_output_folder):
        mkdir(qasm_output_folder)

    Parallel(n_jobs=-1, verbose=100)(
        delayed(generate_benchmark)(benchmark) for benchmark in cfg["benchmarks"]
    )
    return True


def benchmark_generation_watcher(func, args):
    class TimeoutException(Exception):  # Custom exception class
        pass

    def timeout_handler(signum, frame):  # Custom signal handler
        raise TimeoutException("TimeoutException")

    # Change the behavior of SIGALRM
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(timeout)
    try:
        res = func(*args)
    except TimeoutException:
        print(
            "Calculation/Generation exceeded timeout limit for ",
            func.__name__,
            func.__module__.split(".")[-1],
            args[0].name,
            args[1:],
        )
        return False
    except Exception as e:
        print(
            "Exception: ",
            e,
            func.__name__,
            func.__module__.split(".")[-1],
            args[0].name,
            args[1:],
        )
        return False
    else:
        # Reset the alarm
        signal.alarm(0)

    return res


def qc_creation_watcher(func, args):
    class TimeoutException(Exception):  # Custom exception class
        pass

    def timeout_handler(signum, frame):  # Custom signal handler
        raise TimeoutException

    # Change the behavior of SIGALRM
    signal.signal(signal.SIGALRM, timeout_handler)

    signal.alarm(timeout)
    try:
        qc, num_qubits, file_precheck = func(*args)
    except TimeoutException:
        print("Benchmark Creation exceeded timeout limit for ", func, args[1:])
        return False
    except Exception as e:
        print("Something else went wrong: ", e)
        return False
    else:
        # Reset the alarm
        signal.alarm(0)

    return qc, num_qubits, file_precheck


def generate_benchmark(benchmark):
    if benchmark["include"]:
        if benchmark["name"] == "grover" or benchmark["name"] == "qwalk":
            for anc_mode in benchmark["ancillary_mode"]:
                for n in range(
                    benchmark["min_qubits"],
                    benchmark["max_qubits"],
                    benchmark["stepsize"],
                ):
                    res_qc_creation = qc_creation_watcher(
                        create_scalable_qc, [benchmark, n, anc_mode]
                    )
                    if not res_qc_creation:
                        break
                    res = generate_circuits_on_all_levels(*res_qc_creation)
                    if not res:
                        break

        elif benchmark["name"] == "shor":
            for choice in benchmark["instances"]:
                res_qc_creation = qc_creation_watcher(create_shor_qc, [choice])
                if not res_qc_creation:
                    break
                res = generate_circuits_on_all_levels(*res_qc_creation)
                if not res:
                    break

        elif benchmark["name"] == "hhl":
            for i in range(benchmark["min_index"], benchmark["max_index"]):
                res_qc_creation = qc_creation_watcher(create_hhl_qc, [i])
                if not res_qc_creation:
                    break
                res = generate_circuits_on_all_levels(*res_qc_creation)
                if not res:
                    break

        elif benchmark["name"] == "routing":
            for nodes in range(benchmark["min_nodes"], benchmark["max_nodes"]):
                res_qc_creation = qc_creation_watcher(create_routing_qc, [nodes])
                if not res_qc_creation:
                    break
                res = generate_circuits_on_all_levels(*res_qc_creation)
                if not res:
                    break

        elif benchmark["name"] == "tsp":
            for nodes in range(benchmark["min_nodes"], benchmark["max_nodes"]):
                res_qc_creation = qc_creation_watcher(create_tsp_qc, [nodes])
                if not res_qc_creation:
                    break
                res = generate_circuits_on_all_levels(*res_qc_creation)
                if not res:
                    break

        elif benchmark["name"] == "groundstate":
            for choice in benchmark["instances"]:
                res_qc_creation = qc_creation_watcher(create_groundstate_qc, [choice])
                if not res_qc_creation:
                    break
                res = generate_circuits_on_all_levels(*res_qc_creation)
                if not res:
                    break

        elif benchmark["name"] == "pricingcall":
            for nodes in range(
                benchmark["min_uncertainty"], benchmark["max_uncertainty"]
            ):
                res_qc_creation = qc_creation_watcher(create_pricingcall_qc, [nodes])
                if not res_qc_creation:
                    break
                res = generate_circuits_on_all_levels(*res_qc_creation)
                if not res:
                    break

        elif benchmark["name"] == "pricingput":
            for nodes in range(
                benchmark["min_uncertainty"], benchmark["max_uncertainty"]
            ):
                res_qc_creation = qc_creation_watcher(create_pricingput_qc, [nodes])
                if not res_qc_creation:
                    break
                res = generate_circuits_on_all_levels(*res_qc_creation)
                if not res:
                    break
        else:
            for n in range(
                benchmark["min_qubits"], benchmark["max_qubits"], benchmark["stepsize"]
            ):

                res_qc_creation = qc_creation_watcher(
                    create_scalable_qc, [benchmark, n]
                )
                if not res_qc_creation:
                    break
                res = generate_circuits_on_all_levels(*res_qc_creation)
                if not res:
                    break

    return


def generate_circuits_on_all_levels(qc, num_qubits, file_precheck):

    success_generated_circuits_t_indep = generate_target_indep_level_circuit(
        qc, num_qubits, file_precheck
    )

    if not success_generated_circuits_t_indep:
        return False

    generate_target_dep_level_circuit(qc, num_qubits, file_precheck)
    return True


def generate_target_indep_level_circuit(
    qc: QuantumCircuit, num_qubits: int, file_precheck
):

    num_generated_circuits = 0
    res_indep_qiskit = benchmark_generation_watcher(
        qiskit_helper.get_indep_level, [qc, num_qubits, file_precheck]
    )
    if res_indep_qiskit:
        num_generated_circuits += 1

    res_indep_tket = benchmark_generation_watcher(
        tket_helper.get_indep_level, [qc, num_qubits, file_precheck]
    )
    if res_indep_tket:
        num_generated_circuits += 1

    if num_generated_circuits == 0:
        return False
    else:
        return True


def generate_target_dep_level_circuit(
    qc: QuantumCircuit, num_qubits: int, file_precheck
):

    compilation_paths = [
        ("ibm", [("ibm_washington", 127), ("ibm_montreal", 27)]),
        ("rigetti", [("rigetti_aspen_m1", 80)]),
        ("ionq", [("ionq11", 11)]),
        ("oqc", [("oqc_lucy", 8)]),
    ]
    num_generated_benchmarks = 0
    for gate_set_name, devices in compilation_paths:
        # Creating the circuit on both target-dependent levels for qiskit
        for opt_level in range(4):
            res = benchmark_generation_watcher(
                qiskit_helper.get_native_gates_level,
                [
                    qc,
                    gate_set_name,
                    num_qubits,
                    opt_level,
                    file_precheck,
                ],
            )
            if not res:
                break
            else:
                num_generated_benchmarks += 1

        for device_name, max_qubits in devices:
            for opt_level in range(4):
                # Creating the circuit on target-dependent: mapped level qiskit
                if max_qubits >= qc.num_qubits:
                    res = benchmark_generation_watcher(
                        qiskit_helper.get_mapped_level,
                        [
                            qc,
                            gate_set_name,
                            qc.num_qubits,
                            device_name,
                            opt_level,
                            file_precheck,
                        ],
                    )
                    if not res:
                        break
                    else:
                        num_generated_benchmarks += 1

        # Creating the circuit on both target-dependent levels for tket

        res = benchmark_generation_watcher(
            tket_helper.get_native_gates_level,
            [
                qc,
                gate_set_name,
                num_qubits,
                file_precheck,
            ],
        )
        if not res:
            continue
        num_generated_benchmarks += 1

        for device_name, max_qubits in devices:
            if max_qubits >= qc.num_qubits:
                for lineplacement in (False, True):
                    # Creating the circuit on target-dependent: mapped level tket
                    res = benchmark_generation_watcher(
                        tket_helper.get_mapped_level,
                        [
                            qc,
                            gate_set_name,
                            qc.num_qubits,
                            device_name,
                            lineplacement,
                            file_precheck,
                        ],
                    )
                    if not res:
                        continue
                    else:
                        num_generated_benchmarks += 1
    if num_generated_benchmarks == 0:
        return False
    else:
        return True


def create_scalable_qc(benchmark, num_qubits, ancillary_mode=None):
    file_precheck = True
    try:
        # Creating the circuit on Algorithmic Description level
        lib = importlib.import_module(benchmarks_module_paths_dict[benchmark["name"]])
        if benchmark["name"] == "grover" or benchmark["name"] == "qwalk":
            qc = lib.create_circuit(num_qubits, ancillary_mode=ancillary_mode)
            qc.name = qc.name + "-" + ancillary_mode
            file_precheck = False

        else:
            qc = lib.create_circuit(num_qubits)

        n = qc.num_qubits
        return qc, n, file_precheck

    except Exception as e:
        print("\n Problem occurred in outer loop: ", benchmark, num_qubits, e)


def create_shor_qc(choice: str):
    instances = {
        "xsmall": [9, 4],  # 18 qubits
        "small": [15, 4],  # 18 qubits
        "medium": [821, 4],  # 42 qubits
        "large": [11777, 4],  # 58 qubits
        "xlarge": [201209, 4],  # 74 qubits
    }

    try:
        qc = shor.create_circuit(instances[choice][0], instances[choice][1])
        return qc, qc.num_qubits, False

    except Exception as e:
        print(
            "\n Problem occurred in outer loop: ", "create_shor_benchmarks: ", choice, e
        )


def create_hhl_qc(index: int):
    # index is not the number of qubits in this case
    try:
        # Creating the circuit on Algorithmic Description level
        qc = hhl.create_circuit(index)
        return qc, qc.num_qubits, False

    except Exception as e:
        print("\n Problem occurred in outer loop: ", "create_hhl_benchmarks", index, e)


def create_routing_qc(nodes: int):
    try:
        # Creating the circuit on Algorithmic Description level
        qc = routing.create_circuit(nodes, 2)
        return qc, qc.num_qubits, False

    except Exception as e:
        print(
            "\n Problem occurred in outer loop: ", "create_routing_benchmarks", nodes, e
        )


def create_tsp_qc(nodes: int):
    try:
        # Creating the circuit on Algorithmic Description level
        qc = tsp.create_circuit(nodes)
        return qc, qc.num_qubits, False

    except Exception as e:
        print("\n Problem occurred in outer loop: ", "create_tsp_benchmarks", nodes, e)


def create_groundstate_qc(choice: str):
    molecule = utils.get_molecule(choice)

    try:
        qc = groundstate.create_circuit(molecule)
        qc.name = qc.name + "_" + choice
        return qc, qc.num_qubits, False

    except Exception as e:
        print(
            "\n Problem occurred in outer loop: ",
            "create_groundstate_benchmarks",
            choice,
            e,
        )


def create_pricingcall_qc(num_uncertainty: int):
    # num_options is not the number of qubits in this case
    try:
        # Creating the circuit on Algorithmic Description level
        qc = pricingcall.create_circuit(num_uncertainty)
        return qc, qc.num_qubits, False

    except Exception as e:
        print(
            "\n Problem occurred in outer loop: ",
            "create_pricingcall_benchmarks",
            num_uncertainty,
            e,
        )


def create_pricingput_qc(num_uncertainty: int):
    # num_uncertainty is not the number of qubits in this case
    try:
        # Creating the circuit on Algorithmic Description level
        qc = pricingput.create_circuit(num_uncertainty)
        return qc, qc.num_qubits, False

    except Exception as e:
        print(
            "\n Problem occurred in outer loop: ",
            "create_pricingput_benchmarks",
            num_uncertainty,
            e,
        )


def get_one_benchmark(
    benchmark_name: str,
    level: str | int,
    circuit_size: int = None,
    benchmark_instance_name: str = None,
    compiler: str = "qiskit",
    compiler_settings: dict[str, dict[str, any]] = None,
    gate_set_name: str = "ibm",
    device_name: str = "ibm_washington",
):
    """Returns one benchmark as a Qiskit::QuantumCircuit Object.

    Keyword arguments:
    benchmark_name -- name of the to be generated benchmark
    level -- Choice of level, either as a string ("alg", "indep", "gates" or "mapped") or as a number between 0-3 where 0 corresponds to "alg" level and 3 to "mapped" level
    circuit_size -- Input for the benchmark creation, in most cases this is equal to the qubit number
    benchmark_instance_name -- Input selection for some benchmarks, namely "groundstate" and "shor"
    compiler -- "qiskit" or "tket"
    compiler_settings -- Dictionary containing the respective compiler settings for the specified compiler (e.g., optimization level for Qiskit or placement for TKET)
    gate_set_name -- "ibm", "rigetti", "ionq", or "oqc"
    device_name -- "ibm_washington", "ibm_montreal", "aspen_m1", "ionq11", ""lucy""

    Return values:
    Quantum Circuit Object -- Representing the benchmark with the selected options, either as Qiskit::QuantumCircuit or Pytket::Circuit object (depending on the chosen compiler---while the algorithm level is always provided using Qiskit)
    """
    init_module_paths()

    if "grover" in benchmark_name or "qwalk" in benchmark_name:
        if "noancilla" in benchmark_name:
            anc_mode = "noancilla"
        elif "v-chain" in benchmark_name:
            anc_mode = "v-chain"

        short_name = benchmark_name.split("-")[0]
        lib = importlib.import_module(benchmarks_module_paths_dict[short_name])
        qc = lib.create_circuit(circuit_size, ancillary_mode=anc_mode)
        qc.name = qc.name + "-" + anc_mode

    elif benchmark_name == "shor":
        instances = {
            "xsmall": [9, 4],  # 18 qubits
            "small": [15, 4],  # 18 qubits
            "medium": [821, 4],  # 42 qubits
            "large": [11777, 4],  # 58 qubits
            "xlarge": [201209, 4],  # 74 qubits
        }

        qc = shor.create_circuit(*instances[benchmark_instance_name])

    elif benchmark_name == "hhl":
        qc = hhl.create_circuit(circuit_size)

    elif benchmark_name == "routing":
        qc = routing.create_circuit(circuit_size)

    elif benchmark_name == "tsp":
        qc = tsp.create_circuit(circuit_size)

    elif benchmark_name == "groundstate":
        molecule = utils.get_molecule(benchmark_instance_name)
        qc = groundstate.create_circuit(molecule)

    elif benchmark_name == "pricingcall":
        qc = pricingcall.create_circuit(circuit_size)

    elif benchmark_name == "pricingput":
        qc = pricingput.create_circuit(circuit_size)

    else:
        lib = importlib.import_module(benchmarks_module_paths_dict[benchmark_name])
        qc = lib.create_circuit(circuit_size)

    if compiler_settings is None:
        compiler_settings = {
            "qiskit": {"optimization_level": 1},
            "tket": {"placement": "lineplacement"},
        }

    if level == "alg" or level == 0:
        return qc

    elif level == "indep" or level == 1:

        if compiler == "qiskit":
            qc_indep = qiskit_helper.get_indep_level(qc, circuit_size, False, True)
        elif compiler == "tket":
            qc_indep = tket_helper.get_indep_level(qc, circuit_size, False, True)

        return qc_indep

    elif level == "nativegates" or level == 2:

        if compiler == "qiskit":
            opt_level = compiler_settings["qiskit"]["optimization_level"]
            qc_gates = qiskit_helper.get_native_gates_level(
                qc, gate_set_name, circuit_size, opt_level, False, True
            )
        elif compiler == "tket":
            qc_gates = tket_helper.get_native_gates_level(
                qc, gate_set_name, circuit_size, False, True
            )

        return qc_gates

    elif level == "mapped" or level == 3:
        if compiler == "qiskit":
            opt_level = compiler_settings["qiskit"]["optimization_level"]
            qc_mapped = qiskit_helper.get_mapped_level(
                qc,
                gate_set_name,
                circuit_size,
                device_name,
                opt_level,
                False,
                True,
            )
        elif compiler == "tket":
            placement = compiler_settings["tket"]["placement"].lower()
            lineplacement = placement == "lineplacement"
            qc_mapped = tket_helper.get_mapped_level(
                qc,
                gate_set_name,
                circuit_size,
                device_name,
                lineplacement,
                False,
                True,
            )
        return qc_mapped
    else:
        return print("Level specification was wrong.")


if __name__ == "__main__":
    init_module_paths()

    parser = argparse.ArgumentParser(description="Create Configuration")
    parser.add_argument(
        "--file-name", type=str, help="optional filename", default="./config.json"
    )

    args = parser.parse_args()

    print("#### Start generating")
    # create_benchmarks_from_config(args.file_name)
    print("#### Start preprocessing")
    utils.postprocess_oqc_qasm_files()
    print("#### Start zipping")
    # utils.create_zip_file()
    print("#### Generation ended")
