# R268 S64: AIC/BIC selected Bernoulli models under independent one-step Brier risk

Date 2026-10-29 UTC. Target `(r,R268,S64,one-step-independent-holdout-Brier-risk)`. New endpoint protocol committed **before** S64 outcome computation: `a61edfe2f3f479c2309cbc3e5f1e6757730ed7d4`. The original R268 model-selection results were read before this new protocol; this is a nonblind prospective **endpoint** extension within an artificial model. Original R268 `CLOSED_BOUNDED_E1` acceptance and all frozen original files remain unchanged.

## Question and frozen design

The original R268 studied selection frequencies for fixed Bernoulli `M0(q=1/5)` and fitted `M1(qhat=K/n)`, with AIC and BIC selection determined by archived per-K decisions. This extension asks how the four frozen forecasting rules perform for **one future independent Bernoulli observation from the same artificial world**. No new fitted parameter, smoothing, clipping, or threshold tuning. The Brier loss `(q-Y_next)^2` has exact conditional expectation `p(1-p)+(q-p)^2`. All nine original worlds, 3312 complete ordered training sequences and 6624 two-outcome extensions are evaluated.

The R route read all 3312 original CSV rows (Git blob `6296528507012dd1d8d11e3556fcdeb7b6aeb2b5`), validated sequence uniqueness, k, n, true p, exact source probability, qhat and per-K archived AIC/BIC labels, and directly weighted both future outcomes in V8 Fraction arithmetic. The B route independently used `comb(n,k)p^k(1-p)^(n-k)` and the conditional risk identity. Archived original R268 selection JSON Git blob `3d407ddcf524bfc55c0a076d57383c6655a36441`. Both routes agreed exactly on 36 risk cells and nine AIC minus BIC paired differences.

## Complete nine-world results

All fractions below are exact expected Brier risks. A negative AIC minus BIC difference favors AIC.

| True p | n | M0 | M1 | AIC selected | BIC selected | AIC minus BIC |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 1/5 | 4 | 4/25 | 1/5 | 2637/15625 | 3109/15625 | -472/15625 |
| 1/5 | 6 | 4/25 | 14/75 | 213118/1171875 | 213118/1171875 | 0 |
| 1/5 | 10 | 4/25 | 22/125 | 8364374/48828125 | 8192342/48828125 | 172032/48828125 |
| 1/2 | 4 | 17/50 | 5/16 | 549/1600 | 511/1600 | 19/800 |
| 1/2 | 6 | 17/50 | 7/24 | 2921/9600 | 2921/9600 | 0 |
| 1/2 | 10 | 17/50 | 11/40 | 2869/10240 | 3037/10240 | -21/1280 |
| 4/5 | 4 | 13/25 | 1/5 | 3789/15625 | 3148/15625 | 641/15625 |
| 4/5 | 6 | 13/25 | 14/75 | 221236/1171875 | 221236/1171875 | 0 |
| 4/5 | 10 | 13/25 | 22/125 | 8597948/48828125 | 8651708/48828125 | -10752/9765625 |

Three worlds favor AIC, three favor BIC, and three tie. The three ties at n=6 follow the original R268 identical per-K selection decisions. At true p=1/5, n=4 AIC has lower risk, while n=10 BIC has lower risk. At true p=4/5 the ordering is reversed. The selection criterion with lower expected Brier risk depends on the frozen data-generating p and sample size.

AIC/BIC selection also need not beat the fixed M0 or always-fitted M1. At p=1/5, n=4, the correctly specified M0 achieves 4/25, lower than either selection rule. At p=1/2, n=4, M1 risk 5/16 is lower than both selection rules. The original R268 warnings about infinite one-step **log** loss at boundary MLE remain valid; finite Brier loss does not remove that issue.

## Reproduction and evidence audit

Machine receipt: `research/validation/R268_S64_ONE_STEP_BRIER_EXACT_RECEIPT_2026-10-29.json`. Independent native Python standard-library script: `research/validation/r268_s64_independent_binomial.py`. The Python file was run with `--output` locally, produced nine worlds, 36 Fraction risks and four rejected malformed-input controls; the executed file's Git blob matched the archived blob. A separate direct 45-field comparison of the native Python results to the independently obtained V8 source/analytic results passed. V8 strict receipt mutation controls rejected duplicate world, missing world, tampered risk, bool-for-string and tampered paired difference, five of five. Full original CSV was read through the GitHub connector and validated in V8; the archived Python B script uses the frozen per-K table and does not read the original CSV itself. A separate archived native source-route CLI remains NOT_RUN.

This is an internally computed, nonblind, **E1 artificial** out-of-training-sequence calculation under a known fixed DGP. It is not a human held-out experiment, empirical calibration, causal mechanism discovery, historical prediction or external independent-team replication. The design probabilities are assumed known, no sampling uncertainty is estimated, and the shared frozen selection table is not an independent second identification of AIC/BIC thresholds. No new E2/E3 evidence. R073 and PESEN v0.1 frozen.

## A01 to A06 bounded status

A01 PASS for nine-world one-step endpoint. A02 PASS for original Git blob identity and fixed protocol; no new human source. A03 PASS for V8 source route, independent analytic route and native Python binomial execution; original source native Python CLI OPEN. A04 PASS for recorded negative controls, no hidden tuning. A05 PASS for explicit E1-only scope; empirical generalization OPEN. A06 PARTIAL for supplementary archiving and GitHub verification; original R268 acceptance unchanged. New GitHub Actions were not triggered because free runner billing was not independently checked. No new expenditure was initiated.

Next R: review R269 existing Cross Validation closure and select a distinct unresolved endpoint. Next B: run a clean native source-route receipt checker against exact original bytes. Next A: continue independent human source scouting and identity/license checks.
