# R325 S121 prescore protocol: exact state weight sensitivity

UTC freeze date: 2026-10-31T22:47:43Z.
Baseline main HEAD: 58f129a38b7857f6ac0501d8259036251c9f10ce.
Track key: (r,R325,original_2026-10-24_cubic_v1,S121_state_weight_sensitivity).
Status: PRESCORE_FROZEN, no S121 outcome observed before this freeze.

## Unchanged parent and finite universe
Read R325 original 2026-10-24 README, scientific report, original code, receipt, exact JSON and acceptance. Parent R325 is project constructed E1. Keep all 343 ordered integer payoff difference triples d in {-3,-2,-1,0,1,2,3}^3, all three fixed kappa values 0, 1/4, 1, Q_k(d)=d+k*d^3, and all parent files immutable. The parent original 1029-row CSV blob is b4964ef88aded2c9bd2a70280c067176fedcd597. Parent source code blob is e1fd070d271fa9a5516515e162d9057a47e76f46. This is a new artificial sensitivity analysis and does not amend the parent acceptance.

## Frozen perturbation
Four fixed probability vectors over the three payoff states, with exact rational arithmetic:
* U: (1/3,1/3,1/3).
* EARLY: (1/2,1/3,1/6).
* LATE: (1/6,1/3,1/2).
* CENTER: (1/4,1/2,1/4).

For each of 4 profiles x 3 kappas x 343 ordered triples, compute EU=sum(p_i*d_i), F=sum(p_i*(d_i+k*d_i^3)), choice sign(F), EU sign, and strict reversal 1[EU*F<0]. Every profile has 343 states per kappa. No fitted parameters, no random sampling, no real data.

## Prespecified outputs
1. Full deterministic 4116-row CSV with profile, world, kappa, d1..d3, p1..p3, EU, F, EU choice, F choice, strict reversal, uniform-reference choice, and changed-versus-uniform indicator.
2. JSON of per-profile/per-world A/B/tie counts, strict EU-to-regret reversals, changes versus uniform choice on the same triple and kappa, and strict sign disagreements with uniform. Include total weight normalization, finite coverage, and exact fractions.
3. Controls: U reproduces original 3-world choice counts and strict reversals (0,6,6). For all profiles, if every d_i>=0 then F>=0; if every d_i<=0 then F<=0. For every triple d, k, EARLY(d)=LATE(reverse(d)); CENTER(d)=CENTER(reverse(d)). Kappa=0 yields F=EU for all profiles. Verify all 4116 keys unique, each profile x kappa covers exactly 343 triples.
4. Compare each weighted profile with U at the individual ordered triple level. Global aggregate equality cannot be substituted for row-level equality.
5. Independent B program in Python Fraction, no import of the R generator, reconstruct full 4116 mathematical records and compare all columns plus JSON aggregates; negative controls for missing row, duplicate row, wrong profile weights, altered rational score, changed choice and falsely promoted E2.
6. Report any failure, including initial failed tests, and bound interpretation to artificial E1. No claim of stochastic dominance beyond the stated coordinatewise monotonicity check; no human E2 or historical E3.

## Data and governance
A data scout separately checks a public candidate, source fields, rights and suitability for R073, without changing R073 or PESEN v0.1. Existing original239 crosswalk v7.8 blob 36f24235901172642c46853298aebb421f1a3552 and pending154 blob 3b96d46b3d88ccafd779a08509c3cfd0e435772f are read-only. No new cost or paid Actions. Internal independent implementation is nonblind because parent R325 findings were read. No retroactive modification of this frozen protocol.