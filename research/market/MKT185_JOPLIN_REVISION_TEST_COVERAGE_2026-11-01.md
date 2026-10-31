# MKT185 Joplin revision error test coverage at pinned upstream source
Date: 2026-11-01 (Asia/Singapore). Baseline main 3f5cef26ed8a20da14f2f9d30ff86c11af88508e.
Target key: (market,Joplin,upstream-2e1310190489c5325dd69305bb762e887865c6c3,revision-error-test-coverage).
Status: COMPLETE_BOUNDED_STATIC_SOURCE_AUDIT. Nonblind; no upstream test suite executed.

## First-party inputs and mechanism
Pinned upstream commit: https://github.com/laurent22/joplin/tree/2e1310190489c5325dd69305bb762e887865c6c3
RevisionService.ts blob e2aea82a1f1513a1a6a8c7e1e804fe812711cb9f; RevisionService.test.ts blob 91658f2a33759476298d398baadd5a4b94fc3783; Revision.test.ts blob 06f2f68c2818f98104b78a4ae52358f19af9ce9d.
Read exact source and test files through GitHub connector. Test source has 808 lines, 27 active it() declarations and one commented it() declaration by line-prefix count. This count is static, not a Jest execution result.
Inputs are note edits and ItemChange IDs. State includes revision diffs, lastProcessedChangeId, encrypted revisions and retention settings. Source lines 204 to 228 handle generic errors by logging and advancing the cursor, with an explicit source comment at lines 218 to 220 that a skipped change will not be processed again. An encrypted-revision error instead aborts collection before advancing that change's cursor.
At RevisionService.test.ts lines 80 to 115, the only directly matching generic corrupted-string skip scenario is entirely commented out. The comment explains that a former diff-match-patch bug was fixed and the failure could no longer be reproduced by that fixture. It is not an active regression gate for arbitrary generic errors.
The encrypted-revision test at lines 358 to 390 is active. It explicitly checks lastProcessedChangeId remains 3 while change 4 is blocked, then becomes 4 after decryption. Other active tests exercise encrypted revision deletion. Revision.test.ts has an active 'naughty strings' regression for the former text patch bug, a different property from generic error cursor advancement.
## Consequences and boundaries
There is a source-supported asymmetric error policy and a test-coverage gap for the generic skip path in this pinned revision. This does not establish a live deployed incident or prove that every generic failure loses a user-visible revision. Real frequency, runtime behavior across versions and current release status remain unknown. No source patch, Joplin installation, account, or paid service.
For future decision logs, candidate controls are persistent failed-change receipts, explicit retry/ack separation, an audit for processed IDs lacking revision receipts, and visible uncertainty in historical evidence. These are unadopted design candidates.
Privacy: local-first open-source use is available; optional sync and hosting may introduce separate access/cost choices. Vendor pricing was not reverified this round. No personal data used. No real product effectiveness evaluation.
Evidence: pinned upstream source and test static inspection; no new E2/E3; marketing claims excluded.
Next: a separately scoped fault-injection test against a locally runnable upstream revision service if dependencies are available without extra charges; preserve frozen upstream version and avoid any CI billing.
