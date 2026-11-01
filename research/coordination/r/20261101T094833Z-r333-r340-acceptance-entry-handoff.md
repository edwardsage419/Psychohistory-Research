# R track handoff: eight-model P0 acceptance dependency

utc: 2026-11-01T09:48:33Z
track: r
baseline_main: 6278989bf7c957a3ecac54d458127c60bf5cbd6c
main_before_handoff: 84e49cdce20550a8b996adca49e54d9d8919e0b8
status: PARTIAL_CANDIDATE_GATE; PRODUCTION_MANDATORY_ADOPTION_NOT_DONE
claim: NONE
claim_expires_at_utc: N/A

target_key: (r+b,R333-R340,2026-10-24-frozen-originals,optimized_assert_fail_open_and_mandatory_acceptance)
read: current main and recent commits, original239 v7.8 and pending154, R prior handoff, E165, four archived strict gate scripts, Codex PR #1/#3, stratEst English source documentation.
actual: Pinned 8-model CLI wrapper added, checks four validator source Git blobs and invokes 16 normal/optimized child checks. Local synthetic 12/12 ordinary and 12/12 optimized tests PASS. Native original 8-model checkout execution NOT_RUN. Prior eight original optimized false-accepts remain open. No scientific E2/E3 gain. No queue closure.
outputs:
  research/evidence_audit/r333_r340_acceptance_entry_20261101.py
  research/evidence_audit/test_r333_r340_acceptance_entry_20261101.py
  research/validation/R333_R340_P0_ACCEPTANCE_DEPENDENCY_2026-11-01.md
commits: 92e79b2700af10de60be2229ceffa02bc0296678, f338e1e59ce820250442b4a35261e51253c298f9, 84e49cdce20550a8b996adca49e54d9d8919e0b8
verified_entry_blob: 9822418253c6a2888119c2a823ffee62dd945d7c
verified_test_blob: 68e4b6d27eb2a42d24fc1d4e29927b64e86e1081
verified_report_blob: 29b3629c069f7ddf86562106cab9484e61be5055
index: original239_v7.8_blob=36f24235901172642c46853298aebb421f1a3552; pending154_blob=3b96d46b3d88ccafd779a08509c3cfd0e435772f
queue: P0=27 P1=82 P2=45; net reduction=0
A: DF2011 man/DF2011.Rd explicitly defines game as supergame, period within supergame; 7358 rows; package GPL-3 does not settle dataset-specific license; R073 eligibility UNKNOWN, E2 NOT_RUN.
codex: 12 open PRs; #1/#3 unmerged, independent R257 S53 risk.
ci: final pre-handoff commit check-runs=0, actions runs=0, statuses=0; no Actions started.
billing: NOT_VERIFIED; paid operations NONE.
next: native read-only complete checkout replay of entrypoint; pin trusted entrypoint identity in actual acceptance caller and make failure mandatory; independently inspect PR #3 source authentication; then resume P0/P1 queue. No status-only repeats.
