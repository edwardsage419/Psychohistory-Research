# TH170 theory handoff
track: theory
subflow: TH170
run_date: 2026-10-31 (Asia/Singapore)
observed_head: 1ee41b37cd263a75652c090de3e3353dc2f16db3
target_key: (theory,ATANDA2019_SMARTCARDS_TABLE_A8_A9,TH170-theory-v1,card_status_missingness_outcome_denominators_and_partial_identification)
activity: completed_bounded_note
status: COMPLETE
claimed_at_utc: N/A
expires_at_utc: N/A
source_links: https://doi.org/10.23846/RPS0023 ; https://doi.org/10.1093/biomet/63.3.581 ; https://doi.org/10.2307/145818 ; https://doi.org/10.1080/01621459.1988.10478722 ; https://doi.org/10.3386/w11721
work_performed: read Atanda2019 published report §3.1/§4.1/Table A2/A8/A9/B1/§6 and Rubin1976 selected original sections; independently computed exact binary-status missingness bounds from public table counts. Reviewed 12 open Codex PR summaries, PR #1 R257 S53 false positives and PR #3 candidate fix remain unmerged.
results_seen: NREGS treated 2014/2152/3353, control 493/718/1717; SSP treated 987/804/959, control 206/248/628; NREGS district7 all 1425 missing; SSP district7 555/557 missing. NREGS treated-control descriptive adoption bounds approximately [-0.486927,0.545417], SSP [-0.411886,0.517248]. Distinct outcome table denominators cannot be used as card-status missing counts.
evidence_scope: public published table arithmetic and synthetic sharp bounds only, nonblind; real individual source/data replay NOT_RUN, original Stata NOT_RUN, causal identification NOT_ESTABLISHED, R E1/E2/E3 increment 0.
output_paths: theory/TH170_SMARTCARDS_CARD_STATUS_MISSINGNESS_DENOMINATORS_BOUNDS_2026-10-31.md ; theory/th170_smartcard_missingness_bounds_audit_20261031.py ; theory/INDEX.md ; research/coordination/theory/20261031T030841Z-th170-smartcard-missingness-handoff.md
commit_sha: c2cf3986faa6d782951d7eca279f5dd4db745cab (note, script, index); handoff itself in containing later commit
verified_blobs: note=94e5de014bd1f034cad603a19fabdebd1c146c5e ; script=3ef083356aa08640d2c6a1ea7fcd4deec125b183 ; index=f80eb98326387a1f6d300a3d79dd9139ea1bb2c1
math_validation: equivalent independent Python Fraction calculations performed PASS; exact remote script bytes execution NOT_RUN (container cannot resolve raw.githubusercontent.com).
C_today: C008 complete, blob 7baa21237c97630f1a5058ab13d36dc0fe2d5d87, unchanged.
D_this_week: D002 complete, blob b2556a008eca156222acd3f3b85caa50f85c5fac, unchanged.
ci_status: NOT_RUN, no CI requested; commit-triggered status to be checked.
billing_checked: NO; no new paid service/API/data or paid CI initiated.
blockers: openICPSR LICENSE/README raw bytes not recovered, no legal raw data replay, no original mandal IDs, raw GitHub DNS failure.
next_action: TH171 audit district7 missingness mechanism and A8/A9 variable versions if legitimate documentation accessible; otherwise diversify original theory sources. R series remains first for eventual unified classification, PESEN/R073 unchanged.
