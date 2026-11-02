# R127 / original239 05-003: original 1990 Table 2, all ten periods, direct visual source check

track: R+B; A scout briefly checked
run_date_utc: 2026-11-02
local_date: 2026-11-03 Asia/Singapore
starting_main: fdf236fa0007062645c6fcc8a751738e7de0273d
source_script_commit: 59ba2557834cf1111a202ed41d7fc399878c183a
source_script_blob: aa575a803e5547afe24eabc1f232f2b539ef1709
status: COMPLETE_BOUNDED_SINGLE_READER_SOURCE_CHECK / FORMAL_QUEUE_PARTIAL
target_key: (R+B,original239-05-003/R127,2026-10-20-freeze,1990-Table2-all-periods-primary-scan-reinspection)
evidence: PUBLISHED_HUMAN_AGGREGATE_SOURCE_AND_INTERNAL_NONBLIND_ARITHMETIC; new_E2=0; new_E3=0
CI: NOT_RUN; billing/free_quota: NOT_VERIFIED

## Primary source and frozen boundary

Directly inspected the actual scanned English-language 1990 AER article, Van Huyck, Battalio and Beil, *Tacit Coordination Games, Strategic Uncertainty, and Coordination Failure*, AER 80(1), pp.234–248. UCSD-hosted scanned original:
https://econweb.ucsd.edu/~jandreoni/Econ264/papers/Van%20Huyck%20et%20al%20AER%201990.pdf

Read image page index 6 (printed p.240, experiments 1–4) and page index 7 (printed p.241, experiments 5–7), and the printed narrative at pp.239,242. The PDF has effectively no extractable table text; this was direct visual reading, with no OCR. No full PDF bytes were saved, so this run cannot give a verified PDF file hash. Source hosting and scan identity were observed, not independently authenticated against the publisher's master.

R127 frozen protocol: `protocols/R127_VAN_HUYCK_1990_MINIMUM_EFFORT_ORIGINAL_TABLE2_AND_2X2_RISK_SELECTION_FREEZE_2026-10-20.md`, blob `4734ede5133701d622acfda76c4f9474bf660b21`. Its original scope transcribed only period 1 and period 10, seven effort levels per experiment. Existing R127 model source blob `6964fa57e291e719e8cc071cc3a70d73836363e4`. Prior independent finite-math audit `research/validation/R127_05_003_ORIGINAL239_P0_INDEPENDENT_FINITE_ITEMWISE_AUDIT_20261102T1943Z.md` did not reread the original scan.

This run newly transcribed all 10 printed periods, including 56 intermediate experiment-period columns (392 additional numeric cells). The total transcription has 7 experiments × 7 effort rows × 10 periods = 490 integer cells. It is supplementary descriptive source evidence. It does not revise frozen model definitions, source scope, scoring or historical scientific acceptance.

## Reproducible source arithmetic

Script: `research/validation/r127_primary_table2_70_periods_source_audit_20261103.js`. The source was actually executed in the current JavaScript V8 environment as a deterministic function, using integer sums. No randomness; seed N/A. Node.js CLI was NOT_RUN.

Execution receipt:
```json
{
  "status":"PASS_BOUNDED_SOURCE_TRANSCRIPTION_CONSISTENCY",
  "printed_cells":490,
  "session_period_columns":70,
  "group_period_sum_checks":70,
  "printed_minimum_checks":70,
  "frozen_endpoint_vectors_checked":14,
  "new_middle_period_columns":56,
  "published_subjects":107,
  "first_period_7":33,
  "first_period_1":2,
  "tenth_period_1":77,
  "count_effort1_by_period":[2,5,15,25,37,50,47,70,72,77],
  "effort_sum_by_period":[560,454,375,306,254,217,223,171,165,186],
  "negative_controls_rejected":6,
  "individual_transitions_identified":false,
  "independent_second_reader":false,
  "new_E2":0,
  "new_E3":0
}
```

All 70 experiment-period columns sum to the independently printed experiment sizes [16,16,14,15,16,16,14]. All 70 derived minima match the original printed `Minimum` rows. All 14 period-1/period-10 seven-cell vectors match the previously frozen protocol, including 107 subjects, 33 selecting effort 7 initially, two selecting effort 1 initially, and 77 selecting effort 1 at period 10. The original prose's rounded 31% and 72% are consistent.

Six actual negative controls rejected: negative cell, missing period, broken column total, balanced frozen-endpoint mutation, wrong printed minimum and wrong experiment size. These test internal consistency and the preexisting frozen anchors; they do not prove all middle-period cells were transcribed correctly.

New descriptive observation: the total count choosing effort 1 is not monotone across periods, falling from 50 at period 6 to 47 at period 7. The total effort sum also rises from 165 at period 9 to 186 at period 10. These are published aggregate margins across the same seven groups, not participant-level transitions, independent test predictions, learning coefficients or causal effects. The original paper's qualitative convergence interpretation must not be rewritten as a strictly monotonic time-series law.

## Scientific acceptance boundary and open issues

Source check improves itemwise provenance for R127 05-003. It has a single visual transcriber and no blinded second entry. Compensating middle-period transcription errors can survive column sums and printed-minimum checks. A second independent source-image transcription and an explicit comparison of all 490 cells would be valuable before formally closing this item. The original article's subject-level data and session trajectories were not obtained; no individual transitions or E2/E3 prediction scores were inferred.

The original239 pending CSV blob `3b96d46b3d88ccafd779a08509c3cfd0e435772f` still has 154 rows, P0=27/P1=82/P2=45. Row 05-003 remains `PROVISIONAL_PRIMARY_README_LINK` and `ITEMWISE_PRIMARY_SOURCE_AND_SCIENTIFIC_EVIDENCE_AUDIT_REQUIRED`. The crosswalk v7.8 blob `36f24235901172642c46853298aebb421f1a3552` and pending CSV were read, not modified. Formal pending net reduction: zero.

At entry there were 12 open draft Codex PRs. PR #1 and #3 were confirmed open, both scoped to R257 S53. No matching open PR covered this R127 primary-source reinspection. R272 production fail-closed workflow integration remains P0 OPEN; the current environment cannot clone the full repository through git due to DNS/network restrictions. The pinned single-entrypoint's full trusted-checkout run and Actions were NOT_RUN. R257 S53 blind failure and R333–R340 composite caller issues remain unresolved unless separately proven closed. R073 and PESEN v0.1 remain frozen.

## A scout and cost

Brief English-source search revisited known Montero-Porras and Grujić human repeated-game datasets. A potentially separate 2026 OpenNeuro/NeMAR EEG Prisoner's Dilemma dataset `ds007822 / ON007822` lists 11 triads and 33 participants, with behavioral labels in `events.tsv`: https://github.com/OpenNeuroDatasets/ds007822 . A secondary EEGDash listing describes CC0, while the upstream GitHub `LICENSE` file explicitly says license information was not provided with source files. Treat dataset permission as UNKNOWN until the authoritative OpenNeuro dataset license/version is checked. Participant-level events, trial chronology, independent session structure, checksum and R073 freeze compatibility were NOT_RUN. New eligible/scored dataset: zero.

No new paid service, data purchase, personal data access, CI dispatch, or workflow modification. GitHub billing and remaining Actions free quota not independently verified. GitHub source archive uses [skip ci] and is not evidence of Actions execution.

Next action: obtain a complete trusted checkout for R272's original single-entrypoint execution and production enforcement audit without triggering unverified Actions costs. If that remains blocked, independently double-enter the original R127 Table 2 source-image cells and compare all 490 values; then request separate formal queue disposition review.
