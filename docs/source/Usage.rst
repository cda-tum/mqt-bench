Repository Usage
================
There are three ways how to use this benchmark suite:


#. Via the webpage hosted at `https://www.cda.cit.tum.de/mqtbench/ <https://www.cda.cit.tum.de/mqtbench/>`_
#. Via the pip package ``mqt.bench``
#. Directly via this repository

Since the first way is rather self-explanatory, the other two ways are explained in more detail in the following.

Usage via pip package
---------------------

MQT Bench is available via `PyPI <https://pypi.org/project/mqt.bench/>`_

.. code-block:: console

   (venv) $ pip install mqt.bench

To generate a benchmark circuit on the algorithmic level, please use the ``get_benchmark`` method:

.. code-block:: python

   def get_benchmark(
       benchmark_name: str,
       level: Union[str, int],
       circuit_size: int = None,
       benchmark_instance_name: str = None,
       compiler: str = "qiskit",
       compiler_settings: mqt.bench.CompilerSettings = None,
       gate_set_name: str = "ibm",
       device_name: str = "ibm_washington",
   ):
       ...

The available parameters are:


* ``benchmark_name``\ : ``"ae"``\ , ``"dj"``\ , ``"grover-noancilla"``\ , ``"grover-v-chain"``\ , ``"ghz"``\ , ``"graphstate"``\ , ``"portfolioqaoa"``\ ,
  ``"portfoliovqe"``\ , ``"qaoa"``\ , ``"qft"``\ , ``"qftentangled"``\ , ``"qnn"``\ , ``"qpeexact"``\ , ``"qpeinexact"``\ ,
  ``"qwalk-noancilla"``\ , ``"qwalk-v-chain"``\ , ``"random"``\ , ``"realamprandom"``\ , ``"su2random"``\ , ``"twolocalrandom"``\ , ``"vqe"``\ ,
  ``"wstate"``\ , ``"shor"``\ , ``"pricingcall"``\ , ``"pricingput"``\ , ``"groundstate"``\ , ``"routing"``\ ,
  ``"tsp"``
* ``level``\ : ``0`` or ``"alg"``\ , ``1`` or ``"indep"``\ , ``2`` or ``"nativegates"``\ , ``3`` or ``"mapped"``
* ``circuit_size``\ : for most of the cases this is equal to number of qubits
  (all scalable benchmarks except ``"qwalk-v-chain"`` and ``"grover-v-chain"``\ ) while for all other the qubit number is higher
* ``compiler``\ : ``"qiskit"`` or ``"tket"``
* `compiler_settings`: Optimization level for `"qiskit"` (`0`-`3`), placement for `"tket"` (`lineplacement` or `graphplacement`), exemplary shown:

.. code-block:: python

   from mqt.bench import CompilerSettings, QiskitSettings, TKETSettings

   compiler_settings = CompilerSettings(
       qiskit=QiskitSettings(optimization_level=1),
       tket=TKETSettings(placement="lineplacement"),
   )


* ``gate_set_name``\ : ``"ibm"``\ , ``"rigetti"``\ , ``"ionq"``\ , ``"oqc"``\ , or ``"quantinuum"``
* ``device_name``\ : ``"ibm_washington"``\ , ``"ibm_montreal"``\ , ``"rigetti_aspen_m2"``\ , ``"ionq_harmony"``\ , ``"ionq_aria1"``\ , ``"oqc_lucy"``\ , or ``"quantinuum_h2"``

Hereby, the mappings between shortened ``benchmark_name`` and actual benchmarks are:

.. list-table::
   :header-rows: 1

   * - ``benchmark_name``
     - Actual Benchmark
   * - ``"ae"``
     - Amplitude Estimation (AE)
   * - ``"dj"``
     - Deutsch-Jozsa
   * - ``"grover-noancilla"``
     - Grover's (no ancilla)
   * - ``"grover-v-chain"``
     - Grover's (v-chain)
   * - ``"ghz"``
     - GHZ State
   * - ``"graphstate"``
     - Graph State
   * - ``"portfolioqaoa"``
     - Portfolio Optimization with QAOA
   * - ``"portfoliovqe"``
     - Portfolio Optimization with VQE
   * - ``"qaoa"``
     - Quantum Approximation Optimization Algorithm (QAOA)
   * - ``"qft"``
     - Quantum Fourier Transformation (QFT)
   * - ``"qftentangled"``
     - QFT Entangled
   * - ``"qnn"``
     - Quantum Neural Network (QNN)
   * - ``"qpeexact"``
     - Quantum Phase Estimation (QPE) exact
   * - ``"qpeinexact"``
     - Quantum Phase Estimation (QPE) inexact
   * - ``"qwalk-noancilla"``
     - Quantum Walk (no ancilla)
   * - ``"qwalk-v-chain"``
     - Quantum Walk (v-chain)
   * - ``"random"``
     - Random Quantum Circuit
   * - ``"realamprandom"``
     - Real Amplitudes ansatz with Random Parameters
   * - ``"su2random"``
     - Efficient SU2 ansatz with Random Parameters
   * - ``"twolocalrandom"``
     - Two Local ansatz with Random Parameters
   * - ``"vqe"``
     - Variational Quantum Eigensolver (VQE)
   * - ``"wstate"``
     - W-State
   * - ``"shor"``
     - Shor's
   * - ``"pricingcall"``
     - Pricing Call Option
   * - ``"pricingput"``
     - Pricing Put Option
   * - ``"groundstate"``
     - Ground State
   * - ``"routing"``
     - Routing
   * - ``"tsp"``
     - Travelling Salesman


For example, in order to obtain the *5*\ -qubit Deutsch-Josza benchmark on algorithm level, use the following:

.. code-block:: python

   from mqt.bench import get_benchmark

   qc = get_benchmark("dj", "alg", 5)

Examples can be found in the `docs/source/Quickstart.ipynb <docs/source/Quickstart.ipynb>`_ jupyter notebook.

Locally hosting the MQT Bench Viewer
----------------------------------

Additionally, this python package includes the same webserver used for the hosting of the
`MQT Bench webpage <https://www.cda.cit.tum.de/mqtbench>`_.

After the ``mqt.bench`` Python package is installed via

.. code-block:: console

   (venv) $ pip install mqt.bench

the MQT Bench Viewer can be started from the terminal via

.. code-block:: console

   (venv) $ mqt.bench

This first searches for the most recent version of the benchmark files on GitHub and offers to download them.
Afterwards, the webserver is started locally.

Usage directly via this repository
----------------------------------

For that, the repository must be cloned and installed:

.. code-block::

   git clone https://github.com/cda-tum/MQTBench.git
   cd MQTBench
   pip install .

Afterwards, the package can be used as described `above <#Usage via pip package>`_.
