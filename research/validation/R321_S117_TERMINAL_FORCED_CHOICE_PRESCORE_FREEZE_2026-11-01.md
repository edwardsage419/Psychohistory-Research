# R321 S117 prescore freeze: finite sequential terminal-choice counterfactual
Date: 2026-11-01 UTC. Track R. Baseline main 2419e80e421e8329a4f1ed969785e9dff63504ca. Evidence E1 only.

## Immutable input
Reuse exactly original R321 frozen 8 Bernoulli worlds, 7-bit exogenous paths and original first-hit rule, protocol blob 211fc14095398194849995d2795a5e12c2feba69; original CSV Git blob d5e5e183a786e199fbf792589ed68735f30ca1b3 and original JSON blob 5d8a6e807a099ab8b3e653c519a198497335fded. The R321 original PASS_BOUNDED_E1_FINITE_WALD_INSPIRED_ONLY remains unchanged. This extension is a separate question, never an update to original acceptance.

## Frozen question and policies
For each original (p0,p1,K,true hypothesis) and each of the 128 length-7 exogenous bitstrings, compare:
S: first threshold crossing at t<=7, if no crossing force a terminal choice at t=7 by majority of seven bits (>=4 ones chooses H1; otherwise H0).
F: ignore stopping, observe all seven bits and choose H1 for >=4 ones, otherwise H0.
A: original R321 rule, leaving noncrossing paths undecided.
The terminal forced choice uses only bits observed on censored paths; S stops immediately on crossed paths. F is a mathematical full-path counterfactual; suffix bits following S early stopping are unobserved in that policy, so no empirical claim about them.

## Prespecified exact outputs
Eight-world exact Fraction probability masses: S choose H0/H1 and unconditional error, S expected observed samples, F error, S-versus-F disagreement probability, disagreement split by early stopping versus terminal censoring, original A coverage and conditional error, S error minus F error. Enumerate all 1024 original path identities, all probability sums exactly 1, no random sampling. Report each world's probabilities and a complete 8-world table. All claims remain limited to this artificial finite universe. Report sign of differences whether positive, zero or negative, without changing the rule after seeing results.

## Falsification and B audit
Verify original source row uniqueness (world_id,path_bits), 128 rows/world, original first-hit decision and path probability for every row. A B-route implementation must not import the R-route calculation; recompute from Bernoulli likelihoods and an independent live-state or separate full-path enumeration. Mutations must reject wrong world, path, mass, decision, terminal assignment, summary or evidence-grade claims. Preserve failures. Only E1 nonblind internal audit may be claimed without an external group. E2/E3 zero, no general Wald optimality, no model fit, no post-hoc tuning. No Actions until zero-cost confirmed. R073 and PESEN v0.1 frozen.
