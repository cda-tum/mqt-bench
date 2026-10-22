# Target models

MQT Bench provides Qiskit `Target` models for native-gate and mapped
compilation. Use `get_device(name)` to select a device model. For native-gate
compilation, use `get_target_for_gateset(name, num_qubits)`.

All gate parameters use radians. All device models include measurement.

| Device                     | Gates                                    | Architecture                              |
| -------------------------- | ---------------------------------------- | ----------------------------------------- |
| `aqt_ibex_12`              | `r`, `rz`, `rxx`                         | 12-qubit IBEX Q1, all-to-all              |
| `ibm_heron_156`            | `id`, `x`, `sx`, `rz`, `cz`              | 156-qubit Heron, heavy-hex                |
| `ibm_heron_156_fractional` | `id`, `x`, `sx`, `rx`, `rz`, `cz`, `rzz` | Heron with fractional gates               |
| `ibm_nighthawk_120`        | `id`, `x`, `sx`, `rz`, `cz`              | 120-qubit Nighthawk, 12-by-10 grid        |
| `ionq_forte_36`            | `gpi`, `gpi2`, `rz`, `rzz`               | 36-qubit Forte, all-to-all                |
| `iqm_crystal_5`            | `r`, `cz`                                | 5-qubit Crystal (IQM Spark)               |
| `iqm_crystal_20`           | `r`, `cz`                                | 20-qubit Crystal (Garnet)                 |
| `iqm_crystal_54`           | `r`, `cz`                                | 54-qubit Crystal (Emerald)                |
| `quantinuum_h2_56`         | `rx`, `ry`, `rz`, `rzz`                  | 56-qubit H2, all-to-all                   |
| `rigetti_cepheus_108`      | fixed `rx`, `rz`, `cz`                   | 108-qubit Cepheus, 12-by-9 grid           |

The Cepheus model uses physical qubit labels 0 through 107.

## Gate parameters

- **IonQ:** GPI and GPI2 take one phase. GPI is `i * R(pi, phase)`; GPI2 is
  `R(pi / 2, phase)`. Forte includes virtual `rz` rotations and uses Qiskit's
  standard `rzz` entangler.
- **Rigetti:** `rxpi`, `rxpidg`, `rxpi2`, and `rxpi2dg` are standard RX gates
  with fixed angles pi, -pi, pi/2, and -pi/2. RZ accepts arbitrary angles.
- **AQT and IQM:** the provider operation `prx` corresponds to Qiskit's `r`.
  AQT's `xx` corresponds to `rxx`.
- **IBM fractional gates:** RX accepts arbitrary angles. RZZ angles must lie in
  `[0, pi/2]`. Bind symbolic parameters before compilation so Qiskit can fold
  RZZ angles into this interval.

See the [parameter guide](parameter.md) for gate-set names and compilation
options. Provider references:
[IonQ native gates](https://docs.ionq.com/features/getting-started-with-native-gates),
[IBM fractional gates](https://quantum.cloud.ibm.com/docs/en/guides/fractional-gates),
and
[Rigetti Cepheus architecture](https://aws.amazon.com/blogs/quantum-computing/amazon-braket-launches-rigetti-cepheus-1-108q-superconducting-device/).
