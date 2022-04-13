// Benchmark was created by MQT Bench on 2022-04-07
// For more information about MQT Bench, please visit https://www.cda.cit.tum.de/mqtbench/
// MQT Bench version: 0.1.0
// Qiskit version: {'qiskit-terra': '0.19.2', 'qiskit-aer': '0.10.3', 'qiskit-ignis': '0.7.0', 'qiskit-ibmq-provider': '0.18.3', 'qiskit-aqua': '0.9.5', 'qiskit': '0.34.2', 'qiskit-nature': '0.3.1', 'qiskit-finance': '0.3.1', 'qiskit-optimization': '0.3.1', 'qiskit-machine-learning': '0.3.1'}
// Used Gate Set: ['rx', 'rz', 'cz', 'id', 'reset']
// Optimization Level: 3

OPENQASM 2.0;
include "qelib1.inc";
qreg eval[3];
qreg q[1];
creg meas[4];
rz(-pi/2) eval[0];
rx(pi/2) eval[0];
rz(3.6704043) eval[0];
rz(pi/2) eval[1];
rx(pi/2) eval[1];
rz(-0.78437923) eval[1];
rz(-pi/2) eval[2];
rx(pi/2) eval[2];
rz(3.6112822) eval[2];
rz(-pi/2) q[0];
cz eval[0],q[0];
rx(0.92729522) q[0];
rz(pi) q[0];
rx(pi) eval[0];
cz eval[0],q[0];
rx(-2.8577985) q[0];
rx(-pi) eval[0];
rz(1.4346837) eval[0];
cz eval[1],q[0];
rx(1.2870022) q[0];
rz(pi) q[0];
rx(pi) eval[1];
cz eval[1],q[0];
rx(-1.2870022) q[0];
rx(-pi) eval[1];
rz(1.5697774) eval[1];
cz eval[2],q[0];
rx(0.56758822) q[0];
rx(pi) eval[2];
cz eval[2],q[0];
rx(1.0032081) q[0];
rz(-pi/2) q[0];
rz(-1.1011068) eval[2];
rx(-0.59829053) eval[2];
cz eval[1],eval[2];
rx(pi) eval[1];
rx(pi/4) eval[2];
cz eval[1],eval[2];
rx(-1.0992178) eval[1];
rz(pi) eval[1];
rx(0.26640183) eval[2];
cz eval[0],eval[2];
rx(pi) eval[0];
rx(pi/8) eval[2];
rz(pi/2) eval[2];
cz eval[0],eval[2];
rz(-pi/4) eval[0];
cz eval[0],eval[1];
rx(pi) eval[0];
rx(pi/4) eval[1];
rz(pi/2) eval[1];
cz eval[0],eval[1];
rz(-pi/2) eval[0];
rx(pi/2) eval[0];
rz(-pi/2) eval[0];
rx(-pi/2) eval[1];
rz(-0.31381965) eval[1];
rx(pi/2) eval[2];
rz(1.2573914) eval[2];
barrier eval[0],eval[1],eval[2],q[0];
measure eval[0] -> meas[0];
measure eval[1] -> meas[1];
measure eval[2] -> meas[2];
measure q[0] -> meas[3];
