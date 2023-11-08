Parameter Space
================================================

The ``mqt.bench.get_benchmark`` method has the following signature:

    .. automodule:: mqt.bench.benchmark_generator
        :members: get_benchmark

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

with
    .. automodule:: mqt.bench.benchmark_generator
        :members: CompilerSettings, QiskitSettings, TKETSettings

* ``gate_set_name``\ : ``"ibm"``\ , ``"rigetti"``\ , ``"ionq"``\ , ``"oqc"``\ , or ``"quantinuum"``
* ``device_name``\ : ``"ibm_washington"``\ , ``"ibm_montreal"``\ , ``"rigetti_aspen_m2"``\ , ``"ionq_harmony"``\ , ``"ionq_aria1"``\ , ``"oqc_lucy"``\ , or ``"quantinuum_h2"``

Examples how to use the ``get_benchmark`` method for all four abstraction levels can be found on the :doc:`Quickstart jupyter notebook <Quickstart>`.
