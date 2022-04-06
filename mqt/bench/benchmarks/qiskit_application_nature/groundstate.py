# Code from https://qiskit.org/documentation/nature/tutorials/03_ground_state_solvers.html


from qiskit import Aer
from qiskit.utils import QuantumInstance
from qiskit.circuit.library import TwoLocal
from qiskit.algorithms import VQE
from qiskit.algorithms.optimizers import COBYLA


def create_circuit(molecule, basis: str = "sto3g"):
    """Returns a quantum circuit implementing Ground State Estimation.

    Keyword arguments:
    molecule -- Molecule for which the ground state shall be estimated.
    """

    try:
        from qiskit_nature.drivers import Molecule
        from qiskit_nature.drivers.second_quantization import (
            ElectronicStructureDriverType,
            ElectronicStructureMoleculeDriver,
        )
        from qiskit_nature.problems.second_quantization import (
            ElectronicStructureProblem,
        )
        from qiskit_nature.converters.second_quantization import QubitConverter
        from qiskit_nature.mappers.second_quantization import JordanWignerMapper
        from qiskit_nature.algorithms import GroundStateEigensolver
    except:
        print("Please install qiskit_nature.")
        return None

    driver = ElectronicStructureMoleculeDriver(
        molecule, basis=basis, driver_type=ElectronicStructureDriverType.PYSCF
    )

    es_problem = ElectronicStructureProblem(driver)
    qubit_converter = QubitConverter(JordanWignerMapper())

    # quantum_instance = QuantumInstance(backend=Aer.get_backend("aer_simulator_statevector"))
    # vqe_solver = VQEUCCFactory(quantum_instance)

    tl_circuit = TwoLocal(
        rotation_blocks=["h", "rx"],
        entanglement_blocks="cz",
        entanglement="full",
        reps=2,
        parameter_prefix="y",
    )

    another_solver = VQE(
        ansatz=tl_circuit,
        quantum_instance=QuantumInstance(Aer.get_backend("aer_simulator"), shots=1024),
        optimizer=COBYLA(maxiter=25),
    )

    calc = GroundStateEigensolver(qubit_converter, another_solver)
    res = calc.solve(es_problem)

    qc = another_solver.get_optimal_circuit()
    qc.name = "groundstate"
    qc.measure_all()

    return qc
