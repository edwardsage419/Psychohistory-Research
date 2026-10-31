# TH167 theory track handoff
track: theory
subflow: TH167
run_date: 2026-10-31 Asia/Singapore
handoff_utc: 2026-10-31T00:10:33Z
observed_head_at_start: 0896ab9bd80aaacce14ac52f6fdbce45214e9416
target_key: (theory,MURALIDHARAN_NIEHAUS_SUKHTANKAR_SMARTCARDS_2014_2016,TH167-theory-v1,randomization_universe_vintage_and_household_flow)
activity: completed_bounded_note
status: COMPLETE
claim: NO
claim_expiry_utc: N/A
source_links: https://www.nber.org/system/files/working_papers/w19999/revisions/w19999.rev0.pdf ; https://econweb.ucsd.edu/~pniehaus/papers/statecapacity.pdf ; https://pubs.aeaweb.org/doi/10.1257/aer.20141346
work_performed: directly read 2014 NBER rev0 original methods and 2016 author manuscript section 3 and appendix C.1/C.2; inspected page 13 image; 14 conditional propositions, 12 arithmetic/synthetic audits; local standard-library Python PASS.
results_seen: 2014 113+195+45=353 versus 2016 112+139+45=296; 57 total difference and one Nalgonda treated unit; 2016 main-text baseline 8572 conflicts with appendix 8527, appendix reconciles 7425; endline 295 decomposes 287+8. Source-vintage identity remains unresolved.
evidence_scope: nonblind primary manuscript version comparison; no original mandal IDs, no raw microdata, no independent empirical causal estimate, R E1/E2/E3 increments 0.
output_paths: theory/TH167_SMARTCARDS_RANDOMIZATION_UNIVERSE_VINTAGE_DENOMINATOR_2026-10-31.md ; theory/th167_vintage_denominator_audit_20261031.py ; theory/INDEX.md ; research/coordination/theory/20261031T001033Z-th167-smartcards-vintage-handoff.md
commit_sha: null (self-referential same-commit field; inspect Git history and remote HEAD)
PR: null
ci_status: NOT_RUN (do not trigger billable Actions)
billing_checked: no new services or paid CI invoked; actual account charges not inspected
C_today: C008 already completed, blob 7baa21237c97630f1a5058ab13d36dc0fe2d5d87, unchanged
D_this_week: D002 already completed, blob b2556a008eca156222acd3f3b85caa50f85c5fac, unchanged
codex: PR #1 R257 S53 and candidate PR #3 remain unmerged review evidence
blockers: October 2014 revision, 2016 official full text, original randomization list, Nalgonda unit ID, raw household sample flow.
next_action: TH168 administrative identity, treatment weighting and selective inclusion bounds; keep R track separate.
