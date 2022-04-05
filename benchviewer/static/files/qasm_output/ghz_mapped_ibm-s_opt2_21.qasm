// Benchmark was created by MQT Bench on 2022-03-22
// MQT Bench version: 0.1.0
// Qiskit version: {'qiskit-terra': '0.19.2', 'qiskit-aer': '0.10.3', 'qiskit-ignis': '0.7.0', 'qiskit-ibmq-provider': '0.18.3', 'qiskit-aqua': '0.9.5', 'qiskit': '0.34.2', 'qiskit-nature': '0.3.1', 'qiskit-finance': '0.3.1', 'qiskit-optimization': '0.3.1', 'qiskit-machine-learning': '0.3.1'}
// Used Gate Set: ['id', 'rz', 'sx', 'x', 'cx', 'reset']
// Optimization Level: 2
// Coupling List: [[0, 1], [1, 0], [1, 2], [1, 4], [2, 1], [2, 3], [3, 2], [3, 5], [4, 1], [4, 7], [5, 3], [5, 8], [6, 7], [7, 4], [7, 6], [7, 10], [8, 5], [8, 9], [8, 11], [9, 8], [10, 7], [10, 12], [11, 8], [11, 14], [12, 10], [12, 13], [12, 15], [13, 12], [13, 14], [14, 11], [14, 13], [14, 16], [15, 12], [15, 18], [16, 14], [16, 19], [17, 18], [18, 15], [18, 17], [18, 21], [19, 16], [19, 20], [19, 22], [20, 19], [21, 18], [21, 23], [22, 19], [22, 25], [23, 21], [23, 24], [24, 23], [24, 25], [25, 22], [25, 24], [25, 26], [26, 25]]
// Compiled for architecture: ibm-s-fake_montreal

OPENQASM 2.0;
include "qelib1.inc";
qreg q[27];
creg meas[21];
rz(pi/2) q[24];
sx q[24];
rz(pi/2) q[24];
cx q[24],q[23];
cx q[23],q[21];
cx q[21],q[18];
cx q[18],q[15];
cx q[15],q[12];
cx q[12],q[10];
cx q[10],q[7];
cx q[7],q[4];
cx q[4],q[1];
cx q[1],q[2];
cx q[2],q[3];
cx q[3],q[5];
cx q[5],q[8];
cx q[8],q[11];
cx q[11],q[14];
cx q[14],q[16];
cx q[16],q[19];
cx q[19],q[22];
cx q[22],q[25];
cx q[25],q[26];
barrier q[26],q[25],q[22],q[19],q[16],q[14],q[11],q[8],q[5],q[3],q[2],q[1],q[4],q[7],q[10],q[12],q[15],q[18],q[21],q[23],q[24];
measure q[26] -> meas[0];
measure q[25] -> meas[1];
measure q[22] -> meas[2];
measure q[19] -> meas[3];
measure q[16] -> meas[4];
measure q[14] -> meas[5];
measure q[11] -> meas[6];
measure q[8] -> meas[7];
measure q[5] -> meas[8];
measure q[3] -> meas[9];
measure q[2] -> meas[10];
measure q[1] -> meas[11];
measure q[4] -> meas[12];
measure q[7] -> meas[13];
measure q[10] -> meas[14];
measure q[12] -> meas[15];
measure q[15] -> meas[16];
measure q[18] -> meas[17];
measure q[21] -> meas[18];
measure q[23] -> meas[19];
measure q[24] -> meas[20];
