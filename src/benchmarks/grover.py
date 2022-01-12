from qiskit import QuantumCircuit, QuantumRegister, AncillaRegister
from qiskit.circuit.library import GroverOperator
from qiskit.qasm import pi
from qiskit.algorithms import Grover

# checked

def create_circuit(n: int, ancillary_mode: str = 'noancilla'):
    n = n - 1  # magic number due to the flag qubit
    q = QuantumRegister(n, 'q')
    flag = AncillaRegister(1, 'flag')

    state_preparation = QuantumCircuit(q, flag)
    state_preparation.h(q)
    state_preparation.x(flag)

    oracle = QuantumCircuit(q, flag)
    oracle.mcp(pi, q, flag)

    operator = GroverOperator(oracle, mcx_mode=ancillary_mode)
    iterations = Grover.optimal_num_iterations(1, n)

    num_qubits = operator.num_qubits

    # num_qubits may differe now depending on the mcx_mode

    q2 = QuantumRegister(num_qubits, 'q')
    qc = QuantumCircuit(q2, flag, name='grover')
    qc.compose(state_preparation, inplace=True)

    qc.compose(operator.power(iterations), inplace=True)
    qc.measure_all()

    return qc


