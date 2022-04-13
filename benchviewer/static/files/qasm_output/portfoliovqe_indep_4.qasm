// Benchmark was created by MQT Bench on 2022-04-07
// For more information about MQT Bench, please visit https://www.cda.cit.tum.de/mqtbench/
// MQT Bench version: 0.1.0
// Qiskit version: {'qiskit-terra': '0.19.2', 'qiskit-aer': '0.10.3', 'qiskit-ignis': '0.7.0', 'qiskit-ibmq-provider': '0.18.3', 'qiskit-aqua': '0.9.5', 'qiskit': '0.34.2', 'qiskit-nature': '0.3.1', 'qiskit-finance': '0.3.1', 'qiskit-optimization': '0.3.1', 'qiskit-machine-learning': '0.3.1'}

OPENQASM 2.0;
include "qelib1.inc";
qreg q[4];
creg meas[4];
ry(6.90824216214051) q[0];
ry(2.45308700641705) q[1];
cz q[0],q[1];
ry(-6.59795322118399) q[2];
cz q[0],q[2];
cz q[1],q[2];
ry(-0.700583328105825) q[3];
cz q[0],q[3];
ry(2.7946426566341) q[0];
cz q[1],q[3];
ry(-4.30176672533224) q[1];
cz q[0],q[1];
cz q[2],q[3];
ry(1.46233762861663) q[2];
cz q[0],q[2];
cz q[1],q[2];
ry(-1.43698103341348) q[3];
cz q[0],q[3];
ry(-6.07589513545875) q[0];
cz q[1],q[3];
ry(-6.00692692027551) q[1];
cz q[0],q[1];
cz q[2],q[3];
ry(2.01025960736006) q[2];
cz q[0],q[2];
cz q[1],q[2];
ry(5.89791867243858) q[3];
cz q[0],q[3];
ry(-0.458943374963605) q[0];
cz q[1],q[3];
ry(-3.69150873381062) q[1];
cz q[2],q[3];
ry(0.337184015374744) q[2];
ry(-0.949280581229415) q[3];
barrier q[0],q[1],q[2],q[3];
measure q[0] -> meas[0];
measure q[1] -> meas[1];
measure q[2] -> meas[2];
measure q[3] -> meas[3];
