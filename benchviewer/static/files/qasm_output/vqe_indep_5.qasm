// Benchmark was created by MQT Bench on 2022-03-26
// MQT Bench version: 0.1.0
// Qiskit version: {'qiskit-terra': '0.19.2', 'qiskit-aer': '0.10.3', 'qiskit-ignis': '0.7.0', 'qiskit-ibmq-provider': '0.18.3', 'qiskit-aqua': '0.9.5', 'qiskit': '0.34.2', 'qiskit-nature': '0.3.1', 'qiskit-finance': '0.3.1', 'qiskit-optimization': '0.3.1', 'qiskit-machine-learning': '0.3.1'}

OPENQASM 2.0;
include "qelib1.inc";
qreg q[5];
creg meas[5];
ry(2.4837558976442) q[0];
ry(-1.6866976707277) q[1];
cx q[0],q[1];
ry(-0.34964588201705) q[2];
cx q[0],q[2];
cx q[1],q[2];
ry(-2.23635526146304) q[3];
cx q[0],q[3];
cx q[1],q[3];
cx q[2],q[3];
ry(1.94581415362704) q[4];
cx q[0],q[4];
ry(-0.740398769355741) q[0];
cx q[1],q[4];
ry(-0.898963137951661) q[1];
cx q[0],q[1];
cx q[2],q[4];
ry(-1.52773263648427) q[2];
cx q[0],q[2];
cx q[1],q[2];
cx q[3],q[4];
ry(2.1103577997306) q[3];
cx q[0],q[3];
cx q[1],q[3];
cx q[2],q[3];
ry(-0.398674155836213) q[4];
cx q[0],q[4];
ry(-2.8290350836792) q[0];
cx q[1],q[4];
ry(1.90851934984554) q[1];
cx q[2],q[4];
ry(-1.5487816496272) q[2];
cx q[3],q[4];
ry(-1.99788014792039) q[3];
ry(-1.67327325157465) q[4];
barrier q[0],q[1],q[2],q[3],q[4];
measure q[0] -> meas[0];
measure q[1] -> meas[1];
measure q[2] -> meas[2];
measure q[3] -> meas[3];
measure q[4] -> meas[4];
