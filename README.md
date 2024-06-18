[![PyPI](https://img.shields.io/pypi/v/mqt.bench?logo=pypi&style=flat-square)](https://pypi.org/project/mqt.bench/)
![OS](https://img.shields.io/badge/os-linux%20%7C%20macos%20%7C%20windows-blue?style=flat-square)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square)](https://opensource.org/licenses/MIT)
[![CI](https://img.shields.io/github/actions/workflow/status/cda-tum/mqt-bench/ci.yml?branch=main&style=flat-square&logo=github&label=ci)](https://github.com/cda-tum/mqt-bench/actions/workflows/ci.yml)
[![CD](https://img.shields.io/github/actions/workflow/status/cda-tum/mqt-bench/cd.yml?style=flat-square&logo=github&label=cd)](https://github.com/cda-tum/mqt-bench/actions/workflows/cd.yml)
[![Documentation](https://img.shields.io/readthedocs/mqt-bench?logo=readthedocs&style=flat-square)](https://mqt.readthedocs.io/projects/bench)
[![codecov](https://img.shields.io/codecov/c/github/cda-tum/mqt-bench?style=flat-square&logo=codecov)](https://codecov.io/gh/cda-tum/mqt-bench)

<p align="center">
  <a href="https://mqt.readthedocs.io">
   <picture>
     <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/cda-tum/mqt/main/docs/_static/mqt_light.png" width="60%">
     <img src="https://raw.githubusercontent.com/cda-tum/mqt/main/docs/_static/mqt_dark.png" width="60%">
   </picture>
  </a>
</p>

# MQT Bench: Benchmarking Software and Design Automation Tools for Quantum Computing

MQT Bench is a quantum circuit benchmark suite with cross-level support, i.e., providing the same benchmark algorithms for different abstraction levels throughout the quantum computing
software stack.
MQT Bench is part of the [_Munich Quantum Toolkit_ (_MQT_)](https://mqt.readthedocs.io) developed by the [Chair for Design Automation](https://www.cda.cit.tum.de/) at the [Technical University of Munich](https://www.tum.de/) and is hosted at [https://www.cda.cit.tum.de/mqtbench/](https://www.cda.cit.tum.de/mqtbench/).

<p align="center">
  <a href="https://mqt.readthedocs.io/projects/bench">
  <img width=30% src="https://img.shields.io/badge/documentation-blue?style=for-the-badge&logo=read%20the%20docs" alt="Documentation" />
  </a>
</p>

If you have any questions, feel free to create a [discussion](https://github.com/cda-tum/mqt-bench/discussions) or an [issue](https://github.com/cda-tum/mqt-bench/issues) on [GitHub](https://github.com/cda-tum/mqt-bench).

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

## Availability as a PennyLane Dataset

MQT Bench is also available as a [PennyLane dataset](https://pennylane.ai/datasets/other/mqt-bench).

## References

In case you are using MQT Bench in your work, we would be thankful if you referred to it by citing the following publication:

```bibtex
@article{quetschlich2023mqtbench,
  title         = {{{MQT Bench}}: {Benchmarking Software and Design Automation Tools for Quantum Computing}},
  shorttitle    = {{MQT Bench}},
  journal       = {{Quantum}},
  author        = {Quetschlich, Nils and Burgholzer, Lukas and Wille, Robert},
  year          = {2023},
  doi           = {10.22331/q-2023-07-20-1062},
  eprint        = {2204.13719},
  primaryclass  = {quant-ph},
  archiveprefix = {arxiv},
  note          = {{{MQT Bench}} is available at \url{https://www.cda.cit.tum.de/mqtbench/}},
}
```

## Acknowledgements

This project received funding from the European Research Council (ERC) under the European
Union's Horizon 2020 research and innovation program (grant agreement No. 101001318), was
part of the Munich Quantum Valley, which is supported by the Bavarian state government with
funds from the Hightech Agenda Bayern Plus, and has been supported by the BMWK on the basis
of a decision by the German Bundestag through project QuaST, as well as by the BMK, BMDW,
and the State of Upper Austria in the frame of the COMET program (managed by the FFG).

<p align="center">
<picture>
<source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/cda-tum/mqt/main/docs/_static/tum_dark.svg" width="28%">
<img src="https://raw.githubusercontent.com/cda-tum/mqt/main/docs/_static/tum_light.svg" width="28%" alt="TUM Logo">
</picture>
<picture>
<img src="https://raw.githubusercontent.com/cda-tum/mqt/main/docs/_static/logo-bavaria.svg" width="16%" alt="Coat of Arms of Bavaria">
</picture>
<picture>
<source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/cda-tum/mqt/main/docs/_static/erc_dark.svg" width="24%">
<img src="https://raw.githubusercontent.com/cda-tum/mqt/main/docs/_static/erc_light.svg" width="24%" alt="ERC Logo">
</picture>
<picture>
<img src="https://raw.githubusercontent.com/cda-tum/mqt/main/docs/_static/logo-mqv.svg" width="28%" alt="MQV Logo">
</picture>
</p>
