// Benchmark was created by MQT Bench on 2022-04-08
// For more information about MQT Bench, please visit https://www.cda.cit.tum.de/mqtbench/
// MQT Bench version: 0.1.0
// Qiskit version: {'qiskit-terra': '0.19.2', 'qiskit-aer': '0.10.3', 'qiskit-ignis': '0.7.0', 'qiskit-ibmq-provider': '0.18.3', 'qiskit-aqua': '0.9.5', 'qiskit': '0.34.2', 'qiskit-nature': '0.3.1', 'qiskit-finance': '0.3.1', 'qiskit-optimization': '0.3.1', 'qiskit-machine-learning': '0.3.1'}

OPENQASM 2.0;
include "qelib1.inc";
qreg q[3];
creg meas[3];
ry(0.667932137938217) q[0];
ry(0.915714638026921) q[1];
cx q[0],q[1];
ry(0.676064752277633) q[2];
cx q[0],q[2];
ry(0.397339964525675) q[0];
cx q[1],q[2];
ry(0.311761577906195) q[1];
cx q[0],q[1];
ry(0.404229785108226) q[2];
cx q[0],q[2];
ry(0.590669753737999) q[0];
cx q[1],q[2];
ry(0.953896002540022) q[1];
cx q[0],q[1];
ry(0.450981706623153) q[2];
cx q[0],q[2];
ry(0.468254785013938) q[0];
cx q[1],q[2];
ry(0.735371497773062) q[1];
ry(0.103111790523991) q[2];
barrier q[0],q[1],q[2];
measure q[0] -> meas[0];
measure q[1] -> meas[1];
measure q[2] -> meas[2];
