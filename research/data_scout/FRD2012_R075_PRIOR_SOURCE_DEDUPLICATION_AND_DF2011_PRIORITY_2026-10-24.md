# A public data scout: FRD2012 prior-use reconciliation and next-source priority

Date: 2026-10-24. Baseline main HEAD observed: `3a8ac22b9d271848e3838428721d2a8f6975b6d6`.
Status: `DEDUPLICATED_EXISTING_HUMAN_EXPERIMENT; DF2011_ROW_LEVEL_GATE_OPEN`.
This is a provenance reconciliation. No new human model scores are computed.

## Repository-internal evidence actually checked

1. `research/data_scout/FRD2012_INDEPENDENT_HUMAN_PD_SOURCE_REGISTRY_2026-10-24.md` describes Fudenberg, Rand and Dreber (2012), DOI 10.1257/aer.102.2.720, as a potential R073 external replication source with a third-party 13,126-row stratEst RDA and missing original session identifiers.
2. `research/R075/R075_PHASE_A_THIRD_HUMAN_SOURCE_RECOVERY_AND_LAG_SEMANTICS_2026-10-17.md` already states that the early third-party data gate was later superseded by recovery of the original coauthor archive. It reports an observed 13,126-row derived-data schema, 11,590 contiguous lag comparisons, 1,163 own-action mismatches, and unresolved session identification *within that derivative file*. These are earlier project observations, not newly repeated measurements.
3. `research/R075/R075_FINAL_ACCEPTANCE_STATUS.json` records a coauthor-hosted original archive, 1,129,409 bytes, SHA256 `328346c3cf88a71a3d6cf574f7d6ba741dcea460f3926c16266f1784d3a699ef`, 18 original file sessions, 34,446 intended action rows and 26,116 t>=3 scored choices, with pre-frozen R073 model family and a prior session-heldout evaluation. Its own limitations include unknown physical cross-session reenrollment and untested zero-shot cross-experiment parameter transfer.
4. `research/R075/R075_REAL_THIRD_HUMAN_E3_RESULTS_AND_SCIENTIFIC_BOUNDARIES_2026-10-17.md` and R075's archived results are the authoritative prior study for that experiment. The word `E3` in the historical R075 *study title* refers to the third independent human experimental source. Under the present project-wide evidence taxonomy, this is a human repeated-game experiment, not a historical event E3 dataset. Preserve the original title while avoiding evidence-tier inflation.
5. `research/data_scout/DF2011_REPEAT_PD_PUBLIC_SOURCE_REGISTRY_2026-10-24.md` concerns a different Dal Bo and Frechette (2011) human repeated PD experiment, DOI 10.1257/aer.101.1.411. Its raw 7,358 rows and six fields remain documentation declarations because the fixed RDA blob has not been decoded in this workflow. Independent original session identities, participant overlap and partner pairing remain unverified.

## New decision and falsifiable next gates

**FRD2012 is already a previously studied source in R075.** The third-party stratEst representation is a *different data representation* of the same 2012 experiment. Reprocessing it cannot be advertised as a fourth independent human study. The earlier registry remains intact as a valid derivative-source gate record, with this note providing the later cross-workflow provenance correction.

**DF2011 remains a separate candidate** for a new source-eligible test. Before any scoring: (a) decode the exact fixed original binary and verify 7,358 row-level records and fields; (b) prove unique keys and within-game chronology; (c) identify independent sessions or an explicitly justified identity-disjoint evaluation design; (d) independently confirm that `input` is strictly previous-round information, while `other.choice` is contemporaneous; (e) document treatment-specific action semantics and R073 frozen feature compatibility; (f) freeze transfer protocol before viewing model outcomes. If any required gate fails, the score is `NOT_RUN`.

## Evidence and budget

This run verified the repository's existing provenance documents and found an actionable duplication risk. It did not download or decode new participant data, estimate an effect, establish an original-author equivalence of the third-party RDA, or reproduce R075 scores. New human E2 = 0; new historical E3 = 0. No participant identifiers are exported. No private data, registration, paid API, paid database or large runner was used. R073 and PESEN v0.1 remain frozen.
