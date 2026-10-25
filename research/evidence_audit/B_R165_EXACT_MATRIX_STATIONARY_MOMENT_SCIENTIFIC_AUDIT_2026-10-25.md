# B independent method audit: R165 stationary moments and temporal covariance

Date: 2026-10-25 Asia/Singapore. B method audit of the preregistered R165 E1 extension. Original R165 acceptance and frozen model unchanged.

## Preregistered target and method separation

Prospective freeze: `protocols/R165_HETEROZYGOSITY_RECURSION_AND_AUTOCOV_THIRD_METHOD_FREEZE_2026-10-25.md`, commit `c9f670ba2ca603a69f3e4cc9f648233b6b1d7420`.

R main independently generated all moment expectations from a scalar algebraic Fraction recursion. This B implementation separately consumed the **original frozen** `research/R165/R165_EXACT_RESULTS.json`, Git blob `8b8a7ca5b6a1d75b3f8464e0eeb1b7b180e4ccf3`, and used BigInt exact rational sums over full state distributions and explicit powers of the original Markov transition matrices. It does not import the R extension implementation or its output.

The archived JavaScript function was retrieved back from GitHub after commit, then evaluated against the GitHub-fetched original source JSON. The executed archived JS blob is `ce9a318d79afaacd9d45dafd8c0f5c27eb698d00`. This is a **same-project alternative-method replay**, not an external independent team replication.

## Actual checks and results

| Check | Executed and passed |
| --- | ---: |
| Distinct original transition kernels | 12 |
| Exact stochastic row normalizations | 84 |
| Positive-mu stationary distributions, including full balance | 9 |
| Frozen world-time distributions and diversity | 240 |
| Frozen successive diversity transitions | 192 |
| Zero-innovation decay points | 60 |
| Direct stationary diversity vs scalar formula | 9 |
| Stationary covariance via exact matrix powers, lags 1, 2, 4 | 27 |
| Actual finite-sampling-factor omission discrepancies | 168 |
| Actual incorrect linear-mu discrepancies | 126 |

No tolerance was used. Every comparison was rational equality. Zero discrepancy conditions in the negative controls were retained and not counted as detections.

Examples: for N=4 and mu=1/16, stationary diversity is exactly 93/698 and stationary lag-1 covariance is 60/349. For N=8 and mu=1/4, stationary diversity is 49/130 and lag-4 covariance is 81/4160. The complete nine-condition table and 48-world H0/H4 receipt are in `research/validation/R165_MOMENT_EXTENSION_COMPACT_EXACT_RECEIPT_2026-10-25.json`.

## Scientific evidence audit

* Leakage: no train/test split exists in this finite algebraic E1 calculation. It provides no leakage-controlled E2 or E3 test.
* Baselines: zero-innovation neutral drift is present as an algebraic boundary. No empirical alternative fitness, selection or social influence model was evaluated.
* Sample independence: 48 artificial parameter worlds are not 48 independently sampled human populations.
* Calibration and scoring: no empirical predictive probabilities were scored or calibrated.
* Uncertainty: exact fractions eliminate numerical approximation error for the frozen finite model. They do not estimate parameter, sampling-design or historical measurement uncertainty.
* Negative controls: two erroneous formulas were actually evaluated, with 168 and 126 mismatches across the 192 transitions.
* Causal and historical scope: no individual imitation network, newly invented name category, external birth-name dataset or real human behavioural trial was used. The original R165 two-token model cannot reproduce a multi-variant cultural tail.

Decision: `PASS_BOUNDED_INTERNAL_E1`. The new formula and exact frozen-kernel replay are internally consistent. E2=0; E3=0; independent external replication=0. R073 and PESEN v0.1 remain frozen. Original239 v7.8 and the 154-item scientific triage queue remain unchanged.

No Actions were started; new remote CI is `NOT_RUN`. No added charges were incurred through the performed checks. Billing account not directly inspected.
