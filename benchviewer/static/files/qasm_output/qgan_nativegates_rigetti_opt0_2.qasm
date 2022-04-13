// Benchmark was created by MQT Bench on 2022-04-09
// For more information about MQT Bench, please visit https://www.cda.cit.tum.de/mqtbench/
// MQT Bench version: 0.1.0
// Qiskit version: {'qiskit-terra': '0.19.2', 'qiskit-aer': '0.10.3', 'qiskit-ignis': '0.7.0', 'qiskit-ibmq-provider': '0.18.3', 'qiskit-aqua': '0.9.5', 'qiskit': '0.34.2', 'qiskit-nature': '0.3.1', 'qiskit-finance': '0.3.1', 'qiskit-optimization': '0.3.1', 'qiskit-machine-learning': '0.3.1'}
// Used Gate Set: ['rx', 'rz', 'cz', 'id', 'reset']
// Optimization Level: 0

OPENQASM 2.0;
include "qelib1.inc";
qreg q[2];
creg meas[2];
rz(0.0) q[0];
rx(pi/2) q[0];
rz(3*pi/2) q[0];
rx(pi/2) q[0];
rz(3*pi) q[0];
rx(pi) q[0];
rz(0.0) q[0];
rx(pi/2) q[0];
rz(8.04162791557309) q[0];
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
rz(3.40882823362914) q[1];
rx(pi/2) q[1];
rz(3*pi) q[1];
cz q[0],q[1];
rz(0.0) q[0];
rx(pi/2) q[0];
rz(4.03706985938427) q[0];
rx(pi/2) q[0];
rz(3*pi) q[0];
rz(0.0) q[1];
rx(pi/2) q[1];
rz(7.58329035946123) q[1];
rx(pi/2) q[1];
rz(3*pi) q[1];
barrier q[0],q[1];
measure q[0] -> meas[0];
measure q[1] -> meas[1];
