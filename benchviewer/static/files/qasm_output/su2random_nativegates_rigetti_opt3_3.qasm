// Benchmark was created by MQT Bench on 2022-03-23
// MQT Bench version: 0.1.0
// Qiskit version: {'qiskit-terra': '0.19.2', 'qiskit-aer': '0.10.3', 'qiskit-ignis': '0.7.0', 'qiskit-ibmq-provider': '0.18.3', 'qiskit-aqua': '0.9.5', 'qiskit': '0.34.2', 'qiskit-nature': '0.3.1', 'qiskit-finance': '0.3.1', 'qiskit-optimization': '0.3.1', 'qiskit-machine-learning': '0.3.1'}
// Used Gate Set: ['rx', 'rz', 'cz']
// Optimization Level: 3

OPENQASM 2.0;
include "qelib1.inc";
qreg q[3];
creg meas[3];
rz(-pi/2) q[0];
rx(0.87866129) q[0];
rz(-2.9489704) q[0];
rz(-0.7537832) q[1];
rx(1.7655431) q[1];
rz(-2.938283) q[1];
cz q[0],q[1];
rx(pi/2) q[1];
rz(-3.1267484) q[1];
rz(2.2645061) q[2];
rx(1.2145373) q[2];
rz(-4.9946785) q[2];
cz q[0],q[2];
rx(0.74638344) q[0];
rz(2.042355) q[0];
rx(pi) q[2];
cz q[1],q[2];
rx(0.75639058) q[1];
rz(1.5599995) q[1];
cz q[0],q[1];
rx(pi/2) q[1];
rz(pi/2) q[1];
rx(pi/2) q[1];
rz(2.4456276) q[2];
rx(2.1878392) q[2];
rz(3.2913692) q[2];
cz q[0],q[2];
rx(1.4766961) q[0];
rz(0.30705509) q[0];
rx(-1.4810732) q[0];
cz q[1],q[2];
rz(2.4407677) q[1];
rx(1.4350578) q[1];
rz(1.4117596) q[1];
cz q[0],q[1];
rx(pi/2) q[1];
rz(pi/2) q[1];
rx(pi/2) q[1];
rx(0.89559878) q[2];
rz(-1.273334) q[2];
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
