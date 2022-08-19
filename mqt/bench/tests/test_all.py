from mqt.bench.utils import utils, qiskit_helper, tket_helper
from mqt.bench.benchmarks import (
    ghz,
    dj,
    ae,
    graphstate,
    grover,
    hhl,
    qaoa,
    qft,
    qftentangled,
    qpeinexact,
    qpeexact,
    vqe,
    realamprandom,
    su2random,
    twolocalrandom,
    qwalk,
    wstate,
    shor,
)
from mqt.bench.benchmarks.qiskit_application_finance import (
    pricingcall,
    pricingput,
    portfoliovqe,
    portfolioqaoa,
)
from mqt.bench.benchmarks.qiskit_application_ml import qgan
from mqt.bench.benchmarks.qiskit_application_nature import groundstate, excitedstate
from mqt.bench.benchmarks.qiskit_application_optimization import tsp, routing
from qiskit_nature.drivers import Molecule
from qiskit import QuantumCircuit
from pytket.qasm import circuit_to_qasm_str
from mqt.bench.benchmark_generator import get_one_benchmark

import pytest
import os


def test_configure_begin():
    test_qasm_output_path = "./test_output/"
    if not os.path.exists(test_qasm_output_path):
        os.mkdir(test_qasm_output_path)
    utils.set_qasm_output_path(test_qasm_output_path)
    assert utils.get_qasm_output_path() == test_qasm_output_path


@pytest.mark.parametrize(
    "benchmark, input_value, scalable",
    [
        (ae, 8, True),
        (ghz, 5, True),
        (dj, 5, True),
        (graphstate, 8, True),
        (grover, 5, False),
        (hhl, 2, False),
        (qaoa, 5, True),
        (qft, 8, True),
        (qftentangled, 8, True),
        (qpeexact, 8, True),
        (qpeinexact, 8, True),
        (tsp, 3, False),
        (qwalk, 5, False),
        (vqe, 5, True),
        (realamprandom, 9, True),
        (su2random, 7, True),
        (twolocalrandom, 8, True),
        (wstate, 8, True),
        (portfolioqaoa, 5, True),
        # (shor, 15, False),
        (portfoliovqe, 5, True),
        (pricingcall, 5, False),
        (pricingput, 5, False),
        (qgan, 5, True),
    ],
)
def test_quantumcircuit_indep_level(benchmark, input_value, scalable):
    if benchmark == grover or benchmark == qwalk:
        qc = benchmark.create_circuit(input_value, ancillary_mode="noancilla")
    else:
        qc = benchmark.create_circuit(input_value)
    if scalable:
        assert qc.num_qubits == input_value
    res = qiskit_helper.get_indep_level(qc, input_value, file_precheck=False)
    assert res
    res = qiskit_helper.get_indep_level(qc, input_value, file_precheck=True)
    assert res

    res = tket_helper.get_indep_level(qc, input_value, file_precheck=False)
    assert res
    res = tket_helper.get_indep_level(qc, input_value, file_precheck=True)
    assert res


@pytest.mark.parametrize(
    "benchmark, input_value, scalable",
    [
        (ae, 8, True),
        (ghz, 5, True),
        (dj, 5, True),
        (graphstate, 8, True),
        (grover, 5, False),
        # (hhl, 2, False),
        (qaoa, 5, True),
        (qft, 8, True),
        (qftentangled, 8, True),
        (qpeexact, 8, True),
        (qpeinexact, 8, True),
        (tsp, 3, False),
        (qwalk, 5, False),
        (vqe, 5, True),
        (realamprandom, 3, True),
        (su2random, 7, True),
        (twolocalrandom, 5, True),
        (wstate, 8, True),
        (portfolioqaoa, 5, True),
        # (shor, 15, False),
        (portfoliovqe, 5, True),
        (pricingcall, 5, False),
        (pricingput, 5, False),
        (qgan, 5, True),
    ],
)
def test_quantumcircuit_native_and_mapped_levels(benchmark, input_value, scalable):
    if benchmark == grover or benchmark == qwalk:
        qc = benchmark.create_circuit(input_value, ancillary_mode="noancilla")
    else:
        qc = benchmark.create_circuit(input_value)
    if scalable:
        assert qc.num_qubits == input_value

    compilation_paths = [
        ("ibm", [("ibm_washington", 127), ("ibm_montreal", 27)]),
        ("rigetti", [("rigetti_aspen_m1", 80)]),
        ("ionq", [("ionq11", 11)]),
        ("oqc", [("oqc_lucy", 8)]),
    ]
    for gate_set_name, devices in compilation_paths:
        opt_level = 1
        res = qiskit_helper.get_native_gates_level(
            qc,
            gate_set_name,
            qc.num_qubits,
            opt_level,
            file_precheck=False,
        )
        assert res
        res = qiskit_helper.get_native_gates_level(
            qc,
            gate_set_name,
            qc.num_qubits,
            opt_level,
            file_precheck=True,
        )
        assert res
        if gate_set_name != "ionq":
            for device_name, max_qubits in devices:
                # Creating the circuit on target-dependent: mapped level qiskit
                if max_qubits >= qc.num_qubits:
                    res = qiskit_helper.get_mapped_level(
                        qc,
                        gate_set_name,
                        qc.num_qubits,
                        device_name,
                        opt_level,
                        file_precheck=False,
                    )
                    assert res
                    res = qiskit_helper.get_mapped_level(
                        qc,
                        gate_set_name,
                        qc.num_qubits,
                        device_name,
                        opt_level,
                        file_precheck=True,
                    )
                    assert res

    for gate_set_name, devices in compilation_paths:
        res = tket_helper.get_native_gates_level(
            qc,
            gate_set_name,
            qc.num_qubits,
            file_precheck=False,
        )
        assert res
        res = tket_helper.get_native_gates_level(
            qc,
            gate_set_name,
            qc.num_qubits,
            file_precheck=True,
        )
        assert res
        if gate_set_name != "ionq":
            for device_name, max_qubits in devices:
                # Creating the circuit on target-dependent: mapped level qiskit
                if max_qubits >= qc.num_qubits:
                    res = tket_helper.get_mapped_level(
                        qc,
                        gate_set_name,
                        qc.num_qubits,
                        device_name,
                        True,
                        file_precheck=False,
                    )
                    assert res
                    res = tket_helper.get_mapped_level(
                        qc,
                        gate_set_name,
                        qc.num_qubits,
                        device_name,
                        False,
                        file_precheck=True,
                    )
                    assert res


def test_openqasm_gates():
    openqasm_gates = utils.get_openqasm_gates()
    assert len(openqasm_gates) == 42


@pytest.mark.parametrize("num_circles", [2, 3, 4, 5, 10])
def test_rigetti_cmap_generator(num_circles: int):
    if num_circles != 10:
        assert (
            len(utils.get_rigetti_c_map(num_circles))
            == (10 * (num_circles - 1) + 8) * 2
        )
    else:
        assert len(utils.get_rigetti_c_map(num_circles)) == 212


def test_dj_constant_oracle():
    qc = dj.create_circuit(5, False)
    assert qc.depth() > 0


@pytest.mark.skip(reason="Takes really long")
def test_ground_and_excited_state():
    m_1 = Molecule(
        geometry=[["Li", [0.0, 0.0, 0.0]], ["H", [0.0, 0.0, 2.5]]],
        charge=0,
        multiplicity=1,
    )
    qc = groundstate.create_circuit(m_1)
    assert qc.depth() > 0

    qc = excitedstate.create_circuit(m_1)
    assert qc.depth() > 0


def test_routing():
    qc = routing.create_circuit(4, 2)
    assert qc.depth() > 0


@pytest.mark.parametrize(
    "benchmark_name, level, circuit_size, benchmark_instance_name, compiler, compiler_settings, gate_set_name, device_name,",
    [
        ("dj", "alg", 5, None, "qiskit", 1, None, None),
        ("wstate", 0, 6, None, "qiskit", 2, None, None),
        ("wstate", 0, 6, None, "tket", True, None, None),
        ("wstate", 0, 6, None, "tket", False, None, None),
        ("ghz", "indep", 5, None, "qiskit", 3, None, None),
        ("graphstate", 1, 4, None, "qiskit", 0, None, None),
        ("graphstate", 1, 4, None, "tket", True, None, None),
        ("graphstate", 1, 4, None, "tket", False, None, None),
        ("groundstate", 1, 4, "small", "qiskit", 1, None, None),
        ("dj", "nativegates", 5, None, "qiskit", 2, "ionq", None),
        ("dj", "nativegates", 5, None, "qiskit", 2, "ibm", None),
        ("dj", "nativegates", 5, None, "qiskit", 2, "rigetti", None),
        ("dj", "nativegates", 5, None, "qiskit", 2, "oqc", None),
        ("qft", 2, 6, None, "qiskit", 3, "ionq", None),
        ("qft", 2, 6, None, "qiskit", 3, "ibm", None),
        ("qft", 2, 6, None, "tket", False, "rigetti", None),
        ("qft", 2, 6, None, "tket", True, "oqc", None),
        ("qpeexact", "mapped", 5, None, "qiskit", 1, "ibm", "ibm_washington"),
        ("qpeexact", "mapped", 5, None, "qiskit", 1, "ibm", "ibm_montreal"),
        ("qpeexact", "mapped", 5, None, "qiskit", 1, "rigetti", "rigetti_aspen_m1"),
        ("qpeexact", "mapped", 5, None, "qiskit", 1, "ionq", "ionq11"),
        ("qpeexact", "mapped", 5, None, "qiskit", 1, "oqc", "oqc_lucy"),
        ("qpeinexact", 3, 4, None, "qiskit", 1, "ibm", "ibm_washington"),
        ("qpeinexact", 3, 4, None, "tket", True, "ibm", "ibm_washington"),
        ("qpeinexact", 3, 4, None, "qiskit", 1, "ibm", "ibm_montreal"),
        ("qpeinexact", 3, 4, None, "tket", False, "ibm", "ibm_montreal"),
        ("qpeinexact", 3, 4, None, "qiskit", 1, "rigetti", "rigetti_aspen_m1"),
        ("qpeinexact", 3, 4, None, "tket", True, "rigetti", "rigetti_aspen_m1"),
        ("qpeinexact", 3, 4, None, "qiskit", 1, "oqc", "oqc_lucy"),
        ("qpeinexact", 3, 4, None, "tket", False, "oqc", "oqc_lucy"),
    ],
)
def test_get_one_benchmark(
    benchmark_name,
    level,
    circuit_size,
    benchmark_instance_name,
    compiler,
    compiler_settings,
    gate_set_name,
    device_name,
):

    qc = get_one_benchmark(
        benchmark_name,
        level,
        circuit_size,
        benchmark_instance_name,
        compiler,
        compiler_settings,
        gate_set_name,
        device_name,
    )
    assert qc.depth() > 0
    if gate_set_name and "oqc" not in gate_set_name:
        if compiler == "tket":
            qc = QuantumCircuit.from_qasm_str(circuit_to_qasm_str(qc))
        for instruction, qargs, cargs in qc.data:
            gate_type = instruction.name
            assert (
                gate_type in qiskit_helper.get_native_gates(gate_set_name)
                or gate_type == "barrier"
            )


def test_configure_end():
    test_qasm_output_path = "./test_output/"
    for f in os.listdir(test_qasm_output_path):
        os.remove(os.path.join(test_qasm_output_path, f))
    os.rmdir(test_qasm_output_path)
    utils.set_qasm_output_path()
