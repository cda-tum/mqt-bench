from src import utils
from src.benchmarks import ghz, dj
import pytest

@pytest.mark.parametrize("benchmark, num_qubits", [(ghz, 5), (dj, 5)])
def test_quantumcircuit_algo_layer(benchmark, num_qubits):
    qc = benchmark.create_circuit(num_qubits)
    filename_algo, depth = utils.handle_algorithm_layer(qc, num_qubits, save_png=False, save_hist=False)
    assert depth > 0

@pytest.mark.parametrize("benchmark, num_qubits", [(ghz, 5), (dj, 5)])
def test_quantumcircuit_indep_layer(benchmark, num_qubits):
    qc = benchmark.create_circuit(num_qubits)
    filename_indep, depth = utils.get_indep_layer(qc, num_qubits, save_png=False, save_hist=False)
    assert depth > 0

@pytest.mark.parametrize("benchmark, num_qubits", [(ghz, 5), (dj, 5)])
def test_quantumcircuit_native_and_mapped_layers(benchmark, num_qubits):
    qc = benchmark.create_circuit(num_qubits)
    ibm_native_gates = ['id', 'rz', 'sx', 'x', 'cx', 'reset']
    rigetti_native_gates = ['rx', 'rz', 'cz']
    gate_sets = [(ibm_native_gates, "ibm"), (rigetti_native_gates, "rigetti")]
    for (gate_set, gate_set_name) in gate_sets:
        for opt_level in range(4):
            filename_indep, depth_native, n_actual = utils.get_transpiled_layer(qc, gate_set, gate_set_name,
                                                           opt_level, num_qubits, save_png=False, save_hist=False,
                                                           file_precheck=False)
            assert depth_native > 0
            filename_mapped, depth_mapped = utils.get_mapped_layer(qc, gate_set, gate_set_name, opt_level, n_actual,
                             False, save_png=False, save_hist=False, file_precheck=False)
            assert depth_mapped > 0

