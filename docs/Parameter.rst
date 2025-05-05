Parameter Space
===============

The ``mqt.bench.get_benchmark`` method has the following signature:

    .. automodule:: mqt.bench.benchmark_generator
        :no-index:
        :members: get_benchmark

* ``benchmark_name`` (see :doc:`details <Benchmark_selection>`) \ : ``"ae"``\ , ``"bv"``\ , ``"dj"``\ , ``"grover-noancilla"``\ , ``"grover-v-chain"``\ , ``"ghz"``\ , ``"graphstate"``\ ,
  ``"qaoa"``\ , ``"qft"``\ , ``"qftentangled"``\ , ``"qnn"``\ , ``"qpeexact"``\ , ``"qpeinexact"``\ ,
  ``"qwalk-noancilla"``\ , ``"qwalk-v-chain"``\ , ``"randomcircuit"``\ , ``"vqerealamprandom"``\ , ``"vqesu2random"``\ , ``"vqetwolocalrandom"``\ ,
  ``"wstate"``\ , ``"shor"``\
* ``level``\ : ``0`` or ``"alg"``\ , ``1`` or ``"indep"``\ , ``2`` or ``"nativegates"``\ , ``3`` or ``"mapped"``
* ``circuit_size``\ : for most of the cases this is equal to number of qubits
  (all scalable benchmarks except ``"qwalk-v-chain"`` and ``"grover-v-chain"``\ ) while for all other the qubit number is higher
* ``compiler_settings``: Optimization level for ``"qiskit"`` (``0``-``3``), exemplary shown:

.. code-block:: python

   from mqt.bench import CompilerSettings, QiskitSettings

   compiler_settings = CompilerSettings(
       qiskit=QiskitSettings(optimization_level=1),
   )

with
    .. automodule:: mqt.bench.benchmark_generator
        :members: CompilerSettings, QiskitSettings

* ``gateset``\ : ``"ibm_falcon"``\ , ``"ibm_heron_r1"``\ , ``"rigetti"``\ , ``"ionq"``\ , ``"iqm"``\ , ``"oqc"``\ , or ``"quantinuum"`` (required for "nativegates" level)
* ``device_name``\ : ``"ibm_washington"``\ , ``"ibm_montreal"``\ , ``"rigetti_aspen_m3"``\ , ``"ionq_harmony"``\ , ``"ionq_aria1"``\ , ``"oqc_lucy"``\ , or ``"quantinuum_h2"`` (required for "mapped" level)

Quantum Circuit Compiler Support
--------------------------------

At the moment, one compiler is supported:


#. `Qiskit <https://qiskit.org/documentation/>`_ with the compiler settings: Optimization level 0 to 3

Native Gate-Set Support
-----------------------

So far, MQT Bench supports the following native gatesets:

.. jupyter-execute::
   :hide-code:

    from mqt.bench.devices import get_available_native_gatesets

    for num, gateset in enumerate(get_available_native_gatesets()):
        print(str(num + 1) + ":", gateset.name, ": ", gateset.gates)

Device Support
--------------

So far, MQT Bench supports the following devices:

.. jupyter-execute::
   :hide-code:

    from mqt.bench.devices import get_available_devices

    for num, device in enumerate(get_available_devices()):
        print(str(num + 1) + ":", device.name, "with", device.num_qubits, "qubits")


Examples how to use the ``get_benchmark`` method for all four abstraction levels can be found on the :doc:`Quickstart jupyter notebook <Quickstart>`.
