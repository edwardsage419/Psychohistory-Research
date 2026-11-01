# E163: R335 receipt P0 propagation and PR #3 actual-source merge-readiness review

Date: 2026-11-01 UTC
Track: operations / E read-only governance
Key: (operations,R335-and-R257-S53,2026-11-01-main-and-PR3-head,optimized-assert-fail-open-and-unmerged-coverage)
Baseline main after MKT194: 961b86e8a16840a0d2d913e3817799c315a5ed93
Status: COMPLETE_BOUNDED_REVIEW; P0_PRODUCTION_REMEDIATION_PARTIAL; MERGE_REVIEW_PARTIAL
Method: connected GitHub direct source/patch reading, identity checks, prior R/B native evidence review. E did not rerun R/B mathematical or negative-control suites.

## 1. New R335 P0 and scope discipline

Since E162, R and B committed R335 strict additive gate, test program, actual native execution matrix, R335 scientific-scope report and handoff. Directly read:
- research/coordination/r/20261101T064951Z-r335-p0-handoff.md, blob df077ee9728f320a8411d0715d537c7d3a1fd37c
- research/validation/R335_P0_OPTIMIZED_ASSERT_SCIENTIFIC_SCOPE_2026-11-01.md, blob 837a5b16d486d71a3e6501cb05e0bb044af07dc1

R/B report 20 subprocess executions under CPython 3.13.5. Original R335 optimized CLI falsely accepted corrupted CSV, corrupted JSON and both receipts missing, returning success despite a green five-test unittest run. The additive strict gate rejected these negative controls in normal and optimized modes. Original source-only mutation was also accepted by original CLI and rejected by strict gate. This is **R/B observed native execution** corroborated by E's source/report reading, not an E independently executed reproduction.

Production original R335 entry point remains unchanged. The original normal-mode historical CI run 40051490899 cannot be promoted to optimized-mode safety proof. R335 scientific result remains finite constructed E1 and PARTIAL_P0_REMEDIATION. No evidence of actual historical archive tampering or new human E2/history E3.

R334 has the prior separate P0 and additive strict gate. R333 and R336 through R340 have six further source-level assert-only risk observations; native corruption controls for those six remain NOT_RUN. Keep STATIC_RISK distinct from CONFIRMED_FALSE_ACCEPTANCE. The R handoff explicitly owns further native negative controls. E should coordinate, avoiding duplicate B validators.

Immediate P0 coordination recommendation: R owner/reviewer should consider a single mandatory fail-closed acceptance entry point, with source/receipt identity and explicit exceptions verified under ordinary and optimized Python. Do not silently rewrite frozen originals. Pending that review, reject any scientific upgrade supported only by optimized original receipt success.

## 2. PR #1 and #3 actual patch review

GitHub search returned 12 open PRs (#1–#12) at this read. PR #1 and #3 were directly read and are OPEN, DRAFT, unmerged. PR #3 head SHA 97d5f74df5d84916917db943156120f08144f445; its reported base SHA c3ce3cdfff07050b0b6d496860b5c7c4310901b8 is older than current main. The GitHub mergeable flag is true, but draft status, branch age, source authentication and independent acceptance remain review gates.

Directly inspected PR #3's full added validate_receipt.py and test_validate_receipt.py from its 14-file patch. The candidate validator uses Fraction exact arithmetic, fixed 8-world names, five perturbation deltas, two secant steps, uniqueness checks, objective and KKT primal/dual/complementarity checks, exact baseline/derivative/secant checks, strict top-level field/evidence metadata and JSON duplicate-key rejection. Its failure path raises ValueError instead of relying on assert. CLI checks under python -O are represented in the submitted tests.

PR #1's six old-comparator false-acceptance classes map to PR #3 candidate regression tests:
- duplicate world -> test_reject_duplicate_worlds
- duplicate capacity -> test_reject_duplicate_capacity
- multiplier tampering -> test_reject_wrong_multiplier
- derivative tampering -> test_reject_wrong_derivative
- delta tampering -> test_reject_wrong_delta
- evidence upgrade -> test_reject_evidence_upgrade

The candidate additionally tests a complementarity-consistent-looking nonoptimal point, JSON duplicate keys and malformed structures. The PR report claims 32 tests normal and 32 under -O, and records a red complementarity mutation case. **E inspected submitted code and logs but did not rerun the suite**. This is coverage mapping and merge-readiness review, not an independent proof that all tests pass.

Material limitations confirmed by candidate source: the CLI accepts an arbitrary JSON path and validates content, but does not authenticate the original R source, complete upstream CSV, signer, execution identity, original prescore blind ordering or historical receipt Git blob. The returned source_authentication remains NOT_RUN; blinded_prescore_order remains FAIL; full_scientific_acceptance remains PARTIAL. Its assertions_passed=127 check is an expected metadata value, not a replay of 127 assertions. PR's own review records a deeply nested JSON unstructured RecursionError, with nonzero exit, as deferred hardening.

PR #3 changes only additive paths and reports no historical original edits. Before merge: recompare its changed-file paths against current main, verify fixed receipt and source identities, run the submitted tests in a known charge-free local environment, inspect reviews and maintain the PR #1 forensic counterexample evidence. A successful GitHub mergeable flag is insufficient. Owner decision on merge order and gate adoption remains pending. No PR was merged, approved, rebased or modified here.

## 3. Queue, theory, coordination and F

Directly fetched original239 v7.8 crosswalk: Git blob 36f24235901172642c46853298aebb421f1a3552, and the pending154 CSV: Git blob 3b96d46b3d88ccafd779a08509c3cfd0e435772f. Both equal the earlier E162/R335 handoff identities. Thus file-level net change = 0. No full 239-item or 154-row itemwise audit was performed. The number 154 is a filename and historical queue label, not a freshly re-counted scientific completion status.

Latest theory commit 6b19e3c861be726c2dc8650cd7b4198e211a6c82 adds TH197 and a short handoff. Latest R commit 1c32fa29f40d3207a3436398a7086a3161320e62 adds the R335 P0 handoff. No evidence in these reviewed paths of changes to R073 or PESEN v0.1 freezes. Comprehensive all-repo freeze diff: NOT_RUN.

F009 phase56 weekly bounded topic was already COMPLETE. This round adds no artificial phase57. MKT194 documents an independent, product-specific consent lifecycle concern: disconnecting a data source stops new collection while past records remain, and deactivation may only hide records. That is a candidate for future privacy governance review, without processing real personal data.

## 4. Status and owner decisions

P0-R335-01: CONFIRMED_FALSE_ACCEPTANCE under optimized original CLI. Additive gate available; production enforcement PARTIAL. R/B notified by their own dated handoff. Owner/reviewer integration decision pending.
P0-R334-01: Same category of optimized-mode original receipt risk, already recorded in E162; integration PARTIAL.
P0-R257-01: PR #1 forensic evidence and PR #3 strict candidate both DRAFT/UNMERGED; candidate mathematical coverage inspected, source/provenance and blind-order acceptance still open.
P1-R333-R336-R340: six STATIC_RISK items; native negative controls NOT_RUN, R/B owns next verification.
P1-R170, R248, R258: prior PR dependency and receipt-coverage issues remain open; no new review of their long patches this round.
Queue: no file-level change; itemwise verification NOT_RUN.
R073 external eligible second cohort: NOT_ESTABLISHED.

No cross-track file edits, index updates, PR actions or CI launches. Actual GitHub billing/quota: NOT_VERIFIED. No paid operation initiated. E's new evidence is governance review of actual patches and R/B reported executions, with no scientific E1/E2/E3 upgrade.

Next: owner-facing source-authentication and freeze-preserving merge acceptance checklist for PR #3, then monitor R/B native tests of the six static-risk models. Avoid duplicate validators.
