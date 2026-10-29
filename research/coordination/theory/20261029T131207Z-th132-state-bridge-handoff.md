# TH132 theory handoff 2026-10-29

track: theory
subflow: theory main; C and D read only
run_date: 2026-10-29 Asia/Singapore
observed_head: 81c5b03c4a8dc3cf5ef6d06d0b68d09712f5382d
target_key: (theory, CDC_ICD9_ICD10_113CAUSE_TH132, theory-v1, official final table access and state bridge uncertainty/rounding/vintage)
activity: completed
status: COMPLETE (THEORY_NOTE_BOUNDED); final XLS raw replay BLOCKED
claimed_at_utc: N/A
expires_at_utc: N/A
source_links: https://www.dhs.wisconsin.gov/stats/deaths/icd10-9comparetable.pdf ; https://stacks.cdc.gov/view/cdc/6425/cdc_6425_DS1.pdf ; https://www.cdc.gov/nchs/hus/sources-definitions/comparability-ratio.htm ; https://ftp.cdc.gov/pub/health_statistics/nchs/datasets/Comparability/icd9_icd10/
work_performed: Wisconsin 9-page official state table specified-page audit; NCHS preliminary count and SE cross-check; 16 conditional propositions and 8 arithmetic/synthetic audits; documented rounding and interval-method sensitivity
evidence_scope: nonblind official aggregate and mathematics; no final 113-row XLS, no individual-level data, no independent causal/forecast; R E1/E2/E3 new 0
results_seen: TH129 to TH131, C006, D002, main R267 S63 and open Codex PR #1 to #7 (unmerged)
output_paths: theory/TH132_STATE_BRIDGE_ROUNDING_UNCERTAINTY_113_CAUSE_VINTAGE_2026-10-29.md; theory/INDEX.md; research/coordination/theory/20261029T131207Z-th132-state-bridge-handoff.md
commit_sha: SAME_AS_CONTAINING_COMMIT
PR: null
ci_status: NOT_RUN
billing_checked: free official sources, existing GitHub only; [skip ci], no new paid actions
blockers: official final XLS byte access and 130MB ZIP/SAS, exact final 113 cause counts and standard errors NOT_VERIFIED
next_action: TH133 cross-region ratio transport and interval uncertainty, or actual final XLS rowwise audit if free bytes available
