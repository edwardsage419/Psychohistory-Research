# R121 original239 04-004: independent subset-cut recurrence E1 audit

Date: 2026-10-24. Final bounded scientific grade: **PASS_BOUNDED_INTERNAL_SUBSET_CUT_RECURRENCE_E1**.

## Original research reused

Kempe, Kleinberg and Tardos (2003), *Maximizing the Spread of Influence through a Social Network*, DOI 10.1145/956750.956769; author PDF https://www.cs.cornell.edu/home/kleinber/kdd03-inf.pdf . Claim 2.3 equates independent one-chance propagation and independently pre-flipped live-edge reachability in full final-set distribution. Theorem 2.2 concerns expected influence submodularity. Existing R121 2026-10-19 code, 48 tests, source report and frozen protocol were reused unchanged.

New protocol frozen before implementation at commit `22ce983ba369843e4dd5124b147ec14f8dbd7d45`.

## Independent mathematical mechanism

Let f(T) be the probability every vertex in T is reachable from seeds S within the graph induced by T. For each T containing S, calculate f(T) recursively by subtracting the probability that the reachable set is a proper U subset of T, with all U-to-(T\U) edges blocked. The final full-graph probability of terminal set T is f(T) times the probability all T-to-(V\T) edges are blocked. All operations use exact rational arithmetic. The method requires neither full-edge Bernoulli-world enumeration nor a chronological activation event tree.

New program `research/validation/verify_r121_subset_cut_recurrence.py` independently computed the complete terminal distributions for all n=1,2,3 directed loop-free labeled graphs (69 graphs), all seed sets, and two probability schemes (HALF and PARITY). This yielded **1060** graph-seed-scheme cases and **1932** nonzero terminal-set raw CSV rows. Every full distribution matched both original R121 methods exactly. Committed CSV:
`research/validation/R121_SUBSET_CUT_1060_CASE_TERMINAL_DISTRIBUTIONS_2026-10-24.csv`;
SHA256 `60010a03972f41a091987e5d2be55d28347736c46af6cc28fc0bfab803c8efcb`.

Three analytic fixture conditions passed: two-source IC expected 21/8 with target activation 5/8, four-node chain expected 25/12, and directed three-node cycle expected 7/4. Two negative controls reject the mistaken LT two-source probability 3/4 and a repeated-attempt single-edge probability 3/4 in place of correct one-shot 1/2. Two tamper controls reject altered raw CSV and incorrect Git blob SHA. Three original file blob identities matched.

## CI and independent validation

GitHub Actions run https://github.com/edwardsage419/Psychohistory-Research/actions/runs/40083743480 finished `completed/success` on both Python 3.11 and 3.12. Each job logged 1060 exact comparisons, 1932 raw rows, two negative controls, two tamper rejections and the same CSV SHA256. Both versions re-executed all **48 original unit tests** with zero failures. Original R121 source acceptance run is https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39256571643 .

This is an independent mathematical algorithm inside the same research project. The 1060 artificial cases are not 1060 people or real social networks. New real human E2 prediction scores: **0**. New historical E3: **0**. No external research team independently reproduced these results. No human causal mechanism, fitted network edge probabilities, real large-network optimization performance, out-of-sample prediction or calibration is established.

R073 and PESEN v0.1 remain frozen. The original239 link 04-004 can receive bounded E1 reattribution; further R-series studies and evidence audits remain open.
