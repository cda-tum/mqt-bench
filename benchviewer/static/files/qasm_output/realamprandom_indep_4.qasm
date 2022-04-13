// Benchmark was created by MQT Bench on 2022-04-08
// For more information about MQT Bench, please visit https://www.cda.cit.tum.de/mqtbench/
// MQT Bench version: 0.1.0
// Qiskit version: {'qiskit-terra': '0.19.2', 'qiskit-aer': '0.10.3', 'qiskit-ignis': '0.7.0', 'qiskit-ibmq-provider': '0.18.3', 'qiskit-aqua': '0.9.5', 'qiskit': '0.34.2', 'qiskit-nature': '0.3.1', 'qiskit-finance': '0.3.1', 'qiskit-optimization': '0.3.1', 'qiskit-machine-learning': '0.3.1'}

OPENQASM 2.0;
include "qelib1.inc";
qreg q[4];
creg meas[4];
ry(0.440102707271954) q[0];
ry(0.596399770113276) q[1];
cx q[0],q[1];
ry(0.279994478259484) q[2];
cx q[0],q[2];
cx q[1],q[2];
ry(0.505623254512984) q[3];
cx q[0],q[3];
ry(0.444755919557692) q[0];
cx q[1],q[3];
ry(0.261674397672376) q[1];
cx q[0],q[1];
cx q[2],q[3];
ry(0.358007383400196) q[2];
cx q[0],q[2];
cx q[1],q[2];
ry(0.121429372205814) q[3];
cx q[0],q[3];
ry(0.470809154169976) q[0];
cx q[1],q[3];
ry(0.863707416677608) q[1];
cx q[0],q[1];
cx q[2],q[3];
ry(0.99492387130577) q[2];
cx q[0],q[2];
cx q[1],q[2];
ry(0.154932585092747) q[3];
cx q[0],q[3];
ry(0.04865001814311) q[0];
cx q[1],q[3];
ry(0.216016989623934) q[1];
cx q[2],q[3];
ry(0.491957306672112) q[2];
ry(0.0331686014467321) q[3];
barrier q[0],q[1],q[2],q[3];
measure q[0] -> meas[0];
measure q[1] -> meas[1];
measure q[2] -> meas[2];
measure q[3] -> meas[3];
