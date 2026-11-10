# Prior receipt integrity and source-context validation

This increment prevents the previous 460 positive method executions from being presented as fresh validation of changed PR heads. It adds `../receipt_context.py` and 17 regression methods; the existing queue tests bring the local suite to 27 methods per mode.

## Scope and interface

The CLI reads the prior inventory, matrix and raw logs directly from a fixed full Git commit, checks SHA256, typed identities/counts, unique canonical log paths, normal/optimized pairs and the final unittest summary. It checks the supplied current inventory against local fetched main/PR refs and compares the entire source set conservatively. It never runs tests or authorizes cached-result reuse.

```sh
python3 -B -m unittest discover -s research/codex_a/pr_queue -p 'test_*.py' -v
python3 -O -B -m unittest discover -s research/codex_a/pr_queue -p 'test_*.py' -v
python3 -B research/codex_a/pr_queue/receipt_context.py . 19957c794e6dbf152ffce58d3e34c74b88037eae research/codex_a/pr_queue/receipt_validation_20261110/evidence/current-inventory.json
```

Exit 0 means only `SOURCE_CONTEXT_MATCHES`; 2 means `RERUN_REQUIRED`; 1 means malformed, missing or inconsistent evidence (`BLOCKED`). Callers must honor the exit and scope fields. Matching source is necessary, not sufficient, for test-result reuse. Runtime, worktree state, execution time, author identity and scientific acceptance are not authenticated. The historical positive matrix is the bounded input schema; omitted or non-positive ancillary runs are not upgraded to PASS.

## Actual checks and findings

- Both final local modes passed 27 tests, with no skips. Raw logs are retained in `evidence/normal-tests.log` and `optimized-tests.log`.
- Initial test-first failures and three additional red regressions are retained separately. Review identified one log reused for two modes; additional checks reject canonical path aliases and an inner unittest summary inflating the outer test count. Identical bytes in independently named logs are allowed; distinct hashes are not required.
- The immutable historical matrix at `19957c794e6dbf152ffce58d3e34c74b88037eae` passed receipt integrity checks for its 460 prior method executions. This is zero newly executed research tests.
- A temporary bare Git fixture with the historical fetched refs returned 0 / `SOURCE_CONTEXT_MATCHES`. It did not change the real repository refs or execute the old suites.
- Actual fetched main `558ef502ed2e06e76bb35bffdde785075b04f71e` and 21 PRs returned 2 / `RERUN_REQUIRED`: main changed, PRs 10/11/12/14 changed, PR 21 was added. The original R077 legacy failure remains outside the positive matrix and remains a recorded failure.

## Delivery and remaining work

Only Codex A engineering files are added. No frozen protocol, research-owned source or historical receipt is changed. This increment belongs to existing draft PR #14; no merge or CI dispatch is performed. Source SHA256 and Git blob identities are in `artifact_hashes.json`; command results and exact context snapshots are in `evidence/`.

Next: validate the newly added #21 replay, then rerun the combined candidate against freshly captured main and all current PR heads before claiming current integration readiness. The old combined matrix is historical evidence only. Main adoption still requires explicit merge authorization under the user's standing prohibition on automatic merging.
