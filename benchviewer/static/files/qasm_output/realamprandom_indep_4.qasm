// Benchmark was created by MQT Bench on 2022-03-21
// MQT Bench version: 0.1.0
// Qiskit version: {'qiskit-terra': '0.19.2', 'qiskit-aer': '0.10.3', 'qiskit-ignis': '0.7.0', 'qiskit-ibmq-provider': '0.18.3', 'qiskit-aqua': '0.9.5', 'qiskit': '0.34.2', 'qiskit-nature': '0.3.1', 'qiskit-finance': '0.3.1', 'qiskit-optimization': '0.3.1', 'qiskit-machine-learning': '0.3.1'}

OPENQASM 2.0;
include "qelib1.inc";
qreg q[4];
creg meas[4];
ry(0.385746476851301) q[0];
ry(0.46179329396112) q[1];
cx q[0],q[1];
ry(0.0640229580438976) q[2];
cx q[0],q[2];
cx q[1],q[2];
ry(0.0195192550778001) q[3];
cx q[0],q[3];
ry(0.763510182043912) q[0];
cx q[1],q[3];
ry(0.248602754770525) q[1];
cx q[0],q[1];
cx q[2],q[3];
ry(0.284362738787436) q[2];
cx q[0],q[2];
cx q[1],q[2];
ry(0.233016806623876) q[3];
cx q[0],q[3];
ry(0.756459202938074) q[0];
cx q[1],q[3];
ry(0.555188531063433) q[1];
cx q[0],q[1];
cx q[2],q[3];
ry(0.692373357181295) q[2];
cx q[0],q[2];
cx q[1],q[2];
ry(0.951717357712735) q[3];
cx q[0],q[3];
ry(0.797327612828815) q[0];
cx q[1],q[3];
ry(0.269076504966162) q[1];
cx q[2],q[3];
ry(0.150873789488579) q[2];
ry(0.956531325180906) q[3];
barrier q[0],q[1],q[2],q[3];
measure q[0] -> meas[0];
measure q[1] -> meas[1];
measure q[2] -> meas[2];
measure q[3] -> meas[3];
