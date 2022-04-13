// Benchmark was created by MQT Bench on 2022-04-07
// For more information about MQT Bench, please visit https://www.cda.cit.tum.de/mqtbench/
// MQT Bench version: 0.1.0
// Qiskit version: {'qiskit-terra': '0.19.2', 'qiskit-aer': '0.10.3', 'qiskit-ignis': '0.7.0', 'qiskit-ibmq-provider': '0.18.3', 'qiskit-aqua': '0.9.5', 'qiskit': '0.34.2', 'qiskit-nature': '0.3.1', 'qiskit-finance': '0.3.1', 'qiskit-optimization': '0.3.1', 'qiskit-machine-learning': '0.3.1'}

OPENQASM 2.0;
include "qelib1.inc";
qreg q[3];
creg meas[3];
h q[0];
h q[1];
h q[2];
cx q[2],q[1];
rz(-1.1817921) q[1];
cx q[2],q[1];
cx q[2],q[0];
rz(-1.18175) q[0];
cx q[2],q[0];
cx q[1],q[0];
rz(-1.1817932) q[0];
cx q[1],q[0];
u3(1.1236062,-pi/2,2.7515471) q[0];
u3(1.1236062,-pi/2,2.7544135) q[1];
u3(1.1236062,-pi/2,2.7523155) q[2];
cx q[2],q[1];
rz(0.81054681) q[1];
cx q[2],q[1];
cx q[2],q[0];
rz(0.81051798) q[0];
cx q[2],q[0];
cx q[1],q[0];
rz(0.81054759) q[0];
cx q[1],q[0];
u3(2.4359307,-pi/2,0.76096373) q[0];
u3(2.4359307,-pi/2,0.75899775) q[1];
u3(2.4359307,-pi/2,0.76043671) q[2];
cx q[2],q[1];
rz(-5.0861644) q[1];
cx q[2],q[1];
cx q[2],q[0];
rz(-5.0859835) q[0];
cx q[2],q[0];
cx q[1],q[0];
rz(-5.0861693) q[0];
cx q[1],q[0];
u3(2.6434892,-pi/2,0.36929372) q[0];
u3(2.6434892,-pi/2,0.38163023) q[1];
u3(2.6434892,-pi/2,0.37260075) q[2];
barrier q[0],q[1],q[2];
measure q[0] -> meas[0];
measure q[1] -> meas[1];
measure q[2] -> meas[2];
