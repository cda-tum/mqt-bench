from pytket.passes import auto_rebase_pass
from pytket import OpType

def get_ionq_rebase():
    ionq_rebase = auto_rebase_pass({OpType.Rz, OpType.Ry, OpType.Rx, OpType.XXPhase, OpType.Measure})
    return ionq_rebase


def get_oqc_rebase():
    oqc_rebase = auto_rebase_pass({OpType.Rz, OpType.SX, OpType.X, OpType.ECR, OpType.Measure})
    return oqc_rebase


def get_rigetti_rebase():
    rigetti_rebase = auto_rebase_pass({OpType.Rz, OpType.Rx, OpType.CZ, OpType.Measure})
    return rigetti_rebase


def get_ibm_rebase():
    ibm_rebase = auto_rebase_pass({OpType.Rz, OpType.SX, OpType.X, OpType.CX, OpType.Measure})
    return ibm_rebase