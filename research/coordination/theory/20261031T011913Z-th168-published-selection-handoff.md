# TH168 theory track handoff

track: theory
subflow: TH168
run_date: 2026-10-31 Asia/Singapore
handoff_utc: 2026-10-31T01:19:13Z
observed_head_at_start: 6aa5c0419bbe3ad57b87b787ca069622eac74f0d
target_key: (theory,MURALIDHARAN_NIEHAUS_SUKHTANKAR_SMARTCARDS,TH168-theory-v1,published_vintage_sample_selection_and_transport_bounds)
activity: completed_bounded_note
status: COMPLETE
claim: NO
claim_expiry_utc: N/A
source_links: https://econweb.ucsd.edu/~kamurali/papers/Published%20Articles/Publisher%20Formatted%20Versions/Building%20State%20Capacity%20%28AER%202016%29.pdf ; https://econweb.ucsd.edu/~pniehaus/papers/statecapacity.pdf ; https://www.openicpsr.org/openicpsr/project/113012/version/V1/view ; https://www.princeton.edu/~davidlee/wp/resrevision8.pdf
work_performed: Direct read publisher-formatted 2016 AER main text, 2016 author appendix C.1/C.6/C.8, openICPSR V1 metadata, Lee original author open draft. Twelve bounded propositions and twelve source/arithmetic/synthetic audits; exact Python Fraction script local PASS and Git blob identity verified.
results_seen: Published main text still 8572-1000-102 != 7425; author appendix 8527-1000-102 = 7425. C.6 p values 0.19/0.74/1/0.37 are failures to reject, not equivalence. C.8 treatment main effects differ from entrant interaction estimands. OpenICPSR V1 data archive identified; raw files not downloaded. Synthetic 296/353 nested-world ATE bounds [-137/1765,433/1765] include both signs; assumption not established in actual study.
evidence_scope: nonblind primary publication/appendix version comparison, official archive metadata and synthetic math. No mandal identity recovery, no original microdata, no independent real-world ITT, no E1/E2/E3 increment.
output_paths: theory/TH168_SMARTCARDS_PUBLISHED_VINTAGE_SELECTION_TRANSPORT_BOUNDS_2026-10-31.md ; theory/th168_selection_bounds_audit_20261031.py ; theory/INDEX.md ; research/coordination/theory/20261031T011913Z-th168-published-selection-handoff.md
commits: note e1d3113d1190fc6143181507344424563879cc2f ; script 17a724056f6c9c7fa25ad4d1a7daa77335ace169 ; index e3d5fb0e51e01e5a8c9cebe268ba42773a0ef243
commit_sha: null (self-referential handoff commit; inspect remote Git history)
PR: null
ci_status: NOT_RUN; no CI triggered
billing_checked: no new paid services or Actions requested; actual billing balance not inspected
source_blobs: TH168_note=f674a89aa298422984db20358c660e12562af38d ; script=79816a84576bd64073d44dcf3f116908da542bc7 ; theory_index=0bb2ac69340722469500b2a8e6e00db9ade2139b
C_today: C008 already completed, blob 7baa21237c97630f1a5058ab13d36dc0fe2d5d87, unchanged
D_this_week: D002 already completed, blob b2556a008eca156222acd3f3b85caa50f85c5fac, unchanged
coordination: R303 S99/A/B latest main handoff read; open Codex PR #1 R257 S53 issue and strict gate candidate unmerged; no competing TH168 claim seen in main or open PR summaries.
blockers: 2014 October NBER revised full PDF, raw randomization mandal IDs, Nalgonda unit mapping, formal AER online appendix version hash, openICPSR data license/content read.
next_action: TH169 recover openICPSR V1 public license/README and randomization file inventory, compare 2014 October revised manuscript, keep R track untouched.
