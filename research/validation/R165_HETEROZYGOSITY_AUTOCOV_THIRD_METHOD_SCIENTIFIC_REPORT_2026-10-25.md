# R165 third method: exact heterozygosity recursion and stationary memory

Date: 2026-10-25 Asia/Singapore. Track R main. This is a bounded E1 extension. The original R165 `CLOSED_BOUNDED_E1` status and original frozen files are unchanged.

## Prospective protocol and source identity

Protocol was created first at commit `c9f670ba2ca603a69f3e4cc9f648233b6b1d7420`:
`protocols/R165_HETEROZYGOSITY_RECURSION_AND_AUTOCOV_THIRD_METHOD_FREEZE_2026-10-25.md`.

Source: `research/R165/R165_EXACT_RESULTS.json` Git blob `8b8a7ca5b6a1d75b3f8464e0eeb1b7b180e4ccf3`; `research/R165/r165_neutral_drift_exact.py` Git blob `b6baec8fd6f6bbfae2df8945b7aaefaaf565ce7f`. The original study contains 48 synthetic worlds, 12 exact finite kernels, and nine positive-innovation stationary distributions. No original many-name historical observations were used.

## New exact mathematical result

For population size N, token A frequency p_t=K_t/N, and balanced replacement probability mu, the frozen kernel is
[
q_t=(1-mu)p_t+mu/2,qquad K_{t+1}|K_tsim\mathrm{Binomial}(N,q_t).
]
Define expected within-generation pair diversity
[
H_t=E[2p_t(1-p_t)].
]
Conditional binomial sampling gives
[
E[2p_{t+1}(1-p_{t+1})|p_t]
=(1-1/N)2q_t(1-q_t).
]
Consequently the **exact closed scalar recurrence** is
[
H_{t+1}=aH_t+b,quad
a=(1-1/N)(1-mu)^2,quad
b=(1-1/N)mu(1-mu/2).
]
For every finite t>=0, `H_t=a^t H_0+b(1-a^t)/(1-a)`. For positive mu, the unique stationary diversity is
[
H_*=\frac{(1-1/N)mu(1-mu/2)}
{1-(1-1/N)(1-mu)^2}.
]
The frozen process is symmetric, with stationary mean E[p]=1/2. Let lag s be a nonnegative integer. At stationarity and mu>0,
[
\mathrm{Cov}(p_t,p_{t+s})
=(1-mu)^s\frac{1-2H_*}{4}.
]
The stationary covariance formula follows from conditional expectation `E[p_{t+s}-1/2|p_t]=(1-mu)^s(p_t-1/2)`, and the identity `Var(p)=(1-2H_*)/4`.

This reveals two distinct sources of memory loss: sampling noise reduces diversity through `1-1/N`, while symmetric innovation attenuates frequency autocorrelation by `1-mu` each generation. The frozen two-token mechanism has no measured cultural transmission links.

## Executed exact checks

The algebraic Fraction implementation was executed locally using the standard library. It produced the complete 48-world, five-timepoint stdout JSON. The full output SHA256 was `96fea1131d3e0e5eb7bd421065b706043a8d6e1725edf0388c3a9958320b62e2`; the complete stdout is reproducible from the archived source, and the GitHub archive stores a compact exact receipt with world H0/H4, all nine stationary values and 27 covariance values.

* 48 worlds and 240 closed-form diversity timepoint checks passed.
* 192 one-step recurrence checks passed.
* 60 mu=0 neutral diversity decay checks passed.
* Nine positive-mu stationary equations and 27 stationary covariance formulas passed.
* Omitting the finite-sampling factor differs from the correct formula in 168 of 192 transitions.
* Replacing the squared innovation factor by a linear factor differs in 126 of 192 transitions. Degenerate cases are not counted as detections.

The independent B audit directly read original frozen probability distributions and kernels, independently recomputed the 240 diversities, 192 transitions, nine stationary diversities and 27 covariance values by exact matrix powers. All agreed, including the 168 and 126 actual negative-control discrepancies.

Stationary diversity H* by population size and innovation rate:

| N | mu=1/16 | mu=1/8 | mu=1/4 |
| ---: | ---: | ---: | ---: |
| 4 | 93/698 | 45/218 | 21/74 |
| 6 | 155/822 | 75/278 | 35/102 |
| 8 | 217/946 | 105/338 | 49/130 |

These are exact artificial stationary expectations. They are not measurements from human populations. A zero-innovation process has multiple stationary distributions and must not be assigned the unique-positive-mu covariance interpretation.

## Files and execution evidence

* Main executable: `research/validation/r165_moment_extension_20261025.py`, executed locally; Git blob `5fca71b43ad38d7f5971515714a8e3374fe5ee78`.
* Compact exact receipt: `research/validation/R165_MOMENT_EXTENSION_COMPACT_EXACT_RECEIPT_2026-10-25.json`.
* Independent executed JavaScript: `research/evidence_audit/r165_b_matrix_moments_20261025.js`, Git blob `ce9a318d79afaacd9d45dafd8c0f5c27eb698d00`.
* B scientific audit: `research/evidence_audit/B_R165_EXACT_MATRIX_STATIONARY_MOMENT_SCIENTIFIC_AUDIT_2026-10-25.md`.

Status: `PASS_BOUNDED_INTERNAL_E1`. No new E2, E3, independent external team replication, out-of-sample prediction, or causal inference. Remote CI for these new scripts is `NOT_RUN` because zero additional GitHub Actions cost was not established. No fees incurred through the work performed. R073 and PESEN v0.1 remain frozen.

Next R priority: inspect R166 existing primary evidence and unresolved queue gates before selecting another unique extension. Original239 crosswalk v7.8 and 154-item itemwise scientific triage queue are unchanged.
