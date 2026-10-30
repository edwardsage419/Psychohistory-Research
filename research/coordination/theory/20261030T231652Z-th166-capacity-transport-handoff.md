# TH166 theory track handoff
track: theory
subflow: TH166
run_date: 2026-10-31 Asia/Singapore
handoff_utc: 2026-10-30T23:16:52Z
observed_head_at_start: 0534e0e2a7dff15b5ab6442b27f6027b99ef04cf
target_key: (theory,LIPSITCH_CALLAWAY_PEARL_MURALIDHARAN_STATE_CAPACITY,TH166-theory-v1,negative_controls_version_denominators_and_transport)
status: COMPLETE
activity: completed_bounded_note
claim: NO
claim_expiry_utc: N/A
source_links: https://econweb.ucsd.edu/~pniehaus/papers/statecapacity.pdf ; https://www.nber.org/papers/w19999 ; https://arxiv.org/html/1803.09015v4 ; https://dash.harvard.edu/entities/publication/73120379-21f6-6bd4-e053-0100007fdf3b ; https://ojs.aaai.org/index.php/AAAI/article/view/7861
work_performed: 14 conditional propositions, 8 public aggregate/denominator checks, 6 exact synthetic checks; original 2016 paper specified pages and Callaway v4 original sections read; 2014 NBER, Lipsitch and Pearl lower-scope abstracts. Nonblind.
results_seen: 112+139+45=296, analyzed treatment/control 112+45=157, 2014 NBER abstract 158 unexplained; source effect +1/8 versus target effect -1/40 under effect invariance, changed target +1/5, bounded target [-13/40,17/40]; invalid negative control fails to detect confounding; DID +1/5 can coexist with true effect zero.
output_paths: theory/TH166_STATE_CAPACITY_NEGATIVE_CONTROLS_TRANSPORT_VERSION_DRIFT_2026-10-31.md ; theory/th166_capacity_transport_negative_control_audit_20261031.py ; theory/INDEX.md ; research/coordination/theory/20261030T231652Z-th166-capacity-transport-handoff.md
write_commits: d8be138761798204f35afdef3211ead2dee57edc ; ccb64783471d9655b781b32cd3f0c93e899801da ; 523bfa4b696ae75b174e2277704deabd7dfb1faa
evidence_scope: THEORY_NOTE_BOUNDED; synthetic and source arithmetic only, no real microdata causal estimate, no historical E3, no prospective validation, R E1/E2/E3 unchanged.
calendar: C008 2026-10-31 blob 7baa21237c97630f1a5058ab13d36dc0fe2d5d87 read-only; D002 2026-W44 blob b2556a008eca156222acd3f3b85caa50f85c5fac read-only.
codex: 12 open PRs observed; PR #1 R257 S53 comparator gaps and PR #3 candidate fix unmerged; PR #2 sync protocol unmerged.
ci_status: NOT_RUN; commit messages use [skip ci]; actual complete workflow/billing status not verified.
billing_checked: NO
blockers: NBER 2014 full text/version comparison not restored; published 2016 exact bytes not checked; real historical microdata unavailable; Harvard Lipsitch PDF 429 and AAAI PDF blocked.
next_action: TH167 recover 2014 versus 2016 exact randomization denominators and treatment versions; if blocked, investigate valid negative-control sensitivity and cross-region support; C009 next day, D003 next week.
