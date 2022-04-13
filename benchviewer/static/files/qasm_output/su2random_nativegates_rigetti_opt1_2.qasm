// Benchmark was created by MQT Bench on 2022-04-10
// For more information about MQT Bench, please visit https://www.cda.cit.tum.de/mqtbench/
// MQT Bench version: 0.1.0
// Qiskit version: {'qiskit-terra': '0.19.2', 'qiskit-aer': '0.10.3', 'qiskit-ignis': '0.7.0', 'qiskit-ibmq-provider': '0.18.3', 'qiskit-aqua': '0.9.5', 'qiskit': '0.34.2', 'qiskit-nature': '0.3.1', 'qiskit-finance': '0.3.1', 'qiskit-optimization': '0.3.1', 'qiskit-machine-learning': '0.3.1'}
// Used Gate Set: ['rx', 'rz', 'cz', 'id', 'reset']
// Optimization Level: 1

OPENQASM 2.0;
include "qelib1.inc";
qreg q[2];
creg meas[2];
rx(0.5431315) q[0];
rz(1.2360381) q[0];
rx(-1.0724037) q[0];
rx(pi/2) q[1];
rz(2.1827667) q[1];
rx(2.1504203) q[1];
cz q[0],q[1];
rx(0.589813) q[0];
rz(1.1743902) q[0];
rx(-1.0475407) q[0];
rx(-pi/2) q[1];
rz(0.087392359) q[1];
rx(1.7561367) q[1];
cz q[0],q[1];
rx(0.39143484) q[0];
rz(0.21788928) q[0];
rx(-0.39994485) q[0];
rx(-pi/2) q[1];
rz(0.039072565) q[1];
rx(1.9969459) q[1];
cz q[0],q[1];
rx(0.18104796) q[0];
rz(0.97851495) q[0];
rx(-0.31685341) q[0];
rx(2.0806071) q[1];
rz(1.5013538) q[1];
rx(1.532021) q[1];
barrier q[0],q[1];
measure q[0] -> meas[0];
measure q[1] -> meas[1];
