import ghz
import qft

def create_circuit(n: int, include_measurements: bool = True):
    qc = ghz.create_circuit(n, include_measurements=False)
    qc.compose(qft.create_circuit(n, include_measurements), inplace=True)
    qc.name = "qft_entangled"
    return qc