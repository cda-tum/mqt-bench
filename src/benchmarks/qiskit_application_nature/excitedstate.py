## Code from https://qiskit.org/documentation/nature/tutorials/04_excited_states_solvers.html

from qiskit_nature.drivers import UnitsType, Molecule
from qiskit_nature.drivers.second_quantization import (
    ElectronicStructureDriverType,
    ElectronicStructureMoleculeDriver,
)
from qiskit_nature.problems.second_quantization import ElectronicStructureProblem
from qiskit_nature.converters.second_quantization import QubitConverter
from qiskit_nature.mappers.second_quantization import JordanWignerMapper

from qiskit import Aer
from qiskit.utils import QuantumInstance
from qiskit_nature.algorithms import GroundStateEigensolver, QEOM, VQEUCCFactory

def create_circuit(molecule_choice:int):

    molecule = Molecule(
        geometry=[["H", [0.0, 0.0, 0.0]], ["H", [0.0, 0.0, 0.735]]], charge=0, multiplicity=1
    )
    driver = ElectronicStructureMoleculeDriver(
        molecule, basis="sto3g", driver_type=ElectronicStructureDriverType.PYSCF
    )

    es_problem = ElectronicStructureProblem(driver)
    qubit_converter = QubitConverter(JordanWignerMapper())


    # This first part sets the ground state solver
    # see more about this part in the ground state calculation tutorial
    quantum_instance = QuantumInstance(Aer.get_backend("aer_simulator_statevector"))
    solver = VQEUCCFactory(quantum_instance)
    gsc = GroundStateEigensolver(qubit_converter, solver)

    # The qEOM algorithm is simply instantiated with the chosen ground state solver
    qeom_excited_states_calculation = QEOM(gsc, "sd")

    qeom_results = qeom_excited_states_calculation.solve(es_problem)

    qc = solver.get_solver(es_problem, qubit_converter).get_optimal_circuit()
    qc.name = "groundstate"

    print(qeom_results)

    return qc