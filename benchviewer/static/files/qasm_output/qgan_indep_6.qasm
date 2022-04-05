// Benchmark was created by MQT Bench on 2022-03-24
// MQT Bench version: 0.1.0
// Qiskit version: {'qiskit-terra': '0.19.2', 'qiskit-aer': '0.10.3', 'qiskit-ignis': '0.7.0', 'qiskit-ibmq-provider': '0.18.3', 'qiskit-aqua': '0.9.5', 'qiskit': '0.34.2', 'qiskit-nature': '0.3.1', 'qiskit-finance': '0.3.1', 'qiskit-optimization': '0.3.1', 'qiskit-machine-learning': '0.3.1'}

OPENQASM 2.0;
include "qelib1.inc";
qreg q[6];
u3(1.6303329,0,-pi) q[0];
u3(2.5405723,-pi,0) q[1];
cz q[0],q[1];
u3(1.2796131,0,-pi) q[2];
cz q[0],q[2];
cz q[1],q[2];
u3(0.75267856,0,-pi) q[3];
cz q[0],q[3];
cz q[1],q[3];
cz q[2],q[3];
u3(1.1557098,-pi,0) q[4];
cz q[0],q[4];
cz q[1],q[4];
cz q[2],q[4];
cz q[3],q[4];
u3(1.230205,-pi,0) q[5];
cz q[0],q[5];
ry(4.14188064702539) q[0];
cz q[1],q[5];
ry(6.1169919965188) q[1];
cz q[2],q[5];
ry(6.01101544823628) q[2];
cz q[3],q[5];
ry(5.79904755862298) q[3];
cz q[4],q[5];
ry(3.88427803318257) q[4];
ry(1.09249843610554) q[5];
