# Copyright (c) 2023 - 2026 Chair for Design Automation, TUM
# Copyright (c) 2025 - 2026 Munich Quantum Software Company GmbH
# All rights reserved.
#
# SPDX-License-Identifier: MIT
#
# Licensed under the MIT License

"""Result measurements of arithmetic benchmarks."""

from __future__ import annotations

import pytest
from qiskit import qasm3
from qiskit.primitives import StatevectorSampler
from qiskit.providers.fake_provider import GenericBackendV2
from qiskit.transpiler import CouplingMap

from mqt.bench import BenchmarkLevel, get_benchmark
from mqt.bench.benchmarks import create_circuit


@pytest.mark.parametrize(
    ("benchmark", "size", "kind", "result_qubits"),
    [
        ("full_adder", 4, None, (2, 3)),
        ("full_adder", 6, None, (3, 4, 5)),
        ("half_adder", 3, None, (1, 2)),
        ("half_adder", 5, None, (2, 3, 4)),
        ("modular_adder", 2, None, (1,)),
        ("modular_adder", 4, None, (2, 3)),
        ("cdkm_ripple_carry_adder", 4, "full", (2, 3)),
        ("cdkm_ripple_carry_adder", 6, "full", (3, 4, 5)),
        ("cdkm_ripple_carry_adder", 4, "half", (1, 2)),
        ("cdkm_ripple_carry_adder", 6, "half", (2, 3, 4)),
        ("cdkm_ripple_carry_adder", 3, "fixed", (1,)),
        ("cdkm_ripple_carry_adder", 5, "fixed", (2, 3)),
        ("vbe_ripple_carry_adder", 4, "full", (2, 3)),
        ("vbe_ripple_carry_adder", 7, "full", (3, 4, 5)),
        ("vbe_ripple_carry_adder", 3, "half", (1, 2)),
        ("vbe_ripple_carry_adder", 6, "half", (2, 3, 4)),
        ("vbe_ripple_carry_adder", 2, "fixed", (1,)),
        ("vbe_ripple_carry_adder", 5, "fixed", (2, 3)),
        ("draper_qft_adder", 3, "half", (1, 2)),
        ("draper_qft_adder", 5, "half", (2, 3, 4)),
        ("draper_qft_adder", 2, "fixed", (1,)),
        ("draper_qft_adder", 4, "fixed", (2, 3)),
        ("multiplier", 4, None, (2, 3)),
        ("multiplier", 8, None, (4, 5, 6, 7)),
        ("rg_qft_multiplier", 4, None, (2, 3)),
        ("rg_qft_multiplier", 8, None, (4, 5, 6, 7)),
        ("hrs_cumulative_multiplier", 5, None, (2, 3)),
        ("hrs_cumulative_multiplier", 9, None, (4, 5, 6, 7)),
    ],
)
def test_arithmetic_results(
    benchmark: str,
    size: int,
    kind: str | None,
    result_qubits: tuple[int, ...],
) -> None:
    """Each variant measures only its result wires in little-endian order."""
    qc = create_circuit(benchmark, size) if kind is None else create_circuit(benchmark, size, kind=kind)
    assert [(reg.name, len(reg)) for reg in qc.cregs] == [("result", len(result_qubits))]
    assert [
        (qc.find_bit(item.qubits[0]).index, qc.find_bit(item.clbits[0]).index)
        for item in qc.data
        if item.operation.name == "measure"
    ] == list(zip(result_qubits, range(len(result_qubits)), strict=True))


@pytest.mark.parametrize(
    ("benchmark", "size", "input_qubits", "expected"),
    [
        ("full_adder", 6, [0, 1, 2, 3], "101"),  # 3 + 1 + carry-in = 5
        ("modular_adder", 4, [0, 1, 2, 3], "10"),  # (3 + 3) mod 4 = 2
        ("rg_qft_multiplier", 8, [1, 3], "0100"),  # 2 * 2 = 4
    ],
)
@pytest.mark.parametrize("level", list(BenchmarkLevel))
def test_compiled_arithmetic_results(
    benchmark: str, size: int, input_qubits: list[int], expected: str, level: BenchmarkLevel
) -> None:
    """The result register and its carry bit survive compilation and QASM3 export."""
    arithmetic = create_circuit(benchmark, size)
    qc = arithmetic.copy_empty_like()
    qc.x(input_qubits)
    qc.compose(arithmetic, inplace=True)
    target = GenericBackendV2(
        size,
        basis_gates=["rz", "sx", "x", "cx"],
        coupling_map=CouplingMap.from_line(size) if level == BenchmarkLevel.MAPPED else None,
        seed=10,
    ).target
    compiled = get_benchmark(qc, level, target=target)
    restored = qasm3.loads(qasm3.dumps(compiled))
    result = StatevectorSampler(seed=10).run([restored], shots=16).result()[0]
    assert result.data["result"].get_counts() == {expected: 16}


def test_arithmetic_mirror_measurements() -> None:
    """Mirror benchmarks still measure all active qubits to check the identity."""
    qc = get_benchmark("full_adder", BenchmarkLevel.ALG, 6, generate_mirror_circuit=True)
    assert qc.num_clbits == 6
    result = StatevectorSampler(seed=10).run([qc], shots=16).result()[0]
    assert result.data["meas"].get_counts() == {"000000": 16}
