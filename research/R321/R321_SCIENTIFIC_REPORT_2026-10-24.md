# R321 scientific report: finite Wald-inspired sequential probability ratio stopping

Date: 2026-10-24. Original239 01-010 Sequential Sampling Models, P2. **Formal scientific grade: PASS_BOUNDED_E1_FINITE_WALD_INSPIRED_ONLY.**

## Source and reuse audit

Original English references: Abraham Wald (1945), *Sequential Tests of Statistical Hypotheses*, Annals of Mathematical Statistics 16(2):117–186, DOI 10.1214/aoms/1177731118; Forstmann, Ratcliff and Wagenmakers (2016), *Sequential Sampling Models in Cognitive Neuroscience*, Annual Review of Psychology 67:641–666, DOI 10.1146/annurev-psych-122414-033645. R320's discrete absorbing-walk combinatorics is a shared mathematical submechanism. R321 supplies explicit rival likelihoods, Wald-inspired likelihood ratio threshold semantics, exact type-I/type-II and censor probabilities and a fixed-horizon comparison. R289 sequential offers has different satisficing stopping semantics. Repository code search for SPRT and Wald returned no prior itemwise file. Historical ZIP and knowledge card content completeness remains an open reuse gate.

## Temporal freeze and source universe

Prescore protocol [f8895542](https://github.com/edwardsage419/Psychohistory-Research/commit/f889554205b5339f1c52faa4c25d36dc270edb1f) preceded the first outcome source [1da4a0df](https://github.com/edwardsage419/Psychohistory-Research/commit/1da4a0dfaad4494dd11ce35d128f5a2f05d78007). Two simple Bernoulli hypothesis pairs, two score thresholds and two true hypotheses produce **8 worlds and 1024 complete artificial seven-bit exogenous path labels**. Each path has exact rational probability. First threshold crossing determines an H0 or H1 decision; paths with no crossing by seven samples remain **undecided**. Suffix bits after stopping are mathematical enumeration labels, not observed post-decision behavior.

## Prespecified finite results

For p0=1/4, p1=3/4, K=2 and H1 true: accept H1 873/1024, accept H0 97/1024, censored 27/512, expected truncated samples 1579/512. Under H0 true, the accept-H0 and accept-H1 masses swap exactly. For K=3 and H1 true: accept H1 12987/16384, accept H0 481/16384, censored 729/4096, expected truncated samples 609/128. Increasing K from 2 to 3 raises censoring and truncated sample count for both hypothesis pairs and both truths. Under the first pair the unconditional false-H0 decision probability under H1 is 97/1024 for K2 and 481/16384 for K3; conditional-on-decision error is 97/970 and 481/13468 respectively. This tradeoff must retain the undecided mass. The fixed-seven majority comparator for H1 true in the first pair selects H1 with probability 3807/4096. A forced fixed-sample choice and a censored sequential test have different decision coverage, so these raw error rates are not a dominance comparison.

## Independent computation and CI

Generator [r321_finite_sprt.py](r321_finite_sprt.py) has 35 stdlib unit tests and a byte-for-byte source replay. Independent [state-mass audit](../catalogue_audit/independent_r321_sprt_audit.py) reads all 1024 CSV rows, recalculates each probability and first stop independently and propagates only live score states in a separate dynamic program. GitHub Actions [run 40013917870](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/40013917870) completed **success**, with three successful jobs: Python 3.11 35 tests, Python 3.12 35 tests and independent no-import dynamic-programming audit. Git blob hashes and job IDs are recorded in [machine receipt](R321_MACHINE_RECEIPT.json).

## Evidence boundary and remaining gaps

This study proves exact properties of an artificial finite, truncated Wald-inspired SPRT. Wald's original infinite-horizon stopping-time optimality, threshold calibration to a target alpha/beta, likelihood model adequacy, real human reaction-time fit, true human E2 and historical E3 are **not established**. Sequential Sampling Models is a family containing DDM, racing accumulators and other variants; the present primary link documents one bounded mechanism only. The 173 provisional README catalogue associations remain unvalidated. R073 and PESEN v0.1 remain frozen. No model fusion or personal decision system work.
