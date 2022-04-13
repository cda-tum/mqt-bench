// Benchmark was created by MQT Bench on 2022-04-10
// For more information about MQT Bench, please visit https://www.cda.cit.tum.de/mqtbench/
// MQT Bench version: 0.1.0
// Qiskit version: {'qiskit-terra': '0.19.2', 'qiskit-aer': '0.10.3', 'qiskit-ignis': '0.7.0', 'qiskit-ibmq-provider': '0.18.3', 'qiskit-aqua': '0.9.5', 'qiskit': '0.34.2', 'qiskit-nature': '0.3.1', 'qiskit-finance': '0.3.1', 'qiskit-optimization': '0.3.1', 'qiskit-machine-learning': '0.3.1'}
// Used Gate Set: ['rx', 'rz', 'cz', 'id', 'reset']
// Optimization Level: 2

OPENQASM 2.0;
include "qelib1.inc";
qreg q[3];
creg meas[3];
rx(0.44196676) q[0];
rz(0.70473713) q[0];
rx(-0.55583035) q[0];
rx(pi/2) q[1];
rz(2.0724912) q[1];
rx(2.3837591) q[1];
cz q[0],q[1];
rx(pi/2) q[1];
rz(pi/2) q[1];
rx(pi/2) q[1];
rx(pi/2) q[2];
rz(2.4582093) q[2];
rx(1.9839568) q[2];
cz q[0],q[2];
rx(0.87836566) q[0];
rz(0.8711242) q[0];
rx(-1.0802221) q[0];
cz q[1],q[2];
rx(pi/2) q[1];
rz(1.867979) q[1];
rx(2.2024108) q[1];
cz q[0],q[1];
rx(pi/2) q[1];
rz(pi/2) q[1];
rx(pi/2) q[1];
rx(-pi/2) q[2];
rz(0.08205111) q[2];
rx(2.2648144) q[2];
cz q[0],q[2];
rx(0.53877713) q[0];
rz(1.0847349) q[0];
rx(-0.90744749) q[0];
cz q[1],q[2];
rx(pi/2) q[1];
rz(2.3170175) q[1];
rx(1.7476975) q[1];
cz q[0],q[1];
rx(pi/2) q[1];
rz(pi/2) q[1];
rx(pi/2) q[1];
rx(-pi/2) q[2];
rz(0.36668172) q[2];
rx(1.6944101) q[2];
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
