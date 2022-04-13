// Benchmark was created by MQT Bench on 2022-04-07
// For more information about MQT Bench, please visit https://www.cda.cit.tum.de/mqtbench/
// MQT Bench version: 0.1.0
// Qiskit version: {'qiskit-terra': '0.19.2', 'qiskit-aer': '0.10.3', 'qiskit-ignis': '0.7.0', 'qiskit-ibmq-provider': '0.18.3', 'qiskit-aqua': '0.9.5', 'qiskit': '0.34.2', 'qiskit-nature': '0.3.1', 'qiskit-finance': '0.3.1', 'qiskit-optimization': '0.3.1', 'qiskit-machine-learning': '0.3.1'}
// Used Gate Set: ['rx', 'rz', 'cz', 'id', 'reset']
// Optimization Level: 1

OPENQASM 2.0;
include "qelib1.inc";
qreg eval[2];
qreg q[1];
creg meas[3];
rx(pi/2) eval[0];
rz(pi/2) eval[0];
rx(pi/2) eval[0];
rx(pi/2) eval[1];
rz(pi/2) eval[1];
rx(pi/2) eval[1];
rx(pi/2) q[0];
rz(2.4980915) q[0];
rx(pi/2) q[0];
cz eval[0],q[0];
rx(pi/2) q[0];
rz(0.92729522) q[0];
rx(-pi/2) q[0];
cz eval[0],q[0];
rx(-pi/2) q[0];
rz(0.92729522) q[0];
rx(pi/2) q[0];
rz(-pi/4) eval[0];
cz eval[1],q[0];
rx(pi/2) q[0];
rz(1.8545904) q[0];
rx(-pi/2) q[0];
cz eval[1],q[0];
rx(-pi/2) q[0];
rz(0.28379411) q[0];
rx(-pi/2) q[0];
cz eval[0],eval[1];
rx(pi/4) eval[1];
cz eval[0],eval[1];
rx(pi/2) eval[0];
rz(pi/2) eval[0];
rx(pi/2) eval[0];
rx(pi/4) eval[1];
rz(pi/2) eval[1];
rx(pi/2) eval[1];
barrier eval[0],eval[1],q[0];
measure eval[0] -> meas[0];
measure eval[1] -> meas[1];
measure q[0] -> meas[2];
