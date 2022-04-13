// Benchmark was created by MQT Bench on 2022-04-13
// For more information about MQT Bench, please visit https://www.cda.cit.tum.de/mqtbench/
// MQT Bench version: 0.1.0
// Qiskit version: {'qiskit-terra': '0.19.2', 'qiskit-aer': '0.10.3', 'qiskit-ignis': '0.7.0', 'qiskit-ibmq-provider': '0.18.3', 'qiskit-aqua': '0.9.5', 'qiskit': '0.34.2', 'qiskit-nature': '0.3.1', 'qiskit-finance': '0.3.1', 'qiskit-optimization': '0.3.1', 'qiskit-machine-learning': '0.3.1'}

OPENQASM 2.0;
include "qelib1.inc";
qreg q[4];
creg meas[4];
u2(0,1.4543746) q[0];
u2(0,1.2912126) q[1];
cz q[0],q[1];
u2(0,-1.14304) q[2];
cz q[0],q[2];
cz q[1],q[2];
u2(0,-2.4724931) q[3];
cz q[0],q[3];
u2(0,-3.026394) q[0];
cz q[1],q[3];
u2(0,-2.88908) q[1];
cz q[0],q[1];
cz q[2],q[3];
u2(0,2.9787299) q[2];
cz q[0],q[2];
cz q[1],q[2];
u2(0,-0.53613517) q[3];
cz q[0],q[3];
u2(0,-0.15425669) q[0];
cz q[1],q[3];
u2(0,-2.375081) q[1];
cz q[2],q[3];
u2(0,0.16755905) q[2];
u2(0,0.19996978) q[3];
barrier q[0],q[1],q[2],q[3];
measure q[0] -> meas[0];
measure q[1] -> meas[1];
measure q[2] -> meas[2];
measure q[3] -> meas[3];
