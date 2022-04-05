// Benchmark was created by MQT Bench on 2022-03-26
// MQT Bench version: 0.1.0
// Qiskit version: {'qiskit-terra': '0.19.2', 'qiskit-aer': '0.10.3', 'qiskit-ignis': '0.7.0', 'qiskit-ibmq-provider': '0.18.3', 'qiskit-aqua': '0.9.5', 'qiskit': '0.34.2', 'qiskit-nature': '0.3.1', 'qiskit-finance': '0.3.1', 'qiskit-optimization': '0.3.1', 'qiskit-machine-learning': '0.3.1'}

OPENQASM 2.0;
include "qelib1.inc";
qreg q[3];
creg meas[3];
ry(-2.0571104424665) q[0];
ry(-1.26082511631692) q[1];
cx q[0],q[1];
ry(0.933475741965452) q[2];
cx q[0],q[2];
ry(-2.73497061229015) q[0];
cx q[1],q[2];
ry(0.840114867237831) q[1];
cx q[0],q[1];
ry(-1.3885744066224) q[2];
cx q[0],q[2];
ry(-1.97317199291756) q[0];
cx q[1],q[2];
ry(-0.0688126618779186) q[1];
ry(-0.919323745828007) q[2];
barrier q[0],q[1],q[2];
measure q[0] -> meas[0];
measure q[1] -> meas[1];
measure q[2] -> meas[2];
