// Benchmark was created by MQT Bench on 2022-03-24
// MQT Bench version: 0.1.0
// Qiskit version: {'qiskit-terra': '0.19.2', 'qiskit-aer': '0.10.3', 'qiskit-ignis': '0.7.0', 'qiskit-ibmq-provider': '0.18.3', 'qiskit-aqua': '0.9.5', 'qiskit': '0.34.2', 'qiskit-nature': '0.3.1', 'qiskit-finance': '0.3.1', 'qiskit-optimization': '0.3.1', 'qiskit-machine-learning': '0.3.1'}
// Used Gate Set: ['rx', 'rz', 'cz']
// Optimization Level: 2

OPENQASM 2.0;
include "qelib1.inc";
qreg q[6];
rx(pi/2) q[0];
rz(1.5112598) q[0];
rx(pi/2) q[0];
rx(-pi/2) q[1];
rz(0.60102038) q[1];
rx(-pi/2) q[1];
cz q[0],q[1];
rx(pi/2) q[2];
rz(1.8619796) q[2];
rx(pi/2) q[2];
cz q[0],q[2];
cz q[1],q[2];
rx(pi/2) q[3];
rz(2.3889141) q[3];
rx(pi/2) q[3];
cz q[0],q[3];
cz q[1],q[3];
cz q[2],q[3];
rx(-pi/2) q[4];
rz(1.9858828) q[4];
rx(-pi/2) q[4];
cz q[0],q[4];
cz q[1],q[4];
cz q[2],q[4];
cz q[3],q[4];
rx(-pi/2) q[5];
rz(1.9113876) q[5];
rx(-pi/2) q[5];
cz q[0],q[5];
rx(-pi/2) q[0];
rz(2.1413047) q[0];
rx(pi/2) q[0];
cz q[1],q[5];
rx(-pi/2) q[1];
rz(0.16619331) q[1];
rx(pi/2) q[1];
cz q[2],q[5];
rx(-pi/2) q[2];
rz(0.27216986) q[2];
rx(pi/2) q[2];
cz q[3],q[5];
rx(-pi/2) q[3];
rz(0.48413775) q[3];
rx(pi/2) q[3];
cz q[4],q[5];
rx(-pi/2) q[4];
rz(2.3989073) q[4];
rx(pi/2) q[4];
rx(pi/2) q[5];
rz(1.0924984) q[5];
rx(-pi/2) q[5];
