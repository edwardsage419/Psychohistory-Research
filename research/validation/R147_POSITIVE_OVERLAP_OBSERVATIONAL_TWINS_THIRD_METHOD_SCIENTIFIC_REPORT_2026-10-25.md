# R147 third-method extension: causal observational twins with strictly positive assignment

Date: 2026-10-25. Evidence: E1 exact artificial structural causal models only.

## Source and baseline
The existing R147 research reads Berry and Berry (1990, DOI 10.2307/1963526) and Shipan and Volden (2008, DOI 10.1111/j.1540-5907.2008.00346.x) and has already passed a bounded 86-test, two-Python-version remote CI for its original synthetic model. This addendum introduces an entirely new finite counterexample and makes no claim to reproduce their real US policy adoption data.

New prospective protocol was committed as 5144933bdee0762e6f3223850222827b0fc85036 before implementation and execution. The prior R147 protocol, R073 and PESEN v0.1 were untouched.

## Frozen new model and results
U is a fair hidden binary variable. A is an imperfect indicator of U: P(A=1|U=1)=3/4 and P(A=1|U=0)=1/4. Both treatment levels have positive probability within both U strata. In model S, B and C are conditionally independent children of U and have no causal A input. In model D, B and C instead receive A and a shared independent exogenous draw W that reproduces the complete joint conditional distribution P(B,C|A) of S.

The S implementation enumerated 128 elementary equiprobable worlds. The D implementation enumerated 512. An independent symbolic product-sum derivation verified the full eight-cell distribution. In order 000,001,010,011,100,101,110,111, S's numerator over 128 is [28,12,12,12,12,12,12,28]. D's numerator over 512 is [112,48,48,48,48,48,48,112]. All eight observed cells are strictly positive, both distributions sum to one, and every cell agrees exactly.

Observed risk difference P(B=1|A=1)-P(B=1|A=0)=1/4 in BOTH worlds. Under surgical do(A), D's effect on B is 1/4 and S's effect is 0. The common shock survives the intervention in S. Model D's independent W creates within-A residual correlation between B and C, preserving the entire observational three-variable distribution rather than only two marginal regressions.

P(B=C=1|A=1)=7/16 and conditional covariance is 3/64. Forcing B and C independent given A would instead imply P(B=C=1|A=1)=25/64. The frozen independence negative control was rejected. The second negative control correctly rejects interpreting observational conditioning in S as an intervention.

The main JS executable reports 12 passing gates. An independently written Python Fraction algebraic factorization was locally executed with 11 passing checks and identical eight probabilities, observed contrast and two intervention contrasts.

## Interpretation and limitations
The original R147 example used A=U, giving no overlap conditional on U. This new example demonstrates observational non-identification even when A has strictly positive probability in every U stratum. Positivity alone does not remove confounding when U is unobserved. The models differ in causal parent structure and have identical complete observed P(A,B,C). The result does not imply failure under randomized A or when all relevant confounders are observed and correctly adjusted. The D construction is tailored to the S observational distribution, so it is a formal existence proof, not a realistic calibrated model of policy diffusion.

No real city, country, historical panel, human behavior or original paper coefficient was used. No new R147 empirical fit or out-of-sample forecast. This remains an internal E1 mathematical result. Independent algorithms within one project do not constitute external independent replication.

## Reproduction, scope and status
* Frozen protocol: research/validation/R147_POSITIVE_OVERLAP_CAUSAL_TWIN_PROTOCOL_FREEZE_2026-10-25.md
* Main executable: research/validation/r147_positive_overlap_observational_twins.js
* Exact receipt: research/validation/R147_POSITIVE_OVERLAP_8_CELL_640_WORLD_EXACT_RECEIPT_2026-10-25.json
* Independent B script: research/evidence_audit/r147_b_independent_fraction_symbolic_audit.py

Local exact checks: PASS. New remote GitHub Actions: NOT_RUN because zero-cost billing status was not confirmed. No shared original239 index was modified; pending count remains 154. New E2=0, E3=0, external replication=0. R127 and R136 legacy protocol exceptions remain open.

Status: PASS_BOUNDED_LOCAL_INTERNAL_TWO_METHOD_R147_E1; remote CI and empirical validation remain open.
