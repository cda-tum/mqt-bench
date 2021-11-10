## Code from http://localhost:8888/notebooks/Downloads/qiskit-application-modules-demo-sessions/qiskit-finance/Introduction%20to%20Qiskit%20Finance.ipynb

from utils import get_examplary_max_cut_qp
from qiskit.algorithms import VQE
from qiskit.algorithms.optimizers import SLSQP
from qiskit_optimization.algorithms import MinimumEigenOptimizer
from qiskit.circuit.library import RealAmplitudes

def create_circuit(n: int, include_measurements: bool = True):
    qp = get_examplary_max_cut_qp(n)

    sim = Aer.get_backend("qasm_simulator")
    ansatz = RealAmplitudes(3, reps=2)


    vqe = VQE(ansatz, optimizer=SLSQP(), quantum_instance=sim)
    vqe_optimizer = MinimumEigenOptimizer(vqe)
    vqe_result = vqe_optimizer.solve(qp)
    print(vqe_result)
    qc = vqe.get_optimal_circuit()

    if (include_measurements): qc.measure_all()
    qc.name="VQE"

    return qc





## Code from https://qiskit.org/textbook/ch-applications/vqe-molecules.html

from qiskit import Aer

# molecule = Molecule(geometry=[['H', [0., 0., 0.]],
#                               ['H', [0., 0., 0.735]]],
#                      charge=0, multiplicity=1)
# driver = ElectronicStructureMoleculeDriver(molecule, basis='sto3g', driver_type=ElectronicStructureDriverType.PYSCF)
#
# es_problem = ElectronicStructureProblem(driver)
# qubit_converter = QubitConverter(JordanWignerMapper())
#
# from qiskit.providers.aer import StatevectorSimulator
# from qiskit import Aer
# from qiskit.utils import QuantumInstance
# from qiskit_nature.algorithms import VQEUCCFactory
#
# quantum_instance = QuantumInstance(backend = Aer.get_backend('aer_simulator_statevector'))
# vqe_solver = VQEUCCFactory(quantum_instance)
#
# from qiskit_nature.algorithms import GroundStateEigensolver
#
# calc = GroundStateEigensolver(qubit_converter, vqe_solver)
# res = calc.solve(es_problem)
#
#
# print(res)