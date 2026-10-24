# R120 third-method exact integer-grid re-audit: pre-execution freeze

Date: 2026-10-24. Parent main HEAD inspected before freeze: `63f6a0cd5b11e9d220e31c004c562a58f44ba00c`. Catalogue item 04-003, existing R120. No new R identifier.

## Source and immutable subject

Kempe, Kleinberg, Tardos (2003), *Maximizing the Spread of Influence through a Social Network*, SIGKDD, DOI 10.1145/956750.956769; author-hosted original: https://www.cs.cornell.edu/home/kleinber/kdd03-inf.pdf . Theorem 2.5 and Claim 2.6. Reuse existing research/R120 source and original freeze without edits. The subject is the final activated-set distribution for progressive independent fixed Uniform[0,1] node thresholds on directed weighted graphs with nonnegative inbound weights summing to at most one.

## Independent method fixed before executing it

A new Python 3.11/3.12 standard-library auditor must compute the entire final-set distribution using a common denominator L of all edge weights and the L discrete midpoint thresholds (2k+1)/(2L), k=0,...,L-1, for each node, counting all L^n joint threshold configurations. This uniform integer-grid method is distinct from the existing breakpoint-interval integration and distinct from the existing live-edge selection method. All terminal masses must be exact fractions; thresholds are sampled once and retained through all rounds. The auditor must never call the original two solvers to produce its own distributions; it may import them only for post-computation comparison.

## Frozen finite test universe and gates

1. Exhaustively enumerate all labeled loop-free directed graphs on n=1,2,3 nodes, 1,4,64 graphs respectively, with each present incoming edge assigned weight 1/indegree(target). Enumerate all seed subsets. There must be exactly 530 graph-seed cases, 2+16+512.
2. For every case, compare the independent integer-grid full terminal-set distribution with BOTH original R120 exact algorithms, requiring exact Fraction equality and unit total mass. Compute an independent CSV of all nonzero terminal sets; the committed CSV must be checked byte for byte against the new auditor's deterministic regeneration.
3. Independently verify three nonuniform fixtures: two inbound weights 1/2 and 1/4 with seed sets {0}, {1}, {0,1} and expected sizes 3/2, 5/4, 11/4; weighted four-node chain weights 1/2,2/3,3/4 with seed {0}, expectation 25/12; three-node cycle with weight 1/2 per edge with seed {0}, expectation 7/4. Each fixture must match both existing algorithms in full distribution.
4. Negative control: on the two-inbound example with both sources seeded, incorrectly treating two incoming edges as independent Bernoulli successes yields target activation 5/8, whereas the correct model yields 3/4. Auditor must detect and reject this incorrect rule.
5. Tamper test: change a positive count in the generated CSV without updating anything else. The auditor must reject the altered CSV. A wrong expected source-code SHA must also be rejected.
6. Require exact source identity: verify the original R120 Python source Git blob SHA `7029a679174828a6a74fd6adf849157e50285cff`, original test blob `bba10681deac84fe765e51061359baa140b534cf` and original report blob `bdb7ae43f142189c0f4f72ea3623165c87b0383a` via local Git blob hashing, and execute all original 45 unit tests in Python 3.11 and 3.12 if available.
7. Require a clean audit CI on a public repository standard `ubuntu-latest` runner with no purchased runners, packages, cache, artifact upload, secrets or paid API. A failing CI or incomplete execution prohibits formal pass.

## Rejection and interpretation

Any mismatch in a full terminal-set probability, total probability, case coverage, source identity, frozen fixtures, negative control, tamper rejection or executable test is FAIL/OPEN. The strongest possible result is `PASS_BOUNDED_INTERNAL_THIRD_METHOD_EXACT_E1`. This is constructed E1 mathematical evidence and internal algorithmic independence only. Human E2, historical E3, external-team replication, out-of-sample calibration and real network parameter identification remain NOT_ESTABLISHED. Do not change R073, PESEN v0.1, or R120 source. Do not change the original239 crosswalk before the independent tests and CI are verified. No personal decision product or fusion.
