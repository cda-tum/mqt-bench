// Benchmark was created by MQT Bench on 2022-03-24
// MQT Bench version: 0.1.0
// Qiskit version: {'qiskit-terra': '0.19.2', 'qiskit-aer': '0.10.3', 'qiskit-ignis': '0.7.0', 'qiskit-ibmq-provider': '0.18.3', 'qiskit-aqua': '0.9.5', 'qiskit': '0.34.2', 'qiskit-nature': '0.3.1', 'qiskit-finance': '0.3.1', 'qiskit-optimization': '0.3.1', 'qiskit-machine-learning': '0.3.1'}
// Used Gate Set: ['rx', 'rz', 'cz']
// Optimization Level: 1

OPENQASM 2.0;
include "qelib1.inc";
qreg q[3];
rx(pi/2) q[0];
rz(0.58962814) q[0];
rx(pi/2) q[0];
rx(-pi/2) q[1];
rz(2.153169) q[1];
rx(-pi/2) q[1];
cz q[0],q[1];
rx(-pi/2) q[2];
rz(2.4698232) q[2];
rx(-pi/2) q[2];
cz q[0],q[2];
rx(-pi/2) q[0];
rz(1.6870139) q[0];
rx(pi/2) q[0];
cz q[1],q[2];
rx(-pi/2) q[1];
rz(2.7516304) q[1];
rx(pi/2) q[1];
rx(-pi/2) q[2];
rz(2.8989518) q[2];
rx(pi/2) q[2];
