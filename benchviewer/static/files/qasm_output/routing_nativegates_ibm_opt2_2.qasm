// Benchmark was created by MQT Bench on 2022-03-23
// MQT Bench version: 0.1.0
// Qiskit version: {'qiskit-terra': '0.19.2', 'qiskit-aer': '0.10.3', 'qiskit-ignis': '0.7.0', 'qiskit-ibmq-provider': '0.18.3', 'qiskit-aqua': '0.9.5', 'qiskit': '0.34.2', 'qiskit-nature': '0.3.1', 'qiskit-finance': '0.3.1', 'qiskit-optimization': '0.3.1', 'qiskit-machine-learning': '0.3.1'}
// Used Gate Set: ['id', 'rz', 'sx', 'x', 'cx', 'reset']
// Optimization Level: 2

OPENQASM 2.0;
include "qelib1.inc";
qreg q[2];
rz(-pi) q[0];
sx q[0];
rz(0.27644941) q[0];
sx q[0];
sx q[1];
rz(1.3049033) q[1];
sx q[1];
rz(-pi) q[1];
cx q[0],q[1];
rz(-pi) q[0];
sx q[0];
rz(1.0779126) q[0];
sx q[0];
sx q[1];
rz(0.93796724) q[1];
sx q[1];
rz(-pi) q[1];
cx q[0],q[1];
rz(-pi) q[0];
sx q[0];
rz(3.0611389) q[0];
sx q[0];
sx q[1];
rz(0.85400806) q[1];
sx q[1];
rz(-pi) q[1];
cx q[0],q[1];
rz(-pi) q[0];
sx q[0];
rz(1.9538414) q[0];
sx q[0];
rz(-pi) q[1];
sx q[1];
rz(0.99432837) q[1];
sx q[1];
