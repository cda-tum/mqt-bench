# Code based on https://qiskit.org/documentation/nature/tutorials/03_ground_state_solvers.html


from __future__ import annotations

from typing import TYPE_CHECKING

from qiskit.circuit.library import TwoLocal
from qiskit.exceptions import MissingOptionalLibraryError
from qiskit.primitives import Estimator
from qiskit_algorithms.minimum_eigensolvers import VQE
from qiskit_algorithms.optimizers import COBYLA
from qiskit_nature.second_q.drivers import PySCFDriver
from qiskit_nature.second_q.mappers import JordanWignerMapper

if TYPE_CHECKING:  # pragma: no cover
    from qiskit import QuantumCircuit


def create_circuit(choice: str) -> QuantumCircuit:
    """Returns a quantum circuit implementing Ground State Estimation.

    Keyword Arguments:
    molecule -- Molecule for which the ground state shall be estimated.
    """

    molecule = get_molecule(choice)

    try:
        driver = PySCFDriver(atom=molecule)
    except MissingOptionalLibraryError:
        msg = (
            "PySCF is not installed (most likely because you are on a Windows system)."
            "Please either download benchmark from https://www.cda.cit.tum.de/mqtbench/ or try to manually install PySCF."
        )
        raise ImportError(msg) from None

    es_problem = driver.run()
    mapper = JordanWignerMapper()
    second_q_op = es_problem.second_q_ops()
    operator = mapper.map(second_q_op[0])

    tl_circuit = TwoLocal(
        rotation_blocks=["h", "rx"],
        entanglement_blocks="cz",
        entanglement="full",
        reps=2,
        parameter_prefix="y",
    )

    another_solver = VQE(ansatz=tl_circuit, estimator=Estimator(), optimizer=COBYLA(maxiter=25))

    result = another_solver.compute_minimum_eigenvalue(operator)
    qc = another_solver.ansatz.assign_parameters(result.optimal_point)

    qc.name = "groundstate"
    qc.name = qc.name + "_" + choice
    qc.measure_all()

    return qc


def get_molecule(benchmark_instance_name: str) -> list[str]:
    """Returns a Molecule object depending on the parameter value."""
    m_1 = ["H 0.0 0.0 0.0", "H 0.0 0.0 0.735"]
    m_2 = ["Li 0.0 0.0 0.0", "H 0.0 0.0 2.5"]
    m_3 = ["O 0.0 0.0 0.0", "H 0.586, 0.757, 0.0", "H 0.586, -0.757, 0.0"]
    instances = {"small": m_1, "medium": m_2, "large": m_3}

    return instances[benchmark_instance_name]
