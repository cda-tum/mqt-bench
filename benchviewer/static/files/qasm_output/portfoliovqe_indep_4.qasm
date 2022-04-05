// Benchmark was created by MQT Bench on 2022-03-22
// MQT Bench version: 0.1.0
// Qiskit version: {'qiskit-terra': '0.19.2', 'qiskit-aer': '0.10.3', 'qiskit-ignis': '0.7.0', 'qiskit-ibmq-provider': '0.18.3', 'qiskit-aqua': '0.9.5', 'qiskit': '0.34.2', 'qiskit-nature': '0.3.1', 'qiskit-finance': '0.3.1', 'qiskit-optimization': '0.3.1', 'qiskit-machine-learning': '0.3.1'}

OPENQASM 2.0;
include "qelib1.inc";
qreg q[4];
creg meas[4];
ry(1.28968986833421) q[0];
ry(-4.57729482160597) q[1];
cz q[0],q[1];
ry(3.27415134296698) q[2];
cz q[0],q[2];
cz q[1],q[2];
ry(-1.22392527694132) q[3];
cz q[0],q[3];
ry(-4.11126836349984) q[0];
cz q[1],q[3];
ry(3.35243841754169) q[1];
cz q[0],q[1];
cz q[2],q[3];
ry(0.0110084942683879) q[2];
cz q[0],q[2];
cz q[1],q[2];
ry(-2.16166923058369) q[3];
cz q[0],q[3];
ry(1.17370300187723) q[0];
cz q[1],q[3];
ry(3.56437942807824) q[1];
cz q[0],q[1];
cz q[2],q[3];
ry(-0.047263696457234) q[2];
cz q[0],q[2];
cz q[1],q[2];
ry(-2.76554049987184) q[3];
cz q[0],q[3];
ry(-4.7348646337175) q[0];
cz q[1],q[3];
ry(-4.13913090751362) q[1];
cz q[2],q[3];
ry(-5.53493417787299) q[2];
ry(-3.38677130663732) q[3];
barrier q[0],q[1],q[2],q[3];
measure q[0] -> meas[0];
measure q[1] -> meas[1];
measure q[2] -> meas[2];
measure q[3] -> meas[3];
