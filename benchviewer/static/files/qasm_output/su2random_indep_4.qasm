// Benchmark was created by MQT Bench on 2022-04-10
// For more information about MQT Bench, please visit https://www.cda.cit.tum.de/mqtbench/
// MQT Bench version: 0.1.0
// Qiskit version: {'qiskit-terra': '0.19.2', 'qiskit-aer': '0.10.3', 'qiskit-ignis': '0.7.0', 'qiskit-ibmq-provider': '0.18.3', 'qiskit-aqua': '0.9.5', 'qiskit': '0.34.2', 'qiskit-nature': '0.3.1', 'qiskit-finance': '0.3.1', 'qiskit-optimization': '0.3.1', 'qiskit-machine-learning': '0.3.1'}

OPENQASM 2.0;
include "qelib1.inc";
qreg q[4];
creg meas[4];
u3(0.8108411,0.59474888,0) q[0];
u3(0.87270967,0.62286601,0) q[1];
cx q[0],q[1];
u3(0.30390982,0.44260149,0) q[2];
cx q[0],q[2];
cx q[1],q[2];
u3(0.38094391,0.56761476,0) q[3];
cx q[0],q[3];
u3(0.5365138,0.33405156,0) q[0];
cx q[1],q[3];
u3(0.51750701,0.11637351,0) q[1];
cx q[0],q[1];
cx q[2],q[3];
u3(0.28104884,0.28856165,0) q[2];
cx q[0],q[2];
cx q[1],q[2];
u3(0.1239955,0.0018561701,0) q[3];
cx q[0],q[3];
u3(0.69348942,0.025010833,0) q[0];
cx q[1],q[3];
u3(0.70339351,0.32815764,0) q[1];
cx q[0],q[1];
cx q[2],q[3];
u3(0.78526362,0.53102927,0) q[2];
cx q[0],q[2];
cx q[1],q[2];
u3(0.50784165,0.32580199,0) q[3];
cx q[0],q[3];
u3(0.28523351,0.38041535,0) q[0];
cx q[1],q[3];
u3(0.17062559,0.30206033,0) q[1];
cx q[2],q[3];
u3(0.87641837,0.56405611,0) q[2];
u3(0.22167232,0.17560156,0) q[3];
barrier q[0],q[1],q[2],q[3];
measure q[0] -> meas[0];
measure q[1] -> meas[1];
measure q[2] -> meas[2];
measure q[3] -> meas[3];
