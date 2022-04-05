// Benchmark was created by MQT Bench on 2022-03-24
// MQT Bench version: 0.1.0
// Qiskit version: {'qiskit-terra': '0.19.2', 'qiskit-aer': '0.10.3', 'qiskit-ignis': '0.7.0', 'qiskit-ibmq-provider': '0.18.3', 'qiskit-aqua': '0.9.5', 'qiskit': '0.34.2', 'qiskit-nature': '0.3.1', 'qiskit-finance': '0.3.1', 'qiskit-optimization': '0.3.1', 'qiskit-machine-learning': '0.3.1'}

OPENQASM 2.0;
include "qelib1.inc";
qreg q[4];
creg meas[4];
ry(0.177378857981226) q[0];
ry(0.845231461007316) q[1];
cx q[0],q[1];
ry(0.736804071896799) q[2];
cx q[0],q[2];
cx q[1],q[2];
ry(0.0598039564261399) q[3];
cx q[0],q[3];
ry(0.344501738376945) q[0];
cx q[1],q[3];
ry(0.0460965245533083) q[1];
cx q[0],q[1];
cx q[2],q[3];
ry(0.565628676741345) q[2];
cx q[0],q[2];
cx q[1],q[2];
ry(0.271636168045275) q[3];
cx q[0],q[3];
ry(0.286216654939273) q[0];
cx q[1],q[3];
ry(0.0623509736982144) q[1];
cx q[0],q[1];
cx q[2],q[3];
ry(0.83108844312836) q[2];
cx q[0],q[2];
cx q[1],q[2];
ry(0.541205168646597) q[3];
cx q[0],q[3];
ry(0.904058545871172) q[0];
cx q[1],q[3];
ry(0.854941407194415) q[1];
cx q[2],q[3];
ry(0.731222079902973) q[2];
ry(0.650337360538112) q[3];
barrier q[0],q[1],q[2],q[3];
measure q[0] -> meas[0];
measure q[1] -> meas[1];
measure q[2] -> meas[2];
measure q[3] -> meas[3];
