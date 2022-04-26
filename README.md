[![PyPI](https://img.shields.io/pypi/v/mqt.bench?logo=pypi&style=flat-square)](https://pypi.org/project/mqt.bench/)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square)](https://opensource.org/licenses/MIT)
[![CI](https://img.shields.io/github/workflow/status/cda-tum/MQTBench/CodeCov?style=flat-square&logo=github&label=coverage)](https://github.com/cda-tum/MQTBench/actions/workflows/coverage.yml)
[![Bindings](https://img.shields.io/github/workflow/status/cda-tum/MQTBench/Deploy%20to%20PyPI?style=flat-square&logo=github&label=python)](https://github.com/cda-tum/MQTBench/actions/workflows/deploy.yml)
[![codecov](https://img.shields.io/codecov/c/github/cda-tum/MQTBench?style=flat-square&logo=codecov)](https://codecov.io/gh/cda-tum/MQTBench)
[![Server Deployment](https://github.com/cda-tum/MQTBench/actions/workflows/server_deployment.yml/badge.svg)](https://github.com/cda-tum/MQTBench/actions/workflows/server_deployment.yml)

# MQT Bench: Benchmarking Software and Design Automation Tools for Quantum Computing

MQT Bench is a quantum circuit benchmark suite with cross-level support, i.e., providing the same benchmark algorithms for different abstraction levels throughout the quantum computing
software stack. 

MQT Bench is part of the Munich Quantum Toolkit (MQT) developed by the [Chair for Design Automation](https://www.cda.cit.tum.de/) at the [Technical University of Munich](https://www.tum.de/) and is hosted at [https://www.cda.cit.tum.de/mqtbench/](https://www.cda.cit.tum.de/mqtbench/).

[<img src="img/mqtbench.png" align="center" width="500" >](https://www.cda.cit.tum.de/mqtbench)

## Abstraction Levels
It uses the structure proposed by the openQASM 3.0 specification [[1]](https://arxiv.org/abs/2104.14722) and offers benchmarks
on four different abstraction levels:
1) Algorithmic Level
2) Target-independent Level
3) Target-dependent Native Gates Level
4) Target-dependent Mapped Level

An example is given in the following:

1) Algorithmic Level

<img src="img/level_1.png"  align="center" width="250">

Variational Quantum Algorithms (VQAs) are an emerging class of quantum algorithms with a wide range of 
applications. A respective circuit is shown above, it represents an example of an ansatz function 
frequently used for Variational Quantum Eigensolvers (VQEs), a subclass of VQAs. On this abstraction 
level, the circuit is parameterized by the angles θ<sub>i</sub> of the six single-qubit gates.

2) Target-independent Level

<img src="img/level_2.png"  align="center" width="250">

VQAs are hybrid quantum-classical algorithms, where the parameters of the quantum ansatz are 
iteratively updated by a classical optimizer analogous to conventional gradient-based optimization. 
Consider again the circuit from the previous figure. Assuming these parameters have been determined, 
e.g., θ<sub>i</sub> = −π for i = 0, ..., 5, they are now propagated and the resulting quantum circuit is 
shown above.


3) Target-dependent Native Gates Level

<img src="img/level_3.png"  align="center" width="250"/>

Different quantum computer realizations support
different native gate-sets. In our example, we consider the
IBMQ Manila device as the target device which natively supports I, X, √X, Rz and CX gates. 
Consequently, the Ry gates in the previous figure have to be converted using only these native gates. In this case, 
they are substituted by a sequence of X and Rz gates (denoted as • with a phase of −π).

4) Target-dependent Mapped Level

<img src="img/level_4.png"  align="center" width="300"/>
<img src="img/arch.png"  align="center" width="100"/>


The architecture of the IBMQ Manila device is shown 
above on the right and it defines between which qubits a two-qubit operation may be performed. 
Since the circuit shown in the previous figure contains CX gates operating between all combination of qubits, 
there is no mapping directly matching the target architecture’s layout. As a consequence, 
a non-trivial mapping followed by a round of optimization leads to the resulting circuit 
shown above on the left. This is also the reason for the different sequence of CX gates compared 
to the previous example.

This circuit is now executable on the IBMQ Manila device, since all hardware induced requirements are fulfilled.

## Benchmark Selection
So far, the following benchmarks are implemented and provided:
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

See the [benchmark description](https://www.cda.cit.tum.de/mqtbench/benchmark_description) for further details on the individual benchmarks.

## Native Gate-Set Support
So far, MQT Bench supports the following native gate-sets:
1) IBMQ gate-set: *\['id', 'rz', 'sx', 'x', 'cx', 'reset'\]*
2) Rigetti gate-set: *\['id, 'rx', 'rz', 'cz', 'reset'\]*

## Mapping Scheme Support
Currently, MQT Bench supports two mapping schemes:
1) Smallest Fitting Architecture Mapping: Maps quantum circuits to the smallest architecture with a sufficient number of physical qubits
2) Biggest Architecture Mapping: Always use the biggest available hardware architecture

# Repository Structure
- mqt/bench/utils: Directory for the utils.py file 
- mqt/bench/tests: Directory for the tests for MQT Bench
- mqt/bench/benchmarks: On the top-level, each benchmark algorithm is included as a separate file. 
  - Additionally, folders for each IBM Qiskit application module and their respective benchmarks are listed.
- benchviewer: This is the folder for our webpage hosted at [https://www.cda.cit.tum.de/mqtbench/](https://www.cda.cit.tum.de/mqtbench/).

```
MQTBench/
│ - README.md
│
└───mqt/bench/
│   │───benchmark_generator.py  
│   └───utils/
│   │   │ - utils.py
│   │
│   └───tests/
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
1) Via our web-interface hosted at [https://www.cda.cit.tum.de/mqtbench/](https://www.cda.cit.tum.de/mqtbench/)
2) Via our pip package `mqt.bench`
3) Directly via this repository

Since the first way is rather self-explanatory, the other two ways are explained in more detail in the following.

## Usage via pip package
MQT Bench is available via [PyPI](https://pypi.org/project/mqt.bench/)
```console
(venv) $ pip install mqt.bench
```
To generate a benchmark circuit on the algorithmic level, please use the `get_one_benchmark` method:

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
The available parameters are:
  - `benchmark_name`: `"ae"`, `"dj"`, `"grover-noancilla"`, `"grover-v-chain"`, `"ghz"`, `"graphstate"`, `"portfolioqaoa"`,
                        `"portfoliovqe"`, `"qaoa"`, `"qft"`, `"qftentangled"`, `"qgan"`, `"qpeexact"`, `"qpeinexact"`,
                        `"qwalk-noancilla"`, `"qwalk-v-chain"`, `"realamprandom"`, `"su2random"`, `"twolocalrandom"`, `"vqe"`,
                        `"wstate"`, `"shor"`, `"hhl"`, `"pricingcall"`, `"pricingput"`, `"groundstate"`, `"excitedstate"`, `"routing"`,
                        `"tsp"`
  - `level`: `0` or `"alg"`, `1` or `"indep"`, `2` or `"nativegates"`, `3` or `"mapped"`
  - `circuit_size`: most of the cases this is equal to number of qubits (for some benchmarks the number of qubits is higher)
  - `benchmark_instance_name`: `"xsmall"`, `"small"`, `"medium"`, `"large"`, `"xlarge"` (not all instances are available for each benchmark)
  - `opt_level`: `0`, `1`, `2`, `3`
  - `gate_set_name`: `"ibm"`, `"rigetti"`
  - `smallest_fitting_arch`: `False`, `True`

For example, in order to obtain the *5*-qubit Deutsch-Josza algorithm, use the following:
```python
from mqt.bench import get_one_benchmark

qc = get_one_benchmark("dj", "alg", 5)
```

In order to get access to all benchmarks, including the Qiskit application module algorithms, some addtional dependencies are required. 
These can be installed via pip as follows:
```console
(venv) $ pip install mqt.bench[all]
```

## Usage directly via this repository
Since all generated benchmarks hosted on our website are included in this repository, 
the repository is very large (`>25 GB`). Therefore, please do a sparse-checkout if you want to 
directly access the repository itself:
```
git clone --filter=blob:none --no-checkout  https://github.com/cda-tum/MQTBench.git
cd MQTBench
git sparse-checkout init --cone
git sparse-checkout set mqt img
git checkout main
```

# References:
In case you are using MQT Bench in your work, we would be thankful if you referred to it by citing the following publication:
```bibtex
@misc{quetschlich2022mqtbench,
  title={MQT Bench: Benchmarking Software and Design Automation Tools for Quantum Computing},
  author={Quetschlich, Nils and Burgholzer, Lukas and Wille, Robert},
  year={2022},
  note={{MQT Bench} is available at \url{https://www.cda.cit.tum.de/mqtbench/}},
}
````

[1] A.Cross et al., OpenQASM 3: A broader and deeper quantum assembly language, [arXiv:2104.14722](https://arxiv.org/abs/2104.14722), 2021 
