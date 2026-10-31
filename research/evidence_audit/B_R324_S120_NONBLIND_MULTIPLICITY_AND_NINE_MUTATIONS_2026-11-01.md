# B independent method audit: R324 S120

Date: 2026-11-01 UTC. Status: PASS_NONBLIND_INTERNAL_E1_WITH_NATIVE_CLI_OPEN.

## Scope and independence
Read the frozen R324 original protocol, 64 row source, R S120 freeze, R code and persisted S120 CSV/JSON before audit. This is a nonblind internal methodological recheck, not an external team or blinded replication. B source: research/evidence_audit/b_r324_s120_independent_du_oracle.js. The B algorithm uses D/U count multiplicities (1,2,1)x(1,2,1) to compute the six observation partitions without importing the R script or enumerating R's bit-state observation Map. Separately, an independent local Python Fraction script enumerated the 16 states and agreed on all exact fractions.

## Actual persisted source verification
Original R324 CSV Git blob 1b0062eeea020606a3d510d566da43db03ace8d9, 64 rows.
R S120 CSV Git blob eeef39b66165e2ec0a918ccedb4f038b078cd05b, 64 rows.
R S120 JSON Git blob a95be44193a4a7890203049d5615b4f27c93453e.
B directly read all three files from main using GitHub connector, verified 64 source identities, 64 persisted observation rows, each score, each threshold and both ordinal comparisons, six policy summaries, the 3 distinct full ranking profiles, W2/W3 identical ordinal rankings and 15 differing cardinal scores. All matched independent 3x3 count calculations. V8 executed the archived B source body after shebang removal for in-memory evaluation.

Exact policy accuracies: 1/4, 45/64, 13/32, 15/32, 15/32, 9/16. Full profile: 3/4.

## Negative controls
Nine mutations injected into actual persisted inputs or receipt and all rejected:
1 missing atom; 2 duplicated atom; 3 score tamper; 4 threshold tamper; 5 ordinal comparison tamper; 6 world identity tamper; 7 policy accuracy tamper; 8 full profile grouping tamper; 9 false human E2 claim. PASS 9/9 rejected.

## Failure chronology
Initial B oracle code computed only one maximal observation-cell contribution per D/U group and produced a mismatch against R; this was a B implementation mistake. Corrected by summing contributions across all distinct observation cells with multiplicity. No R score or frozen protocol changed. Second B attempt passed the substantive audit but its mutation runner used structuredClone, unavailable in the V8 isolate; changed to JSON parse/stringify clone and reran. Final nine mutations and full audit PASS. Both failures are retained here; they are not evidence of empirical model performance.

## Scientific gates
No data leakage test against real humans, no human baseline, no held-out empirical prediction, no empirical calibration, no bootstrap/cluster uncertainty, no E2/E3, no external blind team. Finite exhaustive E1 results have no sampling uncertainty under the specified uniform prior. The 3x3 B route shares the frozen model assumptions with R. Original source and receipt identity are independently checked within the same project.

Original R archived Node native CLI: NOT_RUN. B archived Node native CLI: NOT_RUN. CI: NOT_DISPATCHED because free Actions billing balance is not independently verified. PASS applies only to executed V8 oracle and local Python arithmetic, not native CLI or real-world scientific validation.
