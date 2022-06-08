// Benchmark was created by MQT Bench on 2022-06-08
// For more information about MQT Bench, please visit https://www.cda.cit.tum.de/mqtbench/
// MQT Bench version: 0.1.0
// Qiskit version: {'qiskit-terra': '0.20.2', 'qiskit-aer': '0.10.4', 'qiskit-ignis': '0.7.1', 'qiskit-ibmq-provider': '0.19.1', 'qiskit-aqua': '0.9.5', 'qiskit': '0.36.2', 'qiskit-nature': '0.3.2', 'qiskit-finance': '0.3.1', 'qiskit-optimization': '0.3.2', 'qiskit-machine-learning': '0.3.1'}
// Used Gate Set: ['rxx', 'rz', 'ry', 'rx', 'measure']
// Coupling List: []

OPENQASM 2.0;
include "qelib1.inc";
qreg eval[3];
qreg q[1];
creg meas[4];
rx(-10.602875) eval[0];
rx(-11*pi/4) eval[1];
rx(-3*pi/2) eval[2];
ry(0.92729522) q[0];
rxx(pi/2) eval[0],q[0];
rz(-0.92729522) q[0];
rx(-pi/2) q[0];
rxx(pi/2) eval[0],q[0];
rz(0.92729522) q[0];
rx(-pi/2) q[0];
rxx(pi/2) eval[1],q[0];
rz(-1.8545904) q[0];
rx(-pi/2) q[0];
rxx(pi/2) eval[1],q[0];
rz(1.8545904) q[0];
rx(-pi/2) q[0];
rxx(pi/2) eval[2],q[0];
rz(2.5740044) q[0];
rx(-pi/2) q[0];
rxx(pi/2) eval[2],q[0];
rz(-2.5740044) q[0];
rx(-pi/2) q[0];
rxx(pi/2) eval[1],eval[2];
rz(pi/4) eval[2];
rxx(pi/2) eval[1],eval[2];
rx(-pi/2) eval[2];
rz(-pi/4) eval[2];
rxx(pi/2) eval[0],eval[2];
rx(-pi/2) eval[2];
rz(pi/8) eval[2];
rxx(pi/2) eval[0],eval[2];
rxx(pi/2) eval[0],eval[1];
rz(pi/4) eval[1];
rxx(pi/2) eval[0],eval[1];
rx(-pi/2) eval[1];
rz(-pi/4) eval[1];
rx(-pi/2) eval[2];
rz(-pi/8) eval[2];
barrier eval[0],eval[1],eval[2],q[0];
measure eval[0] -> meas[0];
measure eval[1] -> meas[1];
measure eval[2] -> meas[2];
measure q[0] -> meas[3];
