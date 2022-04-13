// Benchmark was created by MQT Bench on 2022-04-07
// For more information about MQT Bench, please visit https://www.cda.cit.tum.de/mqtbench/
// MQT Bench version: 0.1.0
// Qiskit version: {'qiskit-terra': '0.19.2', 'qiskit-aer': '0.10.3', 'qiskit-ignis': '0.7.0', 'qiskit-ibmq-provider': '0.18.3', 'qiskit-aqua': '0.9.5', 'qiskit': '0.34.2', 'qiskit-nature': '0.3.1', 'qiskit-finance': '0.3.1', 'qiskit-optimization': '0.3.1', 'qiskit-machine-learning': '0.3.1'}
// Used Gate Set: ['id', 'rz', 'sx', 'x', 'cx', 'reset']
// Optimization Level: 2
// Coupling List: [[0, 1], [1, 0], [1, 2], [2, 1], [2, 3], [3, 2], [3, 4], [4, 3]]
// Compiled for architecture: ibm-s-fake_bogota

OPENQASM 2.0;
include "qelib1.inc";
qreg q[5];
creg meas[3];
sx q[0];
rz(-2.0072142) q[0];
sx q[0];
sx q[1];
rz(2.3591575) q[1];
sx q[1];
rz(-pi) q[2];
sx q[2];
rz(2.649309) q[2];
sx q[2];
cx q[2],q[1];
rz(pi/2) q[1];
sx q[1];
rz(pi/2) q[1];
cx q[1],q[2];
cx q[2],q[1];
cx q[1],q[0];
cx q[2],q[1];
cx q[1],q[2];
cx q[1],q[0];
sx q[0];
rz(2.4841065) q[0];
sx q[0];
sx q[1];
rz(-2.7284533) q[1];
sx q[1];
sx q[2];
rz(1.5141149) q[2];
sx q[2];
cx q[2],q[1];
rz(pi/2) q[1];
sx q[1];
rz(pi/2) q[1];
cx q[0],q[1];
cx q[1],q[0];
cx q[0],q[1];
rz(pi/2) q[1];
sx q[1];
rz(pi/2) q[1];
cx q[2],q[1];
cx q[0],q[1];
sx q[0];
rz(-2.1048813) q[0];
sx q[0];
sx q[1];
rz(-0.45097347) q[1];
sx q[1];
sx q[2];
rz(1.6775536) q[2];
sx q[2];
cx q[1],q[2];
cx q[2],q[1];
cx q[1],q[2];
cx q[1],q[0];
rz(pi/2) q[0];
sx q[0];
rz(-pi/2) q[0];
rz(pi/2) q[2];
sx q[2];
rz(pi/2) q[2];
cx q[1],q[2];
rz(pi/2) q[2];
sx q[2];
rz(pi/2) q[2];
cx q[1],q[2];
cx q[2],q[1];
cx q[1],q[2];
rz(pi/2) q[1];
sx q[1];
rz(pi/2) q[1];
cx q[0],q[1];
sx q[0];
rz(1.3167398) q[0];
sx q[0];
sx q[1];
rz(3.0286856) q[1];
sx q[1];
sx q[2];
rz(1.2405549) q[2];
sx q[2];
rz(-pi) q[2];
barrier q[3],q[4],q[0],q[2],q[1];
measure q[2] -> meas[0];
measure q[0] -> meas[1];
measure q[1] -> meas[2];
