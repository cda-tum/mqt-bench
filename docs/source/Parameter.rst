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