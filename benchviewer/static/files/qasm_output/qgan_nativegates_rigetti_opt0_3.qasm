// Benchmark was created by MQT Bench on 2022-03-24
// MQT Bench version: 0.1.0
// Qiskit version: {'qiskit-terra': '0.19.2', 'qiskit-aer': '0.10.3', 'qiskit-ignis': '0.7.0', 'qiskit-ibmq-provider': '0.18.3', 'qiskit-aqua': '0.9.5', 'qiskit': '0.34.2', 'qiskit-nature': '0.3.1', 'qiskit-finance': '0.3.1', 'qiskit-optimization': '0.3.1', 'qiskit-machine-learning': '0.3.1'}
// Used Gate Set: ['rx', 'rz', 'cz']
// Optimization Level: 0

OPENQASM 2.0;
include "qelib1.inc";
qreg q[3];
rz(0.0) q[0];
rx(pi/2) q[0];
rz(3*pi/2) q[0];
rx(pi/2) q[0];
rz(3*pi) q[0];
rx(pi) q[0];
rz(0.0) q[0];
rx(pi/2) q[0];
rz(4.12276084132808) q[0];
rx(pi/2) q[0];
rz(3*pi) q[0];
rz(0.0) q[1];
rx(pi/2) q[1];
rz(3*pi/2) q[1];
rx(pi/2) q[1];
rz(3*pi) q[1];
rx(pi) q[1];
rz(0.0) q[1];
rx(pi/2) q[1];
rz(6.8655579394325) q[1];
rx(pi/2) q[1];
rz(3*pi) q[1];
cz q[0],q[1];
rz(0.0) q[2];
rx(pi/2) q[2];
rz(3*pi/2) q[2];
rx(pi/2) q[2];
rz(3*pi) q[2];
rx(pi) q[2];
rz(0.0) q[2];
rx(pi/2) q[2];
rz(7.1822122127636) q[2];
rx(pi/2) q[2];
rz(3*pi) q[2];
cz q[0],q[2];
rz(0.0) q[0];
rx(pi/2) q[0];
rz(7.73776404957155) q[0];
rx(pi/2) q[0];
rz(3*pi) q[0];
cz q[1],q[2];
rz(0.0) q[1];
rx(pi/2) q[1];
rz(6.67314759440184) q[1];
rx(pi/2) q[1];
rz(3*pi) q[1];
rz(0.0) q[2];
rx(pi/2) q[2];
rz(6.52582615986381) q[2];
rx(pi/2) q[2];
rz(3*pi) q[2];
