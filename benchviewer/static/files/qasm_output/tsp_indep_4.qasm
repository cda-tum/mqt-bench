// Benchmark was created by MQT Bench on 2022-04-11
// For more information about MQT Bench, please visit https://www.cda.cit.tum.de/mqtbench/
// MQT Bench version: 0.1.0
// Qiskit version: {'qiskit-terra': '0.19.2', 'qiskit-aer': '0.10.3', 'qiskit-ignis': '0.7.0', 'qiskit-ibmq-provider': '0.18.3', 'qiskit-aqua': '0.9.5', 'qiskit': '0.34.2', 'qiskit-nature': '0.3.1', 'qiskit-finance': '0.3.1', 'qiskit-optimization': '0.3.1', 'qiskit-machine-learning': '0.3.1'}

OPENQASM 2.0;
include "qelib1.inc";
qreg q[4];
creg meas[4];
ry(6.28845911639893) q[0];
ry(-3.48501709623492) q[1];
cz q[0],q[1];
ry(1.59359898664864) q[0];
ry(4.25412409637649) q[2];
cz q[1],q[2];
ry(-3.9483960163317) q[1];
cz q[0],q[1];
ry(-2.52193564540607) q[0];
ry(-4.35611141477599) q[3];
cz q[2],q[3];
ry(2.82317938414071) q[2];
cz q[1],q[2];
ry(6.1807920749568) q[1];
cz q[0],q[1];
ry(0.346789107616128) q[0];
ry(4.06489732750758) q[3];
cz q[2],q[3];
ry(3.63960549833966) q[2];
cz q[1],q[2];
ry(2.21265384481984) q[1];
cz q[0],q[1];
ry(-4.05533498631776) q[0];
ry(-2.76229804626122) q[3];
cz q[2],q[3];
ry(4.28881874467116) q[2];
cz q[1],q[2];
ry(4.46684868172685) q[1];
cz q[0],q[1];
ry(-3.40673597685765) q[0];
ry(5.86090019231619) q[3];
cz q[2],q[3];
ry(-3.72990730589565) q[2];
cz q[1],q[2];
ry(4.67982090787643) q[1];
ry(5.80823864218722) q[3];
cz q[2],q[3];
ry(-3.76357505894766) q[2];
ry(5.92181259437003) q[3];
barrier q[0],q[1],q[2],q[3];
measure q[0] -> meas[0];
measure q[1] -> meas[1];
measure q[2] -> meas[2];
measure q[3] -> meas[3];
