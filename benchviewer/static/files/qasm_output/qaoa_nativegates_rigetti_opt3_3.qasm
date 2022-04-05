// Benchmark was created by MQT Bench on 2022-03-21
// MQT Bench version: 0.1.0
// Qiskit version: {'qiskit-terra': '0.19.2', 'qiskit-aer': '0.10.3', 'qiskit-ignis': '0.7.0', 'qiskit-ibmq-provider': '0.18.3', 'qiskit-aqua': '0.9.5', 'qiskit': '0.34.2', 'qiskit-nature': '0.3.1', 'qiskit-finance': '0.3.1', 'qiskit-optimization': '0.3.1', 'qiskit-machine-learning': '0.3.1'}
// Used Gate Set: ['rx', 'rz', 'cz']
// Optimization Level: 3

OPENQASM 2.0;
include "qelib1.inc";
qreg q[3];
creg meas[3];
rz(-pi/2) q[0];
rx(pi/2) q[0];
rz(1.3485307) q[0];
rz(pi/2) q[1];
rx(pi/2) q[1];
rz(4.2787904) q[1];
rx(1.3586585) q[2];
cz q[1],q[2];
rx(pi) q[1];
rx(0.53148815) q[2];
cz q[1],q[2];
rz(1.1371977) q[1];
rx(pi/2) q[1];
rz(-pi/2) q[1];
rx(1.4973801) q[2];
cz q[0],q[2];
rx(pi) q[0];
rx(0.53148815) q[2];
rz(pi/2) q[2];
cz q[0],q[2];
rz(2.919327) q[0];
cz q[0],q[1];
rx(-2.6101045) q[1];
cz q[0],q[1];
rx(12.2143003706164) q[0];
rz(-1.9228666) q[1];
rx(-pi/2) q[1];
rx(0.050756115) q[2];
rz(1.222253) q[2];
rx(2.0352894) q[2];
cz q[1],q[2];
rz(pi/2) q[1];
rx(pi) q[1];
rx(0.54888779) q[2];
cz q[1],q[2];
rz(pi/2) q[1];
rx(pi/2) q[1];
rz(-pi/2) q[1];
rx(-0.95864383) q[2];
cz q[0],q[2];
rx(2.5927049) q[2];
cz q[0],q[2];
cz q[0],q[1];
rx(2.5927049) q[1];
cz q[0],q[1];
rx(-1.52276682977829) q[0];
rx(pi/2) q[1];
rz(pi/2) q[1];
rx(0.048029497) q[1];
rx(pi/2) q[2];
rz(pi/2) q[2];
rx(0.048029497) q[2];
barrier q[0],q[1],q[2];
measure q[0] -> meas[0];
measure q[1] -> meas[1];
measure q[2] -> meas[2];
