# Design Automation for Quantum Circuit Benchmark (DAQCBench)

The Benchmark set contains many different algorithms in the benchmarks directory. These algorithms are used to 
create benchmarks on three different abstraction levels:
1) QuantumCircuit as a Qiskit object
2) Transpiled to QASM file using the IBM basis gates: ['id', 'rz', 'sx', 'x', 'cx', 'reset']
3) Transpiled to QASM file using a specific IBM Quantum Hardware Architecture

So far the following benchmarks are implemented:
- Amplitude Estimation
- Iterative Amplitude Estimation
- GHZ State
- Graph State
- W State
- Grover's Algorithm
- Shor's Algorithm
- QAOA
- VQE
- Quantum Fourier Transformation
- Quantum Fourier Transformation Entangled
- Quantum Phase Estimation Exact
- Quantum Phase Estimation Inexact

