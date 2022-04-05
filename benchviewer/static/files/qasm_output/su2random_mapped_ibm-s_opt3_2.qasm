// Benchmark was created by MQT Bench on 2022-03-23
// MQT Bench version: 0.1.0
// Qiskit version: {'qiskit-terra': '0.19.2', 'qiskit-aer': '0.10.3', 'qiskit-ignis': '0.7.0', 'qiskit-ibmq-provider': '0.18.3', 'qiskit-aqua': '0.9.5', 'qiskit': '0.34.2', 'qiskit-nature': '0.3.1', 'qiskit-finance': '0.3.1', 'qiskit-optimization': '0.3.1', 'qiskit-machine-learning': '0.3.1'}
// Used Gate Set: ['id', 'rz', 'sx', 'x', 'cx', 'reset']
// Optimization Level: 3
// Coupling List: [[0, 1], [1, 0], [1, 2], [2, 1], [2, 3], [3, 2], [3, 4], [4, 3]]
// Compiled for architecture: ibm-s-fake_bogota

OPENQASM 2.0;
include "qelib1.inc";
qreg q[5];
creg meas[2];
rz(1.7809276) q[0];
sx q[0];
rz(-0.33629511) q[0];
sx q[0];
rz(-1.7013828) q[0];
rz(1.0231392) q[1];
sx q[1];
rz(-3.0616981) q[1];
sx q[1];
rz(1.9370685) q[1];
cx q[1],q[0];
rz(-0.42762547) q[0];
sx q[1];
rz(-2.8690525) q[1];
cx q[1],q[0];
rz(0.014498226) q[0];
sx q[1];
cx q[1],q[0];
rz(-2.8771551) q[0];
sx q[0];
rz(-1.7630487) q[0];
sx q[0];
rz(0.72577022) q[0];
rz(-2.1199273) q[1];
sx q[1];
rz(-2.2798503) q[1];
sx q[1];
rz(-1.9550749) q[1];
barrier q[0],q[1];
measure q[0] -> meas[0];
measure q[1] -> meas[1];
