// Benchmark was created by MQT Bench on 2022-03-24
// MQT Bench version: 0.1.0
// Qiskit version: {'qiskit-terra': '0.19.2', 'qiskit-aer': '0.10.3', 'qiskit-ignis': '0.7.0', 'qiskit-ibmq-provider': '0.18.3', 'qiskit-aqua': '0.9.5', 'qiskit': '0.34.2', 'qiskit-nature': '0.3.1', 'qiskit-finance': '0.3.1', 'qiskit-optimization': '0.3.1', 'qiskit-machine-learning': '0.3.1'}
// Used Gate Set: ['rx', 'rz', 'cz']
// Optimization Level: 3

OPENQASM 2.0;
include "qelib1.inc";
qreg q[3];
creg meas[3];
rz(pi/2) q[0];
rx(-0.14746624) q[0];
rz(pi/2) q[1];
rx(1.0857809) q[1];
cz q[0],q[1];
rx(pi) q[0];
rx(-pi/2) q[1];
rz(-pi/2) q[2];
rx(1.8801885) q[2];
rz(-pi/2) q[2];
cz q[0],q[2];
rz(-pi) q[0];
rx(-0.98282299) q[0];
rx(-pi) q[2];
rz(-0.78099271) q[2];
cz q[1],q[2];
rx(-1.6697608) q[1];
rz(pi) q[1];
cz q[0],q[1];
rx(pi/2) q[1];
rx(3.141181) q[2];
rz(1.9198981) q[2];
rx(-0.00032327163) q[2];
cz q[0],q[2];
rx(-0.65578642) q[0];
rx(-pi) q[2];
rz(-3.0458213) q[2];
cz q[1],q[2];
rx(-2.4382747) q[1];
rz(pi) q[1];
cz q[0],q[1];
rz(-pi) q[0];
rx(pi) q[0];
rx(-pi/2) q[1];
rx(-2.1269218) q[2];
rz(2.3683658) q[2];
rx(-1.5266334) q[2];
cz q[0],q[2];
rx(-0.12688383) q[0];
rz(-pi/2) q[0];
rx(-pi) q[2];
rz(-0.81935521) q[2];
cz q[1],q[2];
rx(-2.4069533) q[1];
rz(pi/2) q[1];
rx(1.0242452) q[2];
rz(-pi/2) q[2];
barrier q[0],q[1],q[2];
measure q[0] -> meas[0];
measure q[1] -> meas[1];
measure q[2] -> meas[2];
