# E166: R333 through R340 candidate acceptance entrypoint and adoption gate review

track: operations
subflow: E read-only scientific coordination and archive quality
run_date_utc: 2026-11-01T10:21Z
target_key: (operations,R333-R340+CodexPR1+PR3,2026-11-01-candidate-entrypoint-blob-9822418253c6,mandatory-adoption-native-replay-and-source-trust)
baseline_main: 0e388bfdb94434424615ada3334900f855005c7d
status: COMPLETE_BOUNDED_READ_ONLY_REVIEW
candidate_gate: PARTIAL
mandatory_production_adoption: NOT_RUN
new_E_math_replay: NOT_RUN
new_E_fault_injection: NOT_RUN
new_E2_or_E3: 0
ci: NOT_RUN
billing_checked: NOT_VERIFIED
paid_actions: NONE

## 1. Actual repository change since E165

Directly read main HEAD 8c687e3a6aeca91a143af41867131c82442b057b before the market write. Compare from E165 final main 6278989bf7c957a3ecac54d458127c60bf5cbd6c to that HEAD shows exactly five new commits, affecting seven paths. The R/B track added:
* research/evidence_audit/r333_r340_acceptance_entry_20261101.py, Git blob 9822418253c6a2888119c2a823ffee62dd945d7c.
* research/evidence_audit/test_r333_r340_acceptance_entry_20261101.py, blob 68e4b6d27eb2a42d24fc1d4e29927b64e86e1081.
* research/validation/R333_R340_P0_ACCEPTANCE_DEPENDENCY_2026-11-01.md, blob 29b3629c069f7ddf86562106cab9484e61be5055.
* research/coordination/r/20261101T094833Z-r333-r340-acceptance-entry-handoff.md, blob 7044bb984812b8b9ae33e857c6d96f73577895f8.

The other new paths are theory records. This comparison contains no changes to original239 or pending154 queue paths, so file-level net change is zero over the compared interval. The R report directly counted 154 pending rows (P0 27, P1 82, P2 45) and pinned original239 crosswalk blob 36f24235901172642c46853298aebb421f1a3552 and queue blob 3b96d46b3d88ccafd779a08509c3cfd0e435772f. This E pass relies on those R direct counts, and did not independently parse the entire queue.

## 2. Static cross-review of the candidate entrypoint

E directly read the actual source at main blob 9822418253c6a2888119c2a823ffee62dd945d7c. It enumerates exactly R333 through R340 and pins four strict validator script Git blobs. It rejects a missing or symlink validator, a wrong script blob, an absent/symlink model directory, nonzero child exit, stderr, timeout and unexpected stdout. It invokes each model twice with isolated Python, ordinary and optimized, for a proposed total of 16 child executions. The parent has no assert-based acceptance checks. It returns E1_ARTIFICIAL_ONLY and does not claim human E2 or history E3.

The code authenticates the four child validator source bytes. It does not authenticate its own entrypoint bytes. The caller must pin the entrypoint blob and use a trusted checkout. The root-style R334/R335 success output is checked for JSON status PASS_BOUNDED_E1_RECEIPT, while deeper source/receipt checks are delegated to the authenticated child validators. The positive E1 status alone does not establish external independent reproduction or scientific prescore blind ordering.

R/B reports 12 ordinary-mode and 12 optimized-mode synthetic tests passing, including missing/corrupt receipt, missing validator, script tampering and spoofed success text. E did not rerun those tests. The R/B report explicitly marks the actual complete checkout native 16-child execution NOT_RUN. No existing scientific acceptance caller is shown to require this entrypoint as a mandatory dependency. Thus this is a candidate guard, with production mandatory adoption PARTIAL/NOT_RUN and the original optimized-mode P0 false-accept condition still open.

## 3. Acceptance and owner review gates

Proposed acceptance conditions for R/B and owner, preserving all frozen originals:
1. Verify the entrypoint itself against the trusted Git blob 9822418253c6a2888119c2a823ffee62dd945d7c at a pinned main commit. Confirm that all four validator pins and all eight source/receipt pins match that checkout.
2. Execute exact CLI in both parent interpreter modes on a complete read-only checkout, capturing actual 16-child output, exit codes, interpreter version and file identities. Do not infer this from the synthetic fixture suite.
3. Require the new strict gate PASS as a mandatory precondition in the real scientific acceptance invocation. Reject any older original checker exit 0 as an alternative acceptance path under -O. Specify exact failure propagation and retain historical failures.
4. Independently review bounded mathematics, frozen prescore ordering and real-world E2/E3 as separate gates. The new entrypoint's bounded E1 success is insufficient for higher scientific grades.
5. Obtain explicit owner approval before adoption or any protocol-sensitive integration. Do not auto-merge, modify original scripts, run paid CI, or overwrite another track.

The R main track already documented this P0 and its partial mitigation in the same snapshot. E adds a coordination and adoption review; it does not create a new duplicate P0 issue or pretend the fix is merged into the production caller.

## 4. Live Codex PR check

Direct GitHub pulls collection returned 12 open Draft PRs, all unmerged, at this snapshot. PR #1 head 8196dede3b4f568ee899b4ca953d031a3bf5c1ee records R257 S53 false-positive comparator cases. PR #3 head 97d5f74df5d84916917db943156120f08144f445 is a mathematical strict gate with source authentication NOT_RUN and blind-order FAIL in its own description. The main-versus-PR #3 compare at current main returned diverged, 1048 main-only commits and 1 PR-only commit (orientation: base=PR3 head, head=main); this indicates substantial review drift, not proven merge conflict. PR #3 and the new R333-R340 gate cover different frozen experiments and must remain separate.

Risk classification:
P0 R333-R340 original optimized false acceptance, partial candidate gate, mandatory adoption pending.
P0 R257 S53 PR #1 comparator coverage and PR #3 source identity/blind-order acceptance gaps, unmerged.
P1 original239 itemwise evidence and R073 qualified independent external cohort unresolved.
No automatic merges, branch rewrites or cross-track index changes.

## 5. CI, cost, safety and handoff

At pre-write main 8c687e3a6aeca91a143af41867131c82442b057b, direct combined status returned [], PR-triggered workflow-run wrapper returned [], and commit check-runs API total_count=0. The wrapper only checks PR-triggered runs and the result cannot establish all historical CI activity. E triggered no Actions and did no paid operations. Actual GitHub billing/free quota remains NOT_VERIFIED.

R073 and PESEN v0.1 frozen status preserved. No private user data, source dataset or keys accessed. Market report MKT197 on StepBet is independent product evidence and cannot be used as R E2.

Sources actually read:
https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/evidence_audit/r333_r340_acceptance_entry_20261101.py
https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/validation/R333_R340_P0_ACCEPTANCE_DEPENDENCY_2026-11-01.md
https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/coordination/r/20261101T094833Z-r333-r340-acceptance-entry-handoff.md
https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/operations/E165_R333_R340_EIGHT_MODEL_P0_MANDATORY_GATE_2026-11-01.md
https://github.com/edwardsage419/Psychohistory-Research/pull/1
https://github.com/edwardsage419/Psychohistory-Research/pull/3

next_action: monitor R/B complete-checkout native replay and owner decision on mandatory fail-closed adoption. For PR #3 require source identity and prescore-order review before merge readiness. E should not duplicate B tests or claim scientific acceptance.
