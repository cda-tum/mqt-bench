// Benchmark was created by MQT Bench on 2022-04-13
// For more information about MQT Bench, please visit https://www.cda.cit.tum.de/mqtbench/
// MQT Bench version: 0.1.0
// Qiskit version: {'qiskit-terra': '0.19.2', 'qiskit-aer': '0.10.3', 'qiskit-ignis': '0.7.0', 'qiskit-ibmq-provider': '0.18.3', 'qiskit-aqua': '0.9.5', 'qiskit': '0.34.2', 'qiskit-nature': '0.3.1', 'qiskit-finance': '0.3.1', 'qiskit-optimization': '0.3.1', 'qiskit-machine-learning': '0.3.1'}
// Used Gate Set: ['rx', 'rz', 'cz', 'id', 'reset']
// Optimization Level: 3

OPENQASM 2.0;
include "qelib1.inc";
qreg q[4];
creg meas[4];
rx(pi/2) q[0];
rz(pi/2) q[0];
rx(-1.9935231) q[0];
rx(pi/2) q[1];
rz(pi/2) q[1];
rx(-2.2124057) q[1];
cz q[0],q[1];
rx(pi/2) q[2];
rz(pi/2) q[2];
rx(-1.6970101) q[2];
cz q[0],q[2];
cz q[1],q[2];
rx(pi/2) q[3];
rz(pi/2) q[3];
rx(-2.240326) q[3];
cz q[0],q[3];
rx(pi/2) q[0];
rz(pi/2) q[0];
rx(-2.3653731) q[0];
cz q[1],q[3];
rx(pi/2) q[1];
rz(pi/2) q[1];
rx(1.179791) q[1];
cz q[0],q[1];
cz q[2],q[3];
rx(pi/2) q[2];
rz(pi/2) q[2];
rx(2.9979298) q[2];
cz q[0],q[2];
cz q[1],q[2];
rx(pi/2) q[3];
rz(pi/2) q[3];
rx(1.0107774) q[3];
cz q[0],q[3];
rx(pi/2) q[0];
rz(pi/2) q[0];
rx(-0.011406531) q[0];
cz q[1],q[3];
rx(pi/2) q[1];
rz(pi/2) q[1];
rx(-2.7643324) q[1];
cz q[2],q[3];
rx(pi/2) q[2];
rz(pi/2) q[2];
rx(-0.90336448) q[2];
rx(pi/2) q[3];
rz(pi/2) q[3];
rx(2.4861636) q[3];
barrier q[0],q[1],q[2],q[3];
measure q[0] -> meas[0];
measure q[1] -> meas[1];
measure q[2] -> meas[2];
measure q[3] -> meas[3];
