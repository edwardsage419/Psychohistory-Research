# R158 third-method scientific report: exact Poisson conditional likelihood ratios

Date: 2026-10-25. Frozen addendum protocol commit `12e2388771a1ab83a8aff14d3ad937b096469479`. Original R158 synthetic 60-world evidence and formal acceptance are unchanged.

## Derivation
Under the original artificial model N[t] given previous count N[t-1] follows Poisson(mu+alpha*N[t-1]), with N[-1]=0. For any fixed count history, compare a feedback candidate alpha with alpha=0 at the same mu. All factorial factors cancel. Define S=sum_t N[t-1], R=product_t(1+alpha*N[t-1]/mu) raised to N[t]. The exact likelihood ratio is **L(alpha)/L(0)=R exp(-alpha*S)**. R is a rational number when mu and alpha are rational; the exponential factor is required.

This is a fixed-history likelihood comparison. It is not an estimate of causality, a model fitted to conflict data, or an independent forecast.

## Recalculation
The new independent JavaScript BigInt-rational implementation directly reads the original R158_EXACT_RESULTS.json, Git blob `356ecbc5808cf13d4511f1c79ace8104e103262b`. All **60 archived artificial worlds** were compared with the exact-rational ratio and a separately computed log ratio. There are 48 nonzero-alpha worlds, 12 alpha-zero worlds and 15 all-zero-history H0 worlds with alpha-invariant likelihood. The maximum absolute discrepancy from archived 12-digit-rounded log-score differences was **9.467981954003335e-13**, below the prespecified 2e-11 threshold.

In the prespecified H1 sequence, mu=1 and alpha=1/2, the exact rational product is R=2, lag exposure S=8, so the log likelihood ratio is log(2)-4 = -3.3068528194400546. This independently reproduces the original negative feedback-minus-baseline score difference.

## Negative controls and limitations
Dropping exp(-alpha*S) changes the score, so the omitted exposure control is rejected. Substituting the contemporaneous target count for the lagged count changes the ratio and represents a target leakage mechanism, so that control is rejected. The existence of a favorable conditional likelihood ratio on a synthetic path cannot establish real causal self-excitation. All observations in this calculation are project-constructed counts; no real conflict events, human behavior or historical forecasts are scored.

No additional GitHub Actions were requested. Local mathematical identity and archive replay constitute E1 internal procedure checks. R073 and PESEN v0.1 remain frozen; original239 queue is unchanged.

**Acceptance: PASS_BOUNDED_INTERNAL_E1** for this additional exact ratio audit, without altering original R158 formal status.
