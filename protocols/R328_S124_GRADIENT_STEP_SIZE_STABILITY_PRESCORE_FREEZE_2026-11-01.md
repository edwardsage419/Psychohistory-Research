# R328 S124 frozen prescore protocol: finite gradient step-size stability

Date: 2026-11-01 UTC. Track: r. Baseline main: ecf4c3c51a07caddd2b99c795b92898dd0f37e84. Status at creation: PROTOCOL_ONLY.
Research key: (r, R328 / original239 02-010, S124-v1, learning-rate stability and failure).

## Fixed source and independent question
The frozen R328 scalar predictive-error analogue has 24 deterministic worlds: m in {0,1}, y in {0,1,2}, prior precision r in {1,2}, sensory precision p in {1,2}, x0=m, E(x)=r(x-m)^2/2+p(y-x)^2/2. Existing R328 uses alpha=1/4, four gradient steps and 120 artificial rows. Preserve original sources, original CI, E1 scope, and all original receipts.

This extension asks when the *same* precision-weighted error correction fails to decrease objective energy as the fixed step size changes. Alpha in {1/4, 1/2, 3/4, 1}, 24 worlds each, 5 time points t=0..4, 480 exact artificial rows and 96 complete world summaries. No model fitting or post-hoc parameter selection. World and row order: alpha, m, y, r, p, t.

Update x(t+1)=x(t)+alpha*[p(y-x(t))+r(m-x(t))]. Independent closed-form oracle: x*= (r*m+p*y)/(r+p); lambda=1-alpha*(r+p); x(t)=x*+(m-x*)*lambda^t; E(x(t))-E(x*)=(r+p)/2*(m-x*)^2*lambda^(2t).

## Predefined tests and negative controls
1. Exact 480 unique labelled rows and 96 worlds, 24 worlds for each alpha, rational strings, deterministic CSV and JSON bytes; compare alpha=1/4 with all 120 original R328 rows, every source field except the new alpha column.
2. Independent no-import Fraction implementation checks every x, sensory residual, prior residual, E, x*, lambda and energy gap for all 480 rows. Distinct alpha and world identities are mandatory.
3. Classify each world as FLAT_ZERO_RESIDUAL when y=m; otherwise CONTRACTIVE if |lambda|<1, NEUTRAL if |lambda|=1, EXPANSIVE if |lambda|>1. Test energy monotonicity at every adjacent t. Check E(x)-E(x*) nonnegative and the exact gap ratio identity. A neutral world may remain constant without improving.
4. Frozen witnesses: m=0,y=2,r=2,p=2,alpha=1/4 reaches x*=1 in one step; the same world with alpha=1/2 oscillates between 0 and 2 with constant energy; alpha=3/4 yields x1=3 and E(x1)>E(x0). These are artificial controls.
5. Deliberate mutation tests reject duplicate rows, omitted row, modified energy, wrong alpha, and an E1-to-E2 evidence promotion. Test execution and provenance are separately recorded.

## Scientific gates and limits
Report counts by category and alpha, failures and native execution state. E1 finite deterministic algebra only; no neural signal, human E2, historical E3, original Rao-Ballard cortical simulation, external replication or causal inference. The R328 original bounded acceptance remains unchanged. R073 model and scoring, PESEN v0.1 frozen. No fee-based compute or Actions trigger. If source/identity or calculations disagree, mark FAIL and retain the failed evidence. Independent internal verification is nonblind, not external replication.
