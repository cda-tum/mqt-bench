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