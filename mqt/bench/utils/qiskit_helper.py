def get_ibm_native_gates():
    ibm_gates = ["rz", "sx", "x", "cx", "measure"]
    return ibm_gates


def get_rigetti_native_gates():
    rigetti_gates = ["rx", "rz", "cz", "measure"]
    return rigetti_gates


def get_ionq_native_gates():
    ionq_gates = ["rxx", "rz", "ry", "rx", "measure"]
    return ionq_gates


def get_oqc_native_gates():
    oqc_gates = ["rz", "sx", "x", "ecr", "measure"]
    return oqc_gates