// Benchmark was created by MQT Bench on 2022-04-11
// For more information about MQT Bench, please visit https://www.cda.cit.tum.de/mqtbench/
// MQT Bench version: 0.1.0
// Qiskit version: {'qiskit-terra': '0.19.2', 'qiskit-aer': '0.10.3', 'qiskit-ignis': '0.7.0', 'qiskit-ibmq-provider': '0.18.3', 'qiskit-aqua': '0.9.5', 'qiskit': '0.34.2', 'qiskit-nature': '0.3.1', 'qiskit-finance': '0.3.1', 'qiskit-optimization': '0.3.1', 'qiskit-machine-learning': '0.3.1'}

OPENQASM 2.0;
include "qelib1.inc";
qreg q[3];
creg meas[3];
ry(0.777687484916321) q[0];
ry(0.0537619595231665) q[1];
cx q[0],q[1];
ry(0.643560964427569) q[2];
cx q[0],q[2];
ry(0.0622820198579198) q[0];
cx q[1],q[2];
ry(0.756797625480252) q[1];
cx q[0],q[1];
ry(0.604060169605849) q[2];
cx q[0],q[2];
ry(0.458505393554708) q[0];
cx q[1],q[2];
ry(0.811528775946193) q[1];
cx q[0],q[1];
ry(0.808404694082565) q[2];
cx q[0],q[2];
ry(0.861991639931646) q[0];
cx q[1],q[2];
ry(0.373310261355424) q[1];
ry(0.377981493588618) q[2];
barrier q[0],q[1],q[2];
measure q[0] -> meas[0];
measure q[1] -> meas[1];
measure q[2] -> meas[2];
