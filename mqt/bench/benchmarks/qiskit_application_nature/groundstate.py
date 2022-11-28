# Code based on https://qiskit.org/documentation/nature/tutorials/03_ground_state_solvers.html


from __future__ import annotations

from qiskit.algorithms.minimum_eigensolvers import VQE
from qiskit.algorithms.optimizers import COBYLA
from qiskit.circuit.library import TwoLocal
from qiskit.primitives import Estimator
from qiskit_nature.second_q.drivers import PySCFDriver
from qiskit_nature.second_q.mappers import JordanWignerMapper, QubitConverter


def create_circuit(molecule):
    """Returns a quantum circuit implementing Ground State Estimation.

    Keyword arguments:
    molecule -- Molecule for which the ground state shall be estimated.
    """

    driver = PySCFDriver(atom=molecule)
    es_problem = driver.run()

    converter = QubitConverter(JordanWignerMapper())
    second_q_op = es_problem.second_q_ops()
    operator = converter.convert_only(second_q_op[0])

    tl_circuit = TwoLocal(
        rotation_blocks=["h", "rx"],
        entanglement_blocks="cz",
        entanglement="full",
        reps=2,
        parameter_prefix="y",
    )

    another_solver = VQE(
        ansatz=tl_circuit, estimator=Estimator(), optimizer=COBYLA(maxiter=25)
    )

    result = another_solver.compute_minimum_eigenvalue(operator)
    qc = another_solver.ansatz.bind_parameters(result.optimal_point)

    qc.name = "groundstate"
    qc.measure_all()

    return qc
