// Benchmark was created by MQT Bench on 2022-03-25
// MQT Bench version: 0.1.0
// Qiskit version: {'qiskit-terra': '0.19.2', 'qiskit-aer': '0.10.3', 'qiskit-ignis': '0.7.0', 'qiskit-ibmq-provider': '0.18.3', 'qiskit-aqua': '0.9.5', 'qiskit': '0.34.2', 'qiskit-nature': '0.3.1', 'qiskit-finance': '0.3.1', 'qiskit-optimization': '0.3.1', 'qiskit-machine-learning': '0.3.1'}
// Used Gate Set: ['rx', 'rz', 'cz']
// Optimization Level: 3
// Coupling List: [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 7], [0, 7], [1, 0], [2, 1], [3, 2], [4, 3], [5, 4], [6, 5], [7, 6], [7, 0]]
// Compiled for architecture: rigetti-s-8 qubits

OPENQASM 2.0;
include "qelib1.inc";
qreg q[8];
creg c[2];
rz(pi/2) q[0];
rx(pi/2) q[0];
rz(4.1719695) q[0];
rz(-pi/2) q[1];
rx(pi) q[1];
rz(-pi) q[2];
rx(-1.8678605) q[2];
cz q[1],q[2];
rz(pi/2) q[1];
rx(pi) q[1];
rx(3*pi/8) q[2];
rz(pi) q[2];
cz q[1],q[2];
rx(-pi/2) q[1];
rz(pi/2) q[1];
rx(pi/8) q[1];
cz q[0],q[1];
rx(pi) q[0];
rx(pi/4) q[1];
rz(pi/2) q[1];
cz q[0],q[1];
rx(0.43578401) q[0];
rz(1.7936663) q[0];
rx(-3.0390335) q[0];
rx(pi/2) q[1];
rz(pi/2) q[1];
rx(-pi/2) q[1];
rx(-0.88103303) q[2];
cz q[1],q[2];
rx(pi/2) q[1];
rz(-pi/2) q[2];
rx(pi/2) q[2];
cz q[1],q[2];
rx(-pi/2) q[1];
rz(2.6392047) q[1];
rx(pi/2) q[2];
cz q[1],q[2];
rx(-pi/2) q[1];
cz q[0],q[1];
rx(pi/2) q[0];
rz(-pi/2) q[1];
rx(pi/2) q[1];
cz q[0],q[1];
rx(pi/4) q[0];
rx(pi/2) q[1];
cz q[0],q[1];
rx(2.8585824) q[0];
rz(-1.209696) q[1];
rx(pi) q[1];
rz(pi/2) q[2];
barrier q[0],q[2],q[1],q[3],q[4],q[5],q[6],q[7];
measure q[1] -> c[0];
measure q[0] -> c[1];
