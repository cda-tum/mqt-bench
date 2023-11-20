Parameter Space
===============

The ``mqt.bench.get_benchmark`` method has the following signature:

    .. automodule:: mqt.bench.benchmark_generator
        :no-index:
        :members: get_benchmark

* ``benchmark_name`` (see :doc:`details <Benchmark_selection>`) \ : ``"ae"``\ , ``"dj"``\ , ``"grover-noancilla"``\ , ``"grover-v-chain"``\ , ``"ghz"``\ , ``"graphstate"``\ , ``"portfolioqaoa"``\ ,
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

Quantum Circuit Compiler Support
--------------------------------

At the moment, two compilers are supported:


#. `Qiskit <https://qiskit.org/documentation/>`_ with the compiler settings: Optimization level 0 to 3
#. `TKET <https://cqcl.github.io/tket/pytket/api/>`_ with the compiler settings: Line placement and graph placement

Native Gate-Set Support
-----------------------

So far, MQT Bench supports the following native gate-sets:


#. IBMQ gate-set: *['rz', 'sx', 'x', 'cx', 'measure']*
#. Rigetti gate-set: *['rx', 'rz', 'cz', 'measure']*
#. IonQ gate-set: *['rxx', 'rz', 'ry', 'rx', 'measure']*
#. OQC gate-set: *['rz', 'sx', 'x', 'ecr', 'measure']*
#. Quantinuum gate-set: *['rzz', 'rz', 'ry', 'rx', 'measure']*

Device Support
--------------

So far, MQT Bench supports the following devices:


#. IBMQ Washington with 127 qubits
#. IBMQ Montreal with 27 qubits
#. Rigetti Aspen-M2 with 80 qubits
#. IonQ Harmony with 11 qubits
#. IonQ Aria 1 with 25 qubits
#. OQC Lucy with 8 qubits
#. Quantinuum H2 with 32 qubits


Examples how to use the ``get_benchmark`` method for all four abstraction levels can be found on the :doc:`Quickstart jupyter notebook <Quickstart>`.
