from mqt.bench.devices import IBMProvider
from qiskit.providers.fake_provider import FakeMontreal, FakeMontrealV2


def test_import_v1_backend() -> None:
    """
    Test importing a Qiskit `BackendV1` object.
    """
    backend = FakeMontreal()
    device = IBMProvider.import_qiskit_backend(backend)

    assert device.name == backend.name()
    assert device.num_qubits == backend.configuration().n_qubits
    assert device.coupling_map == [[a, b] for a, b in backend.configuration().coupling_map]
    assert device.basis_gates == backend.configuration().basis_gates


def test_import_v2_backend() -> None:
    """
    Test importing a Qiskit `BackendV2` object.
    """
    backend = FakeMontrealV2()
    device = IBMProvider.import_qiskit_backend(backend)

    assert device.name == backend.name
    assert device.num_qubits == backend.num_qubits
    assert device.coupling_map == backend.coupling_map.get_edges()
    assert device.basis_gates == backend.operation_names


def test_get_ibm_washington_device() -> None:
    """
    Test getting the IBM Washington device.
    """
    device = IBMProvider.get_device("ibm_washington")
    assert device.name == "ibm_washington"
    assert device.num_qubits == 127  # noqa: PLR2004


def test_get_ibmq_montreal_device() -> None:
    """
    Test getting the IBM Montreal device.
    """
    device = IBMProvider.get_device("ibm_montreal")
    assert device.name == "ibm_montreal"
    assert device.num_qubits == 27  # noqa: PLR2004
