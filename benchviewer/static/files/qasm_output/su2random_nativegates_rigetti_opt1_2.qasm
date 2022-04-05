// Benchmark was created by MQT Bench on 2022-03-23
// MQT Bench version: 0.1.0
// Qiskit version: {'qiskit-terra': '0.19.2', 'qiskit-aer': '0.10.3', 'qiskit-ignis': '0.7.0', 'qiskit-ibmq-provider': '0.18.3', 'qiskit-aqua': '0.9.5', 'qiskit': '0.34.2', 'qiskit-nature': '0.3.1', 'qiskit-finance': '0.3.1', 'qiskit-optimization': '0.3.1', 'qiskit-machine-learning': '0.3.1'}
// Used Gate Set: ['rx', 'rz', 'cz']
// Optimization Level: 1

OPENQASM 2.0;
include "qelib1.inc";
qreg q[2];
creg meas[2];
rx(0.94957465) q[0];
rz(0.93932414) q[0];
rx(-1.171016) q[0];
rx(pi/2) q[1];
rz(2.2353816) q[1];
rx(2.1550771) q[1];
cz q[0],q[1];
rx(1.4533012) q[0];
rz(0.026052655) q[0];
rx(-1.4533407) q[0];
rx(-pi/2) q[1];
rz(0.5491938) q[1];
rx(2.0553521) q[1];
cz q[0],q[1];
rx(1.5617379) q[0];
rz(0.80957212) q[0];
rx(-1.5645476) q[0];
rx(-pi/2) q[1];
rz(0.067506903) q[1];
rx(2.3692682) q[1];
cz q[0],q[1];
rx(0.19592229) q[0];
rz(0.71316327) q[0];
rx(-0.25663474) q[0];
rx(1.6000947) q[1];
rz(1.1349249) q[1];
rx(1.5584236) q[1];
barrier q[0],q[1];
measure q[0] -> meas[0];
measure q[1] -> meas[1];
