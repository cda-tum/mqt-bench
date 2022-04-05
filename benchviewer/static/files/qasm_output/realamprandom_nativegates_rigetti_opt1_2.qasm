// Benchmark was created by MQT Bench on 2022-03-21
// MQT Bench version: 0.1.0
// Qiskit version: {'qiskit-terra': '0.19.2', 'qiskit-aer': '0.10.3', 'qiskit-ignis': '0.7.0', 'qiskit-ibmq-provider': '0.18.3', 'qiskit-aqua': '0.9.5', 'qiskit': '0.34.2', 'qiskit-nature': '0.3.1', 'qiskit-finance': '0.3.1', 'qiskit-optimization': '0.3.1', 'qiskit-machine-learning': '0.3.1'}
// Used Gate Set: ['rx', 'rz', 'cz']
// Optimization Level: 1

OPENQASM 2.0;
include "qelib1.inc";
qreg q[2];
creg meas[2];
rz(pi/2) q[0];
rx(3.0597799) q[0];
rx(pi/2) q[1];
rz(0.85739954) q[1];
cz q[0],q[1];
rx(pi/4) q[1];
cz q[0],q[1];
rx(pi) q[0];
cz q[0],q[1];
rx(-pi/4) q[1];
cz q[0],q[1];
rz(pi/2) q[0];
rx(2.2121601) q[0];
rx(pi/2) q[1];
rz(0.56487934) q[1];
cz q[0],q[1];
rx(pi/4) q[1];
cz q[0],q[1];
rx(pi) q[0];
cz q[0],q[1];
rx(-pi/4) q[1];
cz q[0],q[1];
rz(pi/2) q[0];
rx(2.5191645) q[0];
rx(pi/2) q[1];
rz(0.83250807) q[1];
cz q[0],q[1];
rx(pi/4) q[1];
cz q[0],q[1];
rx(pi) q[0];
cz q[0],q[1];
rx(-pi/4) q[1];
cz q[0],q[1];
rx(pi/2) q[0];
rz(0.7055203) q[0];
rx(-pi/2) q[0];
rx(pi/2) q[1];
rz(0.14900496) q[1];
rx(-pi/2) q[1];
barrier q[0],q[1];
measure q[0] -> meas[0];
measure q[1] -> meas[1];
