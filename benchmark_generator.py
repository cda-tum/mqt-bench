from qiskit_nature.drivers import Molecule

import matplotlib.pyplot as plt
import os.path
import json
import importlib
import signal

from src.utils import *
from src.benchmarks import (
    shor,
    hhl,
)
from src.benchmarks.qiskit_application_optimization import routing, tsp
from src.benchmarks.qiskit_application_finance import (
    pricingcall,
    pricingput,
)
from src.benchmarks.qiskit_application_nature import groundstate, excitedstate


def create_benchmarks_from_config(cfg=None):
    characteristics = []

    if not cfg:
        with open("config.json", "r") as jsonfile:
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

    global scalable_benchmarks_module_paths_dict
    scalable_benchmarks_module_paths_dict = {
        "ae": "src.benchmarks.ae",
        "dj": "src.benchmarks.dj",
        "grover": "src.benchmarks.grover",
        "ghz": "src.benchmarks.ghz",
        "graphstate": "src.benchmarks.graphstate",
        "portfolioqaoa": "src.benchmarks.qiskit_application_finance.portfolioqaoa",
        "portfoliovqe": "src.benchmarks.qiskit_application_finance.portfoliovqe",
        "qaoa": "src.benchmarks.qaoa",
        "qft": "src.benchmarks.qft",
        "qftentangled": "src.benchmarks.qftentangled",
        "qgan": "src.benchmarks.qiskit_application_finance.qgan",
        "qpeexact": "src.benchmarks.qpeexact",
        "qpeinexact": "src.benchmarks.qpeinexact",
        "qwalk": "src.benchmarks.qwalk",
        "vqe": "src.benchmarks.vqe",
        "wstate": "src.benchmarks.wstate",
    }

    for benchmark in cfg["benchmarks"]:
        print(benchmark["name"])  #
        characteristics.extend(generate_benchmark(benchmark))
    return characteristics


def benchmark_generation_watcher(func, args):
    class TimeoutException(Exception):  # Custom exception class
        pass

    def timeout_handler(signum, frame):  # Custom signal handler
        raise TimeoutException

    # Change the behavior of SIGALRM
    signal.signal(signal.SIGALRM, timeout_handler)

    signal.alarm(timeout)
    try:
        filename, depth, num_qubits = func(*args)
    except:
        print("Calculation/Generation exceeded timeout limit for ", func, args[1:])

        if func == get_indep_layer:
            qc = args[0]
            num_qubits = args[1]
            filename_indep = qc.name + "_t-indep_" + str(num_qubits)
            path = "qasm_output/" + filename_indep + ".qasm"

            if os.path.isfile(path):
                os.remove(path)
                print("removed file: ", path)

        elif func == get_native_gates_layer:
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

            path = "qasm_output/" + filename_nativegates + ".qasm"
            if os.path.isfile(path):
                os.remove(path)
                print("removed file: ", path)

        elif func == get_mapped_layer:
            qc = args[0]
            gate_set_name_mapped = args[2]
            opt_level = args[3]
            num_qubits = args[4]

            filename_mapped = (
                qc.name
                + "_mapped_"
                + gate_set_name_mapped
                + "_opt"
                + str(opt_level)
                + "_"
                + str(num_qubits)
            )

            path = "qasm_output/" + filename_mapped + ".qasm"
            if os.path.isfile(path):
                os.remove(path)
                print("removed file: ", path)

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
                    res = generate_circuits_on_all_layer(*res_qc_creation)
                    if len(res) == 0:
                        break
                    characteristics.extend(res)

        elif benchmark["name"] == "shor":
            for choice in benchmark["instances"]:
                res_qc_creation = qc_creation_watcher(create_shor_qc, [choice])
                if not res_qc_creation:
                    break
                res = generate_circuits_on_all_layer(*res_qc_creation)
                if len(res) == 0:
                    break
                characteristics.extend(res)

        elif benchmark["name"] == "hhl":
            for i in range(benchmark["min_index"], benchmark["max_index"]):
                res_qc_creation = qc_creation_watcher(create_hhl_qc, [i])
                if not res_qc_creation:
                    break
                res = generate_circuits_on_all_layer(*res_qc_creation)
                if len(res) == 0:
                    break
                characteristics.extend(res)
                break

        elif benchmark["name"] == "routing":
            for nodes in range(benchmark["min_nodes"], benchmark["max_nodes"]):
                res_qc_creation = qc_creation_watcher(create_routing_qc, [nodes])
                if not res_qc_creation:
                    break
                res = generate_circuits_on_all_layer(*res_qc_creation)
                if len(res) == 0:
                    break
                characteristics.extend(res)

        elif benchmark["name"] == "tsp":
            for nodes in range(benchmark["min_nodes"], benchmark["max_nodes"]):
                res_qc_creation = qc_creation_watcher(create_tsp_qc, [nodes])
                if not res_qc_creation:
                    break
                res = generate_circuits_on_all_layer(*res_qc_creation)
                if len(res) == 0:
                    break
                characteristics.extend(res)

        elif benchmark["name"] == "groundstate":
            for choice in benchmark["instances"]:
                res_qc_creation = qc_creation_watcher(create_groundstate_qc, [choice])
                if not res_qc_creation:
                    break
                res = generate_circuits_on_all_layer(*res_qc_creation)
                if len(res) == 0:
                    break
                characteristics.extend(res)

        elif benchmark["name"] == "excitedstate":
            for choice in benchmark["instances"]:
                res_qc_creation = qc_creation_watcher(create_excitedstate_qc, [choice])
                if not res_qc_creation:
                    break
                res = generate_circuits_on_all_layer(*res_qc_creation)
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
                res = generate_circuits_on_all_layer(*res_qc_creation)
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
                res = generate_circuits_on_all_layer(*res_qc_creation)
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
                res = generate_circuits_on_all_layer(*res_qc_creation)
                if len(res) == 0:
                    break
                characteristics.extend(res)

    return characteristics


def generate_circuits_on_all_layer(qc, num_qubits, file_precheck):
    characteristics = []
    # filename_algo, depth = generate_algo_layer_circuit(qc, n, save_png, save_hist)
    # characteristics.append([filename_algo, n, depth])

    res_t_indep = generate_target_indep_layer_circuit(
        qc, num_qubits, save_png, save_hist, file_precheck
    )

    if res_t_indep:
        characteristics.extend(res_t_indep)
    else:
        return characteristics

    res_t_dep = generate_target_dep_layer_circuit(
        qc, num_qubits, save_png, save_hist, file_precheck
    )

    if res_t_dep:
        characteristics.extend(res_t_dep)
    else:
        return characteristics

    return characteristics


def generate_algo_layer_circuit(
    qc: QuantumCircuit, num_qubits: int, save_png, save_hist
):
    characteristics = []
    res = benchmark_generation_watcher(
        handle_algorithm_layer, [qc, num_qubits, save_png, save_hist]
    )
    characteristics.append(res)

    if res:
        characteristics.append(res)
        return characteristics
    else:
        return False


def generate_target_indep_layer_circuit(
    qc: QuantumCircuit, num_qubits: int, save_png, save_hist, file_precheck
):
    characteristics = []
    res = benchmark_generation_watcher(
        get_indep_layer, [qc, num_qubits, save_png, save_hist, file_precheck]
    )
    if res:
        characteristics.append(res)
        return characteristics
    else:
        return False


def generate_target_dep_layer_circuit(
    qc: QuantumCircuit, num_qubits: int, save_png, save_hist, file_precheck
):
    characteristics = []

    ibm_native_gates = FakeMontreal().configuration().basis_gates
    rigetti_native_gates = ["rx", "rz", "cz"]
    gate_sets = [(ibm_native_gates, "ibm"), (rigetti_native_gates, "rigetti")]

    for gate_set, gate_set_name in gate_sets:
        try:
            for opt_level in range(4):

                # Creating the circuit on target-dependent: native gates layer

                res = benchmark_generation_watcher(
                    get_native_gates_layer,
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

                # Creating the circuit on target-dependent: mapped layer for both mapping schemes
                res = benchmark_generation_watcher(
                    get_mapped_layer,
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
                    get_mapped_layer,
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
        # Creating the circuit on Algorithmic Description Layer
        lib = importlib.import_module(
            scalable_benchmarks_module_paths_dict[benchmark["name"]]
        )
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
        # Creating the circuit on Algorithmic Description Layer
        qc = hhl.create_circuit(index)
        return qc, qc.num_qubits, False

    except Exception as e:
        print("\n Problem occured in outer loop: ", "create_hhl_benchmarks", index, e)


def create_routing_qc(nodes: int):
    try:
        # Creating the circuit on Algorithmic Description Layer
        qc = routing.create_circuit(nodes, 2)
        return qc, qc.num_qubits, False

    except Exception as e:
        print(
            "\n Problem occured in outer loop: ", "create_routing_benchmarks", nodes, e
        )


def create_tsp_qc(nodes: int):
    try:
        # Creating the circuit on Algorithmic Description Layer
        qc = tsp.create_circuit(nodes)
        return qc, qc.num_qubits, False

    except Exception as e:
        print("\n Problem occured in outer loop: ", "create_tsp_benchmarks", nodes, e)


def create_groundstate_qc(choice: str):

    m_1 = Molecule(
        geometry=[["Li", [0.0, 0.0, 0.0]], ["H", [0.0, 0.0, 2.5]]],
        charge=0,
        multiplicity=1,
    )
    m_2 = Molecule(
        geometry=[["H", [0.0, 0.0, 0.0]], ["H", [0.0, 0.0, 0.735]]],
        charge=0,
        multiplicity=1,
    )
    m_3 = Molecule(
        geometry=[
            ["O", [0.0, 0.0, 0.0]],
            ["H", [0.586, 0.757, 0.0]],
            ["H", [0.586, -0.757, 0.0]],
        ],
        charge=0,
        multiplicity=1,
    )

    instances = {"small": m_1, "medium": m_2, "large": m_3}

    try:
        qc = groundstate.create_circuit(instances[choice])
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

    m_1 = Molecule(
        geometry=[["Li", [0.0, 0.0, 0.0]], ["H", [0.0, 0.0, 2.5]]],
        charge=0,
        multiplicity=1,
    )
    m_2 = Molecule(
        geometry=[["H", [0.0, 0.0, 0.0]], ["H", [0.0, 0.0, 0.735]]],
        charge=0,
        multiplicity=1,
    )
    m_3 = Molecule(
        geometry=[
            ["O", [0.0, 0.0, 0.0]],
            ["H", [0.586, 0.757, 0.0]],
            ["H", [0.586, -0.757, 0.0]],
        ],
        charge=0,
        multiplicity=1,
    )

    instances = {"small": m_1, "medium": m_2, "large": m_3}

    try:
        qc = excitedstate.create_circuit(instances[choice])
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
        # Creating the circuit on Algorithmic Description Layer
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
        # Creating the circuit on Algorithmic Description Layer
        qc = pricingput.create_circuit(num_uncertainty)
        return qc, qc.num_qubits, False

    except Exception as e:
        print(
            "\n Problem occured in outer loop: ",
            "create_pricingput_benchmarks",
            num_uncertainty,
            e,
        )

if __name__ == "__main__":
    characteristics = create_benchmarks_from_config()
