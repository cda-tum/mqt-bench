Supported Benchmark Algorithms
==============================

So far, the following benchmarks are implemented and provided:


* Amplitude Estimation
* Deutsch-Jozsa
* GHZ State
* Graph State
* Ground State
* Grover's (no ancilla)
* Grover's (v-chain)
* Portfolio Optimization with QAOA
* Portfolio Optimization with VQE
* Pricing Call Option
* Pricing Put Option
* Quantum Fourier Transformation (QFT)
* QFT Entangled
* Quantum Neural Network (QNN)
* Quantum Phase Estimation (QPE) Exact
* Quantum Phase Estimation (QPE) Inexact
* Quantum Walk (no ancilla)
* Quantum Walk (-chain)
* Random Circuit
* Routing
* Shor's
* Travelling Salesman
* Variational Quantum Eigensolver (VQE)
* VQE-ansätze with random values:
  * Efficient SU2 ansatz with Random Parameters
  * Real Amplitudes ansatz with Random Parameters
  * Two Local ansatz with Random Parameters
* W-State

The attached mappings between shortened ``benchmark_name`` parameter and actual benchmarks are:

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

See the `benchmark description <https://www.cda.cit.tum.de/mqtbench/benchmark_description>`_ for further details on the individual benchmarks.
