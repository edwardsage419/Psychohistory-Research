# R183 / 08-007: independent exact 45-world audit

Date: 2026-11-14. Track: closure. Starting observed main commit: `17dd23950efdc88fdfe3c71020ab4c1acae385b7`.

## Sources and frozen scope

* `protocols/R183_LOGISTIC_SEPARATION_45_WORLDS_PRESCORE_FREEZE_2026-10-21.md`, Git blob `e01003e1899739b42b2ed746f1837b8591e870b6`.
* `research/R183/R183_SCIENTIFIC_REPORT_2026-10-21.md`, blob `a091a3b35855d54b1489661324d959469cdeb523`.
* `research/R183/R183_EXACT_RESULTS.json`, blob `81f8fa790f0dea2715d99e1384ec33a6d2cf7a64`.
* `research/R183/R183_FINAL_MACHINE_ACCEPTANCE.json`, blob `145f71b55046985835ff92b53ad66ca799cb14cf`.
* Previous closure `R183_08-007_ORIGINAL_LOGISTIC_NULL_INDEPENDENT_EXACT_AUDIT_20261114.md`, blob `0f75e73f82417f86f3b71cdb6bed64472440db63`. Previous audit covered only 8 fractions for two worlds; this audit expands to all 45.

## Independent computation

An independent JavaScript BigInt rational arithmetic implementation, without importing the audited Python code or using the stored probability arrays as computational inputs, generated the full count PMFs for 45 worlds. World design: n=4,8,12; p0,p1=(1/8,1/4),(1/4,1/2),(1/4,1/4); five fixed IID, beta-binomial and zero-inflated binomial mechanisms. This yields 45 worlds and 4125 ordered training count pairs.

For each n,p and mechanism, compute:

* IID: `C(n,k) p^k (1-p)^(n-k)`.
* Beta-binomial: `C(n,k) (cp)_k (c(1-p))_(n-k) / (c)_n`, with c=2 or 8 and rising factorial.
* Zero inflated: `z 1[k=0] + (1-z) C(n,k) (p/(1-z))^k (1-p/(1-z))^(n-k)`, z=1/8 or 1/4.
* Let `e_x=P(K_x=0)+P(K_x=n)`. Finite two-coefficient logit MLE probability is `(1-e_0)(1-e_1)`; nonfinite is its complement. Strict opposite-edge complete separation probability is `P(K0=0)P(K1=n)+P(K0=n)P(K1=0)`.
* For true marginal p and prediction q, held-out independent Bernoulli Brier risk is `p(1-q)^2+(1-p)q^2`. Calculate its expected value separately for q=k/n and q=(k+1/2)/(n+1), average over the two groups.

All results were calculated as reduced rational numbers with BigInt numerator and denominator, using a separately implemented Euclidean GCD, binomial coefficient, and rising factorial. Each world was checked against the five exact stored result fields and both full source PMF arrays, element by element.

**Observed output:** `worlds=45; count_pairs=4125; exact_field_and_PMF_comparisons=1035; mismatches=0`.

Breakdown: 45×5=225 independent exact probability/Brier comparisons; 2×5×[(4+1)+(8+1)+(12+1)]×3 probability pairs = 810 exact PMF entries; total 1035. This includes the previous eight target fractions but extends coverage to the full prespecified set.

## Evidence limits and disposition

**PARTIAL / internal independent E1 exact arithmetic.** The full stored 45-world PMF and five core exact metrics per world are independently consistent with the frozen formulas. This does not independently re-run the archived Python program, verify the complete 4125-row CSV bytes, reproduce the two numerical logloss pathways, authenticate the R177 source SHA256, or verify historical CI run 39561106676. The audited source JSON itself reports these checks; such self-reports were not upgraded to independent evidence.

Research-level `CLOSED_BOUNDED_E1_ARTIFICIAL_EXACT_LOGISTIC` remains unchanged. Original catalogue 08-007 remains `PROVISIONAL_PRIMARY_README_LINK` pending source identity, native execution, historical CI and itemwise closure criteria. No new E2/E3, no real-human inference, no catalogue closure. No freeze modification, PR merge, CI invocation or paid resource.

Next: independently verify frozen R177 input blob and source result SHA256, inspect native R183 program and archived 4125-row CSV, and check the exact historical CI evidence before deciding whether catalogue-level `CLOSED_BOUNDED` is justified.
