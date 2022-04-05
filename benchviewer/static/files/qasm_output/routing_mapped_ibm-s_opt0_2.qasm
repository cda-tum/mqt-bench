// Benchmark was created by MQT Bench on 2022-03-23
// MQT Bench version: 0.1.0
// Qiskit version: {'qiskit-terra': '0.19.2', 'qiskit-aer': '0.10.3', 'qiskit-ignis': '0.7.0', 'qiskit-ibmq-provider': '0.18.3', 'qiskit-aqua': '0.9.5', 'qiskit': '0.34.2', 'qiskit-nature': '0.3.1', 'qiskit-finance': '0.3.1', 'qiskit-optimization': '0.3.1', 'qiskit-machine-learning': '0.3.1'}
// Used Gate Set: ['id', 'rz', 'sx', 'x', 'cx', 'reset']
// Optimization Level: 0
// Coupling List: [[0, 1], [1, 0], [1, 2], [2, 1], [2, 3], [3, 2], [3, 4], [4, 3]]
// Compiled for architecture: ibm-s-fake_bogota

OPENQASM 2.0;
include "qelib1.inc";
qreg q[5];
rz(0.0) q[0];
sx q[0];
rz(6.00673589557934) q[0];
sx q[0];
rz(3*pi) q[0];
rz(0.0) q[1];
sx q[1];
rz(1.30490329765776) q[1];
sx q[1];
rz(3*pi) q[1];
cx q[0],q[1];
rz(0.0) q[0];
sx q[0];
rz(5.20527273096501) q[0];
sx q[0];
rz(3*pi) q[0];
rz(0.0) q[1];
sx q[1];
rz(0.937967242373524) q[1];
sx q[1];
rz(3*pi) q[1];
cx q[0],q[1];
rz(0.0) q[0];
sx q[0];
rz(3.22204643144809) q[0];
sx q[0];
rz(3*pi) q[0];
rz(0.0) q[1];
sx q[1];
rz(0.854008058939315) q[1];
sx q[1];
rz(3*pi) q[1];
cx q[0],q[1];
rz(0.0) q[0];
sx q[0];
rz(4.32934388587155) q[0];
sx q[0];
rz(3*pi) q[0];
rz(0.0) q[1];
sx q[1];
rz(5.28885693375076) q[1];
sx q[1];
rz(3*pi) q[1];
