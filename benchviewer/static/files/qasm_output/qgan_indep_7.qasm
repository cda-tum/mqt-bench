// Benchmark was created by MQT Bench on 2022-04-09
// For more information about MQT Bench, please visit https://www.cda.cit.tum.de/mqtbench/
// MQT Bench version: 0.1.0
// Qiskit version: {'qiskit-terra': '0.19.2', 'qiskit-aer': '0.10.3', 'qiskit-ignis': '0.7.0', 'qiskit-ibmq-provider': '0.18.3', 'qiskit-aqua': '0.9.5', 'qiskit': '0.34.2', 'qiskit-nature': '0.3.1', 'qiskit-finance': '0.3.1', 'qiskit-optimization': '0.3.1', 'qiskit-machine-learning': '0.3.1'}

OPENQASM 2.0;
include "qelib1.inc";
qreg q[7];
creg meas[7];
u3(1.7560909,-pi,0) q[0];
u3(2.4587006,-pi,0) q[1];
cz q[0],q[1];
u3(1.9177186,0,-pi) q[2];
cz q[0],q[2];
cz q[1],q[2];
u3(2.2524849,0,-pi) q[3];
cz q[0],q[3];
cz q[1],q[3];
cz q[2],q[3];
u3(2.3864892,-pi,0) q[4];
cz q[0],q[4];
cz q[1],q[4];
cz q[2],q[4];
cz q[3],q[4];
u3(2.5912191,0,-pi) q[5];
cz q[0],q[5];
cz q[1],q[5];
cz q[2],q[5];
cz q[3],q[5];
cz q[4],q[5];
u3(1.5802635,0,-pi) q[6];
cz q[0],q[6];
ry(3.30519782076308) q[0];
cz q[1],q[6];
ry(3.03228387786352) q[1];
cz q[2],q[6];
ry(0.582607738616495) q[2];
cz q[3],q[6];
ry(4.53407372840901) q[3];
cz q[4],q[6];
ry(5.85146444426907) q[4];
cz q[5],q[6];
ry(2.72169285653691) q[5];
ry(4.83309300289996) q[6];
barrier q[0],q[1],q[2],q[3],q[4],q[5],q[6];
measure q[0] -> meas[0];
measure q[1] -> meas[1];
measure q[2] -> meas[2];
measure q[3] -> meas[3];
measure q[4] -> meas[4];
measure q[5] -> meas[5];
measure q[6] -> meas[6];
