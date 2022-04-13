// Benchmark was created by MQT Bench on 2022-04-11
// For more information about MQT Bench, please visit https://www.cda.cit.tum.de/mqtbench/
// MQT Bench version: 0.1.0
// Qiskit version: {'qiskit-terra': '0.19.2', 'qiskit-aer': '0.10.3', 'qiskit-ignis': '0.7.0', 'qiskit-ibmq-provider': '0.18.3', 'qiskit-aqua': '0.9.5', 'qiskit': '0.34.2', 'qiskit-nature': '0.3.1', 'qiskit-finance': '0.3.1', 'qiskit-optimization': '0.3.1', 'qiskit-machine-learning': '0.3.1'}
// Used Gate Set: ['id', 'rz', 'sx', 'x', 'cx', 'reset']
// Optimization Level: 3

OPENQASM 2.0;
include "qelib1.inc";
qreg q[3];
creg meas[3];
rz(-pi) q[0];
sx q[0];
rz(2.3639052) q[0];
sx q[0];
rz(-pi) q[1];
sx q[1];
rz(3.0878307) q[1];
sx q[1];
cx q[0],q[1];
rz(-pi) q[2];
sx q[2];
rz(2.4980317) q[2];
sx q[2];
cx q[0],q[2];
rz(-pi) q[0];
sx q[0];
rz(3.0793106) q[0];
sx q[0];
cx q[1],q[2];
rz(-pi) q[1];
sx q[1];
rz(2.384795) q[1];
sx q[1];
cx q[0],q[1];
rz(-pi) q[2];
sx q[2];
rz(2.5375325) q[2];
sx q[2];
cx q[0],q[2];
rz(-pi) q[0];
sx q[0];
rz(2.6830873) q[0];
sx q[0];
cx q[1],q[2];
rz(-pi) q[1];
sx q[1];
rz(2.3300639) q[1];
sx q[1];
cx q[0],q[1];
rz(-pi) q[2];
sx q[2];
rz(2.333188) q[2];
sx q[2];
cx q[0],q[2];
rz(-pi) q[0];
sx q[0];
rz(2.279601) q[0];
sx q[0];
cx q[1],q[2];
rz(-pi) q[1];
sx q[1];
rz(2.7682824) q[1];
sx q[1];
rz(-pi) q[2];
sx q[2];
rz(2.7636112) q[2];
sx q[2];
barrier q[0],q[1],q[2];
measure q[0] -> meas[0];
measure q[1] -> meas[1];
measure q[2] -> meas[2];
