// Benchmark was created by MQT Bench on 2022-03-23
// MQT Bench version: 0.1.0
// Qiskit version: {'qiskit-terra': '0.19.2', 'qiskit-aer': '0.10.3', 'qiskit-ignis': '0.7.0', 'qiskit-ibmq-provider': '0.18.3', 'qiskit-aqua': '0.9.5', 'qiskit': '0.34.2', 'qiskit-nature': '0.3.1', 'qiskit-finance': '0.3.1', 'qiskit-optimization': '0.3.1', 'qiskit-machine-learning': '0.3.1'}
// Used Gate Set: ['rx', 'rz', 'cz']
// Optimization Level: 2

OPENQASM 2.0;
include "qelib1.inc";
qreg q[3];
creg meas[3];
rx(1.3226794) q[0];
rz(0.89389626) q[0];
rx(-1.4134233) q[0];
rx(pi/2) q[1];
rz(1.8513953) q[1];
rx(2.3678817) q[1];
cz q[0],q[1];
rx(pi/2) q[1];
rz(pi/2) q[1];
rx(pi/2) q[1];
rx(pi/2) q[2];
rz(2.0215624) q[2];
rx(2.2133542) q[2];
cz q[0],q[2];
rx(0.92664773) q[0];
rz(0.85790308) q[0];
rx(-1.1142289) q[0];
cz q[1],q[2];
rx(pi/2) q[1];
rz(2.3852571) q[1];
rx(1.5809837) q[1];
cz q[0],q[1];
rx(pi/2) q[1];
rz(pi/2) q[1];
rx(pi/2) q[1];
rx(-pi/2) q[2];
rz(0.7348499) q[2];
rx(2.2471005) q[2];
cz q[0],q[2];
rx(1.4766961) q[0];
rz(0.30705509) q[0];
rx(-1.4810732) q[0];
cz q[1],q[2];
rx(pi/2) q[1];
rz(1.7795111) q[1];
rx(2.4299346) q[1];
cz q[0],q[1];
rx(pi/2) q[1];
rz(pi/2) q[1];
rx(pi/2) q[1];
rx(-pi/2) q[2];
rz(0.84249013) q[2];
rx(1.9216762) q[2];
cz q[0],q[2];
rx(0.74614884) q[0];
rz(0.27195538) q[0];
rx(-0.76483672) q[0];
cz q[1],q[2];
rx(1.3065171) q[1];
rz(0.93163405) q[1];
rx(-1.4107525) q[1];
rx(1.8634215) q[2];
rz(1.5650542) q[2];
rx(1.5690664) q[2];
barrier q[0],q[1],q[2];
measure q[0] -> meas[0];
measure q[1] -> meas[1];
measure q[2] -> meas[2];
