// Benchmark was created by MQT Bench on 2022-03-23
// MQT Bench version: 0.1.0
// Qiskit version: {'qiskit-terra': '0.19.2', 'qiskit-aer': '0.10.3', 'qiskit-ignis': '0.7.0', 'qiskit-ibmq-provider': '0.18.3', 'qiskit-aqua': '0.9.5', 'qiskit': '0.34.2', 'qiskit-nature': '0.3.1', 'qiskit-finance': '0.3.1', 'qiskit-optimization': '0.3.1', 'qiskit-machine-learning': '0.3.1'}
// Used Gate Set: ['id', 'rz', 'sx', 'x', 'cx', 'reset']
// Optimization Level: 0

OPENQASM 2.0;
include "qelib1.inc";
qreg q[2];
creg meas[2];
rz(0.0) q[0];
sx q[0];
rz(3.9798995807056) q[0];
sx q[0];
rz(3*pi) q[0];
rz(0.48905303503699) q[0];
rz(0.0) q[1];
sx q[1];
rz(3.8061779711027) q[1];
sx q[1];
rz(3*pi) q[1];
rz(0.584280820552458) q[1];
cx q[0],q[1];
rz(0.0) q[0];
sx q[0];
rz(3.1674657657473) q[0];
sx q[0];
rz(3*pi) q[0];
rz(0.00305368136092854) q[0];
rz(0.0) q[1];
sx q[1];
rz(3.6907864548983) q[1];
sx q[1];
rz(3*pi) q[1];
rz(0.484555806831463) q[1];
cx q[0],q[1];
rz(0.0) q[0];
sx q[0];
rz(3.95114428540414) q[0];
sx q[0];
rz(3*pi) q[0];
rz(0.00655822139666351) q[0];
rz(0.0) q[1];
sx q[1];
rz(3.20909955659369) q[1];
sx q[1];
rz(3*pi) q[1];
rz(0.798471898486282) q[1];
cx q[0],q[1];
rz(0.0) q[0];
sx q[0];
rz(3.30842656147791) q[0];
sx q[0];
rz(3*pi) q[0];
rz(0.696729783920658) q[0];
rz(0.0) q[1];
sx q[1];
rz(3.57762835210269) q[1];
sx q[1];
rz(3*pi) q[1];
rz(0.0265583465682039) q[1];
barrier q[0],q[1];
measure q[0] -> meas[0];
measure q[1] -> meas[1];
