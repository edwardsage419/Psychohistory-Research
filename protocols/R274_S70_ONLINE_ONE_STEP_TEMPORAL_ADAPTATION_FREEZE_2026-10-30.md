# R274 S70: sequential online update versus frozen t4 forecast, prescore design

UTC design date: 2026-10-29. Baseline main a59180cbef836a2bcd5e31d940ddbfdc13e92eec. Research track R. Original catalogue 12-004. Scope: additional finite E1 mechanism only. Original R274 protocol, 576 source CSV, frozen results, and formal bounded acceptance remain unchanged.

## Frozen sources and timing
Reuse exactly original R274 three independent Bernoulli regimes: STABLE_HALF (a=1/2,b=1/2), RISING_RATE (a=1/4,b=3/4), FALLING_RATE (a=3/4,b=1/4). Enumerate all ordered (X1,X2,X3,X4,Y5,Y6) in {0,1}^6, with mass a^K(1-a)^(4-K)b^J(1-b)^(2-J), K=sum(X), J=Y5+Y6. Exactly 64 ordered sources per regime. Use exact rational arithmetic.

At t4, only K is visible. At t5, score Y5 using a forecast made at t4. At t6, Y5 has become observed and may be used to update; Y6 is strictly unseen until scored.

Three legal, fixed policies:
1. PAST_FIXED: q5=q6=(K+1)/6.
2. ONLINE_ONE_STEP: q5=(K+1)/6, q6=(K+Y5+1)/7.
3. PRECOMMITTED_HALF: q5=q6=1/2.
For every source and policy, score squared Brier losses (Y5-q5)^2 and (Y6-q6)^2 and their arithmetic mean. Compare exact source-weighted expected t5, t6 and two-period average losses in all nine regime-policy cells. No hindsight pooled policy is eligible as a forecast. Keep original illegal hindsight score solely as a historical leakage counterexample.

## Prespecified comparisons and falsifiers
Compare ONLINE_ONE_STEP minus PAST_FIXED expected t6 Brier in each regime, and ONLINE_ONE_STEP minus PRECOMMITTED_HALF average Brier in each regime. Report sign even when unfavorable. Verify q5 does not change if either future bit changes, and q6 does not change if Y6 changes at fixed K,Y5. Verify q6 can change when Y5 changes. Compare source enumeration to an independently written analytic moment method: E[K]=4a, Var(K)=4a(1-a); for online q6, E[K+Y5]=4a+b, Var(K+Y5)=4a(1-a)+b(1-b); for fixed q, use K alone. For any legal q independent of its scored Y, E[(Y-q)^2]=b(1-b)+Var(q)+(E[q]-b)^2. Verify all 18 per-period cells and 9 averages exactly.

Predefined negative controls: exchange future Y6 while keeping past and Y5 fixed; forbid q6 depending on Y6; reject duplicate or missing source identities; reject evidence-grade elevation and numeric type confusion. Preserve failed tests and all limits. The moment oracle must not read source enumeration or its receipt.

## Provenance and acceptance boundary
This new protocol must be committed before S70 scores are calculated. Prior original R274 expected risks and original R273 S69 scores were read; the S70 analysis is therefore nonblind internal research, not external replication. Exact synthetic E1 results do not establish human E2, historical E3, causal time adaptation, calibrated future probability on real data, or general time series behavior. Original R274 bounded E1 acceptance, R073 frozen model and scoring, and PESEN v0.1 remain unchanged.

Deliverables: new R-owned script, exact source CSV, machine JSON and scientific report under research/validation; B independent analytic check under research/evidence_audit; A only if independent data-source verification is possible. No paid APIs or Actions dispatch without verified zero cost. No modifications to existing files.