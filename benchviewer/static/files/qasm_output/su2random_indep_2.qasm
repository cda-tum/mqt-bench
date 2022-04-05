// Benchmark was created by MQT Bench on 2022-03-23
// MQT Bench version: 0.1.0
// Qiskit version: {'qiskit-terra': '0.19.2', 'qiskit-aer': '0.10.3', 'qiskit-ignis': '0.7.0', 'qiskit-ibmq-provider': '0.18.3', 'qiskit-aqua': '0.9.5', 'qiskit': '0.34.2', 'qiskit-nature': '0.3.1', 'qiskit-finance': '0.3.1', 'qiskit-optimization': '0.3.1', 'qiskit-machine-learning': '0.3.1'}

OPENQASM 2.0;
include "qelib1.inc";
qreg q[2];
creg meas[2];
u3(0.83830693,0.48905304,0) q[0];
u3(0.66458532,0.58428082,0) q[1];
cx q[0],q[1];
u3(0.025873112,0.0030536814,0) q[0];
u3(0.5491938,0.48455581,0) q[1];
cx q[0],q[1];
u3(0.80955163,0.0065582214,0) q[0];
u3(0.067506903,0.7984719,0) q[1];
cx q[0],q[1];
u3(0.16683391,0.69672978,0) q[0];
u3(0.4360357,0.026558347,0) q[1];
barrier q[0],q[1];
measure q[0] -> meas[0];
measure q[1] -> meas[1];
