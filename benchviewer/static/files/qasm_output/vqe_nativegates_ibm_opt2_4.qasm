// Benchmark was created by MQT Bench on 2022-04-12
// For more information about MQT Bench, please visit https://www.cda.cit.tum.de/mqtbench/
// MQT Bench version: 0.1.0
// Qiskit version: {'qiskit-terra': '0.19.2', 'qiskit-aer': '0.10.3', 'qiskit-ignis': '0.7.0', 'qiskit-ibmq-provider': '0.18.3', 'qiskit-aqua': '0.9.5', 'qiskit': '0.34.2', 'qiskit-nature': '0.3.1', 'qiskit-finance': '0.3.1', 'qiskit-optimization': '0.3.1', 'qiskit-machine-learning': '0.3.1'}
// Used Gate Set: ['id', 'rz', 'sx', 'x', 'cx', 'reset']
// Optimization Level: 2

OPENQASM 2.0;
include "qelib1.inc";
qreg q[4];
creg meas[4];
rz(-pi) q[0];
sx q[0];
rz(1.6794632) q[0];
sx q[0];
sx q[1];
rz(2.1733192) q[1];
sx q[1];
rz(-pi) q[1];
cx q[0],q[1];
rz(-pi) q[2];
sx q[2];
rz(1.8974481) q[2];
sx q[2];
cx q[0],q[2];
cx q[1],q[2];
sx q[3];
rz(0.54218182) q[3];
sx q[3];
rz(-pi) q[3];
cx q[0],q[3];
rz(-pi) q[0];
sx q[0];
rz(2.0144898) q[0];
sx q[0];
cx q[1],q[3];
sx q[1];
rz(1.4767679) q[1];
sx q[1];
rz(-pi) q[1];
cx q[0],q[1];
cx q[2],q[3];
rz(-pi) q[2];
sx q[2];
rz(1.5556909) q[2];
sx q[2];
cx q[0],q[2];
cx q[1],q[2];
sx q[3];
rz(2.1540109) q[3];
sx q[3];
rz(-pi) q[3];
cx q[0],q[3];
sx q[0];
rz(1.0740423) q[0];
sx q[0];
rz(-pi) q[0];
cx q[1],q[3];
rz(-pi) q[1];
sx q[1];
rz(1.556308) q[1];
sx q[1];
cx q[2],q[3];
rz(-pi) q[2];
sx q[2];
rz(1.1100311) q[2];
sx q[2];
sx q[3];
rz(0.02618369) q[3];
sx q[3];
rz(-pi) q[3];
barrier q[0],q[1],q[2],q[3];
measure q[0] -> meas[0];
measure q[1] -> meas[1];
measure q[2] -> meas[2];
measure q[3] -> meas[3];
