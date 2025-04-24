Repository Usage
================
There are three ways how to use this benchmark suite:


#. Via the webpage hosted at `https://www.cda.cit.tum.de/mqtbench/ <https://www.cda.cit.tum.de/mqtbench/>`_
#. Via the pip package ``mqt.bench``
#. Directly via this repository

Since the first way is rather self-explanatory, the other two ways are explained in more detail in the following.

.. _pip_usage:

Usage via pip package
---------------------

MQT Bench is available via `PyPI <https://pypi.org/project/mqt.bench/>`_

.. code-block:: console

   (venv) $ pip install mqt.bench

To generate a benchmark circuit, use the ``get_benchmark`` method:

    .. automodule:: mqt.bench.benchmark_generator
        :members: get_benchmark
        :no-index:

The available parameters are described on the :doc:`parameter space description page <Parameter>` and the algorithms are described on the :doc:`algorithm page <Benchmark_selection>`.
For example, in order to obtain the *5*\ -qubit Deutsch-Josza benchmark on algorithm level, use the following:

.. code-block:: python

   from mqt.bench import get_benchmark

   qc = get_benchmark("dj", "alg", 5)

Examples can be found in the `docs/Quickstart.ipynb <docs/Quickstart.ipynb>`_ jupyter notebook.


Usage directly via this repository
----------------------------------

For that, the repository must be cloned and installed:

.. code-block::

   git clone https://github.com/munich-quantum-toolkit/bench.git mqt-bench
   cd mqt-bench
   pip install .

Afterwards, the package can be used as described :ref:`above <pip_usage>`.
