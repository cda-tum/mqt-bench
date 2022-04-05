// Benchmark was created by MQT Bench on 2022-03-22
// MQT Bench version: 0.1.0
// Qiskit version: {'qiskit-terra': '0.19.2', 'qiskit-aer': '0.10.3', 'qiskit-ignis': '0.7.0', 'qiskit-ibmq-provider': '0.18.3', 'qiskit-aqua': '0.9.5', 'qiskit': '0.34.2', 'qiskit-nature': '0.3.1', 'qiskit-finance': '0.3.1', 'qiskit-optimization': '0.3.1', 'qiskit-machine-learning': '0.3.1'}
// Used Gate Set: ['rx', 'rz', 'cz']
// Optimization Level: 3

OPENQASM 2.0;
include "qelib1.inc";
qreg q[9];
creg c[8];
rz(-pi/2) q[0];
rx(pi/2) q[0];
rz(-pi/2) q[1];
rx(pi/2) q[1];
rz(-pi/2) q[2];
rx(-pi/2) q[2];
rz(-pi/2) q[3];
rx(-pi/2) q[3];
rz(-pi/2) q[4];
rx(pi/2) q[4];
rz(-pi/2) q[5];
rx(pi/2) q[5];
rz(-pi/2) q[6];
rx(-pi/2) q[6];
rx(pi/2) q[7];
rz(pi/2) q[7];
rx(-pi/2) q[7];
cz q[0],q[8];
rx(pi/2) q[0];
rz(-pi/2) q[0];
rz(pi) q[8];
cz q[1],q[8];
rx(pi/2) q[1];
rz(-pi/2) q[1];
rx(-pi) q[8];
rz(-3*pi) q[8];
cz q[2],q[8];
rx(pi/2) q[2];
rz(pi/2) q[2];
cz q[3],q[8];
rx(pi/2) q[3];
rz(pi/2) q[3];
rx(pi) q[8];
cz q[4],q[8];
rx(pi/2) q[4];
rz(-pi/2) q[4];
rz(pi) q[8];
cz q[5],q[8];
rx(pi/2) q[5];
rz(-pi/2) q[5];
rx(-pi) q[8];
cz q[6],q[8];
rx(pi/2) q[6];
rz(pi/2) q[6];
cz q[7],q[8];
rx(-pi/2) q[7];
rz(pi/2) q[7];
rx(pi/2) q[7];
rx(pi/2) q[8];
rz(pi/2) q[8];
rx(pi/2) q[8];
measure q[0] -> c[0];
measure q[1] -> c[1];
measure q[2] -> c[2];
measure q[3] -> c[3];
measure q[4] -> c[4];
measure q[5] -> c[5];
measure q[6] -> c[6];
measure q[7] -> c[7];
