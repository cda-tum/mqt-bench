# qTUMbench: Benchmarking Software and Design Automation Tools for Quantum Computing

qTUMbench is a benchmarking suite with cross-layer support. This means, that the same benchmarking
algorithms are provided for different abstraction layers throught the quantum computing
software stack.

qTUMbench uses the structure proposed by the openQASM 3.0 consortia [1] and offers benchmarks
on four different abstraction layers:
1) Algorithm Layer
2) Target-independent Layer
3) Target-dependent Native Gates Layer
4) Target-dependent Mapped Layer

## Benchmark Selection
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
- Deutsch Jozsa
- HHL
- Quantum Walk
- Quantum Fourier Transformation
- Quantum Fourier Transformation Entangled
- Quantum Phase Estimation Exact
- Quantum Phase Estimation Inexact

Additionally, several quantum application algorithms are available.

## Native Gate-Set Support
So far, qTUMbench supports the following native gate-sets:
1) IBM-Q gate set with ['id', 'rz', 'sx', 'x', 'cx', 'reset']
2) Rigetti gate set with ['rx','rz','cz']

## Mapping Scheme Support
Currently, qTUMbench supports two mapping schemes:
1) Smallest Fitting Architecture Mapping: Maps quantum circuits to the smallest architecture with a sufficient number of physical qubits
2) Biggest Architecture Mapping: Always use the biggest available hardware architecture


References:
<details open>
<summary> [1] A.Cross et al., OpenQASM 3: A broader and deeper quantum assembly language, arXiv:2104.14722, 2021 </summary>

```bibtex
@misc{cross2021openqasm,
      title={OpenQASM 3: A broader and deeper quantum assembly language}, 
      author={Andrew W. Cross and Ali Javadi-Abhari and Thomas Alexander and Niel de Beaudrap and Lev S. Bishop and Steven Heidel and Colm A. Ryan and John Smolin and Jay M. Gambetta and Blake R. Johnson},
      year={2021},
      eprint={2104.14722},
      archivePrefix={arXiv},
      primaryClass={quant-ph}
}
```

</details>