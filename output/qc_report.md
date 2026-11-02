# QC Report

**FAIL: 2 · WARN: 3**

| Scope | Status | i18n | layout | images | pdf | mode | content |
|---|---|---|---|---|---|---|---|
| `_global` | **PASS** | PASS | PASS | PASS | PASS | PASS | PASS |
| `vertical_lines` | **PASS** | PASS | PASS | PASS | PASS | PASS | PASS |
| `vertical_lines@space` | **FAIL** | PASS | PASS | FAIL | WARN | PASS | PASS |

## `_global` — PASS
- **i18n**: PASS
- **layout**: PASS
- **images**: PASS
- **pdf**: PASS
- **mode**: PASS
- **content**: PASS

## `vertical_lines` — PASS
- **i18n**: PASS
- **layout**: PASS
- **images**: PASS
- **pdf**: PASS
- **mode**: PASS
- **content**: PASS

## `vertical_lines@space` — FAIL
- **i18n**: PASS
- **layout**: PASS
- **images**: FAIL
  - [FAIL] 'icon_pencil.png' resolusi 96x96 terlalu kecil _(…id/bw, id/color)_
  - [WARN] 10 gambar masih placeholder: balloon, cloud, cupcake, flame, flower_head, grass_tuft, … (+4) _(…id/bw, id/color)_
- **pdf**: WARN
  - [WARN] Ukuran file 10.5 MB cukup besar _(…id/color)_
- **mode**: PASS
- **content**: PASS
