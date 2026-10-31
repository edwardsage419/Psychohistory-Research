# R track handoff R305 S101

utc: 2026-10-31T02:45:13Z
track: r
subflows: R-main, A-public-data, B-independent-method-internal-audit
baseline_main: d9debc5cefa930ea54a8ccd106775bf417d3b602
freeze_commit: 04dcb04d465002c6f0292887f49ab19f39aa5a11
pre_handoff_head: 34876551756681ed3534ab55f3045da20af0c017
target_keys: (r,R305,S101-v1,interpolated-feature-context-category-switching); (A,Neville-2020-Hive,OSF-kjt4u,raw-data-license-and-session-gate); (B,R305,S101-v1,nonblind-independent-Fraction-and-optimized-assert-gate)
claim: NO
status: R PARTIAL, A RAW_DATA_BLOCKED, B INTERNAL_NONBLIND_PASS_WITH_V1_FAILURE_RETAINED
source_read: original R305 original frozen protocol, README, scientific report, 243-world JSON, original239 v7.8, pending154, latest other-track handoffs, all 12 open Codex PR titles and summaries. No overlap with PR #1/#3, both unmerged.
R: 405 synthetic decision worlds, 810 category source cells, 81 fixed configurations, 324 adjacent comparisons, 36 switches, hist 55/16/10/0/0. Original X/MID/Y parity 243/243. Frozen original R305 untouched.
R_artifacts: research/validation/R305_S101_INTERPOLATED_CONTEXT_PRESCORE_FREEZE_2026-10-31.md; research/validation/r305_s101_interpolated_context.js; research/validation/R305_S101_ALL_405_CONTEXT_WORLDS.csv; research/validation/R305_S101_EXACT_RESULTS.json; research/validation/R305_S101_INTERPOLATED_CONTEXT_SCIENTIFIC_REPORT_2026-10-31.md
A: Neville et al 2020 PLOS ONE DOI 10.1371/journal.pone.0241227, 965 analyzed humans, groups 4-12, 3 tasks. Official St Andrews OSF dataset listed, public OSF link returned HTTP403. Raw fields, exact file license and hashes UNKNOWN. R073 ineligible.
A_artifact: research/data_scout/A_NEVILLE_2020_HIVE_SELF_CATEGORIZATION_965_HUMAN_OSF_ACCESS_GATE_2026-10-31.md
B: independent local Python Fraction route regenerates archived 27133-byte CSV Git blob b940c07bfe6d2ef4f29c806f752b6989202af63f and 22216-byte JSON Git blob e3771b29c4e7eeaeef57690ecd9541880881a15c; 9 mutations rejected. v1 python -O FAIL (mutation escaped) retained; explicit v2 ensure gates normal and -O PASS, 9 rejected each. Archived v2 exact remote CLI NOT_RUN.
B_artifacts: research/evidence_audit/r305_s101_independent_fraction_audit.py; research/evidence_audit/r305_s101_independent_fraction_audit_v2.py; research/evidence_audit/B_R305_S101_NONBLIND_FRACTION_AND_OPTIMIZED_GATES_2026-10-31.md
original239_crosswalk_blob: 36f24235901172642c46853298aebb421f1a3552
pending154_blob: 3b96d46b3d88ccafd779a08509c3cfd0e435772f
ci: NOT_RUN, check_runs=0, statuses=0, actions_head_sha_runs=0 as observed at pre_handoff_head
billing: no new chargeable operations, no Actions triggered; actual account balance/remaining free quota NOT_VERIFIED
evidence: E1 only; E2=0, E3=0; external independent replication=0; R073 and PESEN v0.1 frozen
next: R306 after fresh queue and claim read; if time prioritize native Node R305 S101 and archived Python v2 CLI with actual remote bytes, assess A OSF fields/permission if publicly accessible; preserve v1 -O failure and Codex PR #1/#3 pending state.
