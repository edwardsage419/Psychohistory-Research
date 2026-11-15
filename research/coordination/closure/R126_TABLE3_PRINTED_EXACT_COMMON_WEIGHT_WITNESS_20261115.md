# R126 / 05-002: printed-exact common-weight feasibility (2026-11-15)

Baseline main: 42f9c29fbdac502b33b42cf1632765f3db387869. Source: research/R126/R126_FEHR_GAECHTER_2000_ORIGINAL_PGG_COSTLY_PUNISHMENT_TABLE3_SCIENTIFIC_REPORT_2026-10-20.md, published Table 3 transcription. This is an independent arithmetic witness; it does not establish actual session sizes or original aggregation rules.

The prior 4:4:3 witness adjusted hypothetical unrounded session values. A simpler positive **10:9:10** common weight works even when **all twelve displayed session values are treated as exact**, without any invented hidden decimals:

| Column | Numerator / 29 | Weighted mean | Published Mean |
| --- | --- | --- | --- |
| Ten-round no punishment | (10*2.7+9*4.0+10*4.5)/29 | 108/29 = 3.724137931 | 3.7 |
| Ten-round punishment | (10*10.9+9*12.9+10*10.7)/29 | 332.1/29 = 11.451724138 | 11.5 |
| Final-round no punishment | (10*1.3+9*2.3+10*2.0)/29 | 53.7/29 = 1.851724138 | 1.9 |
| Final-round punishment | (10*9.8+9*14.3+10*13.1)/29 | 357.7/29 = 12.334482759 | 12.3 |

Each is strictly inside the ordinary nearest-tenth interval, with no tie ambiguity. Reproduce using Python standard library:

```python
from fractions import Fraction as F
w = (10, 9, 10)
columns = [('2.7','4.0','4.5'), ('10.9','12.9','10.7'), ('1.3','2.3','2.0'), ('9.8','14.3','13.1')]
targets = ('3.7','11.5','1.9','12.3')
for c,t in zip(columns,targets):
    v = sum(F(n)*F(x) for n,x in zip(w,c))/sum(w)
    assert abs(v-F(t)) < F(1,20)
    print(v, float(v))
```

**Boundary:** 10:9:10 is a synthetic mathematical witness, not an inferred experimental session sample size. It does not establish whether the original authors used participant weighting, group weighting or another calculation. Source-level denominators and aggregation notes remain UNKNOWN. No new E2/E3, original-person data, or scientific closure. R126 bounded E1 and itemwise ACTIVE/provisional unchanged. This strengthens the feasibility result without modifying frozen research code or running CI. New itemwise closures: 0; cost: 0.
