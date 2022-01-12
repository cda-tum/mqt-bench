## Code from https://qiskit.org/documentation/nature/tutorials/03_ground_state_solvers.html

from qiskit_nature.drivers import Molecule
from qiskit_nature.drivers.second_quantization import (
    ElectronicStructureDriverType,
    ElectronicStructureMoleculeDriver,
)
from qiskit_nature.problems.second_quantization import ElectronicStructureProblem
from qiskit_nature.converters.second_quantization import QubitConverter
from qiskit_nature.mappers.second_quantization import JordanWignerMapper

from qiskit import Aer
from qiskit.utils import QuantumInstance
from qiskit_nature.algorithms import VQEUCCFactory
from qiskit_nature.algorithms import GroundStateEigensolver

def create_circuit(molecule_choice:int):


    molecule = Molecule(
        geometry=[["H", [0.0, 0.0, 0.0]], ["H", [0.0, 0.0, 0.735]]], charge=0, multiplicity=1
    )
    driver = ElectronicStructureMoleculeDriver(
        molecule, basis="sto3g", driver_type=ElectronicStructureDriverType.PYSCF
    )

    es_problem = ElectronicStructureProblem(driver)
    qubit_converter = QubitConverter(JordanWignerMapper())

    quantum_instance = QuantumInstance(backend=Aer.get_backend("aer_simulator_statevector"))
    vqe_solver = VQEUCCFactory(quantum_instance)


    calc = GroundStateEigensolver(qubit_converter, vqe_solver)
    res = calc.solve(es_problem)

    qc = vqe_solver.get_solver(es_problem, qubit_converter).get_optimal_circuit()
    qc.name = "groundstate"

    print(res)

    return qc