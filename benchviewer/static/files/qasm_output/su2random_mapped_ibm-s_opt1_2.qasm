// Benchmark was created by MQT Bench on 2022-04-10
// For more information about MQT Bench, please visit https://www.cda.cit.tum.de/mqtbench/
// MQT Bench version: 0.1.0
// Qiskit version: {'qiskit-terra': '0.19.2', 'qiskit-aer': '0.10.3', 'qiskit-ignis': '0.7.0', 'qiskit-ibmq-provider': '0.18.3', 'qiskit-aqua': '0.9.5', 'qiskit': '0.34.2', 'qiskit-nature': '0.3.1', 'qiskit-finance': '0.3.1', 'qiskit-optimization': '0.3.1', 'qiskit-machine-learning': '0.3.1'}
// Used Gate Set: ['id', 'rz', 'sx', 'x', 'cx', 'reset']
// Optimization Level: 1
// Coupling List: [[0, 1], [1, 0], [1, 2], [2, 1], [2, 3], [3, 2], [3, 4], [4, 3]]
// Compiled for architecture: ibm-s-fake_bogota

OPENQASM 2.0;
include "qelib1.inc";
qreg q[5];
creg meas[2];
sx q[0];
rz(-2.1632116) q[0];
sx q[0];
rz(-2.1998708) q[0];
sx q[1];
rz(-2.5296223) q[1];
sx q[1];
rz(-2.5619687) q[1];
cx q[0],q[1];
sx q[0];
rz(-2.2159169) q[0];
sx q[0];
rz(-2.2680618) q[0];
sx q[1];
rz(-3.0542003) q[1];
sx q[1];
rz(-2.9562523) q[1];
cx q[0],q[1];
sx q[0];
rz(-3.0573236) q[0];
sx q[0];
rz(-2.9404197) q[0];
sx q[1];
rz(-3.1025201) q[1];
sx q[1];
rz(-2.715443) q[1];
cx q[0],q[1];
sx q[0];
rz(-2.8801165) q[0];
sx q[0];
rz(-2.1869475) q[0];
sx q[1];
rz(-3.062073) q[1];
sx q[1];
rz(-2.6331289) q[1];
barrier q[0],q[1];
measure q[0] -> meas[0];
measure q[1] -> meas[1];
