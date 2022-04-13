// Benchmark was created by MQT Bench on 2022-04-07
// For more information about MQT Bench, please visit https://www.cda.cit.tum.de/mqtbench/
// MQT Bench version: 0.1.0
// Qiskit version: {'qiskit-terra': '0.19.2', 'qiskit-aer': '0.10.3', 'qiskit-ignis': '0.7.0', 'qiskit-ibmq-provider': '0.18.3', 'qiskit-aqua': '0.9.5', 'qiskit': '0.34.2', 'qiskit-nature': '0.3.1', 'qiskit-finance': '0.3.1', 'qiskit-optimization': '0.3.1', 'qiskit-machine-learning': '0.3.1'}

OPENQASM 2.0;
include "qelib1.inc";
qreg q[6];
creg meas[6];
h q[0];
h q[1];
h q[2];
h q[3];
h q[4];
rzz(-1.75673946673406) q[2],q[4];
h q[5];
rzz(-1.75673946673406) q[3],q[5];
rzz(-1.75673946673406) q[0],q[3];
rzz(-1.75673946673406) q[0],q[2];
rx(8.90399790588764) q[0];
rzz(-1.75673946673406) q[1],q[5];
rzz(-1.75673946673406) q[1],q[4];
rx(8.90399790588764) q[1];
rx(8.90399790588764) q[2];
rx(8.90399790588764) q[3];
rx(8.90399790588764) q[4];
rzz(5.08712887134137) q[2],q[4];
rx(8.90399790588764) q[5];
rzz(5.08712887134137) q[3],q[5];
rzz(5.08712887134137) q[0],q[3];
rzz(5.08712887134137) q[0],q[2];
rx(11.72583519996) q[0];
rzz(5.08712887134137) q[1],q[5];
rzz(5.08712887134137) q[1],q[4];
rx(11.72583519996) q[1];
rx(11.72583519996) q[2];
rx(11.72583519996) q[3];
rx(11.72583519996) q[4];
rx(11.72583519996) q[5];
barrier q[0],q[1],q[2],q[3],q[4],q[5];
measure q[0] -> meas[0];
measure q[1] -> meas[1];
measure q[2] -> meas[2];
measure q[3] -> meas[3];
measure q[4] -> meas[4];
measure q[5] -> meas[5];
