// Benchmark was created by MQT Bench on 2022-03-23
// MQT Bench version: 0.1.0
// Qiskit version: {'qiskit-terra': '0.19.2', 'qiskit-aer': '0.10.3', 'qiskit-ignis': '0.7.0', 'qiskit-ibmq-provider': '0.18.3', 'qiskit-aqua': '0.9.5', 'qiskit': '0.34.2', 'qiskit-nature': '0.3.1', 'qiskit-finance': '0.3.1', 'qiskit-optimization': '0.3.1', 'qiskit-machine-learning': '0.3.1'}

OPENQASM 2.0;
include "qelib1.inc";
qreg q[3];
creg meas[3];
u3(0.87866129,0.19262225,0) q[0];
u3(0.28059901,0.79708533,0) q[1];
cx q[0],q[1];
u3(0.4507661,0.64255791,0) q[2];
cx q[0],q[2];
u3(0.74638344,0.4715587,0) q[0];
cx q[1],q[2];
u3(0.81446074,0.010187396,0) q[1];
cx q[0],q[1];
u3(0.7348499,0.67630418,0) q[2];
cx q[0],q[2];
u3(0.3057799,0.028403931,0) q[0];
cx q[1],q[2];
u3(0.20871476,0.8591383,0) q[1];
cx q[0],q[1];
u3(0.84249013,0.35087984,0) q[2];
cx q[0],q[2];
u3(0.18708393,0.19854857,0) q[0];
cx q[1],q[2];
u3(0.91463313,0.21121586,0) q[1];
u3(0.005997039,0.29262018,0) q[2];
barrier q[0],q[1],q[2];
measure q[0] -> meas[0];
measure q[1] -> meas[1];
measure q[2] -> meas[2];
