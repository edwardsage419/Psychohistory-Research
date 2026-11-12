# R134 / original 05-010: independent numerical receipt consistency audit

Date: 2026-11-13. Track: closure independent audit. Source main: `a057f0133b66bbecb18e1d7f10810e1db91db02e`.
Source: `research/R134/R134_FINAL_ACCEPTANCE_STATUS.json`, blob `804a0fe71d404376d7bef1fcdc205a1c17edd1d3`.
Scope: four published final-state pairs and the stated invariant `H=x(1-x)y(1-y)`, reference `16/625`. This is an independent receipt arithmetic check, not a rerun of R134 dynamics, 34,992 exact comparisons, or original Taylor 1979 code.

Independent computation: using Python 3 standard arithmetic only, evaluate `h=x*(1-x)*y*(1-y)` and `h-16/625` from the four JSON coordinate pairs. No import from R134.

| steps | recalculated H | recalculated H minus 16/625 | claimed error | difference from claim |
| --- | --- | --- | --- | --- |
| 40 | 0.025607380178163441 | 7.3801781634401376e-06 | 7.3801781634401376e-06 | 0 |
| 80 | 0.02560025414283772 | 2.5414283771896251e-07 | 2.5414283771896251e-07 | 0 |
| 160 | 0.025600009260974992 | 9.260974990349391e-09 | 9.260974990349391e-09 | 0 |
| 320 | 0.025600000370765708 | 3.7076570633121086e-10 | 3.7076570633121086e-10 | 0 |

Reproducible check:

```python
from math import log2
rows = [
    (40, .7123424601663905, .1464020638870984, 7.3801781634401376e-6),
    (80, .7123090069907367, .14634064770912364, 2.541428377189625e-7),
    (160, .7123027554654028, .1463366705290539, 9.260974990349391e-9),
    (320, .7123022357580676, .1463364190174172, 3.7076570633121086e-10),
]
for n, x, y, claimed in rows:
    observed = x * (1-x) * y * (1-y) - 16/625
    assert observed == claimed, (n, observed, claimed)
print([log2(rows[i][3]/rows[i+1][3]) for i in range(3)])
```

Observed adjacent error reduction orders are approximately 4.85994, 4.77833, 4.64258. These finite-grid ratios alone do not establish global fourth-order convergence or the correctness of the numerical trajectory. The exact equality here is equality of Python binary floating point results using the published decimals, not an independently established physical invariant.

Conclusion: four internally consistent reported numerical artifacts. Existing R134 `CLOSED_BOUNDED` unchanged. New E1/E2/E3 promotion: 0. Itemwise original-239 `05-010` remains provisional pending complete evidence-scope adjudication. No human/animal prediction or external replication was performed. No CI dispatched; no fee incurred. No R core or frozen protocol modified.
