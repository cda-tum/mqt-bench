// Benchmark was created by MQT Bench on 2022-03-24
// MQT Bench version: 0.1.0
// Qiskit version: {'qiskit-terra': '0.19.2', 'qiskit-aer': '0.10.3', 'qiskit-ignis': '0.7.0', 'qiskit-ibmq-provider': '0.18.3', 'qiskit-aqua': '0.9.5', 'qiskit': '0.34.2', 'qiskit-nature': '0.3.1', 'qiskit-finance': '0.3.1', 'qiskit-optimization': '0.3.1', 'qiskit-machine-learning': '0.3.1'}

OPENQASM 2.0;
include "qelib1.inc";
qreg q[3];
u3(2.5519645,0,-pi) q[0];
u3(0.98842369,-pi,0) q[1];
cz q[0],q[1];
u3(0.67176942,-pi,0) q[2];
cz q[0],q[2];
ry(4.59617139598176) q[0];
cz q[1],q[2];
ry(3.53155494081205) q[1];
ry(3.38423350627402) q[2];
