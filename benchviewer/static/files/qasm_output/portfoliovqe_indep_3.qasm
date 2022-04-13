// Benchmark was created by MQT Bench on 2022-04-07
// For more information about MQT Bench, please visit https://www.cda.cit.tum.de/mqtbench/
// MQT Bench version: 0.1.0
// Qiskit version: {'qiskit-terra': '0.19.2', 'qiskit-aer': '0.10.3', 'qiskit-ignis': '0.7.0', 'qiskit-ibmq-provider': '0.18.3', 'qiskit-aqua': '0.9.5', 'qiskit': '0.34.2', 'qiskit-nature': '0.3.1', 'qiskit-finance': '0.3.1', 'qiskit-optimization': '0.3.1', 'qiskit-machine-learning': '0.3.1'}

OPENQASM 2.0;
include "qelib1.inc";
qreg q[3];
creg meas[3];
ry(0.49228365021784) q[0];
ry(0.78836117672633) q[1];
cz q[0],q[1];
ry(2.70517476425641) q[2];
cz q[0],q[2];
ry(-1.62747779367121) q[0];
cz q[1],q[2];
ry(1.98393564160861) q[1];
cz q[0],q[1];
ry(5.36987518230213) q[2];
cz q[0],q[2];
ry(-4.81914623387862) q[0];
cz q[1],q[2];
ry(-3.67567765160191) q[1];
cz q[0],q[1];
ry(-4.26141550944205) q[2];
cz q[0],q[2];
ry(4.38214758575175) q[0];
cz q[1],q[2];
ry(-4.45833242440858) q[1];
ry(4.8252960762241) q[2];
barrier q[0],q[1],q[2];
measure q[0] -> meas[0];
measure q[1] -> meas[1];
measure q[2] -> meas[2];
