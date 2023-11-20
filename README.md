[![PyPI](https://img.shields.io/pypi/v/mqt.bench?logo=pypi&style=flat-square)](https://pypi.org/project/mqt.bench/)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square)](https://opensource.org/licenses/MIT)
[![CI](https://img.shields.io/github/actions/workflow/status/cda-tum/MQTBench/coverage.yml?branch=main&style=flat-square&logo=github&label=coverage)](https://github.com/cda-tum/MQTBench/actions/workflows/coverage.yml)
[![Bindings](https://img.shields.io/github/actions/workflow/status/cda-tum/MQTBench/deploy.yml?branch=main&style=flat-square&logo=github&label=python)](https://github.com/cda-tum/MQTBench/actions/workflows/deploy.yml)
[![codecov](https://img.shields.io/codecov/c/github/cda-tum/mqt-bench?style=flat-square&logo=codecov)](https://codecov.io/gh/cda-tum/mqt-bench)
[![Documentation](https://img.shields.io/readthedocs/mqt-bench?logo=readthedocs&style=flat-square)](https://mqt.readthedocs.io/projects/bench)

<p align="center">
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/cda-tum/mqtbench/main/docs/_static/mqt_light.png" width="60%">
  <img src="https://raw.githubusercontent.com/cda-tum/mqtbench/main/docs/_static/mqt_dark.png" width="60%">
</picture>
</p>

# MQT Bench: Benchmarking Software and Design Automation Tools for Quantum Computing

MQT Bench is a quantum circuit benchmark suite with cross-level support, i.e., providing the same benchmark algorithms for different abstraction levels throughout the quantum computing
software stack.

<p align="center">
  <a href="https://mqt.readthedocs.io/projects/bench">
  <img width=30% src="https://img.shields.io/badge/documentation-blue?style=for-the-badge&logo=read%20the%20docs" alt="Documentation" />
  </a>
</p>

If you have any questions, feel free to create a [discussion](https://github.com/cda-tum/mqt-bench/discussions) or an [issue](https://github.com/cda-tum/mqt-bench/issues) on [GitHub](https://github.com/cda-tum/mqt-bench).

MQT Bench is part of the Munich Quantum Toolkit (MQT) developed by the [Chair for Design Automation](https://www.cda.cit.tum.de/) at the [Technical University of Munich](https://www.tum.de/) and is hosted at [https://www.cda.cit.tum.de/mqtbench/](https://www.cda.cit.tum.de/mqtbench/).

[<img src="https://raw.githubusercontent.com/cda-tum/mqtbench/main/docs/_static/mqtbench.png" align="center" width="500" >](https://www.cda.cit.tum.de/mqtbench)

## Getting Started

`mqt-bench` is available via [PyPI](https://pypi.org/project/mqt.bench/).

```console
(venv) $ pip install mqt.bench
```

The following code gives an example on the usage:

```python3
from mqt.bench import get_benchmark

# get a benchmark circuit on algorithmic level representing the GHZ state with 5 qubits
qc_algorithmic_level = get_benchmark(benchmark_name="dj", level="alg", circuit_size=5)

# draw the circuit
print(qc_algorithmic_level.draw())
```

**Detailed documentation and examples are available at [ReadTheDocs](https://mqt.readthedocs.io/projects/bench).**

# Repository Structure

- src/mqt/: main source directory
  - bench: Directory for the MQT Bench package
  - bench/benchmarks: Directory for the benchmarks
  - benchviewer: Directory for the webpage (which can be started locally and is also hosted at
    [https://www.cda.cit.tum.de/mqtbench/](https://www.cda.cit.tum.de/mqtbench/))
- tests: Directory for the tests for MQT Bench

## Acknowledgements

The Munich Quantum Toolkit has been supported by the European
Research Council (ERC) under the European Union's Horizon 2020 research and innovation program (grant agreement
No. 101001318), the Bavarian State Ministry for Science and Arts through the Distinguished Professorship Program, as well as the
Munich Quantum Valley, which is supported by the Bavarian state government with funds from the Hightech Agenda Bayern Plus.

<p align="center">
<picture>
<source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/cda-tum/mqt-bench/main/docs/_static/tum_dark.svg" width="28%">
<img src="https://raw.githubusercontent.com/cda-tum/mqt-bench/main/docs/_static/tum_light.svg" width="28%">
</picture>
<picture>
<img src="https://raw.githubusercontent.com/cda-tum/mqt-bench/main/docs/_static/logo-bavaria.svg" width="16%">
</picture>
<picture>
<source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/cda-tum/mqt-bench/main/docs/_static/erc_dark.svg" width="24%">
<img src="https://raw.githubusercontent.com/cda-tum/mqt-bench/main/docs/_static/erc_light.svg" width="24%">
</picture>
<picture>
<img src="https://raw.githubusercontent.com/cda-tum/mqt-bench/main/docs/_static/logo-mqv.svg" width="28%">
</picture>
</p>
