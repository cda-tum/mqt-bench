// Benchmark was created by MQT Bench on 2022-03-26
// MQT Bench version: 0.1.0
// Qiskit version: {'qiskit-terra': '0.19.2', 'qiskit-aer': '0.10.3', 'qiskit-ignis': '0.7.0', 'qiskit-ibmq-provider': '0.18.3', 'qiskit-aqua': '0.9.5', 'qiskit': '0.34.2', 'qiskit-nature': '0.3.1', 'qiskit-finance': '0.3.1', 'qiskit-optimization': '0.3.1', 'qiskit-machine-learning': '0.3.1'}
// Used Gate Set: ['rx', 'rz', 'cz']
// Optimization Level: 3

OPENQASM 2.0;
include "qelib1.inc";
qreg q[4];
creg meas[4];
rz(pi/2) q[0];
rx(2.5371375) q[0];
rz(pi/2) q[1];
rx(0.2540857) q[1];
cz q[0],q[1];
rx(pi) q[0];
rx(pi/2) q[1];
rz(pi/2) q[2];
rx(2.8800827) q[2];
cz q[0],q[2];
cz q[1],q[2];
rz(-pi) q[1];
rx(-pi/2) q[2];
rz(pi/2) q[3];
rx(1.292379) q[3];
rz(-2.3900442) q[3];
cz q[0],q[3];
rx(-0.79119597) q[0];
cz q[1],q[3];
rx(3.1407274) q[1];
cz q[0],q[1];
rz(-pi) q[0];
rx(pi) q[0];
rx(-pi/2) q[1];
cz q[2],q[3];
rx(1.1137338) q[2];
rz(0.86715738) q[2];
cz q[0],q[2];
rx(-pi) q[2];
cz q[1],q[2];
rz(-pi) q[1];
rx(pi) q[1];
rz(0.86715738) q[2];
rx(pi/2) q[2];
rx(-2.6830137) q[3];
rz(0.90166605) q[3];
rx(-2.1398163) q[3];
cz q[0],q[3];
rx(-0.19855927) q[0];
rz(-pi/2) q[0];
rz(-2.7746342) q[3];
cz q[1],q[3];
rx(3.0596761) q[1];
rz(-pi/2) q[1];
cz q[2],q[3];
rx(3.016714) q[2];
rz(-pi/2) q[2];
rx(0.88227251) q[3];
rz(pi/2) q[3];
barrier q[0],q[1],q[2],q[3];
measure q[0] -> meas[0];
measure q[1] -> meas[1];
measure q[2] -> meas[2];
measure q[3] -> meas[3];
