# R133 / original 239 item 05-009: independent exact arithmetic closure audit

Date: 2026-11-13. Track: independent closure audit. Start main: `dc713b48c9dfcd1d75cc2d157aa06d87ad504d67`.

## Fixed source identity and scope

R133 final acceptance Git blob `70d36423e87eca9a14f7b6f9f18177e66c9116d5`; phase A receipt blob `b91625e942a583051c21ad442ba45bc073c138ed`; original research report blob `da878d919956c56d5be60a4c010bb2a9a61044e9`. Catalogue ID 05-009, priority P2. Original source: Maynard Smith & Price (1973), *Nature* 246, 15–18, DOI 10.1038/246015a0. Historical report says original printed pages 16 and 17 were read; this audit did not independently inspect the scanned article. Historical CI run 39368129476, SHA `a2c0ee1f5953de0fdce3b4fd0e62afa85a02d5bd`, two 36-test jobs: receipt claims only, not independently rerun here.

## Independent calculation

Executed Python standard-library Fraction enumeration across all 625 integer payoff matrices with a,b,c,d in {-2,-1,0,1,2}. Pure A ESS iff a>c or (a=c and b>d); pure B iff d>b or (d=b and c>a). Interior Nash candidate x=-(b-d)/(a-b-c+d) with 0<x<1; strict interior ESS iff additionally a-b-c+d<0.

Observed counts: pure A 300, pure B 300, both pure 100, interior Nash 200, strict interior ESS 100, no strict ESS 25. All six counts equal the fixed R133 receipt.

Independently evaluated the project-constructed symmetric three-strategy matrix A=[[-1,-3,4],[-3,-1,4],[4,4,-8]], resident p=(1/3,1/3,1/3). For q=e1,e2,e3 and q=(1/2,1/6,1/3), calculated D0=(p-q)^T A p and D1=-(p-q)^T A(p-q) with Fraction. Results (D0,D1)=(0,1),(0,1),(0,8),(0,-1/9). This confirms a counterexample to pure-mutant-only ESS screening in this constructed setting.

## Reproduction command

```python
from fractions import Fraction as F
from itertools import product
counts=[0]*6
for a,b,c,d in product(range(-2,3),repeat=4):
    pure_a=a>c or (a==c and b>d)
    pure_b=d>b or (d==b and c>a)
    alpha=a-b-c+d
    interior=alpha!=0 and 0<F(d-b,alpha)<1
    mixed=interior and alpha<0
    for i,v in enumerate((pure_a,pure_b,pure_a and pure_b,interior,mixed,not(pure_a or pure_b or mixed))):
        counts[i]+=int(v)
assert counts==[300,300,100,200,100,25],counts
A=[[-1,-3,4],[-3,-1,4],[4,4,-8]]
p=[F(1,3)]*3
qs=[[F(1),F(0),F(0)],[F(0),F(1),F(0)],[F(0),F(0),F(1)],[F(1,2),F(1,6),F(1,3)]]
results=[]
for q in qs:
    v=[p[i]-q[i] for i in range(3)]
    d0=sum(v[i]*sum(A[i][j]*p[j] for j in range(3)) for i in range(3))
    d1=-sum(v[i]*sum(A[i][j]*v[j] for j in range(3)) for i in range(3))
    results.append((d0,d1))
assert results==[(0,F(1)),(0,F(1)),(0,F(8)),(0,F(-1,9))],results
print(counts,results)
```

## Scientific boundaries and itemwise disposition

Independent exact mathematical replay passed; evidence is synthetic/mathematical E1 scope only. This run did not unpack or natively execute the R133 ZIP, verify its SHA256, inspect CI logs, reproduce original 1973 random simulation, or obtain human/animal observations. The printed 1973 payoff table has rounding uncertainty. Existing R133 CLOSED_BOUNDED remains unchanged. Catalogue item 05-009 remains provisional pending full itemwise source and provenance adjudication. E2/E3 additions 0; formal new closures 0. Do not interpret six overlapping category counts as a partition. R073 and PESEN v0.1 frozen. No CI dispatched and no paid service used.

Next: verify historical CI job identity and three archived file hashes against immutable bytes; then reconcile itemwise catalogue status with the formal bounded acceptance and explicit missing original simulation evidence.
