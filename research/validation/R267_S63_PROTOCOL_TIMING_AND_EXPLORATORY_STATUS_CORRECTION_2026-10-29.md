# R267 S63 protocol timing correction and exploratory status

Date: 2026-10-29 UTC. This correction has precedence over any contradictory statement in the S63 R scientific report, B audit, frozen-file title, machine receipt or coordination handoff. Original files remain byte-for-byte unchanged for auditability.

## Observed execution order

Before GitHub commit `6b086febb09dcf5da854bad0e2e5cc256b2ca2a7` created `protocols/R267_S63_FINITE_TAIL_RISK_PRESCORE_FREEZE_2026-10-29.md`, the same execution context had already run an exploratory Python calculation of the R267 nine-world IID/LHS tail probabilities at thresholds `1/3` and `2/3`. Those results were visible when the S63 protocol was written.

Consequently, the protocol was committed before the *archived S63 result receipt* and before the later formal V8 calculation, but **after preliminary S63 outcome inspection**. The filename `PRESCORE_FREEZE` and report language asserting genuine prescore or prospectively selected thresholds overstate the actual timing. The two thresholds and the ranking reversal must be treated as `EXPLORATORY_RESULT_INFORMED`. No claim of strict preregistration, blindness or prospective confirmatory discovery is supported.

## What remains verified

The original R267 nine-world frozen source universe and original formal E1 acceptance are unchanged. The S63 archived receipt was derived with exact rational arithmetic from the original PMFs. A separate full 6885-primitive V8 enumeration and local Python enumeration agreed with all 18 S63 rows; six in-memory negative controls were rejected. These are internally reproducible arithmetic findings and valid finite artificial counterexamples. They do not become prospectively tested scientific hypotheses by a later protocol commit.

B verification remains `NON_BLIND_INTERNAL`. Archived Python CLI native execution `NOT_RUN`. New real-human E2=0, historical E3=0, external team independent replication=0. R073 and PESEN v0.1 remain frozen.

## Corrected acceptance

`S63_EXPLORATORY_E1_EXACT_ARITHMETIC_WITH_INTERNAL_CROSSCHECK=PASS`.

`S63_STRICT_PRESCORE_FREEZE=FAIL_TIMING`.

`S63_PROSPECTIVE_CONFIRMATORY_TEST=NOT_RUN`.

Future confirmatory testing requires a genuinely prospective freeze before looking at new independent functions, data or other untouched targets, with a new protocol ID and preserved exploratory history. The present nine-world S63 results cannot be retrospectively converted into an unseen holdout.
