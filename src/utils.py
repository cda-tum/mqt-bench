from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, AncillaRegister
from qiskit.compiler import transpile
from qiskit.transpiler import CouplingMap
from qiskit.providers.ibmq.ibmqbackend import IBMQBackend
from qiskit_optimization.applications import Maxcut
from qiskit.visualization import plot_histogram
from qiskit.circuit import qpy_serialization

import networkx as nx

def get_compiled_circuit(qc: QuantumCircuit, opt_level: int = 2, basis_gates: list = ['id', 'rz', 'sx', 'x', 'cx', 'reset'], c_map: CouplingMap = None):
    t_qc = transpile(qc, basis_gates=basis_gates, optimization_level=opt_level, coupling_map=c_map)
    return t_qc


def get_IBM_cmap(quantum_computer: IBMQBackend):
    return quantum_computer.configuration().coupling_map


def save_as_qasm(qc: QuantumCircuit, n_qubits: int, mapped: bool = False):
    filename = qc.name + "_transpiled_"
    if mapped: filename += "mapped_"
    if n_qubits is not None: filename += str(n_qubits)

    with open("qasm_output/" + filename + ".qasm", "w") as f:
        f.write(qc.qasm())
    f.close()

def serialize_qc(qc: QuantumCircuit, n_qubits: int):
    filename = qc.name
    with open("qpy_output/" + filename + "_" + str(n_qubits) + '.qpy', 'wb') as f:
        qpy_serialization.dump(qc, f)
    f.close()

def get_examplary_max_cut_qp(n_qubits: int):
    graph = nx.random_regular_graph(d=2, n=n_qubits, seed=111)
    maxcut = Maxcut(graph)
    return maxcut.to_quadratic_program()


def sim_and_print_hist(qc: QuantumCircuit, simulator, filename: str):
    result = simulator.run(qc, shots=1024).result()
    counts = result.get_counts()
    plot = plot_histogram(counts, figsize=(15, 5), title=filename)
    plot.savefig("hist_output/" + filename + '.png', bbox_inches="tight")

