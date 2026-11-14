# R183 / original catalogue 08-007: independent exact logistic null audit

Date: 2026-11-14. Track: closure. Base main: `8e90e950a9da3101508e278819bcce9c3af92019`.
Scope: the two prespecified n=4, p0=p1=1/4 artificial training worlds, IID_BIN and CLUSTERED_BB_C2, from the **original logistic** prescore protocol. This is separate from later Fisher/oracle addenda. Internal independent E1 arithmetic only; no source-code import, no human data, no external replication.

Source identities on base main:
* `protocols/R183_LOGISTIC_SEPARATION_45_WORLDS_PRESCORE_FREEZE_2026-10-21.md` blob `e01003e1899739b42b2ed746f1837b8591e870b6`.
* `research/R183/R183_SCIENTIFIC_REPORT_2026-10-21.md` blob `a091a3b35855d54b1489661324d959469cdeb523`.
* `research/R183/R183_FINAL_MACHINE_ACCEPTANCE.json` blob `145f71b55046985835ff92b53ad66ca799cb14cf`.
* `research/R183/README.md` blob `db5d8c49bd46436637f40a8b1f5bca5f0716bc5e`.
* Original catalogue queue `docs/ORIGINAL_239_PENDING_154_ITEMWISE_EVIDENCE_TRIAGE_QUEUE_2026-10-25.csv` blob `3b96d46b3d88ccafd779a08509c3cfd0e435772f`.

Independent derivation: with one-group edge probability `e=P(K=0)+P(K=n)`, the probability that either of two independent training groups has nonfinite logistic coefficients is `1-(1-e)^2`. The strict opposite-edge complete separation probability is `2 P(K=0)P(K=n)`. For an independent future Bernoulli event of true marginal `p`, Brier risk at prediction `q` is `p(1-q)^2+(1-p)q^2`. Average the two identical groups; calculate each expectation directly from its one-group exact PMF. IID count PMF is binomial. Beta-binomial count PMF is `C(n,k) (a)_k (b)_(n-k)/(a+b)_n` with `a=2p,b=2(1-p)`.

| n=4, p=1/4 | nonfinite MLE | strict complete separation | unshrunk Brier | half-count Brier |
|---|---|---|---|---|
| IID_BIN | 8815/16384 = 53.802490234375% | 81/32768 = 0.2471923828125% | 15/64 = 0.234375 | 11/50 = 0.22 |
| CLUSTERED_BB_C2 | 3255/4096 = 79.4677734375% | 441/8192 = 5.38330078125% | 9/32 = 0.28125 | 1/4 = 0.25 |

All eight independently derived fractions agree with the original report's rounded entries. Reproduction, Python standard library only:

```python
from fractions import Fraction as F
from math import comb

def rising(x, k):
    v = F(1)
    for j in range(k):
        v *= x + j
    return v

def pmf(n, p, kind):
    if kind == "iid":
        return [comb(n, k) * p**k * (1-p)**(n-k) for k in range(n+1)]
    a, b = 2*p, 2*(1-p)
    return [comb(n,k)*rising(a,k)*rising(b,n-k)/rising(a+b,n)
            for k in range(n+1)]

def audit(kind):
    n, p = 4, F(1,4)
    w = pmf(n,p,kind)
    assert sum(w) == 1
    e = w[0]+w[n]
    risk = lambda q: p*(1-q)**2+(1-p)*q*q
    return (1-(1-e)**2, 2*w[0]*w[n],
            sum(w[k]*risk(F(k,n)) for k in range(n+1)),
            sum(w[k]*risk(F(2*k+1,2*n+2)) for k in range(n+1)))

assert audit("iid") == (F(8815,16384),F(81,32768),F(15,64),F(11,50))
assert audit("bb") == (F(3255,4096),F(441,8192),F(9,32),F(1,4))
print("PASS: 8 exact fractions")
```

Scientific disposition: **PARTIAL / E1 internal independent exact arithmetic** for original 08-007 logistic. The 45-world complete enumeration, source R177 SHA256, archived CSV/JSON bytes, native test run, and CI run 39561106676 were reported in original files but **not independently rerun in this audit**. The existing research-level `CLOSED_BOUNDED_E1_ARTIFICIAL_EXACT_LOGISTIC` is preserved. Catalogue-level `PROVISIONAL_PRIMARY_README_LINK` remains ACTIVE pending explicit itemwise closure criteria, original paper coverage and frozen-source/CI verification. No E2/E3, no full catalogue closure, no change to R073/PESEN, no new scientific grade. No paid resources or CI were invoked.
