// Benchmark was created by MQT Bench on 2022-04-08
// For more information about MQT Bench, please visit https://www.cda.cit.tum.de/mqtbench/
// MQT Bench version: 0.1.0
// Qiskit version: {'qiskit-terra': '0.19.2', 'qiskit-aer': '0.10.3', 'qiskit-ignis': '0.7.0', 'qiskit-ibmq-provider': '0.18.3', 'qiskit-aqua': '0.9.5', 'qiskit': '0.34.2', 'qiskit-nature': '0.3.1', 'qiskit-finance': '0.3.1', 'qiskit-optimization': '0.3.1', 'qiskit-machine-learning': '0.3.1'}
// Used Gate Set: ['id', 'rz', 'sx', 'x', 'cx', 'reset']
// Optimization Level: 2

OPENQASM 2.0;
include "qelib1.inc";
qreg q[3];
creg meas[3];
rz(-pi) q[0];
sx q[0];
rz(2.4736605) q[0];
sx q[0];
rz(-pi) q[1];
sx q[1];
rz(2.225878) q[1];
sx q[1];
cx q[0],q[1];
rz(-pi) q[2];
sx q[2];
rz(2.4655279) q[2];
sx q[2];
cx q[0],q[2];
rz(-pi) q[0];
sx q[0];
rz(2.7442527) q[0];
sx q[0];
cx q[1],q[2];
rz(-pi) q[1];
sx q[1];
rz(2.8298311) q[1];
sx q[1];
cx q[0],q[1];
rz(-pi) q[2];
sx q[2];
rz(2.7373629) q[2];
sx q[2];
cx q[0],q[2];
rz(-pi) q[0];
sx q[0];
rz(2.5509229) q[0];
sx q[0];
cx q[1],q[2];
rz(-pi) q[1];
sx q[1];
rz(2.1876967) q[1];
sx q[1];
cx q[0],q[1];
rz(-pi) q[2];
sx q[2];
rz(2.6906109) q[2];
sx q[2];
cx q[0],q[2];
rz(-pi) q[0];
sx q[0];
rz(2.6733379) q[0];
sx q[0];
cx q[1],q[2];
rz(-pi) q[1];
sx q[1];
rz(2.4062212) q[1];
sx q[1];
rz(-pi) q[2];
sx q[2];
rz(3.0384809) q[2];
sx q[2];
barrier q[0],q[1],q[2];
measure q[0] -> meas[0];
measure q[1] -> meas[1];
measure q[2] -> meas[2];
