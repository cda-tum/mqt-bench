// Benchmark was created by MQT Bench on 2022-06-08
// For more information about MQT Bench, please visit https://www.cda.cit.tum.de/mqtbench/
// MQT Bench version: 0.1.0
// Qiskit version: {'qiskit-terra': '0.20.2', 'qiskit-aer': '0.10.4', 'qiskit-ignis': '0.7.1', 'qiskit-ibmq-provider': '0.19.1', 'qiskit-aqua': '0.9.5', 'qiskit': '0.36.2', 'qiskit-nature': '0.3.2', 'qiskit-finance': '0.3.1', 'qiskit-optimization': '0.3.2', 'qiskit-machine-learning': '0.3.1'}
// Used Gate Set: <tket::BasePass>

OPENQASM 2.0;
include "qelib1.inc";

qreg eval[2];
qreg q[1];
creg meas[3];
sx eval[0];
sx eval[1];
rz(0.5*pi) q[0];
rz(0.5*pi) eval[0];
rz(0.5*pi) eval[1];
sx q[0];
sx eval[0];
sx eval[1];
rz(3.5*pi) q[0];
x eval[0];
rz(0.5*pi) eval[1];
sx q[0];
rz(3.5*pi) eval[0];
x eval[1];
rz(0.7951672353008665*pi) q[0];
rz(3.5*pi) eval[1];
sx q[0];
ecr eval[0],q[0];
rz(0.25*pi) eval[0];
rz(3.7048327646991335*pi) q[0];
x eval[0];
sx q[0];
rz(3.5*pi) eval[0];
ecr eval[0],q[0];
x eval[0];
rz(0.2951672353008665*pi) q[0];
rz(3.5*pi) eval[0];
sx q[0];
ecr eval[1],q[0];
x eval[1];
rz(3.4096655293982683*pi) q[0];
rz(3.5*pi) eval[1];
sx q[0];
ecr eval[1],q[0];
rz(0.5*pi) eval[1];
rz(0.09033447060173172*pi) q[0];
sx eval[1];
sx q[0];
rz(3.5*pi) eval[1];
rz(3.5*pi) q[0];
sx eval[1];
sx q[0];
rz(1.0*pi) eval[1];
rz(1.5*pi) q[0];
sx eval[1];
ecr eval[0],eval[1];
x eval[0];
rz(0.25*pi) eval[1];
rz(3.5*pi) eval[0];
sx eval[1];
ecr eval[0],eval[1];
rz(0.5*pi) eval[0];
rz(3.75*pi) eval[1];
sx eval[0];
rz(3.5*pi) eval[0];
sx eval[0];
rz(1.0*pi) eval[0];
barrier eval[0],eval[1],q[0];
measure eval[0] -> meas[0];
measure eval[1] -> meas[1];
measure q[0] -> meas[2];
