// Benchmark was created by MQT Bench on 2022-04-09
// For more information about MQT Bench, please visit https://www.cda.cit.tum.de/mqtbench/
// MQT Bench version: 0.1.0
// Qiskit version: {'qiskit-terra': '0.19.2', 'qiskit-aer': '0.10.3', 'qiskit-ignis': '0.7.0', 'qiskit-ibmq-provider': '0.18.3', 'qiskit-aqua': '0.9.5', 'qiskit': '0.34.2', 'qiskit-nature': '0.3.1', 'qiskit-finance': '0.3.1', 'qiskit-optimization': '0.3.1', 'qiskit-machine-learning': '0.3.1'}

OPENQASM 2.0;
include "qelib1.inc";
qreg q[2];
creg meas[2];
ry(2.86514324198955) q[0];
ry(-1.83668935593204) q[1];
cx q[0],q[1];
ry(2.06368007737522) q[0];
ry(-2.20362541121627) q[1];
cx q[0],q[1];
ry(0.0804537778582946) q[0];
ry(-2.28758459465048) q[1];
cx q[0],q[1];
ry(1.18775123228175) q[0];
ry(2.14726428016097) q[1];
barrier q[0],q[1];
measure q[0] -> meas[0];
measure q[1] -> meas[1];
