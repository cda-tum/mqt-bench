from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, AncillaRegister
from qiskit.compiler import transpile
from qiskit.transpiler import CouplingMap
from qiskit.providers.ibmq.ibmqbackend import IBMQBackend
import networkx as nx
from qiskit_optimization.applications import Maxcut


# def measure(qc: QuantumCircuit, q: QuantumRegister, c: ClassicalRegister):
#     for i in reversed(range(q.size)):
#         qc.measure(q[i], c[i])


def get_compiled_circuit(qc: QuantumCircuit, opt_level: int = 2, c_map: CouplingMap = None):
    t_qc = transpile(qc, basis_gates=['id', 'rz', 'sx', 'x', 'cx', 'reset'], optimization_level=opt_level, coupling_map=c_map)
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


def get_examplary_max_cut_qp(n_qubits: int):
    graph = nx.random_regular_graph(d=2, n=n_qubits, seed=111)
    maxcut = Maxcut(graph)
    return maxcut.to_quadratic_program()
