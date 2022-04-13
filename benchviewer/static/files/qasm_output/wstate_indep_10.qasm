// Benchmark was created by MQT Bench on 2022-04-13
// For more information about MQT Bench, please visit https://www.cda.cit.tum.de/mqtbench/
// MQT Bench version: 0.1.0
// Qiskit version: {'qiskit-terra': '0.19.2', 'qiskit-aer': '0.10.3', 'qiskit-ignis': '0.7.0', 'qiskit-ibmq-provider': '0.18.3', 'qiskit-aqua': '0.9.5', 'qiskit': '0.34.2', 'qiskit-nature': '0.3.1', 'qiskit-finance': '0.3.1', 'qiskit-optimization': '0.3.1', 'qiskit-machine-learning': '0.3.1'}

OPENQASM 2.0;
include "qelib1.inc";
qreg q[10];
creg meas[10];
ry(-pi/4) q[0];
ry(-0.95531662) q[1];
ry(-pi/3) q[2];
ry(-1.1071487) q[3];
ry(-1.150262) q[4];
ry(-1.1831996) q[5];
ry(-1.2094292) q[6];
ry(-1.2309594) q[7];
ry(-1.2490458) q[8];
x q[9];
cz q[9],q[8];
ry(1.2490458) q[8];
cz q[8],q[7];
ry(1.2309594) q[7];
cz q[7],q[6];
ry(1.2094292) q[6];
cz q[6],q[5];
ry(1.1831996) q[5];
cz q[5],q[4];
ry(1.150262) q[4];
cz q[4],q[3];
ry(1.1071487) q[3];
cz q[3],q[2];
ry(pi/3) q[2];
cz q[2],q[1];
ry(0.95531662) q[1];
cz q[1],q[0];
ry(pi/4) q[0];
cx q[8],q[9];
cx q[7],q[8];
cx q[6],q[7];
cx q[5],q[6];
cx q[4],q[5];
cx q[3],q[4];
cx q[2],q[3];
cx q[1],q[2];
cx q[0],q[1];
barrier q[0],q[1],q[2],q[3],q[4],q[5],q[6],q[7],q[8],q[9];
measure q[0] -> meas[0];
measure q[1] -> meas[1];
measure q[2] -> meas[2];
measure q[3] -> meas[3];
measure q[4] -> meas[4];
measure q[5] -> meas[5];
measure q[6] -> meas[6];
measure q[7] -> meas[7];
measure q[8] -> meas[8];
measure q[9] -> meas[9];
