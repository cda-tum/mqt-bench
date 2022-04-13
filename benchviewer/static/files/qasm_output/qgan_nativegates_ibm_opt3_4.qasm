// Benchmark was created by MQT Bench on 2022-04-09
// For more information about MQT Bench, please visit https://www.cda.cit.tum.de/mqtbench/
// MQT Bench version: 0.1.0
// Qiskit version: {'qiskit-terra': '0.19.2', 'qiskit-aer': '0.10.3', 'qiskit-ignis': '0.7.0', 'qiskit-ibmq-provider': '0.18.3', 'qiskit-aqua': '0.9.5', 'qiskit': '0.34.2', 'qiskit-nature': '0.3.1', 'qiskit-finance': '0.3.1', 'qiskit-optimization': '0.3.1', 'qiskit-machine-learning': '0.3.1'}
// Used Gate Set: ['id', 'rz', 'sx', 'x', 'cx', 'reset']
// Optimization Level: 3

OPENQASM 2.0;
include "qelib1.inc";
qreg q[4];
creg meas[4];
sx q[0];
rz(1.4644934) q[0];
sx q[0];
rz(-1.5696051) q[1];
sx q[1];
rz(-1.5713726) q[1];
sx q[1];
rz(-2.6910043) q[1];
cx q[0],q[1];
x q[0];
rz(pi/2) q[1];
sx q[1];
rz(-0.0013232938) q[1];
rz(-1.5695671) q[2];
sx q[2];
rz(-1.5712864) q[2];
sx q[2];
rz(-2.7621774) q[2];
cx q[0],q[2];
rz(-pi/2) q[2];
sx q[2];
rz(-1.569473) q[2];
sx q[2];
rz(-pi/2) q[2];
cx q[1],q[2];
rz(-pi/2) q[2];
sx q[2];
rz(pi/2) q[2];
rz(1.5701552) q[3];
sx q[3];
rz(-1.5719539) q[3];
sx q[3];
rz(-1.0649978) q[3];
cx q[0],q[3];
sx q[0];
rz(-1.6656863) q[0];
sx q[0];
rz(-pi/2) q[3];
sx q[3];
rz(-1.7216676) q[3];
sx q[3];
rz(-pi/2) q[3];
cx q[1],q[3];
sx q[1];
rz(0.61140743) q[1];
sx q[1];
rz(pi/2) q[3];
sx q[3];
rz(-2.0685468) q[3];
sx q[3];
rz(pi/2) q[3];
cx q[2],q[3];
sx q[2];
rz(1.1742191) q[2];
sx q[2];
rz(1.2660257) q[3];
sx q[3];
rz(-1.2400043) q[3];
sx q[3];
rz(1.4689794) q[3];
barrier q[0],q[1],q[2],q[3];
measure q[0] -> meas[0];
measure q[1] -> meas[1];
measure q[2] -> meas[2];
measure q[3] -> meas[3];
