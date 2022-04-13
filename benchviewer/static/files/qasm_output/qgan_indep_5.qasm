// Benchmark was created by MQT Bench on 2022-04-09
// For more information about MQT Bench, please visit https://www.cda.cit.tum.de/mqtbench/
// MQT Bench version: 0.1.0
// Qiskit version: {'qiskit-terra': '0.19.2', 'qiskit-aer': '0.10.3', 'qiskit-ignis': '0.7.0', 'qiskit-ibmq-provider': '0.18.3', 'qiskit-aqua': '0.9.5', 'qiskit': '0.34.2', 'qiskit-nature': '0.3.1', 'qiskit-finance': '0.3.1', 'qiskit-optimization': '0.3.1', 'qiskit-machine-learning': '0.3.1'}

OPENQASM 2.0;
include "qelib1.inc";
qreg q[5];
creg meas[5];
u3(1.1172509,0,-pi) q[0];
u3(0.95078818,0,-pi) q[1];
cz q[0],q[1];
u3(1.1284746,-pi,0) q[2];
cz q[0],q[2];
cz q[1],q[2];
u3(1.1072747,-pi,0) q[3];
cz q[0],q[3];
cz q[1],q[3];
cz q[2],q[3];
u3(1.7318545,-pi,0) q[4];
cz q[0],q[4];
ry(1.17233349640483) q[0];
cz q[1],q[4];
ry(0.549079094514068) q[1];
cz q[2],q[4];
ry(0.964596175346147) q[2];
cz q[3],q[4];
ry(0.475241504218651) q[3];
ry(3.52400227532335) q[4];
barrier q[0],q[1],q[2],q[3],q[4];
measure q[0] -> meas[0];
measure q[1] -> meas[1];
measure q[2] -> meas[2];
measure q[3] -> meas[3];
measure q[4] -> meas[4];
