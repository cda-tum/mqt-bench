from src.benchmarks import ghz, qft


def create_circuit(n: int):
    qc = ghz.create_circuit(n)
    qc.compose(qft.create_circuit(n), inplace=True)
    qc.name = "qft_entangled"
    return qc