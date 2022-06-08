// Benchmark was created by MQT Bench on 2022-06-08
// For more information about MQT Bench, please visit https://www.cda.cit.tum.de/mqtbench/
// MQT Bench version: 0.1.0
// Qiskit version: {'qiskit-terra': '0.20.2', 'qiskit-aer': '0.10.4', 'qiskit-ignis': '0.7.1', 'qiskit-ibmq-provider': '0.19.1', 'qiskit-aqua': '0.9.5', 'qiskit': '0.36.2', 'qiskit-nature': '0.3.2', 'qiskit-finance': '0.3.1', 'qiskit-optimization': '0.3.2', 'qiskit-machine-learning': '0.3.1'}
// Used Gate Set: ['rz', 'sx', 'x', 'cx', 'measure']
// Coupling List: [[0, 1], [1, 0], [1, 2], [1, 4], [2, 1], [2, 3], [3, 2], [3, 5], [4, 1], [4, 7], [5, 3], [5, 8], [6, 7], [7, 4], [7, 6], [7, 10], [8, 5], [8, 9], [8, 11], [9, 8], [10, 7], [10, 12], [11, 8], [11, 14], [12, 10], [12, 13], [12, 15], [13, 12], [13, 14], [14, 11], [14, 13], [14, 16], [15, 12], [15, 18], [16, 14], [16, 19], [17, 18], [18, 15], [18, 17], [18, 21], [19, 16], [19, 20], [19, 22], [20, 19], [21, 18], [21, 23], [22, 19], [22, 25], [23, 21], [23, 24], [24, 23], [24, 25], [25, 22], [25, 24], [25, 26], [26, 25]]

OPENQASM 2.0;
include "qelib1.inc";
qreg q[27];
creg meas[3];
sx q[12];
rz(2.0344439) q[12];
rz(pi/2) q[13];
sx q[13];
rz(pi) q[13];
rz(-pi/2) q[15];
sx q[15];
rz(2.2278713) q[15];
cx q[12],q[15];
x q[12];
rz(0.92729522) q[15];
cx q[12],q[15];
rz(0.1798535) q[12];
sx q[12];
cx q[13],q[12];
sx q[12];
rz(1.2870022) q[12];
sx q[12];
rz(-pi) q[12];
cx q[13],q[12];
rz(-pi) q[12];
sx q[12];
rz(1.2870022) q[12];
sx q[12];
sx q[13];
rz(pi/2) q[13];
rz(0.65707494) q[15];
cx q[12],q[15];
cx q[15],q[12];
cx q[12],q[15];
rz(pi/4) q[12];
cx q[12],q[13];
rz(pi/4) q[13];
cx q[12],q[13];
sx q[12];
rz(pi/2) q[12];
rz(-pi/4) q[13];
barrier q[26],q[0],q[3],q[9],q[6],q[15],q[18],q[12],q[21],q[24],q[4],q[1],q[7],q[10],q[16],q[13],q[19],q[22],q[25],q[2],q[5],q[11],q[8],q[14],q[17],q[23],q[20];
measure q[12] -> meas[0];
measure q[13] -> meas[1];
measure q[15] -> meas[2];
