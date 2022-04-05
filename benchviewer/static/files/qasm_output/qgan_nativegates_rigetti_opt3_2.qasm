// Benchmark was created by MQT Bench on 2022-03-24
// MQT Bench version: 0.1.0
// Qiskit version: {'qiskit-terra': '0.19.2', 'qiskit-aer': '0.10.3', 'qiskit-ignis': '0.7.0', 'qiskit-ibmq-provider': '0.18.3', 'qiskit-aqua': '0.9.5', 'qiskit': '0.34.2', 'qiskit-nature': '0.3.1', 'qiskit-finance': '0.3.1', 'qiskit-optimization': '0.3.1', 'qiskit-machine-learning': '0.3.1'}
// Used Gate Set: ['rx', 'rz', 'cz']
// Optimization Level: 3

OPENQASM 2.0;
include "qelib1.inc";
qreg q[2];
rz(pi/2) q[0];
rx(-1.5526604) q[0];
rz(-pi/2) q[1];
rx(-0.52341705) q[1];
cz q[0],q[1];
rx(0.97830203) q[0];
rz(pi/2) q[0];
rx(3.0499312) q[1];
rz(-pi/2) q[1];
