# Theory handoff TH130 2026-10-29

track: theory
subflow: main theory; C and D read only
run_date: 2026-10-29 Asia/Singapore
observed_head: 9a512a4547024635ea578c181fc42e7d81777bf4
target_key: (theory, TH130/CDC_ICD9_ICD10_1996_PUBLIC_USE, v1-theory, original documentation and missingness audit)
status: COMPLETE bounded original documentation review; individual record validation BLOCKED_ON_ZIP_DOWNLOAD
claim_lease: none
source_links: https://ftp.cdc.gov/pub/health_statistics/nchs/datasets/Comparability/icd9_icd10/ICD9_ICD10_comparability_file_documentation.pdf ; https://ftp.cdc.gov/pub/health_statistics/nchs/datasets/Comparability/icd9_icd10/ ; https://www.cdc.gov/nchs/hus/sources-definitions/comparability-ratio.htm
work_performed: read original 58-page dictionary selected pages; confirm 144 variables and field offsets, 2318212 records and 21290 missing; 16 conditional propositions and 8 aggregate/synthetic audits; document download failures
evidence_scope: nonblind theory and official aggregate arithmetic; no ZIP bytes, no individual record replay, no independent causal estimate, E1/E2/E3 new 0
results_seen: TH129; C006 2026-10-29; D002 2026-W44; R265 S61; seven open Codex PRs including #1 and #3 unmerged
output_paths: theory/TH130_CDC_PUBLIC_BRIDGE_FILE_DICTIONARY_MISSINGNESS_VINTAGE_AUDIT_2026-10-29.md; theory/INDEX.md; research/coordination/theory/20261029T111250Z-th130-cdc-bridge-dictionary-handoff.md
commit_sha: SAME_AS_CONTAINING_COMMIT
PR: null
ci_status: NOT_RUN
billing_checked: no paid service or CI
blockers: ZIP/DAT bytes, SAS/Read_Me bytes, full usage terms, 1996 universe delta
next_action: TH131 subgroup missingness bounds and historical transport with official aggregate tables
