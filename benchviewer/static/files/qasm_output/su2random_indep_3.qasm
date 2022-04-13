// Benchmark was created by MQT Bench on 2022-04-10
// For more information about MQT Bench, please visit https://www.cda.cit.tum.de/mqtbench/
// MQT Bench version: 0.1.0
// Qiskit version: {'qiskit-terra': '0.19.2', 'qiskit-aer': '0.10.3', 'qiskit-ignis': '0.7.0', 'qiskit-ibmq-provider': '0.18.3', 'qiskit-aqua': '0.9.5', 'qiskit': '0.34.2', 'qiskit-nature': '0.3.1', 'qiskit-finance': '0.3.1', 'qiskit-optimization': '0.3.1', 'qiskit-machine-learning': '0.3.1'}

OPENQASM 2.0;
include "qelib1.inc";
qreg q[3];
creg meas[3];
u3(0.34886207,0.62560117,0) q[0];
u3(0.50169489,0.8129628,0) q[1];
cx q[0],q[1];
u3(0.88741297,0.41316044,0) q[2];
cx q[0],q[2];
u3(0.74072738,0.51027551,0) q[0];
cx q[1],q[2];
u3(0.29718271,0.63161446,0) q[1];
cx q[0],q[1];
u3(0.08205111,0.69401811,0) q[2];
cx q[0],q[2];
u3(0.77075308,0.86165892,0) q[0];
cx q[1],q[2];
u3(0.74622122,0.17690119,0) q[1];
cx q[0],q[1];
u3(0.36668172,0.12361373,0) q[2];
cx q[0],q[2];
u3(0.72518068,0.21383074,0) q[0];
cx q[1],q[2];
u3(0.13304619,0.7794835,0) q[1];
u3(0.29550903,0.21985984,0) q[2];
barrier q[0],q[1],q[2];
measure q[0] -> meas[0];
measure q[1] -> meas[1];
measure q[2] -> meas[2];
