// Benchmark was created by MQT Bench on 2022-04-09
// For more information about MQT Bench, please visit https://www.cda.cit.tum.de/mqtbench/
// MQT Bench version: 0.1.0
// Qiskit version: {'qiskit-terra': '0.19.2', 'qiskit-aer': '0.10.3', 'qiskit-ignis': '0.7.0', 'qiskit-ibmq-provider': '0.18.3', 'qiskit-aqua': '0.9.5', 'qiskit': '0.34.2', 'qiskit-nature': '0.3.1', 'qiskit-finance': '0.3.1', 'qiskit-optimization': '0.3.1', 'qiskit-machine-learning': '0.3.1'}
// Used Gate Set: ['id', 'rz', 'sx', 'x', 'cx', 'reset']
// Optimization Level: 3
// Coupling List: [[0, 1], [1, 0], [1, 2], [2, 1], [2, 3], [3, 2], [3, 4], [4, 3]]
// Compiled for architecture: ibm-s-fake_bogota

OPENQASM 2.0;
include "qelib1.inc";
qreg q[5];
creg meas[3];
rz(-pi) q[1];
sx q[1];
rz(1.9474786) q[1];
sx q[1];
sx q[2];
rz(1.1705332) q[2];
sx q[2];
rz(1.570243) q[3];
sx q[3];
rz(-1.5695943) q[3];
sx q[3];
rz(1.1394174) q[3];
cx q[2],q[3];
rz(-3.1402694) q[2];
sx q[2];
rz(pi/2) q[2];
cx q[1],q[2];
rz(-pi) q[1];
rz(-1.0957689) q[2];
sx q[2];
rz(-1.5696195) q[2];
sx q[2];
rz(1.5714016) q[2];
rz(pi/2) q[3];
sx q[3];
rz(-0.0013232938) q[3];
cx q[2],q[3];
cx q[3],q[2];
cx q[2],q[3];
rz(-0.0013232938) q[2];
sx q[2];
rz(-pi/2) q[2];
cx q[1],q[2];
sx q[1];
rz(0.31844569) q[1];
sx q[1];
rz(1.0444527) q[2];
sx q[2];
rz(-1.5719405) q[2];
sx q[2];
rz(-1.5701315) q[2];
barrier q[2],q[4],q[1],q[3],q[0];
measure q[3] -> meas[0];
measure q[2] -> meas[1];
measure q[1] -> meas[2];
