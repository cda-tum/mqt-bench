from qiskit import QuantumCircuit, transpile

import matplotlib.pyplot as plt
import json
import importlib
import signal
import argparse
import numpy as np

from typing import Union
from os import path, mkdir, remove

from mqt.bench.utils import utils
from mqt.bench.benchmarks import (
    shor,
    hhl,
)
from mqt.bench.benchmarks.qiskit_application_optimization import routing, tsp
from mqt.bench.benchmarks.qiskit_application_finance import (
    pricingcall,
    pricingput,
)
from mqt.bench.benchmarks.qiskit_application_nature import groundstate, excitedstate


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
    characteristics = []

    with open(cfg_path, "r") as jsonfile:
        cfg = json.load(jsonfile)
        print("Read config successful")

    # global seetings
    global save_png
    save_png = cfg["save_png"]
    global save_hist
    save_hist = cfg["save_hist"]
    global max_depth
    max_depth = cfg["max_depth"]
    global timeout
    timeout = cfg["timeout"]

    global qasm_output_folder
    qasm_output_folder = utils.get_qasm_output_path()
    if not path.isdir(qasm_output_folder):
        mkdir(qasm_output_folder)

    for benchmark in cfg["benchmarks"]:
        print(benchmark["name"])
        characteristics.extend(generate_benchmark(benchmark))
    return characteristics


def benchmark_generation_watcher(func, args):
    class TimeoutException(Exception):  # Custom exception class
        pass

    def timeout_handler(signum, frame):  # Custom signal handler
        raise TimeoutException("TimeoutException")

    # Change the behavior of SIGALRM
    signal.signal(signal.SIGALRM, timeout_handler)

    signal.alarm(timeout)
    try:
        filename, depth, num_qubits = func(*args)
    except Exception as e:
        # print("Calculation/Generation exceeded timeout limit for ", func, args[1:])
        print("Exception: ", e, func, args[1:])
        if func == utils.get_indep_level:
            qc = args[0]
            num_qubits = args[1]
            filename_indep = qc.name + "_t-indep_" + str(num_qubits)
            file_path = qasm_output_folder + filename_indep + ".qasm"

            if path.isfile(file_path):
                remove(file_path)
                # print("removed file: ", path)

        elif func == utils.get_native_gates_level:
            qc = args[0]
            gate_set_name = args[2]
            opt_level = args[3]
            num_qubits = args[4]

            filename_nativegates = (
                qc.name
                + "_nativegates_"
                + gate_set_name
                + "_opt"
                + str(opt_level)
                + "_"
                + str(num_qubits)
            )

            file_path = qasm_output_folder + filename_nativegates + ".qasm"
            if path.isfile(file_path):
                remove(file_path)

        elif func == utils.get_mapped_level:
            qc = args[0]
            gate_set_name_mapped = args[2]
            opt_level = args[3]
            num_qubits = args[4]
            smallest_arch = args[5]
            if smallest_arch:
                gate_set_name_mapped += "-s"
            else:
                gate_set_name_mapped += "-b"

            filename_mapped = (
                qc.name
                + "_mapped_"
                + gate_set_name_mapped
                + "_opt"
                + str(opt_level)
                + "_"
                + str(num_qubits)
            )

            file_path = qasm_output_folder + filename_mapped + ".qasm"
            if path.isfile(file_path):
                remove(file_path)

        return False
    else:
        # Reset the alarm
        signal.alarm(0)

    if depth > max_depth:
        print("Depth of generated circuit is too large: ", depth)
        return False

    return filename, depth, num_qubits


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
        print("Calculation/Generation exceeded timeout limit for ", func, args[1:])
        return False
    except Exception as e:
        print("Something else went wrong: ", e)
        return False
    else:
        # Reset the alarm
        signal.alarm(0)

    return qc, num_qubits, file_precheck


def generate_benchmark(benchmark):
    characteristics = []
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
                    if len(res) == 0:
                        break
                    characteristics.extend(res)

        elif benchmark["name"] == "shor":
            for choice in benchmark["instances"]:
                res_qc_creation = qc_creation_watcher(create_shor_qc, [choice])
                if not res_qc_creation:
                    break
                res = generate_circuits_on_all_levels(*res_qc_creation)
                if len(res) == 0:
                    break
                characteristics.extend(res)

        elif benchmark["name"] == "hhl":
            for i in range(benchmark["min_index"], benchmark["max_index"]):
                res_qc_creation = qc_creation_watcher(create_hhl_qc, [i])
                if not res_qc_creation:
                    break
                res = generate_circuits_on_all_levels(*res_qc_creation)
                if len(res) == 0:
                    break
                characteristics.extend(res)

        elif benchmark["name"] == "routing":
            for nodes in range(benchmark["min_nodes"], benchmark["max_nodes"]):
                res_qc_creation = qc_creation_watcher(create_routing_qc, [nodes])
                if not res_qc_creation:
                    break
                res = generate_circuits_on_all_levels(*res_qc_creation)
                if len(res) == 0:
                    break
                characteristics.extend(res)

        elif benchmark["name"] == "tsp":
            for nodes in range(benchmark["min_nodes"], benchmark["max_nodes"]):
                res_qc_creation = qc_creation_watcher(create_tsp_qc, [nodes])
                if not res_qc_creation:
                    break
                res = generate_circuits_on_all_levels(*res_qc_creation)
                if len(res) == 0:
                    break
                characteristics.extend(res)

        elif benchmark["name"] == "groundstate":
            for choice in benchmark["instances"]:
                res_qc_creation = qc_creation_watcher(create_groundstate_qc, [choice])
                if not res_qc_creation:
                    break
                res = generate_circuits_on_all_levels(*res_qc_creation)
                if len(res) == 0:
                    break
                characteristics.extend(res)

        elif benchmark["name"] == "excitedstate":
            for choice in benchmark["instances"]:
                res_qc_creation = qc_creation_watcher(create_excitedstate_qc, [choice])
                if not res_qc_creation:
                    break
                res = generate_circuits_on_all_levels(*res_qc_creation)
                if len(res) == 0:
                    break
                characteristics.extend(res)

        elif benchmark["name"] == "pricingcall":
            for nodes in range(
                benchmark["min_uncertainty"], benchmark["max_uncertainty"]
            ):
                res_qc_creation = qc_creation_watcher(create_pricingcall_qc, [nodes])
                if not res_qc_creation:
                    break
                res = generate_circuits_on_all_levels(*res_qc_creation)
                if len(res) == 0:
                    break
                characteristics.extend(res)

        elif benchmark["name"] == "pricingput":
            for nodes in range(
                benchmark["min_uncertainty"], benchmark["max_uncertainty"]
            ):
                res_qc_creation = qc_creation_watcher(create_pricingput_qc, [nodes])
                if not res_qc_creation:
                    break
                res = generate_circuits_on_all_levels(*res_qc_creation)
                if len(res) == 0:
                    break
                characteristics.extend(res)
        else:
            for n in range(
                benchmark["min_qubits"], benchmark["max_qubits"], benchmark["stepsize"]
            ):

                # res_qc_creation == qc, num_qubits, file_precheck
                # res == filename, depth, num_qubits
                res_qc_creation = qc_creation_watcher(
                    create_scalable_qc, [benchmark, n]
                )
                if not res_qc_creation:
                    break
                res = generate_circuits_on_all_levels(*res_qc_creation)
                if len(res) == 0:
                    break
                characteristics.extend(res)

    return characteristics


def generate_circuits_on_all_levels(qc, num_qubits, file_precheck):
    characteristics = []
    # filename_algo, depth = generate_algo_level_circuit(qc, n, save_png, save_hist)
    # characteristics.append([filename_algo, n, depth])

    res_t_indep = generate_target_indep_level_circuit(
        qc, num_qubits, save_png, save_hist, file_precheck
    )

    if res_t_indep:
        characteristics.extend(res_t_indep)
    else:
        return characteristics

    res_t_dep = generate_target_dep_level_circuit(
        qc, num_qubits, save_png, save_hist, file_precheck
    )

    if res_t_dep:
        characteristics.extend(res_t_dep)
    else:
        return characteristics

    return characteristics


def generate_algo_level_circuit(
    qc: QuantumCircuit, num_qubits: int, save_png, save_hist
):
    characteristics = []
    res = benchmark_generation_watcher(
        utils.handle_algorithm_level, [qc, num_qubits, save_png, save_hist]
    )
    characteristics.append(res)

    if res:
        characteristics.append(res)
        return characteristics
    else:
        return False


def generate_target_indep_level_circuit(
    qc: QuantumCircuit, num_qubits: int, save_png, save_hist, file_precheck
):
    characteristics = []

    res = benchmark_generation_watcher(
        utils.get_indep_level,
        [qc, num_qubits, save_png, save_hist, file_precheck],
    )
    if res:
        characteristics.append(res)
        return characteristics
    else:
        return False


def generate_target_dep_level_circuit(
    qc: QuantumCircuit, num_qubits: int, save_png, save_hist, file_precheck
):
    characteristics = []

    ibm_native_gates = utils.FakeMontreal().configuration().basis_gates
    rigetti_native_gates = utils.get_rigetti_native_gates()
    gate_sets = [(ibm_native_gates, "ibm"), (rigetti_native_gates, "rigetti")]

    for gate_set, gate_set_name in gate_sets:
        try:
            for opt_level in range(4):

                # Creating the circuit on target-dependent: native gates level

                res = benchmark_generation_watcher(
                    utils.get_native_gates_level,
                    [
                        qc,
                        gate_set,
                        gate_set_name,
                        opt_level,
                        num_qubits,
                        save_png,
                        save_hist,
                        file_precheck,
                    ],
                )
                if res:
                    characteristics.append(res)
                else:
                    break
                n_actual = res[2]

                # Creating the circuit on target-dependent: mapped level for both mapping schemes
                res = benchmark_generation_watcher(
                    utils.get_mapped_level,
                    [
                        qc,
                        gate_set,
                        gate_set_name,
                        opt_level,
                        n_actual,
                        True,
                        save_png,
                        save_hist,
                        file_precheck,
                    ],
                )

                if res:
                    characteristics.append(res)
                else:
                    break
                res = benchmark_generation_watcher(
                    utils.get_mapped_level,
                    [
                        qc,
                        gate_set,
                        gate_set_name,
                        opt_level,
                        n_actual,
                        False,
                        save_png,
                        save_hist,
                        file_precheck,
                    ],
                )

                if res:
                    characteristics.append(res)
                else:
                    break
        except Exception as e:
            print(
                "\n Problem occured in inner loop: ",
                qc.name,
                num_qubits,
                gate_set_name,
                e,
            )

    return characteristics


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
        print("\n Problem occured in outer loop: ", benchmark, num_qubits, e)


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
            "\n Problem occured in outer loop: ", "create_shor_benchmarks: ", choice, e
        )


def create_hhl_qc(index: int):
    # index is not the number of qubits in this case
    try:
        # Creating the circuit on Algorithmic Description level
        qc = hhl.create_circuit(index)
        return qc, qc.num_qubits, False

    except Exception as e:
        print("\n Problem occured in outer loop: ", "create_hhl_benchmarks", index, e)


def create_routing_qc(nodes: int):
    try:
        # Creating the circuit on Algorithmic Description level
        qc = routing.create_circuit(nodes, 2)
        return qc, qc.num_qubits, False

    except Exception as e:
        print(
            "\n Problem occured in outer loop: ", "create_routing_benchmarks", nodes, e
        )


def create_tsp_qc(nodes: int):
    try:
        # Creating the circuit on Algorithmic Description level
        qc = tsp.create_circuit(nodes)
        return qc, qc.num_qubits, False

    except Exception as e:
        print("\n Problem occured in outer loop: ", "create_tsp_benchmarks", nodes, e)


def create_groundstate_qc(choice: str):
    molecule = utils.get_molecule(choice)

    try:
        qc = groundstate.create_circuit(molecule)
        qc.name = qc.name + "-" + choice
        return qc, qc.num_qubits, False

    except Exception as e:
        print(
            "\n Problem occured in outer loop: ",
            "create_groundstate_benchmarks",
            choice,
            e,
        )


def create_excitedstate_qc(choice: str):
    molecule = utils.get_molecule(choice)

    try:
        qc = excitedstate.create_circuit(molecule)
        qc.name = qc.name + "-" + choice
        return qc, qc.num_qubits, False

    except Exception as e:
        print(
            "\n Problem occured in outer loop: ",
            "create_excitedstate_benchmarks",
            choice,
            e,
        )
        return False


def create_pricingcall_qc(num_uncertainty: int):
    # num_options is not the number of qubits in this case
    try:
        # Creating the circuit on Algorithmic Description level
        qc = pricingcall.create_circuit(num_uncertainty)
        return qc, qc.num_qubits, False

    except Exception as e:
        print(
            "\n Problem occured in outer loop: ",
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
            "\n Problem occured in outer loop: ",
            "create_pricingput_benchmarks",
            num_uncertainty,
            e,
        )


def save_benchmark_hist(characteristics):
    characteristics = np.array(characteristics)
    plt.scatter(
        x=characteristics[:, 2].astype(int), y=characteristics[:, 1].astype(int)
    )
    plt.yscale("log")
    plt.title("Depth and Width of generated Benchmarks")
    plt.xlabel("# of Qubits")
    plt.ylabel("Circuit Depth")
    plt.savefig("benchmark_histogram")


def get_one_benchmark(
    benchmark_name: str,
    level: Union[str, int],
    circuit_size: int = None,
    benchmark_instance_name: str = None,
    opt_level: int = 0,
    gate_set_name: str = "ibm",
    smallest_fitting_arch: bool = True,
):
    """Returns one benchmark as a Qiskit::QuantumCircuit Object.

    Keyword arguments:
    benchmark_name -- name of the to be generated benchmark
    level -- Choice of level, either as a string ("alg", "indep", "gates" or "mapped") or as a number between 0-3 where
    circuit_size -- Input for the benchmark creation, in most cases this is equal to the qubit number
    benchmark_instance_name -- Input selection for some benchmarks, namely "groundstate", "excitedstate" and "shor"
    0 corresponds to "alg" level and 3 to "mapped" level
    opt_level -- Level of optimization (relevant to "gates" and "mapped" levels)
    gate_set_name -- Either "ibm" or "rigetti"
    smallest_fitting_arch -- True->Smallest architecture is selected, False->Biggest one is selected (ibm: 127 qubits,
    rigetti: 80 qubits)


    Return values:
    QuantumCircuit -- Representing the benchmark with the selected options
    """
    init_module_paths()
    ibm_native_gates = utils.FakeMontreal().configuration().basis_gates
    rigetti_native_gates = utils.get_rigetti_native_gates()

    if gate_set_name and "ibm" in gate_set_name:
        gate_set = ibm_native_gates
    elif gate_set_name and "rigetti" in gate_set_name:
        gate_set = rigetti_native_gates
    else:
        gate_set = None

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

    elif benchmark_name == "excitedstate":
        molecule = utils.get_molecule(benchmark_instance_name)
        qc = excitedstate.create_circuit(molecule)

    elif benchmark_name == "pricingcall":
        qc = pricingcall.create_circuit(circuit_size)

    elif benchmark_name == "pricingput":
        qc = pricingput.create_circuit(circuit_size)

    else:
        lib = importlib.import_module(benchmarks_module_paths_dict[benchmark_name])
        qc = lib.create_circuit(circuit_size)

    if level == "alg" or level == 0:
        return qc

    elif level == "indep" or level == 1:

        qc_indep = transpile(qc, basis_gates=utils.get_openqasm_gates())
        return qc_indep

    elif level == "nativegates" or level == 2:
        qc_gates = utils.get_compiled_circuit_with_gateset(
            qc=qc, opt_level=opt_level, basis_gates=gate_set
        )
        return qc_gates

    elif level == "mapped" or level == 3:
        c_map, backend_name, gate_set_name_mapped, c_map_found = utils.select_c_map(
            gate_set_name, smallest_fitting_arch, circuit_size
        )
        if c_map_found:
            qc_mapped = utils.get_compiled_circuit_with_gateset(
                qc=qc, opt_level=opt_level, basis_gates=gate_set, c_map=c_map
            )
            return qc_mapped
        else:
            return print("No Hardware Architecture available for that config.")
    else:
        return print("Level specification was wrong.")


if __name__ == "__main__":
    init_module_paths()

    parser = argparse.ArgumentParser(description="Create Configuration")
    parser.add_argument(
        "--file-name", type=str, help="optional filename", default="./config.json"
    )

    args = parser.parse_args()

    print(args.file_name)
    characteristics = create_benchmarks_from_config(args.file_name)
    save_benchmark_hist(characteristics)
