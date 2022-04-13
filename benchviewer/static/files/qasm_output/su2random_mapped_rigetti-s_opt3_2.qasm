// Benchmark was created by MQT Bench on 2022-04-10
// For more information about MQT Bench, please visit https://www.cda.cit.tum.de/mqtbench/
// MQT Bench version: 0.1.0
// Qiskit version: {'qiskit-terra': '0.19.2', 'qiskit-aer': '0.10.3', 'qiskit-ignis': '0.7.0', 'qiskit-ibmq-provider': '0.18.3', 'qiskit-aqua': '0.9.5', 'qiskit': '0.34.2', 'qiskit-nature': '0.3.1', 'qiskit-finance': '0.3.1', 'qiskit-optimization': '0.3.1', 'qiskit-machine-learning': '0.3.1'}
// Used Gate Set: ['rx', 'rz', 'cz', 'id', 'reset']
// Optimization Level: 3
// Coupling List: [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 7], [0, 7], [1, 0], [2, 1], [3, 2], [4, 3], [5, 4], [6, 5], [7, 6], [7, 0]]
// Compiled for architecture: rigetti-s-8 qubits

OPENQASM 2.0;
include "qelib1.inc";
qreg q[8];
creg meas[2];
rz(1.6712382) q[0];
rx(2.1837478) q[0];
rz(2.2452589) q[0];
rz(0.79886083) q[1];
rx(1.2195642) q[1];
rz(-1.1428344) q[1];
cz q[0],q[1];
rx(0.33396358) q[0];
rx(pi/2) q[1];
rz(0.029882232) q[1];
cz q[0],q[1];
rx(0.010411428) q[0];
rz(-0.25839011) q[0];
rx(pi/2) q[1];
cz q[0],q[1];
rx(2.1196348) q[0];
rz(0.30040422) q[0];
rz(1.754284) q[1];
rx(1.6697907) q[1];
rz(-2.4299136) q[1];
barrier q[0],q[1];
measure q[0] -> meas[0];
measure q[1] -> meas[1];
