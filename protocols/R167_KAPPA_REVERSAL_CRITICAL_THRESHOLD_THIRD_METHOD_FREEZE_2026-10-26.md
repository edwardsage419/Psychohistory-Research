# R167 third method: exact critical reweighting threshold, preregistration

Date: 2026-10-26 (Asia/Singapore). Parent frozen R167 remains immutable. Repository main inspected at 862a986cdeca56526b0a6dc8a9b51e4936bcdb78. This protocol is a new E1-only extension, not a reopening of the prior CLOSED_BOUNDED_E1 decision.

## Fixed input and primary question

Use the original R167 72 synthetic initial worlds: four ordered pairs (1/4,3/4), (1/3,2/3), (1/5,4/5), (1/2,1/2); high-group weight h in {1/2,3/4}; delta in {-1/4,0,1/4}; kappa in {0,1,2}. Evaluate only the first transition, holding both initial group frequencies and group weights fixed when varying kappa. Read original frozen R167_EXACT_RESULTS.json as an independent archival comparison, without editing it.

Let a<=b, x=1-h, y=h, m=xa+yb, S=xa(1-a)+yb(1-b), C=1-delta(1-a-b). Under the original pre-state reweighting convention, predict exactly
W=-delta*S,
B=xy*kappa*(b-a)^2*C/(1+kappa*m),
DeltaP=W+B.

For delta>0, define D=xy*(b-a)^2*C-delta*S*m. If D>0, the strict aggregation reversal DeltaP>0 occurs iff kappa>delta*S/D. If D<=0, no finite kappa>=0 reverses the within decline. At equality, DeltaP=0. This threshold is a one-step conditional theorem for this specific two-group rule, not an empirical selection estimate. For delta<=0, report W and B without using the positive-delta threshold rule.

## Fixed verification and negative controls

1. Enumerate all 72 initial worlds using exact rational arithmetic, compare W,B,DeltaP and next P with original archived first transition, and check the threshold sign prediction for all 24 delta>0 grid worlds. Record every world and the exact critical kappa or null.
2. For the original reversal a=1/4,b=3/4,x=y=1/2,delta=1/4, require critical kappa=6/5; kappa=1 must give negative DeltaP, kappa=6/5 zero, kappa=2 positive.
3. Check kappa=0 and a=b as negative controls; a=b implies B=0 and no reversal when delta>0.
4. Independent B route will use direct post-update normalized weights rather than the factorized B formula, and test exact boundary kappa=critical, critical/2 and critical+1 for every finite positive threshold. All exact comparisons must agree. The B route must report if no thresholds are finite.
5. Failure or a mismatch must be recorded, never silently amended. Any correction requires an append-only amendment. No fitting, no E2/E3 claim, no external independent replication claim. No paid computing or GitHub Actions.

## Acceptance

Pass only if all 72 archival first steps match, all 24 delta-positive sign predictions match, specified reversal boundary matches, and B independent direct-weight route matches every finite-threshold boundary. Report counts and any exception. Preserve R073 and PESEN v0.1 freezes, original239 v7.8 and the 154-item queue unchanged.
