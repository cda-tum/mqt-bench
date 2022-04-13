// Benchmark was created by MQT Bench on 2022-04-12
// For more information about MQT Bench, please visit https://www.cda.cit.tum.de/mqtbench/
// MQT Bench version: 0.1.0
// Qiskit version: {'qiskit-terra': '0.19.2', 'qiskit-aer': '0.10.3', 'qiskit-ignis': '0.7.0', 'qiskit-ibmq-provider': '0.18.3', 'qiskit-aqua': '0.9.5', 'qiskit': '0.34.2', 'qiskit-nature': '0.3.1', 'qiskit-finance': '0.3.1', 'qiskit-optimization': '0.3.1', 'qiskit-machine-learning': '0.3.1'}

OPENQASM 2.0;
include "qelib1.inc";
qreg q[4];
creg meas[4];
ry(1.46212950048812) q[0];
ry(-0.968273418787402) q[1];
cx q[0],q[1];
ry(1.2441445127239) q[2];
cx q[0],q[2];
cx q[1],q[2];
ry(-2.59941082994815) q[3];
cx q[0],q[3];
ry(1.12710284542787) q[0];
cx q[1],q[3];
ry(-1.66482476584116) q[1];
cx q[0],q[1];
cx q[2],q[3];
ry(1.58590178481215) q[2];
cx q[0],q[2];
cx q[1],q[2];
ry(-0.98758175627156) q[3];
cx q[0],q[3];
ry(-2.0675503716056) q[0];
cx q[1],q[3];
ry(1.58528461845526) q[1];
cx q[2],q[3];
ry(2.0315615734501) q[2];
ry(-3.11540896377294) q[3];
barrier q[0],q[1],q[2],q[3];
measure q[0] -> meas[0];
measure q[1] -> meas[1];
measure q[2] -> meas[2];
measure q[3] -> meas[3];
