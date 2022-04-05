// Benchmark was created by MQT Bench on 2022-03-24
// MQT Bench version: 0.1.0
// Qiskit version: {'qiskit-terra': '0.19.2', 'qiskit-aer': '0.10.3', 'qiskit-ignis': '0.7.0', 'qiskit-ibmq-provider': '0.18.3', 'qiskit-aqua': '0.9.5', 'qiskit': '0.34.2', 'qiskit-nature': '0.3.1', 'qiskit-finance': '0.3.1', 'qiskit-optimization': '0.3.1', 'qiskit-machine-learning': '0.3.1'}

OPENQASM 2.0;
include "qelib1.inc";
qreg q[4];
u3(3.0038525,-pi,0) q[0];
u3(0.99049578,-pi,0) q[1];
cz q[0],q[1];
u3(1.5834476,-pi,0) q[2];
cz q[0],q[2];
cz q[1],q[2];
u3(2.5720792,0,-pi) q[3];
cz q[0],q[3];
ry(5.99424671903472) q[0];
cz q[1],q[3];
ry(1.47932143580702) q[1];
cz q[2],q[3];
ry(6.04295448864928) q[2];
ry(2.33198298268303) q[3];
