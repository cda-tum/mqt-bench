// Benchmark was created by MQT Bench on 2022-04-12
// For more information about MQT Bench, please visit https://www.cda.cit.tum.de/mqtbench/
// MQT Bench version: 0.1.0
// Qiskit version: {'qiskit-terra': '0.19.2', 'qiskit-aer': '0.10.3', 'qiskit-ignis': '0.7.0', 'qiskit-ibmq-provider': '0.18.3', 'qiskit-aqua': '0.9.5', 'qiskit': '0.34.2', 'qiskit-nature': '0.3.1', 'qiskit-finance': '0.3.1', 'qiskit-optimization': '0.3.1', 'qiskit-machine-learning': '0.3.1'}

OPENQASM 2.0;
include "qelib1.inc";
qreg q[5];
creg meas[5];
ry(2.56112899454298) q[0];
ry(-0.331902241357565) q[1];
cx q[0],q[1];
ry(2.03970358586616) q[2];
cx q[0],q[2];
cx q[1],q[2];
ry(2.52126405430814) q[3];
cx q[0],q[3];
cx q[1],q[3];
cx q[2],q[3];
ry(-0.81012536992829) q[4];
cx q[0],q[4];
ry(-1.8410922575144) q[0];
cx q[1],q[4];
ry(3.04869757819212) q[1];
cx q[0],q[1];
cx q[2],q[4];
ry(0.889417844490214) q[2];
cx q[0],q[2];
cx q[1],q[2];
cx q[3],q[4];
ry(2.26341668164218) q[3];
cx q[0],q[3];
cx q[1],q[3];
cx q[2],q[3];
ry(-0.958203461873944) q[4];
cx q[0],q[4];
ry(-2.60760189593223) q[0];
cx q[1],q[4];
ry(2.9116268926219) q[1];
cx q[2],q[4];
ry(1.63875496667116) q[2];
cx q[3],q[4];
ry(1.66479450385975) q[3];
ry(-1.79481197425916) q[4];
barrier q[0],q[1],q[2],q[3],q[4];
measure q[0] -> meas[0];
measure q[1] -> meas[1];
measure q[2] -> meas[2];
measure q[3] -> meas[3];
measure q[4] -> meas[4];
