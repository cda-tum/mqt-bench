// Benchmark was created by qTUMbench on 2022-02-18
// qTUMbench version: 0.1.0
// Qiskit version: {'qiskit-terra': '0.19.1', 'qiskit-aer': '0.10.2', 'qiskit-ignis': '0.7.0', 'qiskit-ibmq-provider': '0.18.3', 'qiskit-aqua': '0.9.5', 'qiskit': '0.34.1', 'qiskit-nature': '0.3.0', 'qiskit-finance': '0.3.0', 'qiskit-optimization': '0.3.0', 'qiskit-machine-learning': '0.3.0'}

OPENQASM 2.0;
include "qelib1.inc";
qreg q[5];
creg meas[5];
h q[4];
cx q[4],q[3];
cx q[3],q[2];
cx q[2],q[1];
cx q[1],q[0];
barrier q[0],q[1],q[2],q[3],q[4];
measure q[0] -> meas[0];
measure q[1] -> meas[1];
measure q[2] -> meas[2];
measure q[3] -> meas[3];
measure q[4] -> meas[4];
