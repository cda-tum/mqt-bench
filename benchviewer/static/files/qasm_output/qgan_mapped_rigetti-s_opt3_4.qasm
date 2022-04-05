// Benchmark was created by MQT Bench on 2022-03-24
// MQT Bench version: 0.1.0
// Qiskit version: {'qiskit-terra': '0.19.2', 'qiskit-aer': '0.10.3', 'qiskit-ignis': '0.7.0', 'qiskit-ibmq-provider': '0.18.3', 'qiskit-aqua': '0.9.5', 'qiskit': '0.34.2', 'qiskit-nature': '0.3.1', 'qiskit-finance': '0.3.1', 'qiskit-optimization': '0.3.1', 'qiskit-machine-learning': '0.3.1'}
// Used Gate Set: ['rx', 'rz', 'cz']
// Optimization Level: 3
// Coupling List: [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 7], [0, 7], [1, 0], [2, 1], [3, 2], [4, 3], [5, 4], [6, 5], [7, 6], [7, 0]]
// Compiled for architecture: rigetti-s-8 qubits

OPENQASM 2.0;
include "qelib1.inc";
qreg q[8];
rz(-pi/2) q[3];
rx(-1.0012829) q[3];
rz(-pi/2) q[4];
rx(3.0038525) q[4];
rz(-1.2321004) q[4];
rz(-pi/2) q[5];
rx(0.99049578) q[5];
rz(pi/2) q[5];
cz q[4],q[5];
rx(pi/2) q[5];
rz(pi) q[5];
rz(-pi) q[6];
rx(-pi/2) q[6];
cz q[5],q[6];
rx(pi/2) q[5];
rz(-pi/2) q[6];
rx(pi/2) q[6];
cz q[5],q[6];
rx(-pi/2) q[5];
rz(pi/2) q[5];
rx(pi/2) q[6];
cz q[5],q[6];
rx(-3.1289414) q[5];
rz(-3*pi/2) q[5];
cz q[4],q[5];
rx(-pi/2) q[4];
cz q[3],q[4];
rx(-pi/2) q[3];
rz(0.27335146) q[3];
rx(pi/2) q[4];
rz(pi/2) q[4];
cz q[3],q[4];
rx(1.6656101) q[3];
rz(-0.3256463) q[3];
rx(pi/2) q[4];
rz(pi/2) q[4];
rx(-pi) q[6];
rz(-pi) q[6];
cz q[6],q[5];
rx(-pi) q[5];
cz q[4],q[5];
rx(pi/2) q[4];
rz(-pi/2) q[5];
rx(pi/2) q[5];
cz q[4],q[5];
rx(-pi/2) q[4];
rx(pi/2) q[5];
cz q[4],q[5];
rx(pi/2) q[4];
rz(pi/2) q[4];
rx(-pi) q[5];
rz(-pi) q[5];
cz q[6],q[5];
cz q[4],q[5];
rx(-pi/2) q[4];
rz(0.24023082) q[4];
rx(pi/2) q[4];
rx(pi/2) q[5];
rz(2.331983) q[5];
rx(-pi/2) q[5];
rx(pi/2) q[6];
rz(1.4793214) q[6];
rx(-pi/2) q[6];
