// Benchmark was created by MQT Bench on 2022-03-24
// MQT Bench version: 0.1.0
// Qiskit version: {'qiskit-terra': '0.19.2', 'qiskit-aer': '0.10.3', 'qiskit-ignis': '0.7.0', 'qiskit-ibmq-provider': '0.18.3', 'qiskit-aqua': '0.9.5', 'qiskit': '0.34.2', 'qiskit-nature': '0.3.1', 'qiskit-finance': '0.3.1', 'qiskit-optimization': '0.3.1', 'qiskit-machine-learning': '0.3.1'}

OPENQASM 2.0;
include "qelib1.inc";
qreg q[5];
u3(2.0264197,0,-pi) q[0];
u3(0.65343607,0,-pi) q[1];
cz q[0],q[1];
u3(0.96154465,-pi,0) q[2];
cz q[0],q[2];
cz q[1],q[2];
u3(1.3661671,-pi,0) q[3];
cz q[0],q[3];
cz q[1],q[3];
cz q[2],q[3];
u3(2.4201091,-pi,0) q[4];
cz q[0],q[4];
ry(4.38950783513777) q[0];
cz q[1],q[4];
ry(5.01933173077815) q[1];
cz q[2],q[4];
ry(3.69235635180722) q[2];
cz q[3],q[4];
ry(3.04383298393737) q[3];
ry(4.86958908380973) q[4];
