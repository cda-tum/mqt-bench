// Benchmark was created by MQT Bench on 2022-03-23
// MQT Bench version: 0.1.0
// Qiskit version: {'qiskit-terra': '0.19.2', 'qiskit-aer': '0.10.3', 'qiskit-ignis': '0.7.0', 'qiskit-ibmq-provider': '0.18.3', 'qiskit-aqua': '0.9.5', 'qiskit': '0.34.2', 'qiskit-nature': '0.3.1', 'qiskit-finance': '0.3.1', 'qiskit-optimization': '0.3.1', 'qiskit-machine-learning': '0.3.1'}
// Used Gate Set: ['rx', 'rz', 'cz']
// Optimization Level: 3

OPENQASM 2.0;
include "qelib1.inc";
qreg q[2];
creg meas[2];
rz(1.9042753) q[0];
rx(1.6137797) q[0];
rz(1.2371559) q[0];
rz(-0.5476571) q[1];
rx(0.079894583) q[1];
rz(-2.7753204) q[1];
cz q[0],q[1];
rx(0.42762547) q[0];
rx(pi/2) q[1];
rz(0.27254014) q[1];
cz q[0],q[1];
rx(-0.014498226) q[0];
rz(-0.64014227) q[0];
rx(pi/2) q[1];
cz q[0],q[1];
rx(2.8159847) q[0];
rz(0.11127413) q[0];
rz(-0.549131) q[1];
rx(0.86174237) q[1];
rz(2.7573141) q[1];
barrier q[0],q[1];
measure q[0] -> meas[0];
measure q[1] -> meas[1];
