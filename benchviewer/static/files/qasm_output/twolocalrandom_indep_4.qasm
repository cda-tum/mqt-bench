// Benchmark was created by MQT Bench on 2022-04-11
// For more information about MQT Bench, please visit https://www.cda.cit.tum.de/mqtbench/
// MQT Bench version: 0.1.0
// Qiskit version: {'qiskit-terra': '0.19.2', 'qiskit-aer': '0.10.3', 'qiskit-ignis': '0.7.0', 'qiskit-ibmq-provider': '0.18.3', 'qiskit-aqua': '0.9.5', 'qiskit': '0.34.2', 'qiskit-nature': '0.3.1', 'qiskit-finance': '0.3.1', 'qiskit-optimization': '0.3.1', 'qiskit-machine-learning': '0.3.1'}

OPENQASM 2.0;
include "qelib1.inc";
qreg q[4];
creg meas[4];
ry(0.527375900430352) q[0];
ry(0.748664414814351) q[1];
cx q[0],q[1];
ry(0.174594085031227) q[2];
cx q[0],q[2];
cx q[1],q[2];
ry(0.00645745287883159) q[3];
cx q[0],q[3];
ry(0.380112153497047) q[0];
cx q[1],q[3];
ry(0.455844364791778) q[1];
cx q[0],q[1];
cx q[2],q[3];
ry(0.484639067046327) q[2];
cx q[0],q[2];
cx q[1],q[2];
ry(0.314457591772084) q[3];
cx q[0],q[3];
ry(0.0830509478756317) q[0];
cx q[1],q[3];
ry(0.67820205984155) q[1];
cx q[0],q[1];
cx q[2],q[3];
ry(0.234006151422778) q[2];
cx q[0],q[2];
cx q[1],q[2];
ry(0.914735090471568) q[3];
cx q[0],q[3];
ry(0.597882470961247) q[0];
cx q[1],q[3];
ry(0.453983335880367) q[1];
cx q[2],q[3];
ry(0.221343550617468) q[2];
ry(0.901338095843427) q[3];
barrier q[0],q[1],q[2],q[3];
measure q[0] -> meas[0];
measure q[1] -> meas[1];
measure q[2] -> meas[2];
measure q[3] -> meas[3];
