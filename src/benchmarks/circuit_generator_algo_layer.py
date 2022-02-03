import importlib
import ast

#def generate_algo_layer_benchmarks():
algo_dicts_filename = "algo_dicts.txt"
with open(algo_dicts_filename) as file:
    algo_dicts = ast.literal_eval(file.readline())

print (algo_dicts)

qc_results = []
for circuit_dict in algo_dicts:
    #print(circuit_dict["name"])
    benchmark_name = circuit_dict["name"]
    if "grover" in benchmark_name:
        lib = importlib.import_module("grover")
    elif "qwalk" in benchmark_name:
        lib = importlib.import_module("qwalk")
    else:
        try:
            print("benchmark_name: ", benchmark_name)
            lib = importlib.import_module(benchmark_name)
        except Exception as e:
            print(e)
            continue

#################### non scalable benchmarks

        if benchmark_name == "shor":
            # create_shor_benchmarks()
            continue
        elif benchmark_name == "hhl":  # 5 is max number which fits my RAM
            continue
        elif benchmark_name == "pricingcall":
            continue
        elif benchmark_name == "pricingput":
            continue
        elif benchmark_name == "groundstate":
            continue
        elif benchmark_name == "excitedstate":
            continue
        elif benchmark_name == "tsp":
            continue
        elif benchmark_name == "routing":
            continue

#################### non scalable benchmarks end

    for i in range(3, int(circuit_dict["n_max"]), int(circuit_dict["stepsize"])):
        if "v-chain" in benchmark_name:
            qc = lib.create_circuit(i, ancillary_mode="v-chain")
            qc.name = qc.name + "-" + "ancillary_mode"
        elif "noancilla" in benchmark_name:
            qc = lib.create_circuit(i, ancillary_mode="noancilla")
            qc.name = qc.name + "-" + "noancilla"
        # First treat all "special" benchmarks with n != num qubits or different constructor parameters

        else:
            qc = lib.create_circuit(i)

        tmp_result = {
            "name": qc.name,
            "n_qubits": i,
            "quantum_circuit": qc,
        }

        qc_results.append(tmp_result)
print(qc_results)
   # return qc_results