// Benchmark was created by MQT Bench on 2022-04-07
// For more information about MQT Bench, please visit https://www.cda.cit.tum.de/mqtbench/
// MQT Bench version: 0.1.0
// Qiskit version: {'qiskit-terra': '0.19.2', 'qiskit-aer': '0.10.3', 'qiskit-ignis': '0.7.0', 'qiskit-ibmq-provider': '0.18.3', 'qiskit-aqua': '0.9.5', 'qiskit': '0.34.2', 'qiskit-nature': '0.3.1', 'qiskit-finance': '0.3.1', 'qiskit-optimization': '0.3.1', 'qiskit-machine-learning': '0.3.1'}
// Used Gate Set: ['rx', 'rz', 'cz', 'id', 'reset']
// Optimization Level: 3
// Coupling List: [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 7], [0, 7], [1, 0], [2, 1], [3, 2], [4, 3], [5, 4], [6, 5], [7, 6], [7, 0]]
// Compiled for architecture: rigetti-s-8 qubits

OPENQASM 2.0;
include "qelib1.inc";
qreg q[8];
creg meas[4];
rz(pi/2) q[0];
rz(-pi/2) q[1];
rx(-pi/2) q[2];
rz(pi) q[2];
rx(-1.4295609) q[3];
cz q[2],q[3];
rx(pi) q[2];
rx(0.92729522) q[3];
cz q[2],q[3];
rz(1.8545904) q[2];
rx(-pi/2) q[2];
cz q[1],q[2];
rx(pi/2) q[1];
rz(-pi/2) q[2];
rx(pi/2) q[2];
cz q[1],q[2];
rx(-0.28379411) q[1];
rz(pi/2) q[1];
rx(pi/2) q[2];
cz q[1],q[2];
rx(-pi/2) q[1];
rz(2.8577985) q[1];
rx(-pi/2) q[1];
cz q[0],q[1];
rx(pi/2) q[0];
rz(-pi/2) q[1];
rx(pi/2) q[1];
cz q[0],q[1];
rx(1.0032081) q[0];
rx(pi/2) q[1];
cz q[0],q[1];
rx(1.0032081) q[0];
rz(-pi/2) q[0];
rx(pi/2) q[1];
rz(2.0819736) q[1];
rz(-3*pi/4) q[2];
rx(pi/2) q[2];
rz(-pi/2) q[2];
cz q[1],q[2];
rx(pi) q[1];
rx(pi/4) q[2];
rz(pi/2) q[2];
cz q[1],q[2];
rz(-1.8450172) q[1];
rx(pi/2) q[1];
rz(pi/2) q[1];
rx(pi/2) q[2];
rz(pi/2) q[2];
rx(-3.0003573) q[3];
cz q[2],q[3];
rx(pi/2) q[2];
rz(-pi/2) q[3];
rx(pi/2) q[3];
cz q[2],q[3];
rx(-pi/2) q[2];
rz(-7*pi/8) q[2];
rx(pi/2) q[3];
cz q[2],q[3];
cz q[2],q[1];
rx(pi/8) q[1];
cz q[2],q[1];
rx(3*pi/8) q[1];
rz(pi/2) q[1];
rx(pi/2) q[1];
rx(-pi) q[2];
rx(-pi/2) q[3];
rz(pi/2) q[3];
rx(1.6464483) q[3];
cz q[2],q[3];
rz(pi/2) q[2];
rx(pi) q[2];
rx(pi/4) q[3];
rz(pi/2) q[3];
cz q[2],q[3];
rz(-pi/2) q[2];
rx(pi/2) q[2];
rz(pi/2) q[2];
rx(pi/2) q[3];
rz(2.4318464) q[3];
barrier q[4],q[7],q[2],q[1],q[6],q[5],q[0],q[3];
measure q[2] -> meas[0];
measure q[3] -> meas[1];
measure q[1] -> meas[2];
measure q[0] -> meas[3];
