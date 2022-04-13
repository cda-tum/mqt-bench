// Benchmark was created by MQT Bench on 2022-04-10
// For more information about MQT Bench, please visit https://www.cda.cit.tum.de/mqtbench/
// MQT Bench version: 0.1.0
// Qiskit version: {'qiskit-terra': '0.19.2', 'qiskit-aer': '0.10.3', 'qiskit-ignis': '0.7.0', 'qiskit-ibmq-provider': '0.18.3', 'qiskit-aqua': '0.9.5', 'qiskit': '0.34.2', 'qiskit-nature': '0.3.1', 'qiskit-finance': '0.3.1', 'qiskit-optimization': '0.3.1', 'qiskit-machine-learning': '0.3.1'}
// Used Gate Set: ['rx', 'rz', 'cz', 'id', 'reset']
// Optimization Level: 3

OPENQASM 2.0;
include "qelib1.inc";
qreg q[3];
creg meas[3];
rz(-pi/2) q[0];
rx(0.34886207) q[0];
rz(0.62560117) q[0];
rz(2.4489917) q[1];
rx(1.233905) q[1];
rz(-3.5207139) q[1];
cz q[0],q[1];
rx(pi/2) q[1];
rz(3.7947066) q[1];
rz(2.1776852) q[2];
rx(0.78102471) q[2];
rz(-5.0723112) q[2];
cz q[0],q[2];
rx(0.74072738) q[0];
rz(2.0810718) q[0];
cz q[1],q[2];
rx(1.3322052) q[1];
rz(1.3919034) q[1];
cz q[0],q[1];
rx(pi/2) q[1];
rz(pi/2) q[1];
rx(-pi/2) q[1];
rx(0.69805142) q[2];
rz(-0.12786603) q[2];
cz q[0],q[2];
rx(0.53877713) q[0];
rz(1.0847349) q[0];
rx(-0.90744749) q[0];
rx(-pi) q[2];
cz q[1],q[2];
rz(-1.8096194) q[1];
rx(2.3026831) q[1];
rz(-1.7320875) q[1];
cz q[0],q[1];
rx(pi/2) q[1];
rz(pi/2) q[1];
rx(pi/2) q[1];
rz(-1.2371928) q[2];
rx(2.7555304) q[2];
rz(1.8814508) q[2];
cz q[0],q[2];
rx(1.2544011) q[0];
rz(0.75051843) q[0];
rx(-1.3357862) q[0];
cz q[1],q[2];
rx(0.13343497) q[1];
rz(0.78838627) q[1];
rx(-0.1881512) q[1];
rx(1.800279) q[2];
rz(1.2826073) q[2];
rx(1.5045013) q[2];
barrier q[0],q[1],q[2];
measure q[0] -> meas[0];
measure q[1] -> meas[1];
measure q[2] -> meas[2];
