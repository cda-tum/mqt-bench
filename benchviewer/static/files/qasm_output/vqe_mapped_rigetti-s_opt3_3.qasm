// Benchmark was created by MQT Bench on 2022-03-26
// MQT Bench version: 0.1.0
// Qiskit version: {'qiskit-terra': '0.19.2', 'qiskit-aer': '0.10.3', 'qiskit-ignis': '0.7.0', 'qiskit-ibmq-provider': '0.18.3', 'qiskit-aqua': '0.9.5', 'qiskit': '0.34.2', 'qiskit-nature': '0.3.1', 'qiskit-finance': '0.3.1', 'qiskit-optimization': '0.3.1', 'qiskit-machine-learning': '0.3.1'}
// Used Gate Set: ['rx', 'rz', 'cz']
// Optimization Level: 3
// Coupling List: [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 7], [0, 7], [1, 0], [2, 1], [3, 2], [4, 3], [5, 4], [6, 5], [7, 6], [7, 0]]
// Compiled for architecture: rigetti-s-8 qubits

OPENQASM 2.0;
include "qelib1.inc";
qreg q[8];
creg meas[3];
rz(pi/2) q[2];
rx(pi/2) q[2];
rz(-pi/2) q[3];
rx(0.30997121) q[3];
rz(pi/2) q[3];
rz(-pi/2) q[4];
rx(1.0844822) q[4];
cz q[3],q[4];
rx(pi/2) q[3];
cz q[2],q[3];
rx(pi/2) q[2];
rz(-pi/2) q[3];
rx(pi/2) q[3];
cz q[2],q[3];
rx(-pi/2) q[2];
rz(1.755051) q[2];
rx(pi/2) q[3];
cz q[2],q[3];
rx(-pi/2) q[2];
rx(-0.63732058) q[3];
rz(-pi) q[3];
rx(pi) q[4];
cz q[3],q[4];
rx(-pi/2) q[3];
cz q[2],q[3];
rx(-pi/2) q[2];
rz(-pi) q[2];
rx(pi/2) q[3];
rz(pi/2) q[3];
cz q[2],q[3];
rx(-0.18222192) q[2];
rx(-2.9690832) q[3];
rz(1.5813211) q[3];
rx(-0.84017668) q[3];
rx(2.7349706) q[4];
cz q[3],q[4];
rz(-1.586567) q[3];
rx(-pi/2) q[3];
cz q[2],q[3];
rx(pi/2) q[2];
rz(-pi/2) q[3];
rx(pi/2) q[3];
cz q[2],q[3];
rx(-pi/2) q[2];
rz(pi/2) q[2];
rx(pi/2) q[3];
cz q[2],q[3];
rx(pi/2) q[3];
rz(-2.1094779) q[3];
rx(pi) q[4];
cz q[3],q[4];
rx(-pi) q[3];
cz q[2],q[3];
rx(0.068812662) q[2];
rz(-pi/2) q[2];
rz(1.0321148) q[3];
rx(0.65147258) q[3];
rz(pi/2) q[3];
rx(1.1684207) q[4];
rz(pi/2) q[4];
barrier q[2],q[6],q[5],q[3],q[1],q[7],q[4],q[0];
measure q[4] -> meas[0];
measure q[2] -> meas[1];
measure q[3] -> meas[2];
