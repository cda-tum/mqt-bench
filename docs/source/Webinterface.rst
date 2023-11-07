MQT Bench Webinterface
--------------------------------
MQT Bench is hosted at is hosted at `https://www.cda.cit.tum.de/mqtbench/ <https://www.cda.cit.tum.de/mqtbench/>`_.
`\ :raw-html-m2r:`<img src="https://raw.githubusercontent.com/cda-tum/mqtbench/main/img/mqtbench.png" align="center" width="500" >` <https://www.cda.cit.tum.de/mqtbench>`_


Local Usage within Python Package
---------------------------------
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

