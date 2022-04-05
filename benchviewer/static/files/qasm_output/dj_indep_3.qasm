// Benchmark was created by MQT Bench on 2022-03-22
// MQT Bench version: 0.1.0
// Qiskit version: {'qiskit-terra': '0.19.2', 'qiskit-aer': '0.10.3', 'qiskit-ignis': '0.7.0', 'qiskit-ibmq-provider': '0.18.3', 'qiskit-aqua': '0.9.5', 'qiskit': '0.34.2', 'qiskit-nature': '0.3.1', 'qiskit-finance': '0.3.1', 'qiskit-optimization': '0.3.1', 'qiskit-machine-learning': '0.3.1'}

OPENQASM 2.0;
include "qelib1.inc";
qreg q[3];
creg c[2];
u2(0,0) q[0];
u2(0,0) q[1];
u2(-pi,-pi) q[2];
cx q[0],q[2];
u2(-pi,-pi) q[0];
cx q[1],q[2];
u2(-pi,-pi) q[1];
measure q[0] -> c[0];
measure q[1] -> c[1];
