// Benchmark was created by MQT Bench on 2022-04-07
// For more information about MQT Bench, please visit https://www.cda.cit.tum.de/mqtbench/
// MQT Bench version: 0.1.0
// Qiskit version: {'qiskit-terra': '0.19.2', 'qiskit-aer': '0.10.3', 'qiskit-ignis': '0.7.0', 'qiskit-ibmq-provider': '0.18.3', 'qiskit-aqua': '0.9.5', 'qiskit': '0.34.2', 'qiskit-nature': '0.3.1', 'qiskit-finance': '0.3.1', 'qiskit-optimization': '0.3.1', 'qiskit-machine-learning': '0.3.1'}

OPENQASM 2.0;
include "qelib1.inc";
qreg q[5];
creg meas[5];
h q[0];
h q[1];
h q[2];
h q[3];
h q[4];
rzz(2.51556151567525) q[3],q[4];
rzz(2.51556151567525) q[1],q[3];
rzz(2.51556151567525) q[2],q[4];
rzz(2.51556151567525) q[0],q[2];
rzz(2.51556151567525) q[0],q[1];
rx(5.04557174961663) q[0];
rx(5.04557174961663) q[1];
rx(5.04557174961663) q[2];
rx(5.04557174961663) q[3];
rx(5.04557174961663) q[4];
rzz(2.2464589899768) q[3],q[4];
rzz(2.2464589899768) q[1],q[3];
rzz(2.2464589899768) q[2],q[4];
rzz(2.2464589899768) q[0],q[2];
rzz(2.2464589899768) q[0],q[1];
rx(-10.3461780053708) q[0];
rx(-10.3461780053708) q[1];
rx(-10.3461780053708) q[2];
rx(-10.3461780053708) q[3];
rx(-10.3461780053708) q[4];
barrier q[0],q[1],q[2],q[3],q[4];
measure q[0] -> meas[0];
measure q[1] -> meas[1];
measure q[2] -> meas[2];
measure q[3] -> meas[3];
measure q[4] -> meas[4];
