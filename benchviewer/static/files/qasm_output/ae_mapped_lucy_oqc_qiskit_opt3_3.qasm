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
creg meas[3];
rz(-pi/4) q[3];
sx q[3];
rz(pi/2) q[3];
rz(-pi/2) q[4];
sx q[4];
rz(-2.3431156) q[4];
ecr q[4],q[3];
rz(-2.8017557) q[3];
sx q[3];
rz(-2.4980915) q[3];
sx q[3];
rz(0.33983691) q[3];
ecr q[4],q[3];
rz(-0.48761624) q[3];
sx q[3];
rz(-0.87629806) q[3];
sx q[3];
rz(0.48761624) q[3];
rz(2.3431156) q[4];
sx q[4];
rz(-pi/2) q[4];
sx q[5];
rz(3*pi/4) q[5];
sx q[5];
rz(-pi/2) q[5];
ecr q[4],q[5];
rz(pi/2) q[4];
sx q[4];
rz(-pi) q[4];
rz(-0.61547971) q[5];
sx q[5];
rz(-pi/3) q[5];
sx q[5];
rz(-2.5261129) q[5];
ecr q[4],q[5];
rz(-pi/2) q[4];
sx q[4];
rz(-pi/2) q[4];
rz(2.5261129) q[5];
sx q[5];
rz(-2*pi/3) q[5];
sx q[5];
rz(-0.61547971) q[5];
ecr q[4],q[5];
x q[4];
ecr q[4],q[3];
rz(-2.6539764) q[3];
sx q[3];
rz(-2.2652946) q[3];
sx q[3];
rz(0.48761624) q[3];
ecr q[4],q[3];
rz(1.1795787) q[3];
sx q[3];
rz(-0.82463843) q[3];
sx q[3];
rz(1.2977876) q[3];
rz(pi/2) q[4];
sx q[4];
rz(pi/2) q[4];
rz(0.52756445) q[5];
sx q[5];
rz(-0.93277638) q[5];
sx q[5];
rz(2.6140282) q[5];
ecr q[4],q[5];
rz(-2.8566685) q[5];
sx q[5];
rz(-2.5935642) q[5];
sx q[5];
rz(0.28492413) q[5];
ecr q[4],q[5];
rz(3*pi/4) q[4];
rz(-0.80943066) q[5];
sx q[5];
rz(-2.1973795) q[5];
sx q[5];
rz(2.6319784) q[5];
barrier q[6],q[2],q[4],q[5],q[1],q[7],q[0],q[3];
measure q[5] -> meas[0];
measure q[4] -> meas[1];
measure q[3] -> meas[2];
