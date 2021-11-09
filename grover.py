from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, AncillaRegister
from qiskit.circuit.library import QFT, GraphState, GroverOperator
from qiskit.qasm import pi
from utils import measure

def create_circuit(n: int, include_measurements: bool = True):
    from qiskit.algorithms import Grover

    q = QuantumRegister(n, 'q')
    flag = AncillaRegister(1, 'flag')
    c = ClassicalRegister(n)

    state_preparation = QuantumCircuit(q, flag)
    state_preparation.h(q)
    state_preparation.x(flag)

    oracle = QuantumCircuit(q, flag)
    oracle.mcp(pi, q, flag)

    operator = GroverOperator(oracle)
    iterations = Grover.optimal_num_iterations(1, n)

    qc = QuantumCircuit(q, flag, c, name='grover')
    qc.compose(state_preparation, inplace=True)

    qc.compose(operator.power(iterations), inplace=True)
    if include_measurements:
        measure(qc, q, c)

    return qc


