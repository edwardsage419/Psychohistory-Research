# R126 / 05-002 Table 3: feasible common-weight counterexample (2026-11-15)

Scope: independent arithmetic feasibility check of rounded, published session aggregates. No claim about the original authors' actual weighting or participant records. Existing R126 bounded E1, frozen protocol and itemwise ACTIVE/provisional remain unchanged.

## Source and version

Baseline main at selection: `57de968bd4aad7b3f5690513b14cb8dc92b38915`.
Source transcription: `research/R126/R126_FEHR_GAECHTER_2000_ORIGINAL_PGG_COSTLY_PUNISHMENT_TABLE3_SCIENTIFIC_REPORT_2026-10-20.md`.
Earlier audit: `research/coordination/closure/R126_TABLE3_WEIGHT_EXAMPLE_CROSS_COLUMN_CHECK_20261115.md`.

Published session columns, ordered [ten-round no punishment, ten-round punishment, final-round no punishment, final-round punishment]:

1: [2.7, 10.9, 1.3, 9.8]
2: [4.0, 12.9, 2.3, 14.3]
3: [4.5, 10.7, 2.0, 13.1]
Published Mean: [3.7, 11.5, 1.9, 12.3].

## Constructive feasibility witness

Use one **common** hypothetical positive session-weight vector 4:4:3, and take the displayed session values as exact for three columns. For the ten-round punishment column only, use hypothetical unrounded values [10.87, 12.87, 10.67], which individually round to the published [10.9, 12.9, 10.7] at one decimal place.

The four weighted means are respectively:

* (4*2.7 + 4*4.0 + 3*4.5)/11 = 40.3/11 = 3.663636..., rounds to 3.7.
* (4*10.87 + 4*12.87 + 3*10.67)/11 = 126.97/11 = 11.542727..., rounds to 11.5.
* (4*1.3 + 4*2.3 + 3*2.0)/11 = 20.4/11 = 1.854545..., rounds to 1.9.
* (4*9.8 + 4*14.3 + 3*13.1)/11 = 135.7/11 = 12.336363..., rounds to 12.3.

All four are strictly inside the relevant nearest-tenth rounding intervals, avoiding tie-rule ambiguity. Thus the published four Mean cells **can** coexist with one shared positive session-weight vector and ordinary nearest-tenth rounding of underlying session values. This refutes any stronger claim that the four-column table is inherently incompatible with common session weights. It does **not** rehabilitate the earlier illustrative 5:4:5 weights, which fail their ten-round punishment constraint under the same assumptions.

## Reproducible independent calculation

```python
from fractions import Fraction as F
weights = [4, 4, 3]
columns = [
    ['2.7', '4.0', '4.5'],
    ['10.87', '12.87', '10.67'],
    ['1.3', '2.3', '2.0'],
    ['9.8', '14.3', '13.1'],
]
targets = ['3.7', '11.5', '1.9', '12.3']
for column, target in zip(columns, targets):
    mean = sum(F(w) * F(x) for w, x in zip(weights, column)) / sum(weights)
    assert abs(mean - F(target)) < F(1, 20), (mean, target)
    print(float(mean), target)
```

Expected values: 3.663636..., 11.542727..., 1.854545..., 12.336363....

## Evidence limits and next gate

Weights 4:4:3 and the unrounded values are **synthetic witnesses**, not historical session sizes or observed participant data. The actual weighting, sample denominators, rounding rule and published Table 3 notes remain UNKNOWN. No original individual data, new E2/E3, independent historical reconstruction or scientific closure is established. The original printed 12.3 must remain unchanged. A source-level check of session sizes and aggregation notes is needed before attributing a real explanation. This independent feasibility check does not alter the frozen model or mathematical implementation.

New itemwise scientific closures: 0. E-level upgrades: 0. CI: not triggered. No paid resources.
