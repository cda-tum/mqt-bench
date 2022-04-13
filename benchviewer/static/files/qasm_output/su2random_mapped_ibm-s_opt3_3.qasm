// Benchmark was created by MQT Bench on 2022-04-10
// For more information about MQT Bench, please visit https://www.cda.cit.tum.de/mqtbench/
// MQT Bench version: 0.1.0
// Qiskit version: {'qiskit-terra': '0.19.2', 'qiskit-aer': '0.10.3', 'qiskit-ignis': '0.7.0', 'qiskit-ibmq-provider': '0.18.3', 'qiskit-aqua': '0.9.5', 'qiskit': '0.34.2', 'qiskit-nature': '0.3.1', 'qiskit-finance': '0.3.1', 'qiskit-optimization': '0.3.1', 'qiskit-machine-learning': '0.3.1'}
// Used Gate Set: ['id', 'rz', 'sx', 'x', 'cx', 'reset']
// Optimization Level: 3
// Coupling List: [[0, 1], [1, 0], [1, 2], [2, 1], [2, 3], [3, 2], [3, 4], [4, 3]]
// Compiled for architecture: ibm-s-fake_bogota

OPENQASM 2.0;
include "qelib1.inc";
qreg q[5];
creg meas[3];
sx q[1];
rz(-2.2541797) q[1];
sx q[1];
rz(-2.7284322) q[1];
sx q[2];
rz(-2.7927306) q[2];
sx q[2];
rz(-2.5159915) q[2];
sx q[3];
rz(-2.6398978) q[3];
sx q[3];
rz(-2.3286298) q[3];
cx q[2],q[3];
cx q[2],q[1];
sx q[2];
rz(-2.4008653) q[2];
sx q[2];
rz(-2.6313171) q[2];
cx q[2],q[3];
cx q[3],q[2];
cx q[2],q[3];
cx q[2],q[1];
sx q[1];
rz(-3.0595415) q[1];
sx q[1];
rz(-2.4475745) q[1];
sx q[2];
rz(-2.8444099) q[2];
sx q[2];
rz(-2.5099782) q[2];
cx q[3],q[2];
cx q[1],q[2];
cx q[2],q[1];
sx q[1];
rz(0.74622122) q[1];
sx q[1];
rz(-0.17690119) q[1];
cx q[3],q[2];
sx q[2];
rz(-2.7749109) q[2];
sx q[2];
rz(-3.0179789) q[2];
sx q[3];
rz(-2.3708396) q[3];
sx q[3];
rz(-2.2799337) q[3];
cx q[2],q[3];
cx q[3],q[2];
rz(-1.8993947) q[2];
sx q[2];
cx q[1],q[2];
sx q[1];
rz(-pi/2) q[1];
sx q[1];
rz(pi/2) q[2];
cx q[1],q[2];
rz(-0.69798877) q[1];
sx q[1];
rz(-1.3550786) q[1];
sx q[1];
rz(2.034463) q[1];
rz(-pi/2) q[2];
sx q[2];
rz(-pi) q[2];
cx q[2],q[3];
sx q[2];
rz(-3.0085465) q[2];
sx q[2];
rz(-2.3621092) q[2];
sx q[3];
rz(-2.8460836) q[3];
sx q[3];
rz(-2.9217328) q[3];
barrier q[4],q[1],q[2],q[0],q[3];
measure q[1] -> meas[0];
measure q[2] -> meas[1];
measure q[3] -> meas[2];
