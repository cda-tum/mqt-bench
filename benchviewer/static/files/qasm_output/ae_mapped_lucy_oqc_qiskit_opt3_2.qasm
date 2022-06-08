// Benchmark was created by MQT Bench on 2022-06-08
// For more information about MQT Bench, please visit https://www.cda.cit.tum.de/mqtbench/
// MQT Bench version: 0.1.0
// Qiskit version: {'qiskit-terra': '0.20.2', 'qiskit-aer': '0.10.4', 'qiskit-ignis': '0.7.1', 'qiskit-ibmq-provider': '0.19.1', 'qiskit-aqua': '0.9.5', 'qiskit': '0.36.2', 'qiskit-nature': '0.3.2', 'qiskit-finance': '0.3.1', 'qiskit-optimization': '0.3.2', 'qiskit-machine-learning': '0.3.1'}
// Used Gate Set: ['rz', 'sx', 'x', 'ecr', 'measure']
// Coupling List: [[0, 1], [0, 7], [1, 2], [2, 3], [7, 6], [6, 5], [4, 3], [4, 5]]

OPENQASM 2.0;
include "qelib1.inc";
gate rzx(param0) q0,q1 { h q1; cx q0,q1; rz(-pi/4) q1; cx q0,q1; h q1; }
gate rzx(param0) q0,q1 { h q1; cx q0,q1; rz(pi/4) q1; cx q0,q1; h q1; }
gate ecr q0,q1 { rzx(pi/4) q0,q1; x q0; rzx(-pi/4) q0,q1; }
qreg q[8];
creg meas[2];
sx q[0];
rz(-pi/2) q[0];
sx q[7];
rz(-pi/4) q[7];
sx q[7];
rz(-pi/2) q[7];
ecr q[0],q[7];
rz(-2.8017557) q[7];
sx q[7];
rz(-2.4980915) q[7];
sx q[7];
rz(0.33983691) q[7];
ecr q[0],q[7];
rz(0.28379411) q[0];
sx q[0];
rz(-pi) q[0];
rz(pi/2) q[7];
sx q[7];
rz(-pi/4) q[7];
sx q[7];
barrier q[7],q[0];
measure q[7] -> meas[0];
measure q[0] -> meas[1];
