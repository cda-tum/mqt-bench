[![PyPI](https://img.shields.io/pypi/v/mqt.bench?logo=pypi&style=flat-square)](https://pypi.org/project/mqt.bench/)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square)](https://opensource.org/licenses/MIT)
[![Deploy to PyPI](https://github.com/cda-tum/MQTBench/actions/workflows/deploy.yml/badge.svg)](https://github.com/cda-tum/MQTBench/actions/workflows/deploy.yml)
[![CodeCov](https://github.com/cda-tum/MQTBench/actions/workflows/coverage.yml/badge.svg)](https://github.com/cda-tum/MQTBench/actions/workflows/coverage.yml)
[![codecov](https://codecov.io/gh/cda-tum/mqtbench/branch/main/graph/badge.svg?token=m9ocRq7OxR)](https://codecov.io/gh/cda-tum/mqtbench)
# MQT Bench: Benchmarking Software and Design Automation Tools for Quantum Computing

MQT Bench is a benchmark suite with cross-level support. This means, that the same benchmarking
algorithms are provided for different abstraction levels through the quantum computing
software stack.

MQT Bench uses the structure proposed by the openQASM 3.0 consortia [1] and offers benchmarks
on four different abstraction levels:
1) Algorithm Level
2) Target-independent Level
3) Target-dependent Native Gates Level
4) Target-dependent Mapped Level


<img src="img/layer_1.png"  align="left" width="250"/>

Variational Quantum Algorithms (VQAs) are an emerging class of quantum algorithms with a wide range of 
applications. A respective circuit is shown on the left, it represents an example of an ansatz function 
frequently used for Variational Quantum Eigensolvers (VQEs), a subclass of VQAs. On this abstraction 
level, the circuit is parameterized by the angles θ<sub>i</sub> of the six single-qubit gates.

<img src="img/layer_2.png"  align="left" width="250"/>

VQAs are hybrid quantum-classical algorithms, where the parameters of the quantum ansatz are 
iteratively updated by a classical optimizer analogous to conventional gradient-based optimization. 
Consider again the circuit from the previous image. Assuming these parameters have been determined, 
e.g., θ<sub>i</sub> = −π for i = 0, ..., 5, they are now propagated and the resulting quantum circuit is 
shown here.


<img src="img/layer_3.png"  align="left" width="250"/>

<img src="img/arch.png"  align="right" width="100"/>

Different quantum computer realizations support
different native gate-sets. In our example, we consider the
IBMQ Manila device as the target device which natively supports I, X, √X, Rz and CX gates. 
Consequently, the Ry gates in the previous figure have to be converted using only these native gates. In this case, 
they are substituted by a sequence of X and Rz gates (denoted as • with a phase of −π).


<img src="img/layer_4.png"  align="left" width="300"/>

Consider again the previous scenario. The architecture of the IBMQ Manila device is shown 
on the right and it defines between which qubits a two-qubit operation may be performed. 
Since the circuit shown in the previous figure contains CX gates operating between all combination of qubits, 
there is no mapping directly matching the target architecture’s layout. As a consequence, 
a non-trivial mapping followed by a round of optimization leads to the resulting circuit 
shown on the left. This is also the reason for the different sequence of CX gates compared 
to the previous example.

## Benchmark Selection
So far, the following benchmarks are implemented:
- Amplitude Estimation
- Deutsch-Jozsa
- Excited State
- GHZ State
- Graph State
- Ground State
- Grover's (no ancilla)
- Grover's (v-chain)
- HHL
- Portfolio Optimization with QAOA
- Portfolio Optimization with VQE
- Pricing Call Option
- Pricing Put Option
- Quantum Fourier Transformation (QFT)
- QFT Entangled
- Quantum Generative Adversarial Network (QGAN)
- Quantum Phase Estimation (QPE) Exact
- Quantum Phase Estimation (QPE) Inexact
- Quantum Walk (no ancilla)
- Quantum Walk (-chain)
- Routing
- Shor's
- Travelling Salesman
- Variational Quantum Eigensolver (VQE)
- VQE-ansätze with random values:
  - Efficient SU2 ansatz with Random Parameters
  - Real Amplitudes ansatz with Random Parameters
  - Two Local ansatz with Random Parameters
- W-State

## Native Gate-Set Support
So far, MQT Bench supports the following native gate-sets:
1) IBM-Q gate set with ['id', 'rz', 'sx', 'x', 'cx', 'reset']
2) Rigetti gate set with ['id, 'rx', 'rz', 'cz', 'reset']

## Mapping Scheme Support
Currently, MQT Bench supports two mapping schemes:
1) Smallest Fitting Architecture Mapping: Maps quantum circuits to the smallest architecture with a sufficient number of physical qubits
2) Biggest Architecture Mapping: Always use the biggest available hardware architecture

# Structure
- src: Directory for  utils.py file and the source code of the benchmarks
- benchmarks: On top level, the benchmarks are included with one benchmark algorithms per file. 
  - Additionally, folders for each qiskit application module and their respective benchmarks are listed
- benchviewer: This is the folder for our webpage hosted at [https://www.cda.cit.tum.de/app/benchviewer/](https://www.cda.cit.tum.de/app/benchviewer/).
```
MQT Bench/
│ - README.md
│
└───mqt/bench/
│   │───benchmark_generator.py  
│   └───utils/
│   │   │ - utils.py
│   │
│   └───benchmarks/
│       │ - ae.py
│       │   ...
│       │ - wstate.py
│       └─── qiskit_application_finance
│       │       ...
│       └─── qiskit_application_ml
│       │       ...
│       └─── qiskit_application_nature
│       │       ...
│       └─── qiskit_application_optimization
│       │       ...
│
│───benchviewer/
```

# Repository Usage
There are three ways how to use this benchmark suite:
1) Via our webinterface hosted at [https://www.cda.cit.tum.de/mqtbench/](https://www.cda.cit.tum.de/mqtbench/)
2) Via our pip package
3) Directly via this repository

Since the first way is rather self-explainatory, we explain the other two ways in detail in the following.

## Usage via pip package
To use our basic benchmarks, please follow these installation and import instructions:
```python
pip install mqt.bench
from mqt.bench import get_one_benchmark
```

To generate one benchmark on the algorithm level, please use this method:

```python
get_one_benchmark(
    benchmark_name: str,
    level: Union[str, int],
    circuit_size: int = None,
    benchmark_instance_name: str = None,
    opt_level: int = None,
    gate_set_name: str = None,
    smallest_fitting_arch: bool = None,
)
```

For example:

```python
qc = get_one_benchmark("dj", "alg", 5)
```

If you want to use all benchmarks including the application ones, please install the package like this:
```python
pip install mqt.bench[all]
from mqt.bench import get_one_benchmark
```

The available parameters are:
  - benchmark_name: "ae", "dj", "grover-noancilla", "grover-v-chain", "ghz", "graphstate", "portfolioqaoa",
                        "portfoliovqe", "qaoa", "qft", "qftentangled", "qgan", "qpeexact", "qpeinexact",
                        "qwalk-noancilla", "qwalk-v-chain", "realamprandom", "su2random", "twolocalrandom", "vqe",
                        "wstate", "shor", "hhl", "pricingcall", "pricingput", "groundstate", "excitedstate", "routing",
                        "tsp"
  - level: 0 or "alg", 1 or "indep", 2 or "nativegates", 3 or "mapped"
  - circuit_size: most of the cases this is equal to number of qubits (for some benchmarks the number of qubits is higher)
  - benchmark_instance_name: "xsmall", "small", "medium", "large", "xlarge" (not all instances are available for each benchmark)
  - opt_level: 0, 1, 2, 3
  - gate_set_name: "ibm", "rigetti"
  - smallest_fitting_arch: False, True

## Usage directly via this repository
Since all generated benchmarks hosted on our website are included in this repository, 
the repository is very large (>25 GB). Therefore, please do a sparse-checkout if you want to 
directly access the repository itself:
```
git clone --filter=blob:none --no-checkout  https://github.com/cda-tum/MQTBench.git
cd MQTBench
git sparse-checkout init --cone
git sparse-checkout set mqt
git checkout main
```

# References:
[1] A.Cross et al., OpenQASM 3: A broader and deeper quantum assembly language, [arXiv:2104.14722](https://arxiv.org/abs/2104.14722), 2021 
