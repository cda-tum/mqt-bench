// Benchmark was created by MQT Bench on 2022-03-21
// MQT Bench version: 0.1.0
// Qiskit version: {'qiskit-terra': '0.19.2', 'qiskit-aer': '0.10.3', 'qiskit-ignis': '0.7.0', 'qiskit-ibmq-provider': '0.18.3', 'qiskit-aqua': '0.9.5', 'qiskit': '0.34.2', 'qiskit-nature': '0.3.1', 'qiskit-finance': '0.3.1', 'qiskit-optimization': '0.3.1', 'qiskit-machine-learning': '0.3.1'}

OPENQASM 2.0;
include "qelib1.inc";
qreg q[2];
creg meas[2];
ry(0.081812781508772) q[0];
ry(0.857399539707819) q[1];
cx q[0],q[1];
ry(0.929432525182958) q[0];
ry(0.564879336226136) q[1];
cx q[0],q[1];
ry(0.622428187760993) q[0];
ry(0.832508068927503) q[1];
cx q[0],q[1];
ry(0.705520302551492) q[0];
ry(0.149004960050354) q[1];
barrier q[0],q[1];
measure q[0] -> meas[0];
measure q[1] -> meas[1];
