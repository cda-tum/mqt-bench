import importlib

def generate_algo_layer_benchmarks():
    algo_dicts_filename = "algo_dicts.txt"
    with open(algo_dicts_filename) as file:
        algo_dicts = file.readline()

    # algo_dicts = []
    #
    # qft_dict_1 = {
    #   "name": "grover",
    #   "n_max": 20,
    #   "stepsize": 5,
    #   "ancillary_mode": "noancilla",
    # }
    # qft_dict_2 = {
    #   "name": "qft",
    #   "n_max": 10,
    #   "stepsize": 3,
    #   "ancillary_mode": None,
    # }

    #algo_dicts.append(qft_dict_1)
    #algo_dicts.append(qft_dict_2)

    qc_results = []

    for circuit_dict in algo_dicts:
        filename = circuit_dict["name"]
        lib = importlib.import_module(filename)
        for i in range(3, circuit_dict["n_max"], circuit_dict["stepsize"]):
            if circuit_dict["ancillary_mode"]:
                qc = lib.create_circuit(i, ancillary_mode=circuit_dict["ancillary_mode"])
                qc.name = qc.name + "-" + circuit_dict["ancillary_mode"]
            else:
                qc = lib.create_circuit(i)

            tmp_result = {
                "name": qc.name,
                "n_qubits": i,
                "quantum_circuit": qc,
                "ancilla_mode": circuit_dict["ancillary_mode"]
            }

            qc_results.append(tmp_result)
    print(qc_results)
    return qc_results