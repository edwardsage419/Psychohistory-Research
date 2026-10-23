# R319 prescore freeze: finite two-point random-coefficient Mixed Logit

Date: 2026-10-24. Original239 01-007 Mixed Logit (P2). Status: **PRESCORE FROZEN ONLY**. This file must be committed to main before any R319 source/score/results files. No retrospective adjustment to the registered grid or witness.

## Original sources and reuse gate

Primary original exposition: Kenneth Train, *Discrete Choice Methods with Simulation*, 2nd ed. (2009), chapter 6, pp. 134-150, author-hosted https://eml.berkeley.edu/books/choice2nd/Ch06_p134-150.pdf (particularly §6.1 eq. 6.1 and finite discrete mixing on p. 135). Primary journal: McFadden and Train (2000), *Mixed MNL Models for Discrete Response*, *Journal of Applied Econometrics* 15:447-470, DOI 10.1002/1099-1255(200009/10)15:5<447::AID-JAE570>3.0.CO;2-1.

R111 supplies fixed-coefficient conditional logit, including Gumbel derivation and IIA; it does **not** establish random coefficient mixing or the mixture-level odds counterexample. R192 and R193 have finite mixtures with different observation kernels and different research questions; they cannot be substituted for mixed discrete-choice utility. The R319 mathematical mechanism is newly tested, and those studies remain independently unchanged. GitHub code search for `mixed logit` and `random coefficients` returned no itemwise earlier result at freeze; filename/README token search is an incomplete historical archive audit, so no claim of comprehensive absence.

## Frozen finite universe and falsifiable tests

Use *only* the artificial five ordered choice sets of one-dimensional integer features: S0=(0,1), S1=(0,1,2), S2=(0,1,1), S3=(0,2,1), S4=(0,2,2). For each, set mixing mass q=P(beta=+1) in {1/4,1/2,3/4}, beta in {-1,+1}; utility is beta*x*ln(2) with iid unit-scale Gumbel shocks, so conditional probabilities equal 2^(beta*x) / sum_j 2^(beta*x_j). Compute rational probabilities with Fraction. Mixed P(j)=q*P(j|+1)+(1-q)*P(j|-1), preserving original alternative order even for duplicated feature values. No estimated parameters, random draws, simulated persons, or observed human choices.

All 5*3=15 artificial choice worlds, 2 conditional types, and every alternative produce **84 original conditional contribution source atoms**: 3*2*(2+3+3+3+3)=84. The 15 worlds produce **42 marginal alternative probabilities**. Commit full 84-atom CSV and full 15-world JSON; no filtering of examples. Source columns: world_id, choice_set_id, features, q_plus, beta, alternative_index, feature_x, conditional_probability, mixing_mass, weighted_contribution, mixed_probability. Exact rational strings are required. JSON retains each world and all its alternative marginal probabilities.

**Registered exact witnesses**:
1. S0, q=1/2 has P(A)=P(B)=1/2, odds A/B=1.
2. S1, q=1/2 has P=(5/14,2/7,5/14), odds A/B=5/4, while conditional odds A/B for either fixed beta are unaffected by adding C. Thus the constructed nondegenerate mixture violates IIA; this does not claim all mixtures violate IIA.
3. Each of 15 worlds has sum_j P(j)=1, positive entries, component sum identities, and q*conditional+other component exactly.
4. q=1/4 and q=3/4 satisfy the exact type-swap symmetry P(q; x)=P(1-q; -x) (with both beta signs inverted), checked for each set by direct rational evaluation. Fixed-beta type conditional odds are invariant to inclusion of the third option, given fixed features of A and B.
5. Equal-feature alternatives must have equal conditional and marginal probabilities.

## Execution, audit, acceptance

One stdlib Python implementation generates source CSV and results JSON with deterministic canonical serialization, replay verifies full exact bytes, and >=20 unit tests cover normalization, source counts, registered witnesses, component sums, type symmetry, equal features, corrupted source detection, invalid grid parameters and no accidental empirical claim. A separate no-import audit independently reconstructs each source row and 15-world marginals by a second Fraction formula using integer powers of two and verifies Git-source file content. GitHub Actions must show Python 3.11 and 3.12 tests and independent audit, all three jobs success. Source and program blob SHA1 receipts must be independently fetched before formal acceptance; absence of green CI or original source means **PENDING**, never PASS.

Permitted acceptance: `PASS_BOUNDED_E1_ONLY` for a small exact mathematical mechanism with complete artificial source. **Human E2=NOT_ESTABLISHED; historical E3=NOT_ESTABLISHED; no original real choice sample, fit, out-of-sample prediction, or population heterogeneity inference.** Any scientific claim outside this finite artificial grid is unverified. Update only original239 01-007 to R319 after green CI and separate metadata checks, preserving all other 238 entries. R073 and PESEN v0.1 remain frozen. Complete R series before taxonomy or fusion.