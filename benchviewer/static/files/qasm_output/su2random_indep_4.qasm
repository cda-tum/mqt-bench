// Benchmark was created by MQT Bench on 2022-03-23
// MQT Bench version: 0.1.0
// Qiskit version: {'qiskit-terra': '0.19.2', 'qiskit-aer': '0.10.3', 'qiskit-ignis': '0.7.0', 'qiskit-ibmq-provider': '0.18.3', 'qiskit-aqua': '0.9.5', 'qiskit': '0.34.2', 'qiskit-nature': '0.3.1', 'qiskit-finance': '0.3.1', 'qiskit-optimization': '0.3.1', 'qiskit-machine-learning': '0.3.1'}

OPENQASM 2.0;
include "qelib1.inc";
qreg q[4];
creg meas[4];
u3(0.56461629,0.48532464,0) q[0];
u3(0.94784973,0.23943842,0) q[1];
cx q[0],q[1];
u3(0.044551344,0.058927121,0) q[2];
cx q[0],q[2];
cx q[1],q[2];
u3(0.42796594,0.24160167,0) q[3];
cx q[0],q[3];
u3(0.4844069,0.67247484,0) q[0];
cx q[1],q[3];
u3(0.31405097,0.27465877,0) q[1];
cx q[0],q[1];
cx q[2],q[3];
u3(0.37804512,0.14213905,0) q[2];
cx q[0],q[2];
cx q[1],q[2];
u3(0.35370119,0.60721265,0) q[3];
cx q[0],q[3];
u3(0.22047351,0.03931215,0) q[0];
cx q[1],q[3];
u3(0.56767341,0.83443898,0) q[1];
cx q[0],q[1];
cx q[2],q[3];
u3(0.057458497,0.17343683,0) q[2];
cx q[0],q[2];
cx q[1],q[2];
u3(0.035431277,0.34719094,0) q[3];
cx q[0],q[3];
u3(0.96329212,0.3320376,0) q[0];
cx q[1],q[3];
u3(0.94108203,0.90659019,0) q[1];
cx q[2],q[3];
u3(0.16280298,0.27733565,0) q[2];
u3(0.20424428,0.94887932,0) q[3];
barrier q[0],q[1],q[2],q[3];
measure q[0] -> meas[0];
measure q[1] -> meas[1];
measure q[2] -> meas[2];
measure q[3] -> meas[3];
