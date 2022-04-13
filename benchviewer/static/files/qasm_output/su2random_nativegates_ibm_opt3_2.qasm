// Benchmark was created by MQT Bench on 2022-04-10
// For more information about MQT Bench, please visit https://www.cda.cit.tum.de/mqtbench/
// MQT Bench version: 0.1.0
// Qiskit version: {'qiskit-terra': '0.19.2', 'qiskit-aer': '0.10.3', 'qiskit-ignis': '0.7.0', 'qiskit-ibmq-provider': '0.18.3', 'qiskit-aqua': '0.9.5', 'qiskit': '0.34.2', 'qiskit-nature': '0.3.1', 'qiskit-finance': '0.3.1', 'qiskit-optimization': '0.3.1', 'qiskit-machine-learning': '0.3.1'}
// Used Gate Set: ['id', 'rz', 'sx', 'x', 'cx', 'reset']
// Optimization Level: 3

OPENQASM 2.0;
include "qelib1.inc";
qreg q[2];
creg meas[2];
rz(2.2949423) q[0];
sx q[0];
rz(-2.2638076) q[0];
sx q[0];
rz(-2.415504) q[0];
rz(2.3696572) q[1];
sx q[1];
rz(-1.9220285) q[1];
sx q[1];
rz(-2.7136308) q[1];
cx q[1],q[0];
rz(0.33396358) q[0];
sx q[1];
rz(-3.1117104) q[1];
cx q[1],q[0];
rz(0.010411428) q[0];
sx q[1];
cx q[1],q[0];
rz(2.1347749) q[0];
sx q[0];
rz(-1.3510359) q[0];
sx q[0];
rz(-2.7041688) q[0];
rz(0.18348767) q[1];
sx q[1];
rz(-1.4718019) q[1];
sx q[1];
rz(-0.85911724) q[1];
barrier q[0],q[1];
measure q[0] -> meas[0];
measure q[1] -> meas[1];
