// Benchmark was created by MQT Bench on 2022-04-13
// For more information about MQT Bench, please visit https://www.cda.cit.tum.de/mqtbench/
// MQT Bench version: 0.1.0
// Qiskit version: {'qiskit-terra': '0.19.2', 'qiskit-aer': '0.10.3', 'qiskit-ignis': '0.7.0', 'qiskit-ibmq-provider': '0.18.3', 'qiskit-aqua': '0.9.5', 'qiskit': '0.34.2', 'qiskit-nature': '0.3.1', 'qiskit-finance': '0.3.1', 'qiskit-optimization': '0.3.1', 'qiskit-machine-learning': '0.3.1'}
// Used Gate Set: ['id', 'rz', 'sx', 'x', 'cx', 'reset']
// Optimization Level: 2

OPENQASM 2.0;
include "qelib1.inc";
qreg q[4];
creg meas[4];
rz(0.74834728) q[0];
sx q[0];
rz(0.1558367) q[0];
rz(0.91240182) q[1];
cx q[0],q[1];
rz(pi/2) q[1];
sx q[1];
rz(1.519824) q[1];
rz(0.40573888) q[2];
cx q[0],q[2];
cx q[1],q[2];
rz(pi/2) q[2];
sx q[2];
rz(1.8297126) q[2];
rz(1.4137977) q[3];
cx q[0],q[3];
sx q[0];
rz(-0.283497) q[0];
cx q[1],q[3];
cx q[0],q[1];
rz(pi/2) q[1];
sx q[1];
rz(-0.8809671) q[1];
cx q[2],q[3];
cx q[0],q[2];
cx q[1],q[2];
rz(pi/2) q[2];
sx q[2];
rz(2.1417698) q[2];
rz(pi/2) q[3];
sx q[3];
rz(-1.7958631) q[3];
cx q[0],q[3];
sx q[0];
rz(pi/2) q[0];
cx q[1],q[3];
sx q[1];
rz(pi/2) q[1];
cx q[2],q[3];
sx q[2];
rz(pi/2) q[2];
rz(-pi/2) q[3];
sx q[3];
rz(-2.6771236) q[3];
sx q[3];
rz(-pi/2) q[3];
barrier q[0],q[1],q[2],q[3];
measure q[0] -> meas[0];
measure q[1] -> meas[1];
measure q[2] -> meas[2];
measure q[3] -> meas[3];
