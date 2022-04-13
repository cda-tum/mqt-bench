// Benchmark was created by MQT Bench on 2022-04-09
// For more information about MQT Bench, please visit https://www.cda.cit.tum.de/mqtbench/
// MQT Bench version: 0.1.0
// Qiskit version: {'qiskit-terra': '0.19.2', 'qiskit-aer': '0.10.3', 'qiskit-ignis': '0.7.0', 'qiskit-ibmq-provider': '0.18.3', 'qiskit-aqua': '0.9.5', 'qiskit': '0.34.2', 'qiskit-nature': '0.3.1', 'qiskit-finance': '0.3.1', 'qiskit-optimization': '0.3.1', 'qiskit-machine-learning': '0.3.1'}

OPENQASM 2.0;
include "qelib1.inc";
qreg q[4];
creg meas[4];
u3(1.6770993,0,-pi) q[0];
u3(0.45058866,0,-pi) q[1];
cz q[0],q[1];
u3(0.37941552,0,-pi) q[2];
cz q[0],q[2];
cz q[1],q[2];
u3(2.0765945,-pi,0) q[3];
cz q[0],q[3];
ry(1.66568634332848) q[0];
cz q[1],q[3];
ry(2.53018522042041) q[1];
cz q[2],q[3];
ry(5.1089662414032) q[2];
ry(1.85855725417167) q[3];
barrier q[0],q[1],q[2],q[3];
measure q[0] -> meas[0];
measure q[1] -> meas[1];
measure q[2] -> meas[2];
measure q[3] -> meas[3];
