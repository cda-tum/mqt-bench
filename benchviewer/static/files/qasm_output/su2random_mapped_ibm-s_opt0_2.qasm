// Benchmark was created by MQT Bench on 2022-04-10
// For more information about MQT Bench, please visit https://www.cda.cit.tum.de/mqtbench/
// MQT Bench version: 0.1.0
// Qiskit version: {'qiskit-terra': '0.19.2', 'qiskit-aer': '0.10.3', 'qiskit-ignis': '0.7.0', 'qiskit-ibmq-provider': '0.18.3', 'qiskit-aqua': '0.9.5', 'qiskit': '0.34.2', 'qiskit-nature': '0.3.1', 'qiskit-finance': '0.3.1', 'qiskit-optimization': '0.3.1', 'qiskit-machine-learning': '0.3.1'}
// Used Gate Set: ['id', 'rz', 'sx', 'x', 'cx', 'reset']
// Optimization Level: 0
// Coupling List: [[0, 1], [1, 0], [1, 2], [2, 1], [2, 3], [3, 2], [3, 4], [4, 3]]
// Compiled for architecture: ibm-s-fake_bogota

OPENQASM 2.0;
include "qelib1.inc";
qreg q[5];
creg meas[2];
rz(0.0) q[0];
sx q[0];
rz(4.1199737324286) q[0];
sx q[0];
rz(3*pi) q[0];
rz(0.941721887183498) q[0];
rz(0.0) q[1];
sx q[1];
rz(3.75356302931032) q[1];
sx q[1];
rz(3*pi) q[1];
rz(0.579624001616089) q[1];
cx q[0],q[1];
rz(0.0) q[0];
sx q[0];
rz(4.06726843584606) q[0];
sx q[0];
rz(3*pi) q[0];
rz(0.873530886778315) q[0];
rz(0.0) q[1];
sx q[1];
rz(3.22898501271982) q[1];
sx q[1];
rz(3*pi) q[1];
rz(0.185340386083191) q[1];
cx q[0],q[1];
rz(0.0) q[0];
sx q[0];
rz(3.22586166182133) q[0];
sx q[0];
rz(3*pi) q[0];
rz(0.201172999375883) q[0];
rz(0.0) q[1];
sx q[1];
rz(3.18066521843402) q[1];
sx q[1];
rz(3*pi) q[1];
rz(0.426149608211637) q[1];
cx q[0],q[1];
rz(0.0) q[0];
sx q[0];
rz(3.40306881159464) q[0];
sx q[0];
rz(3*pi) q[0];
rz(0.954645191699434) q[0];
rz(0.0) q[1];
sx q[1];
rz(3.22111228779923) q[1];
sx q[1];
rz(3*pi) q[1];
rz(0.508463705088342) q[1];
barrier q[0],q[1];
measure q[0] -> meas[0];
measure q[1] -> meas[1];
