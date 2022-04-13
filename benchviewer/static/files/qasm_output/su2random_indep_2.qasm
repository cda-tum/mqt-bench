// Benchmark was created by MQT Bench on 2022-04-10
// For more information about MQT Bench, please visit https://www.cda.cit.tum.de/mqtbench/
// MQT Bench version: 0.1.0
// Qiskit version: {'qiskit-terra': '0.19.2', 'qiskit-aer': '0.10.3', 'qiskit-ignis': '0.7.0', 'qiskit-ibmq-provider': '0.18.3', 'qiskit-aqua': '0.9.5', 'qiskit': '0.34.2', 'qiskit-nature': '0.3.1', 'qiskit-finance': '0.3.1', 'qiskit-optimization': '0.3.1', 'qiskit-machine-learning': '0.3.1'}

OPENQASM 2.0;
include "qelib1.inc";
qreg q[2];
creg meas[2];
u3(0.97838108,0.94172189,0) q[0];
u3(0.61197038,0.579624,0) q[1];
cx q[0],q[1];
u3(0.92567578,0.87353089,0) q[0];
u3(0.087392359,0.18534039,0) q[1];
cx q[0],q[1];
u3(0.084269008,0.201173,0) q[0];
u3(0.039072565,0.42614961,0) q[1];
cx q[0],q[1];
u3(0.26147616,0.95464519,0) q[0];
u3(0.079519634,0.50846371,0) q[1];
barrier q[0],q[1];
measure q[0] -> meas[0];
measure q[1] -> meas[1];
