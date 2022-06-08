// Benchmark was created by MQT Bench on 2022-06-08
// For more information about MQT Bench, please visit https://www.cda.cit.tum.de/mqtbench/
// MQT Bench version: 0.1.0
// Qiskit version: {'qiskit-terra': '0.20.2', 'qiskit-aer': '0.10.4', 'qiskit-ignis': '0.7.1', 'qiskit-ibmq-provider': '0.19.1', 'qiskit-aqua': '0.9.5', 'qiskit': '0.36.2', 'qiskit-nature': '0.3.2', 'qiskit-finance': '0.3.1', 'qiskit-optimization': '0.3.2', 'qiskit-machine-learning': '0.3.1'}
// Used Gate Set: <tket::BasePass>

OPENQASM 2.0;
include "qelib1.inc";

qreg node[26];
creg meas[2];
rz(0.5*pi) node[24];
sx node[25];
sx node[24];
rz(0.5*pi) node[25];
rz(3.5*pi) node[24];
sx node[25];
sx node[24];
rz(0.5*pi) node[25];
rz(0.7951672353008665*pi) node[24];
cx node[25],node[24];
rz(3.7048327646991335*pi) node[24];
cx node[25],node[24];
rz(3.7951672353008665*pi) node[24];
rz(0.5*pi) node[25];
sx node[24];
sx node[25];
rz(3.5*pi) node[24];
rz(3.5*pi) node[25];
sx node[24];
sx node[25];
rz(1.5*pi) node[24];
rz(1.0*pi) node[25];
barrier node[25],node[24];
measure node[25] -> meas[0];
measure node[24] -> meas[1];
