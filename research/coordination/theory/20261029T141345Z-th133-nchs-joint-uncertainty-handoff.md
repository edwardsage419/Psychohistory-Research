# TH133 theory handoff 2026-10-29

track: theory
subflow: theory main; C and D read only
run_date: 2026-10-29 Asia/Singapore
observed_head: 538c06ee04f53be5baa7c7f3f6894e93306cb46b
target_key: (theory, CDC_ICD9_ICD10_TH133, theory-v1, state transport × ratio sampling error × count uncertainty × model-dependent coding jump)
activity: completed
status: COMPLETE (THEORY_NOTE_BOUNDED); final XLS raw replay BLOCKED
claimed_at_utc: N/A
expires_at_utc: N/A
source_links: https://ftp.cdc.gov/pub/health_statistics/nchs/datasets/Comparability/icd9_icd10/CR_application_sate_guide.pdf ; https://www.cdc.gov/nchs/data/nvsr/nvsr49/nvsr49_08.pdf ; https://www.dhs.wisconsin.gov/stats/deaths/icd10-9comparetable.pdf ; https://doi.org/10.2478/jos-2020-0003
work_performed: original NCHS 51-page guide formula 3 and 2001 NVSR formula 15 direct reading including page images; 16 conditional propositions, 8 arithmetic/synthetic audits; independent conditional variance and transport threshold calculation
evidence_scope: nonblind official aggregate plus mathematical conditional demonstration; no state population exposure verification, no final 113-row XLS, no individual-level causal/forecast; R E1/E2/E3 new 0
results_seen: TH129-TH132, C006, D002, main R268 S64, seven open Codex PR including unmerged R257 S53 gate
output_paths: theory/TH133_STATE_RATIO_TRANSPORT_JOINT_UNCERTAINTY_NCHS_Z_2026-10-29.md; theory/INDEX.md; research/coordination/theory/20261029T141345Z-th133-nchs-joint-uncertainty-handoff.md
commit_sha: SAME_AS_CONTAINING_COMMIT
PR: null
ci_status: NOT_RUN
billing_checked: free public sources and existing GitHub only; [skip ci], no new paid actions
blockers: final 208896-byte XLS raw access failed due DNS and unsupported binary fetch; final 113 rows/SE and Wisconsin population exposures NOT_VERIFIED
next_action: TH134 official state population exposures and subgroup transport or full final XLS if bytes become available
