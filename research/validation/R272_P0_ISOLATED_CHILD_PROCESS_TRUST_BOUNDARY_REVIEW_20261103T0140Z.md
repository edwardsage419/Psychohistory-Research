# R272 P0: Python child-process isolation boundary review

UTC: 2026-11-03 01:40. Track: R / B. Status: PARTIAL. Scope: internal nonblind E1 engineering audit, not production acceptance.

## Read-only source identities
Observed main before writing: `b86ec28fbf9279b49faa91208c6223281f401adf`.
Entry candidate `research/validation/r272_single_entrypoint_failclosed_20261102.py`, Git blob `f33e4e7e544560d65342a899606311d169e4d122`.
Caller candidate `research/validation/r272_single_entrypoint_caller_candidate_20261103.yml`, Git blob `a84b3d13d7d6bc8da45dc523454d7804520ca79c`.
Prior shadow counterexample `research/validation/r272_shadow_import_audit_20261103.py`, Git blob `bef93e291f1c298c880d37225f47b4bd0b6d2f95`.
Workflow requirements blob `d4b8548ba45961f5aa0bdcafefdb226d7cd2fc9e`.

## Static findings
1. Candidate workflow executes `python research/validation/r272_single_entrypoint_failclosed_20261102.py --root .` without interpreter isolation.
2. Entrypoint invokes three kinds of Python children using `[sys.executable, *flags, ...]`, where flags are `[]`, `['-O']`, `['-OO']`. No `-I` or `-S` is propagated to the wrapper, original generator, or negative suite.
3. Even after adding `-I` to the parent invocation, its subprocess arguments remain unisolated unless changed separately. The parent checks child exit codes and selected JSON fields; a successful exit before authentic work is a plausible false acceptance path if an untrusted import runs first and forges expected output. This is a conditional attack argument, not a demonstrated end-to-end forgery of the authentic full repository.
4. The candidate workflow trigger paths do not cover arbitrary sibling `.py` modules in `research/validation/`; the earlier `json.py` example is one such input. A broader validation-directory trigger or an explicit reviewed dependency closure is needed.
5. Candidate is not installed as production workflow. Historical three-job freeze compatibility, mandatory branch enforcement, and no-cost CI eligibility remain separately open.

## New bounded local control
A fresh local CPython experiment created temporary `entry.py` and sibling `json.py`; the sibling prints `FORGED_PASS` and exits 0. With `python -S entry.py`, the injected module executed and exit code was 0. With `python -I -S entry.py`, the injected module was excluded and the entry exited 17 as intended. With `python -O -S entry.py`, the injected module again executed and exited 0. These are three deterministic synthetic controls. They do not execute the original R272 files or certify a specific default interpreter configuration. The original source imports may vary with interpreter startup and installed packages.

## Required next acceptance
1. Freeze the intended interpreter and its trusted standard-library assumptions; decide whether `-I -S` is compatible with the authentic wrapper, generator and negative suite. Execute this in a trusted complete checkout.
2. Apply isolation to **every** Python subprocess, including verifier entry and test runners. Strip untrusted `PYTHONPATH` and relevant environment variables or use a controlled environment. Confirm actual dependency imports, rather than assuming isolation works.
3. Replay the original import-shadow counterexample against the **actual** candidate source in all three modes. Include sibling-module and environment-path injections at parent and child boundaries, verify rejection with an authenticated receipt, and prove no archived evidence was overwritten.
4. Verify all pinned archived preimages, independent gate, native 83 tests and 15 negative controls in each mode, then check historical freeze three-job compatibility.
5. Before production adoption, independently review trigger coverage, required checks and GitHub Actions billing. No Actions were started in this audit.

## Evidence and limitations
No R272 full checkout run, no real archived preimage execution, no Actions, no E2/E3 scoring, no independent external replication. Existing R257 S53 blind-order failure and other P0 items are unaffected. No new costs were incurred in the local experiment; actual account billing was not independently checked.
