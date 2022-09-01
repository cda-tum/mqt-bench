# Code based on https://qiskit.org/documentation/nature/tutorials/03_ground_state_solvers.html


from __future__ import annotations

from qiskit import Aer
from qiskit.algorithms import VQE
from qiskit.algorithms.optimizers import COBYLA
from qiskit.circuit.library import TwoLocal
from qiskit.utils import QuantumInstance
from qiskit_nature.converters.second_quantization import QubitConverter
from qiskit_nature.drivers.second_quantization import (
    ElectronicStructureDriverType,
    ElectronicStructureMoleculeDriver,
)
from qiskit_nature.mappers.second_quantization import JordanWignerMapper
from qiskit_nature.problems.second_quantization import ElectronicStructureProblem


def create_circuit(molecule, basis: str = "sto3g"):
    """Returns a quantum circuit implementing Ground State Estimation.

    Keyword arguments:
    molecule -- Molecule for which the ground state shall be estimated.
    """

    driver = ElectronicStructureMoleculeDriver(
        molecule, basis=basis, driver_type=ElectronicStructureDriverType.PYSCF
    )

    es_problem = ElectronicStructureProblem(driver)
    qubit_converter = QubitConverter(JordanWignerMapper())
    second_q_op = es_problem.second_q_ops()
    operator = qubit_converter.convert_only(second_q_op[0])

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

    result = another_solver.compute_minimum_eigenvalue(operator)
    qc = another_solver.ansatz.bind_parameters(result.optimal_point)

    qc.name = "groundstate"
    qc.measure_all()

    return qc
