// Benchmark was created by MQT Bench on 2022-03-24
// MQT Bench version: 0.1.0
// Qiskit version: {'qiskit-terra': '0.19.2', 'qiskit-aer': '0.10.3', 'qiskit-ignis': '0.7.0', 'qiskit-ibmq-provider': '0.18.3', 'qiskit-aqua': '0.9.5', 'qiskit': '0.34.2', 'qiskit-nature': '0.3.1', 'qiskit-finance': '0.3.1', 'qiskit-optimization': '0.3.1', 'qiskit-machine-learning': '0.3.1'}

OPENQASM 2.0;
include "qelib1.inc";
qreg q[3];
creg meas[3];
ry(0.14746624496364) q[0];
ry(0.485015444304087) q[1];
cx q[0],q[1];
ry(0.309392208068307) q[2];
cx q[0],q[2];
ry(0.982822990098865) q[0];
cx q[1],q[2];
ry(0.0989644272665784) q[1];
cx q[0],q[1];
ry(0.000427718342424166) q[2];
cx q[0],q[2];
ry(0.655786419001016) q[0];
cx q[1],q[2];
ry(0.867478395418131) q[1];
cx q[0],q[1];
ry(0.947251213616135) q[2];
cx q[0],q[2];
ry(0.126883828314742) q[0];
cx q[1],q[2];
ry(0.734639336042693) q[1];
ry(0.546551147226067) q[2];
barrier q[0],q[1],q[2];
measure q[0] -> meas[0];
measure q[1] -> meas[1];
measure q[2] -> meas[2];
