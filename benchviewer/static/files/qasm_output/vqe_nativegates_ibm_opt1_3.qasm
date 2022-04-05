// Benchmark was created by MQT Bench on 2022-03-26
// MQT Bench version: 0.1.0
// Qiskit version: {'qiskit-terra': '0.19.2', 'qiskit-aer': '0.10.3', 'qiskit-ignis': '0.7.0', 'qiskit-ibmq-provider': '0.18.3', 'qiskit-aqua': '0.9.5', 'qiskit': '0.34.2', 'qiskit-nature': '0.3.1', 'qiskit-finance': '0.3.1', 'qiskit-optimization': '0.3.1', 'qiskit-machine-learning': '0.3.1'}
// Used Gate Set: ['id', 'rz', 'sx', 'x', 'cx', 'reset']
// Optimization Level: 1

OPENQASM 2.0;
include "qelib1.inc";
qreg q[3];
creg meas[3];
sx q[0];
rz(1.0844822) q[0];
sx q[0];
rz(-pi) q[0];
sx q[1];
rz(1.8807675) q[1];
sx q[1];
rz(-pi) q[1];
cx q[0],q[1];
rz(-pi) q[2];
sx q[2];
rz(2.2081169) q[2];
sx q[2];
cx q[0],q[2];
sx q[0];
rz(0.40662204) q[0];
sx q[0];
rz(-pi) q[0];
cx q[1],q[2];
rz(-pi) q[1];
sx q[1];
rz(2.3014778) q[1];
sx q[1];
cx q[0],q[1];
sx q[2];
rz(1.7530182) q[2];
sx q[2];
rz(-pi) q[2];
cx q[0],q[2];
sx q[0];
rz(1.1684207) q[0];
sx q[0];
rz(-pi) q[0];
cx q[1],q[2];
sx q[1];
rz(3.07278) q[1];
sx q[1];
rz(-pi) q[1];
sx q[2];
rz(2.2222689) q[2];
sx q[2];
rz(-pi) q[2];
barrier q[0],q[1],q[2];
measure q[0] -> meas[0];
measure q[1] -> meas[1];
measure q[2] -> meas[2];
