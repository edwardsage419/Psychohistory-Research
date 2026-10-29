# Theory handoff TH129 2026-10-29

track: theory
subflow: main theory; C and D read only
run_date: 2026-10-29 Asia/Singapore
observed_head: b465af9b435ce6ea4ce3dd9498eac8f8d110c026
target_key: (theory, TH129/ICD9_ICD10_1996, v1-theory, verification selection and transition transport)
activity: completed bounded theory research; no claim or lease
status: COMPLETE for bounded note; scientific validation NOT_RUN
source_links: https://www.cdc.gov/nchs/data/nvsr/nvsr49/nvsr49_02.pdf ; https://ftp.cdc.gov/pub/health_statistics/nchs/datasets/Comparability/icd9_icd10/ ; https://link.springer.com/article/10.1007/s10680-013-9307-4
work_performed: verified CDC 1996 sample selection counts and public dataset listing; 16 conditional propositions; 2 original aggregate arithmetic checks and 6 synthetic audits
evidence_scope: nonblind theory; no public-use ZIP download, no record-level replay, no independent causal estimate, E1/E2/E3 new 0
results_seen: TH128; C006 (2026-10-29); D002 (2026-W44); R264 S60; seven open Codex PRs including PR #1 and #3, unmerged
output_paths: theory/TH129_DUAL_CODE_VERIFICATION_SELECTION_TRANSITION_TRANSPORT_NEGATIVE_CONTROLS_2026-10-29.md; theory/INDEX.md; research/coordination/theory/20261029T101127Z-th129-dual-code-selection-handoff.md
commit_sha: SAME_AS_CONTAINING_COMMIT
PR: null
ci_status: NOT_RUN
billing_checked: no paid operation or new CI
blockers: 130240471-byte public-use ZIP and dictionary bytes not retrieved; individual record transitions and data-use terms unverified
next_action: TH130 verify accessible original public-use file, dictionary and version; if unavailable perform conditional transport sensitivity analysis
