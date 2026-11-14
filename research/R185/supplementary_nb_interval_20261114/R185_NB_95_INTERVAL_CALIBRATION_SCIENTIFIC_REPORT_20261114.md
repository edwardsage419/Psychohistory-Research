# R185 postfreeze: Negative binomial prediction intervals, structural-zero failure, and expected interval score

**Date:** 2026-11-14. **Research track:** manual R-series, 08-009 Negative Binomial Regression. **Scope:** bounded new synthetic mathematical E1 audit. **Scientific status:** COMPLETE_BOUNDED_E1_POSTFREEZE_DIAGNOSTIC; historical R185 acceptance remains unchanged.

## Provenance and overlap exclusion

Last independently observed repository main before calculation: `02117f08214c00ca74f2f2185a32decbf50448dd` (2026-11-14 03:35:30 UTC). Original source files already present:

* R177 `research/R177/R177_EXACT_RESULTS.json` Git blob `8a8819e4d85989b518b9152cfc98336457c76a9c`, original R177 generating script Git blob `2d032513ce84141214b6b3f84df9c0ed9976a02b`.
* R185 `research/R185/R185_EXACT_RESULTS.json` Git blob `857dcb286bf66692952930fc736e133bc3d2b3aa`.
* R184 postfreeze 95% Poisson interval control `research/R184/supplementary_oracle_prediction_interval_20261114/R184_45_ORACLE_POISSON_INTERVAL_RESULTS_20261114.json`, blob `349e5a9cf5286c2a95a78d6f42011c7bcdd9638e`.
* R185 original frozen protocol `protocols/R185_NEGATIVE_BINOMIAL_135_WORLDS_PRESCORE_FREEZE_2026-10-21.md`; original final acceptance remains `CLOSED_BOUNDED_E1_ARTIFICIAL_EXACT_NEGATIVE_BINOMIAL`.
* R185 previous postfreeze experiment `research/validation/R185_ZERO_EVENT_NB_POISSON_270_SCIENTIFIC_REPORT_2026-10-26.md` compared binary **zero-event Brier** only. This research evaluates **full-count 95% central prediction interval coverage plus interval score**, a different observable.

The artificial count laws and shapes are inherited without parameter search. No original prescore file, source datum, acceptance receipt or frozen model was edited. The 45 distinct marginal designs arise from `n in [4,8,12]`, `p in [1/8,1/4,1/2]`, and five mechanisms BIN, BB(c=2), BB(c=8), ZIB(z=1/8), ZIB(z=1/4). Each marginal has one independent future count Y from the same law, **not** n independently scored test people. The 45 marginals correspond to the 135 original shape/source combinations, while the original 135 two-group full training worlds have 270 marginal records with repeated conditions. These are 45 artificial designs, not 45 independent experiments.

## Precise mathematical definitions

For source random count `K in {0,...,n}`, true mean `mu=np`, source generating law `Q`, and fixed negative binomial shape `r`:

`P_NB(Y=y | mu,r) = C(y+r-1,y) [r/(r+mu)]^r [mu/(r+mu)]^y`, `y>=0`.

We also use `P_Pois(Y=y|mu) = exp(-mu) mu^y/y!`. Both forecast families use the **true artificial mean**, a privileged oracle information condition; the original R185 trained predictor `lambda=K_train+1/2` is not re-scored.

For both models, central equal-tail nominal 95% interval `[L,U]` is defined by smallest nonnegative integers with `CDF(L)>=1/40` and `CDF(U)>=39/40`. Do not silently optimize interval endpoints against true test probability. Model-assumed 95% coverage follows from the defined quantiles. Actual coverage is `sum_{y=L}^U Q(y)` and can be below 95%.

All NB conditional count PMFs and quantiles are calculated exactly by two disjoint Fraction algorithms: closed generalized combinations and recursion from `P0`. Poisson CDF comparisons have **independent rigorous Fraction bounds**: `S_64(mu)<=exp(mu)<=S_64(mu)+a_65/[1-mu/66]` for `mu<=6`, where `S_64 = sum_{j=0}^64 mu^j/j!`, `a_65=mu^65/65!`. Therefore `S_k / upper_exp <= CDF_Pois(k) <= S_k / lower_exp`. Both boundaries and their preceding counts are certified strictly against `1/40,39/40`. Additional 80- and 110-digit Decimal evaluations are diagnostics only.

To prevent treating unnecessarily wider intervals as automatically better forecasts, we independently compute the negatively oriented **interval score**, where smaller values are preferred:

`S_(alpha)(L,U;y)=(U-L)+(2/alpha)*(L-y)*1[y<L]+(2/alpha)*(y-U)*1[y>U]`, `alpha=1/20`, hence out-of-interval distance penalty multiplier 40. One algorithm directly enumerates every true y and its Fraction mass; the second uses only exact lower/upper tail probabilities and first partial moments. All 135 scores have exact parity. We retain the true-law oracle interval only as an artificial information benchmark.

Primary scoring source: Gneiting, T. and Raftery, A. E. (2007), *Strictly Proper Scoring Rules, Prediction, and Estimation*, JASA 102(477), p.370, §6.2, Eq.(43), DOI `10.1198/016214506000001437`. First-party author manuscript https://sites.stat.washington.edu/raftery/Research/PDF/Gneiting2007jasa.pdf . Original page 370 was visually checked for Eq.(43). This source is a scoring-rule theorem, not empirical evidence for the R185 synthetic source family.

## All 135 comparisons, full grid retained

| NB fixed r | NB true coverage under 95% | Poisson undercoverage eliminated | NB wider than Poisson | NB lower expected interval score | NB higher expected interval score | Score tied | Mean added integer-count width |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 2 | 2/45 | 12 | 45/45 | 12 | 33 | 0 | 3.0000 |
| 6 | 8/45 | 6 | 40/45 | 16 | 24 | 5 | 1.4444 |
| 8 | 8/45 | 6 | 40/45 | 16 | 24 | 5 | 1.3333 |

For the same 45 distinct artificial laws, the Poisson model had 14/45 undercoverage. All fixed-shape NB intervals in this grid have coverage at least as high as the corresponding Poisson intervals, because their `[L,U]` are supersets or equal, **but this is a specific grid result, not a universal property of NB intervals**. Coverage is a property of both model and source. Increased interval width can worsen a proper scoring metric even as coverage improves. The r=2 case increases interval cardinality by 3 positions on average, improving interval score on only 12/45 sources, worsening it on 33/45; r=6 and 8 each improve 16/45, worsen 24/45 and tie on 5/45.

## New failure counterexample: latent zero mass excluded by the model interval

For `n=12`, `p=1/2`, `ZIB(z=1/4)`, source mean is 6. Source probability of K=0 is strictly above 1/4 because there is structural inactivity in addition to occasional active zero counts. Prediction intervals:

* Oracle Poisson mean=6: `[2,11]`; true coverage `131830/177147 = 74.418421%`.
* NB(mean=6,r=6): `[1,14]`; true coverage `132860/177147 = 74.999859%`.
* NB(mean=6,r=8): `[1,13]`; true coverage is the same `132860/177147` since the true source cannot exceed n=12.
* True Q-quantile interval: `[0,11]`, has coverage at least 95% by exact source construction.

Both fixed NB intervals exclude all Y=0 outcomes, accounting for the large loss of source coverage. Extending the upper endpoint from 11 to 14 does not repair this lower-tail error. Their expected interval scores are `4074391/177147` (r=6) and `3897244/177147` (r=8). Even the increased 75% coverage remains far below nominal.

The strongest observed NB r=2 failure is `n=12,p=1/8,BB(c=2)`: interval `[0,6]`, true coverage `8021048037/8589934592 = 93.377289%`, despite being wider than corresponding Poisson interval `[0,4]`.

## Matched mean and variance, different distributional calibration

The original prescored R185 alias remains intact: `n=8,p=1/4` for `BB(c=8)` and `ZIB(z=1/4)` both have exact mean 2, variance 8/3, thus the same moment-implied shape r=6. Forecast `NB(2,6)` gives interval `[0,6]` for both, but their **actual** coverages differ:

* True BB(c=8): `2126/2145 = 99.114219%`; oracle source interval `[0,6]`.
* True ZIB(z=1/4): `8731/8748 = 99.805670%`; oracle source interval `[0,5]`.

Mean and variance matching does not identify the full source distribution, its true quantiles, or the realized proper interval score. This supplements the existing R185 same-moment/different-zero-probability result with a new full-count predictive implication.

## Independent cross-audit and execution status

The 45 canonical source PMF rows were read directly from the archived `R177_EXACT_RESULTS.json` fixed Git blob above. The ordered canonical `n|p|family|regime|PMF` identity string (4,946 UTF-8 bytes) gave `FNV1a64 = 3c59eec04a66770d`. The newly implemented independent Fraction source-formula path generates **exactly the same digest and byte length**; a separately coded stepwise-event DP produces all 45 identical PMFs. This FNV is a deterministic comparison checksum, not cryptographic provenance; the referenced Git blob SHA anchors the original archive identity.

Tests were run locally in both `python` and `python -O`; test methods use unittest assertion functions and all core validations use explicit exceptions. Machine result JSON is byte-identical in the two modes. No GitHub Actions have been triggered. This postfreeze proof is an E1 internal synthetic method test and cannot upgrade historic R185 acceptance or imply empirical calibration on real-human/historical count data. **Real human E2 added=0, external historical E3 added=0, outside team replication=0.** R073 and PESEN v0.1 remain frozen. No additional paid resources.

## Next scientific gate

Prioritize actual original239 itemwise source-and-acceptance disposition with R127/R132 engineering evidence delegated to existing tracks. A future independent empirical count dataset with enough independent groups and public source identity is required before promoting prediction interval calibration beyond synthetic E1. For real data, count the actual independent exposure/cluster unit, reserve a genuinely held-out period or independent cluster and compare coverage and proper interval scores against Poisson/NB and nonparametric baselines without retrospective threshold selection.
