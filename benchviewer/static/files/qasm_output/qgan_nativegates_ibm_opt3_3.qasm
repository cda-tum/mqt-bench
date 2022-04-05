// Benchmark was created by MQT Bench on 2022-03-24
// MQT Bench version: 0.1.0
// Qiskit version: {'qiskit-terra': '0.19.2', 'qiskit-aer': '0.10.3', 'qiskit-ignis': '0.7.0', 'qiskit-ibmq-provider': '0.18.3', 'qiskit-aqua': '0.9.5', 'qiskit': '0.34.2', 'qiskit-nature': '0.3.1', 'qiskit-finance': '0.3.1', 'qiskit-optimization': '0.3.1', 'qiskit-machine-learning': '0.3.1'}
// Used Gate Set: ['id', 'rz', 'sx', 'x', 'cx', 'reset']
// Optimization Level: 3

OPENQASM 2.0;
include "qelib1.inc";
qreg q[3];
rz(-pi) q[0];
sx q[0];
rz(2.5519645) q[0];
sx q[0];
rz(1.5700685) q[1];
sx q[1];
rz(-1.5696912) q[1];
sx q[1];
rz(0.98842329) q[1];
cx q[0],q[1];
rz(-pi) q[0];
x q[0];
rz(-pi/2) q[1];
sx q[1];
rz(-3.1402694) q[1];
rz(1.5697606) q[2];
sx q[2];
rz(-1.5699727) q[2];
sx q[2];
rz(0.67176899) q[2];
cx q[0],q[2];
sx q[0];
rz(-1.4545787) q[0];
sx q[0];
rz(pi/2) q[2];
sx q[2];
rz(-2.9044673) q[2];
sx q[2];
rz(pi/2) q[2];
cx q[1],q[2];
sx q[1];
rz(-0.38996229) q[1];
sx q[1];
rz(2.9055616) q[2];
sx q[2];
rz(-1.6275768) q[2];
sx q[2];
rz(1.3390817) q[2];
