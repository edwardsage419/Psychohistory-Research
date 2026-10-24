# R121 third-method subset-cut recurrence: frozen protocol before code

Date: 2026-10-24. Parent main HEAD `e8b727a1bcb095f118cb4d74f415ed422138670d`. Original239 item 04-004, existing R121. The original R121 research and acceptance remain unchanged.

## Source and target

Kempe, Kleinberg and Tardos (2003), *Maximizing the Spread of Influence through a Social Network*, DOI 10.1145/956750.956769, original author PDF https://www.cs.cornell.edu/home/kleinber/kdd03-inf.pdf . Claim 2.3 and Theorem 2.2. Independent Cascade IC has one independent attempt along each outgoing edge when its source is newly active; successful targets activate at the next step, no retries, no deactivation.

## Third independent mathematical algorithm

For graph V, seed set S, and each T containing S, define f(T) as the probability all vertices in T are reachable from S **inside the graph induced by T**. Define C(U,W) as the product of (1-p_uv) for directed edges from U to W. Recursively in increasing |T|:

f(T) = 1 - sum over S subseteq U proper-subset T of f(U)*C(U,T\U).

The probability that the final reachable set in the full graph equals exactly T is q(T)=f(T)*C(T,V\T). Compute with exact Fraction and reject negative or non-normalized masses. This subset-cut recurrence does not enumerate complete Bernoulli edge worlds and does not traverse chronological attempt trees. Original R121 algorithms may be called only after computing q(T) for equality comparison.

## Frozen cases and rejection gates

1. All labeled loop-free directed graphs n=1,2,3 (1,4,64), all seed sets, two frozen edge probability schemes: HALF p=1/2 for every present edge; PARITY p=1/4 when (source+target) even and 3/4 otherwise. Exactly 1060 graph-seed-scheme comparisons. Require exact equality of every terminal-set mass with both original R121 algorithms.
2. Independent analytic fixtures: two incoming edges p=1/2 and 1/4, both sources seeded, target activation 5/8 and expected size 21/8; chain 1/2,2/3,3/4 expectation 25/12; directed 3-cycle p=1/2 expectation 7/4.
3. Reject wrong alternative mechanisms: LT at-most-one-inbound activation probability 3/4 versus IC 5/8 for the two-source case; erroneous two-try probability 3/4 versus one-try p=1/2 for a single edge.
4. Original R121 source, original test and original report Git blob identities must match the current repository before comparison. Re-execute the 48 original tests under Python 3.11 and 3.12.
5. Independently generated full terminal-set raw CSV must be byte-identical to the deterministic output of the new algorithm. Deliberately changed CSV row and wrong expected SHA must both be rejected. Archive CSV and source.
6. Formal E1 acceptance only after actual free standard public Ubuntu Actions run has both Python versions successful, source/CSV receipt, negative controls and no conflict with concurrent changes.

A mismatch or missing file is FAIL/OPEN. Max grade `PASS_BOUNDED_INTERNAL_SUBSET_CUT_RECURRENCE_E1`. No human E2, historical E3, real network edge estimation, sample-out prediction, external-team replication or model fusion. R073 and PESEN v0.1 frozen.
