# E124: R294 S90 original B receipt metadata mutation gate

UTC 2026-10-30. Track operations. Target (operations,R294,S90-v1,original-B-nine-unchecked-receipt-metadata-fields). Baseline main 37a5f525a0a6c67499a09840bc7513db57fa3c6e. Status COMPLETE_BOUNDED_NONBLIND_DYNAMIC_ENGINEERING. Scientific S90 PARTIAL.

## Source identities and actual work

Read latest main commits, R294 S90 freeze, R/B reports, A data gate, R handoff, E123, TH159, owner workflow and all 12 open codex/* PR titles/abstracts including #1, #2, #3. Original B checker research/evidence_audit/b_r294_s90_independent_direct_formula_20261030.js Git blob c9ab6638e389b7f9debd72ca1cf49a20801c641e. Original R294 144-row CSV blob 098e45b9ba81de9bd7dc59c0a3466083b03e6ab4. S90 288-row CSV blob 362903ece27b1607580829902c991757884c74cb. S90 JSON blob 7f7493ab534e35dd9fe3fb766b8695b0c606a0c8. Frozen S90 protocol commit 905467c19d04c01b4fea3f26592625fbc8229d13 predates results.

Original B audit function was loaded unchanged in V8 and run against connector-fetched persisted original CSV, S90 CSV and JSON. Baseline PASS: original_rows=144, new_rows=288, worlds=72, summary_cells=12, family reversals H=8, EXP=0, Q=7. Each of nine JSON fields was independently replaced by a wrong value, then deleted, leaving all numeric CSV and summary data unchanged. All 18 variants returned PASS: research_id, stage, status, freeze_commit, original_source_blob, fees, original_reversals, R073, PESEN_v0_1. Three positive rejection controls were correctly rejected: evidence=E2_HUMAN, new_E2=1, summary[0].purchases=999. The nine earlier B negative controls remain separately valid. These 18 new false accepts show missing receipt metadata binding, without demonstrating errors in persisted numeric results.

Reproducible script research/operations/e124_r294_s90_metadata_mutation_20261030.js calls the original B module and archived files in a checkout. Native Node CLI NOT_RUN; V8 original-function replay actually executed. This is NONBLIND internal engineering verification and not independent external scientific replication. Original R294 CLOSED_BOUNDED_E1 unchanged, S90 PARTIAL, new E2/E3=0.

## Governance and remediation boundary

R293 S89 E123 unchecked research_id/scope and optional baseline issue remains open; R290 S86, R291 S87, R286 S82 and R281 S77 historical issues remain open unless separately closed. A-track Zhang Ma 2024 OSF raw data access still blocked; theory TH159 C008 additive. Twelve Codex PRs remain OPEN_UNMERGED; #1 R257 S53 comparator blind failure and #3 strict checker candidate cannot be counted as main adoption. No frozen protocol or other-track result modified.

Suggested B-owned candidate: validate exact metadata identities/types, fixed fee grid, original reversal summary, freeze/source provenance and frozen project evidence states; add 18 cases to regression suite. No CI or new paid services initiated. Actual billing/free quota NOT_VERIFIED. Next E125: native CLI if available; latest R stage and R293 S89 gap follow-up.
