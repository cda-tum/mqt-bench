// Benchmark was created by MQT Bench on 2022-04-08
// For more information about MQT Bench, please visit https://www.cda.cit.tum.de/mqtbench/
// MQT Bench version: 0.1.0
// Qiskit version: {'qiskit-terra': '0.19.2', 'qiskit-aer': '0.10.3', 'qiskit-ignis': '0.7.0', 'qiskit-ibmq-provider': '0.18.3', 'qiskit-aqua': '0.9.5', 'qiskit': '0.34.2', 'qiskit-nature': '0.3.1', 'qiskit-finance': '0.3.1', 'qiskit-optimization': '0.3.1', 'qiskit-machine-learning': '0.3.1'}
// Used Gate Set: ['rx', 'rz', 'cz', 'id', 'reset']
// Optimization Level: 3

OPENQASM 2.0;
include "qelib1.inc";
qreg q[3];
creg meas[3];
rz(pi/2) q[0];
rx(-0.66793214) q[0];
rz(pi/2) q[1];
rx(0.65508169) q[1];
cz q[0],q[1];
rx(pi/2) q[1];
rz(pi/2) q[2];
rx(0.89473157) q[2];
rz(-2.6159702) q[2];
cz q[0],q[2];
rx(2.7442527) q[0];
rx(-pi) q[2];
cz q[1],q[2];
rx(-1.2590347) q[1];
cz q[0],q[1];
rx(-pi/2) q[1];
rx(-0.2117711) q[2];
rz(0.95591459) q[2];
rx(-0.24400843) q[2];
cz q[0],q[2];
rx(-0.59066975) q[0];
rz(0.30530754) q[2];
cz q[1],q[2];
rx(-0.61690032) q[1];
cz q[0],q[1];
rz(-pi) q[0];
rx(pi/2) q[1];
rx(-0.41404258) q[2];
rz(1.3345695) q[2];
rx(0.3129673) q[2];
cz q[0],q[2];
rx(-2.6733379) q[0];
rz(pi/2) q[0];
rz(-0.55674084) q[2];
rx(-pi) q[2];
cz q[1],q[2];
rx(-0.7353715) q[1];
rz(-pi/2) q[1];
rz(1.4709622) q[2];
rx(1.6739081) q[2];
rz(pi/2) q[2];
barrier q[0],q[1],q[2];
measure q[0] -> meas[0];
measure q[1] -> meas[1];
measure q[2] -> meas[2];
