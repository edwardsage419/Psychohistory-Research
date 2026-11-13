# R183 Fisher exact null, independent 15-world rational audit

Date: 2026-11-13. Track: closure. Scope: postfreeze internal artificial E1, independent arithmetic verification only.

Source: main candidate f267eb660fb4e81fb9b788d87816ec57db1784f3, research R183 Fisher exact report and JSON in that commit. Original frozen R183 acceptance remains unchanged. This independent script uses Python stdlib Fraction and comb; it does not import R183's implementation. It enumerates all 1375 ordered count pairs across n=4,8,12, reconstructs the probability-ordered two-sided Fisher reference distribution and independently weights rejections by five source count distributions at p=1/4.

Run with Python 3: save the fenced script as r183_independent.py and execute python r183_independent.py. Executed in the assistant's isolated Python environment on 2026-11-13; all 15 rational outputs below were observed.

| n | mechanism | exact rejection probability | percentage |
|---|---|---|---|
| 4 | IID | 81/32768 | 0.247192 |
| 4 | BB2 | 441/8192 | 5.383301 |
| 4 | BB8 | 7/605 | 1.157025 |
| 4 | ZIB8 | 484/117649 | 0.411393 |
| 4 | ZIB4 | 43/5832 | 0.737311 |
| 8 | IID | 17107929/2147483648 | 0.796650 |
| 8 | BB2 | 94226561/536870912 | 17.551065 |
| 8 | BB8 | 16388/306735 | 5.342723 |
| 8 | ZIB8 | 1809741632/96889010407 | 1.867850 |
| 8 | ZIB4 | 1573963/38263752 | 4.113457 |
| 12 | IID | 2126320497459/140737488355328 | 1.510842 |
| 12 | BB2 | 2459701310851/8796093022208 | 27.963566 |
| 12 | BB8 | 1904585/17631601 | 10.802110 |
| 12 | ZIB8 | 254829350188866624/3909821048582988049 | 6.517673 |
| 12 | ZIB4 | 12434515993/83682825624 | 14.859101 |

All displayed percentages agree with the R183 source report at six decimal places. This verifies the full 15-world Fisher false-positive table independently, extending earlier checks limited to a subset of worlds. It does not independently verify the report's oracle-calibrated control, original R177 source pin, 13 unit tests, or historical dataset and freeze protocol. No real-human E2, historical E3, external-team replication, or scientific queue closure is claimed.

Reproduction code:

```python
from fractions import Fraction as Q
from math import comb

def rising(x, n):
    v = Q(1)
    for i in range(n):
        v *= x + i
    return v

def source(n, kind):
    p = Q(1, 4)
    if kind == "IID":
        return [Q(comb(n,k))*p**k*(1-p)**(n-k) for k in range(n+1)]
    if kind.startswith("BB"):
        c = Q(int(kind[2:]))
        return [Q(comb(n,k))*rising(p*c,k)*rising((1-p)*c,n-k)/rising(c,n) for k in range(n+1)]
    z = Q(1, int(kind[3:]))
    q = p/(1-z)
    return [z*(k==0)+(1-z)*comb(n,k)*q**k*(1-q)**(n-k) for k in range(n+1)]

def fisher(n, a, b):
    s = a+b
    weights = {j: Q(comb(n,j)*comb(n,s-j),comb(2*n,s))
               for j in range(max(0,s-n),min(n,s)+1)}
    return sum((v for v in weights.values() if v <= weights[a]),Q(0))

for n in (4,8,12):
    rejected = [(a,b) for a in range(n+1) for b in range(n+1)
                if fisher(n,a,b) <= Q(1,20)]
    for kind in ("IID","BB2","BB8","ZIB8","ZIB4"):
        p = source(n,kind)
        assert sum(p) == 1
        rate = sum((p[a]*p[b] for a,b in rejected),Q(0))
        print(n,kind,rate,f"{float(rate)*100:.6f}%")
```

Status: COMPLETE_BOUNDED_INTERNAL_E1_ARITHMETIC. Scientific closure: unchanged. CI: NOT_RUN. Additional spending: zero. No source/freeze changes.

Next: independently verify the 15 oracle null tail probabilities and source identity against frozen R177/R183; then address itemwise provisional acceptance evidence.
