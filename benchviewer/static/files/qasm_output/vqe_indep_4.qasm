// Benchmark was created by MQT Bench on 2022-03-26
// MQT Bench version: 0.1.0
// Qiskit version: {'qiskit-terra': '0.19.2', 'qiskit-aer': '0.10.3', 'qiskit-ignis': '0.7.0', 'qiskit-ibmq-provider': '0.18.3', 'qiskit-aqua': '0.9.5', 'qiskit': '0.34.2', 'qiskit-nature': '0.3.1', 'qiskit-finance': '0.3.1', 'qiskit-optimization': '0.3.1', 'qiskit-machine-learning': '0.3.1'}

OPENQASM 2.0;
include "qelib1.inc";
qreg q[4];
creg meas[4];
ry(-2.53713753590652) q[0];
ry(1.31671062734335) q[1];
cx q[0],q[1];
ry(1.83230626959971) q[2];
cx q[0],q[2];
cx q[1],q[2];
ry(-2.86317528573076) q[3];
cx q[0],q[3];
ry(0.791195967990987) q[0];
cx q[1],q[3];
ry(-1.57166153222488) q[1];
cx q[0],q[1];
cx q[2],q[3];
ry(-0.457062513843978) q[2];
cx q[0],q[2];
cx q[1],q[2];
ry(1.82535013753249) q[3];
cx q[0],q[3];
ry(0.198559269245156) q[0];
cx q[1],q[3];
ry(-3.05967605180697) q[1];
cx q[2],q[3];
ry(-3.01671400823206) q[2];
ry(-0.688523820575221) q[3];
barrier q[0],q[1],q[2],q[3];
measure q[0] -> meas[0];
measure q[1] -> meas[1];
measure q[2] -> meas[2];
measure q[3] -> meas[3];
