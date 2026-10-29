# Theory handoff TH131 2026-10-29

track: theory
subflow: main theory; C and D read only
run_date: 2026-10-29 Asia/Singapore
observed_head: 122e27fdee969f113fa8f07171ddfbc6e59ac2f2
target_key: (theory, TH131/CDC_ICD9_ICD10_COMPARABILITY, v1-theory, preliminary-final published aggregate audit and subgroup transport bounds)
activity: completed
status: COMPLETE (THEORY_NOTE_BOUNDED); individual-record replay BLOCKED
claim_lease: none
source_links: https://stacks.cdc.gov/view/cdc/6425/cdc_6425_DS1.pdf ; https://www.cdc.gov/nchs/hus/sources-definitions/comparability-ratio.htm ; https://www.cdc.gov/nchs/nvss/mortality/comparability_icd.htm
work_performed: direct read of 2001 original Table1 and methodological sections, 2026 final official table, 2006 injury original selected sections; 16 conditional propositions, 8 arithmetic/synthetic audits and eight preliminary-final published comparisons
evidence_scope: nonblind official aggregate and mathematical examples; no raw ZIP/XLS, no individual records, no independent causal estimate or forecast; R E1/E2/E3 new 0
results_seen: TH129/TH130; C006 blob e7ea4d1ddf5045fe61c74192df730bee35bb7136; D002 blob b2556a008eca156222acd3f3b85caa50f85c5fac; main R266 S62 at initial read; open Codex PR including #1 unmerged
output_paths: theory/TH131_CDC_COMPARABILITY_PRELIM_FINAL_SUBGROUP_MISSINGNESS_TRANSPORT_2026-10-29.md; theory/INDEX.md; research/coordination/theory/20261029T121704Z-th131-cdc-comparability-handoff.md
commit_sha: SAME_AS_CONTAINING_COMMIT
PR: null
ci_status: NOT_RUN
billing_checked: free public sources and existing GitHub only, [skip ci] commit; no paid API/service
blockers: official final XLS, 130MB ZIP/DAT, SAS/Read_Me original bytes and full rowwise crosswalk; source files unverified
next_action: TH132 official final 113-cause table counts/SE, definition version alignment, subgroup transport bounds
