# TH196 theory handoff
track: theory
subflow: main
run_date: 2026-11-01 (Asia/Singapore)
observed_baseline_head: e52fd34f4c8aabb3db2e4cfefcfefdb8193cb187
target_key: (theory,Chan2009+RoedigerKarpicke2006+AngristImbensRubin1996+Lee2009,theory-v1,retrieval_reactivity_exposure_compliance_attrition_bounds)
status: COMPLETE_BOUNDED_THEORY_NOTE; SCIENTIFIC_ACCEPTANCE_NOT_RUN
nonblind_scope: TH193 TH194 TH195 read; original Chan2009 author manuscript PDF pages 3 to 15; other original abstracts and bibliography
outputs: theory/TH196_RETRIEVAL_REACTIVITY_COMPLIANCE_ATTRITION_BOUNDS_2026-11-01.md; theory/th196_reactivity_compliance_attrition_audit.py; theory/INDEX.md
note_commit: 0f964fb2c29136e3cba27a372fe86b261014d524
script_commit: 52fcf6c257d8dd57e25112e96499f09b922f5f02
script_blob: f25c3a1a58e13fe20b47e5cf4512844e3e9bcd4d
results_seen: synthetic 2x2 interaction +1/4; exclusion failure Wald 1/2 versus 7/10; attrition ATE bounds [-1/8,5/8]; monotone-selection always-observed bounds [0,1/2]
local_tests: 25 unittest ordinary PASS; 25 unittest python -O PASS; no real data
science_evidence: NONBLIND; SYNTHETIC_ONLY; R E1/E2/E3 unchanged
C_today: C009 already present 2026-11-01; unchanged
D_week: D002 already recorded 2026-W44; unchanged
codex: open PR #1 comparator gap and #3 candidate fix not merged; PR #2 workflow protocol also unmerged
ci_status: NOT_TRIGGERED; all commits [skip ci]; actual account billing NOT_CHECKED
next_action: TH197 group-level network interference and informative attrition, after fresh main HEAD and target recheck
handoff_note: coordination is advisory, not an atomic lock; no active claim
