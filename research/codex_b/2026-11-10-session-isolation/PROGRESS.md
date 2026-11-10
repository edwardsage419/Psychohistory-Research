# Plan: research/codex_b/2026-11-10-session-isolation/PLAN.md

Investigation: original synthetic suites PASS: R073 23, R074 20, R075 24, R077 24.
Disposable actual-source duplicate-donor mutations survive R074 20 and R075 24.
No historical input/model/freeze changed. Main and 12 open PR scopes reviewed.
Ruling: use the clean managed checkout with a dedicated codex-b branch, and keep
all engineering artifacts in the user-requested Codex B directory. No additional
worktree or global dependency installation is needed for this additive package.
Ruling: follow user's autonomous execution instruction; implement and deliver the
reviewable engineering package without intermediate design approval pauses.
This author will implement inline using executing-plans and TDD; one fresh final
review will inspect the complete package. The plan ledger is retained as evidence.

Task 1 complete: exact oracle hand expectations and negative fit controls;
RED initial 10 methods (9 assertion failures/2 KeyErrors including subtests),
GREEN 10/10. Original trainers match 24 fictional folds/5376 probabilities.
Task 2 complete: archived 91 tests and new 10 initially pass normal/-O; actual
R074/R075 duplicate-donor source mutants pass old 20/24, heldout source mutants
fail by assertions, all four new gates reject FIT_MISMATCH/42 in both modes.
All 34 code input fingerprints unchanged before/after each replay and historical
source Git blobs independently match HEAD. Context manifest 154 pending items:
27 P0/82 P1/45 P2, net formal closure 0. Main refreshed, unchanged e5f2baa7.

Fresh-context reviewer session_validation_review (read-only) reviewed
e5f2baa7..488423de. No Critical finding. One Important: check_trainer({}, ...)
reported 0-fold success. Reproduced in review-red.log, fixed to reject empty
sessions; review-green.log 12/12 PASS. One Minor: missing corrupted-predictor
regression, addressed because it directly protects numerical fail-closed behavior.
Removing probability validation in a disposable oracle makes seven subcases fail;
the normal guard rejects bool/int/NaN/Inf/0/1/constant-half predictions.
Reviewer ran both full scoped replays in fresh /tmp dirs and verified 16 context
hashes plus 34 code fingerprints per mode, with no edits to this checkout.

Review boundary rulings: historical human numerical correctness, participant
identity, formal science acceptance, full-repository behavior and CI/billing stay
NOT_RUN/NOT_ESTABLISHED per user scope; synthetic evidence cannot establish them.
Remote freshness is checked separately before publishing. No minors deferred.
Final fixed sources rerun in evidence/final-normal and evidence/final-optimized:
103/103 positive methods each (206 final executions), four mutation rejections
per mode, correct heldout positive controls, all source fingerprints stable.
No second review dispatch: fixes are verified by RED/GREEN and scoped replay.
