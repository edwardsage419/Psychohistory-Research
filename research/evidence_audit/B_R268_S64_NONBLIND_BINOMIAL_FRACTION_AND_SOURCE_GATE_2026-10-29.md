# B audit: R268 S64 independent binomial oracle, source identity and negative controls

Date 2026-10-29 UTC. Key `(B,R268,S64,source-weighted-future-Brier-and-coverage)`. Nonblind internal method audit. Read before implementing B: original R268 fixed per-K selection results and original source code, and the R-track S64 frozen endpoint. This is not blind, not an independent human cohort, and not an external team replication.

## Immutable inputs and actual execution

1. R268 original source CSV Git blob `6296528507012dd1d8d11e3556fcdeb7b6aeb2b5`, 666285 bytes, 3312 complete ordered Bernoulli training sequences. Actual complete connector read, rowwise validation in V8 of sequence identity, n, p, K, exact source probability, qhat, unique ordered sequence, and AIC/BIC labels. All nine world masses exactly 1. Exactly 6624 synthetic independent next-outcome event types.
2. Original R268 result JSON Git blob `3d407ddcf524bfc55c0a076d57383c6655a36441`, nine unique worlds and all n+1 frozen K selection keys. No post-result selection change.
3. New endpoint freeze commit `a61edfe2f3f479c2309cbc3e5f1e6757730ed7d4`, committed before S64 outcome computation. Prior original R268 results had been read, hence nonblind selection-table reuse.
4. Source route: exact rational sum over each ordered training sequence and both independent next-outcome values, run in isolated V8 tool environment. B route: independent binomial K mass and algebraic `p(1-p)+(q-p)^2` calculation, exact BigInt Fraction. Nine worlds × four methods = 36 risk cells and nine paired AIC minus BIC differences all equal.
5. A separate **native Python 3.13 standard-library** program `research/validation/r268_s64_independent_binomial.py` was actually run locally with `--output`. Its Git blob `2f6fbcacfa4e37f1747f6a91b886ad71be2cfc58` was compared to the remote archived file. It independently recomputed all nine binomial worlds and 36 Fraction risks, and its nine paired differences were compared against the V8 result, 45 exact fields equal. Local output JSON SHA256 `40dc27f8f43caf101e2b24a49bd1452d0b8de3d1df3f0d42d5fa679d82ae3e9d` (local output is not claimed as byte-identical to the archived R receipt).
6. V8 strict receipt mutation controls: duplicate world, missing world, risk changed to 999, bool substituted for a fraction string, paired difference changed. All five rejected. Native Python negative inputs: missing K, invalid label, unknown p, inconsistent n. All four rejected.

Persisted R receipt `research/validation/R268_S64_ONE_STEP_BRIER_EXACT_RECEIPT_2026-10-29.json` records 36 exact risk cells, 9 paired differences and five receipt mutation rejections. This is the original R-route calculation's stored result, not a substitute for rerunning a source-route CLI from a clean checkout.

## Scientific assessment

At p=1/5, n=4, the M0 fixed forecast is exactly correct and both AIC/BIC selection rules increase one-step expected Brier risk. At p=1/2, n=4, M1 risk is 5/16 while AIC risk is 549/1600 and BIC risk 511/1600. AIC/BIC rankings reverse across n and p; nine worlds split into three AIC wins, three BIC wins and three ties. No claim that one selection criterion is uniformly better.

No train/test leakage is present within the specified artificial probability calculation: the future outcome is analytically integrated independently of the n training bits. The analyst knows the generating p, so this is a known-DGP exact expectation, not an empirical holdout protocol or real predictive calibration. MLE boundary probabilities 0/1 create infinite expected **log loss** in some worlds; Brier's finite loss is an intentionally different frozen endpoint. No sample-based confidence interval or cluster bootstrap is warranted for the complete artificial probability space. No E2 human or E3 historical inference is supported.

## Open gates and scope

* Native Python B analytic CLI: PASS, with remote Git blob identity and 4/4 malformed controls.
* Full original CSV connector read and V8 source route: PASS, 3312 rows.
* V8 versus independent Python risk and paired-difference comparison: PASS, 45 exact fields.
* Strict persisted receipt mutation controls: PASS, 5/5.
* Native archived R source-route CLI reading original CSV and JSON from a clean checkout: NOT_RUN.
* Blind reviewer or external independent team: NOT_RUN.
* Human out-of-study prediction, empirical calibration, historical extrapolation: NOT_RUN.
* New CI: NOT_RUN, runner free-billing status not independently confirmed. No paid API, private data, rented compute or purchases.

The original R268 formal bounded E1 acceptance remains unchanged; S64 is a separate supplemental artificial calculation. R073 model/scoring and PESEN v0.1 remain FROZEN. Next B: clean exact-byte source-route native CLI and stricter source file identity proof; retain the distinction between arithmetic and scientific validity.
