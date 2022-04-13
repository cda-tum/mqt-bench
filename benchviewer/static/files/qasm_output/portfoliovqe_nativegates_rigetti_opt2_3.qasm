// Benchmark was created by MQT Bench on 2022-04-07
// For more information about MQT Bench, please visit https://www.cda.cit.tum.de/mqtbench/
// MQT Bench version: 0.1.0
// Qiskit version: {'qiskit-terra': '0.19.2', 'qiskit-aer': '0.10.3', 'qiskit-ignis': '0.7.0', 'qiskit-ibmq-provider': '0.18.3', 'qiskit-aqua': '0.9.5', 'qiskit': '0.34.2', 'qiskit-nature': '0.3.1', 'qiskit-finance': '0.3.1', 'qiskit-optimization': '0.3.1', 'qiskit-machine-learning': '0.3.1'}
// Used Gate Set: ['rx', 'rz', 'cz', 'id', 'reset']
// Optimization Level: 2

OPENQASM 2.0;
include "qelib1.inc";
qreg q[3];
creg meas[3];
rx(pi/2) q[0];
rz(0.49228365) q[0];
rx(-pi/2) q[0];
rx(pi/2) q[1];
rz(0.78836118) q[1];
rx(-pi/2) q[1];
cz q[0],q[1];
rx(pi/2) q[2];
rz(2.7051748) q[2];
rx(-pi/2) q[2];
cz q[0],q[2];
rx(-pi/2) q[0];
rz(1.6274778) q[0];
rx(pi/2) q[0];
cz q[1],q[2];
rx(pi/2) q[1];
rz(1.9839356) q[1];
rx(-pi/2) q[1];
cz q[0],q[1];
rx(-pi/2) q[2];
rz(0.91331012) q[2];
rx(pi/2) q[2];
cz q[0],q[2];
rx(pi/2) q[0];
rz(1.4640391) q[0];
rx(-pi/2) q[0];
cz q[1],q[2];
rx(pi/2) q[1];
rz(2.6075077) q[1];
rx(-pi/2) q[1];
cz q[0],q[1];
rx(pi/2) q[2];
rz(2.0217698) q[2];
rx(-pi/2) q[2];
cz q[0],q[2];
rx(-pi/2) q[0];
rz(1.9010377) q[0];
rx(pi/2) q[0];
cz q[1],q[2];
rx(pi/2) q[1];
rz(1.8248529) q[1];
rx(-pi/2) q[1];
rx(-pi/2) q[2];
rz(1.4578892) q[2];
rx(pi/2) q[2];
barrier q[0],q[1],q[2];
measure q[0] -> meas[0];
measure q[1] -> meas[1];
measure q[2] -> meas[2];
