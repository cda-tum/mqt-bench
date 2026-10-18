---
file_format: mystnb
kernelspec:
  name: python3
mystnb:
  number_source_lines: true
---

```{code-cell} ipython3
:tags: [remove-cell]
%config InlineBackend.figure_formats = ['svg']
```

# Supported Benchmark Algorithms

The current release includes the following benchmark algorithms, with each
abbreviated `benchmark_name` mapped to its full description in the table below:

```{code-cell} ipython3
:tags: [hide-input]
from mqt.bench.benchmarks import get_benchmark_catalog
import pandas as pd
from IPython.display import HTML

df = pd.DataFrame(
    [
        {"Actual Benchmark": desc or name, "benchmark_name": name}
        for name, desc in sorted(get_benchmark_catalog().items())
    ]
)

def dark_even_rows(s):
    return ['background-color:#262626;color:#f8f8f8' if s.name % 2 else '' for _ in s]

html = (
    df.style
      .apply(dark_even_rows, axis=1)                         # zebra rows
      .set_table_styles([
          # index cells in zebra rows
          {'selector': 'tr:nth-child(even) th',
           'props': [('background-color','#262626'),
                     ('color','#f8f8f8')]},

          # entire header row
          {'selector': 'thead th',
           'props': [('background-color','#3b3b3b'),
                     ('color','#f8f8f8')]}
      ], overwrite=False)
      .to_html()
)

HTML(html)
```

See the
[benchmark description](https://www.cda.cit.tum.de/mqtbench/benchmark_description)
for further details on the individual benchmarks.

## Arithmetic results

Adder and multiplier benchmarks measure only the arithmetic output into a
classical register named `result`. Bit `result[0]` is the least-significant bit.

| Benchmarks                                                              | Measured output                                                         |
| ----------------------------------------------------------------------- | ----------------------------------------------------------------------- |
| `full_adder`, `half_adder`                                              | Sum, with carry-out as the most-significant bit                         |
| `modular_adder`                                                         | Sum modulo $2^n$, where $n$ is the input register width                 |
| `cdkm_ripple_carry_adder`, `vbe_ripple_carry_adder`, `draper_qft_adder` | Sum including carry-out for `full`/`half`; sum modulo $2^n$ for `fixed` |
| `multiplier`, `rg_qft_multiplier`, `hrs_cumulative_multiplier`          | Full $2n$-bit product                                                   |

Input registers, carry-in, and helper qubits are not measured. The benchmarks
leave inputs in their default zero state; prepare inputs before the arithmetic
operations to obtain nonzero results. Mirror benchmarks continue to measure all
active qubits to check that the circuit and its inverse return them to zero.
