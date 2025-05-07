Supported Benchmark Algorithms
==============================

So far, the following benchmarks are implemented and provided:


* Amplitude Estimation
* Bernstein-Vazirani
* Deutsch-Jozsa
* GHZ State
* Graph State
* Grover's (no ancilla)
* Grover's (v-chain)
* Quantum Fourier Transformation (QFT)
* QFT Entangled
* Quantum Neural Network (QNN)
* Quantum Phase Estimation (QPE) Exact
* Quantum Phase Estimation (QPE) Inexact
* Quantum Walk (no ancilla)
* Quantum Walk (-chain)
* Random Circuit
* Shor's
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
   * - ``"bv"``
     - Bernstein-Vazirani
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
   * - ``"randomcircuit"``
     - Random Quantum Circuit
   * - ``"vqerealamprandom"``
     - Real Amplitudes ansatz with Random Parameters
   * - ``"vqesu2random"``
     - Efficient SU2 ansatz with Random Parameters
   * - ``"vqetwolocalrandom"``
   * - ``"wstate"``
     - W-State
   * - ``"shor"``
     - Shor's

See the `benchmark description <https://www.cda.cit.tum.de/mqtbench/benchmark_description>`_ for further details on the individual benchmarks.
