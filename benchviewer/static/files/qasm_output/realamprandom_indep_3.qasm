// Benchmark was created by MQT Bench on 2022-03-21
// MQT Bench version: 0.1.0
// Qiskit version: {'qiskit-terra': '0.19.2', 'qiskit-aer': '0.10.3', 'qiskit-ignis': '0.7.0', 'qiskit-ibmq-provider': '0.18.3', 'qiskit-aqua': '0.9.5', 'qiskit': '0.34.2', 'qiskit-nature': '0.3.1', 'qiskit-finance': '0.3.1', 'qiskit-optimization': '0.3.1', 'qiskit-machine-learning': '0.3.1'}

OPENQASM 2.0;
include "qelib1.inc";
qreg q[3];
creg meas[3];
ry(0.0528509031040038) q[0];
ry(0.306766093657403) q[1];
cx q[0],q[1];
ry(0.135492039030627) q[2];
cx q[0],q[2];
ry(0.0857454656709278) q[0];
cx q[1],q[2];
ry(0.585750663012298) q[1];
cx q[0],q[1];
ry(0.988817314507591) q[2];
cx q[0],q[2];
ry(0.547519782750423) q[0];
cx q[1],q[2];
ry(0.648930486697847) q[1];
cx q[0],q[1];
ry(0.0284110103717194) q[2];
cx q[0],q[2];
ry(0.0434221589882515) q[0];
cx q[1],q[2];
ry(0.913946268768217) q[1];
ry(0.0157096448462561) q[2];
barrier q[0],q[1],q[2];
measure q[0] -> meas[0];
measure q[1] -> meas[1];
measure q[2] -> meas[2];
