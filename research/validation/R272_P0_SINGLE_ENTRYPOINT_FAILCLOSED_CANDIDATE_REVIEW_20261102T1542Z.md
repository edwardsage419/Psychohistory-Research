# R272 P0: proposed single-entrypoint fail-closed acceptance runner

Date UTC: 2026-11-02T15:42Z. Track: R/B. Starting main: df729872af4b5131e8dd9e0a0b7ab8d48001c290. Candidate code commit: 26387a59f046c25f2e6c9dd5eff3ae27d0a8389a. Status: COMPLETE for local self-tests; PARTIAL for complete-checkout execution; production P0 OPEN.

## Problem and scope

Earlier R/B reports established that the active R272 workflow runs the original generator with --emit before checking historical archived evidence. Its inline asserts are optimization-sensitive and its push path filter excludes relevant validation inputs. The unadopted three-job proposal contains shell run blocks. A previously archived mutation audit showed that inserting an early successful shell exit before required checks was falsely accepted by the original structural checker in 3/3 reconstructed tests. Those historical failures and source files are preserved unchanged.

This increment offers a different caller design: a single standard-library Python command, with an internal fixed sequence of checked subprocess invocations and explicit JSON/exit-status verification. It does not rely on multiple shell commands being reached inside a YAML run block. This narrows the shell reachability problem once a separately reviewed workflow invokes this command as a mandatory step. Workflow source integrity and job skip semantics still require separate review.

## Fixed inputs read from current main

* original239 crosswalk v7.8, blob 36f24235901172642c46853298aebb421f1a3552, 239 original items.
* itemwise pending queue, blob 3b96d46b3d88ccafd779a08509c3cfd0e435772f: 154 records, P0=27, P1=82, P2=45.
* active workflow .github/workflows/r272-exact-train-test-oos-e1.yml, blob 3132b08cf4ee64b55f5112d2249894ea0ec9d42d.
* unadopted workflow proposal, blob fe7165cf0dfe1de12664ddfbcf4360b73c29a518.
* frozen protocol, blob 9fbdb0078a58c4a9c0a548643227e30da5731119.
* original R272 source, blob 13843eecf2f9f05c19ee5545bdb224f58313f367.
* pinned wrapper, blob 8722fd4388421e3b1f77c6648b4ed1b38088c4b0; native negative test, blob 9b8a5a566b7f48c7e72ba34505d49eebe3a94b44.
* archive triplet Git blobs: 8fbbc73d239765f5c66395af1bcf9cf7a8df1f41, db3ca11ae224af52c2caf385c898e24aaa0cc54b, 85d36858911a7eb79c73c607cddf45ea88852a60.
* candidate ZIP SHA256 f23b04706b60ac70bdbee6f051a74551779fb9d9a9b9af08c96cda345b055151; extracted gate SHA256 f7109f8f815d166128ca3429fb42ff3e7cac780d03fb78f8243aeabbd6fbb786.

The candidate is research/validation/r272_single_entrypoint_failclosed_20261102.py, Git blob f33e4e7e544560d65342a899606311d169e4d122. Only additive R/B files were written. No frozen source, archived receipt, active workflow, or Codex PR was changed.

## Implemented caller behavior

Before any execution, authenticate the original source, freeze, archived CSV, results, receipt, wrapper and negative regression by exact Git blob. Authenticate the ZIP SHA256, require its sole named member, bound its declared size, and verify the extracted gate SHA256. Extract only to a temporary directory. The checked-out evidence remains read-only.

For each of normal, Python -O and Python -OO, run the pinned wrapper against the original checkout with isolated regeneration, require its preimage/science/unchanged-archive flags and 576-row scientific receipt, run the original 83-test suite and require its unittest summary, then run the existing pinned native negative suite and require all 15 corrupted preimage rejections and the historical overwrite masking demonstration. Recheck every pinned source and archive byte against the initial snapshot. Child commands use subprocess.run with shell=False, an explicit argument vector, exit-code checking and JSON claim checks. Any missing requirement raises an unconditional ValueError.

The standalone invocation on an authenticated full checkout is:

    python research/validation/r272_single_entrypoint_failclosed_20261102.py --root .

This is a proposed callable interface. No production workflow has adopted it.

## Actual execution and negative controls

The new code was executed locally with CPython standard library in normal, -O and -OO modes. Each mode passed one positive synthetic identity check and five isolated rejection controls: wrong Git blob, nonzero child exit, false JSON PASS claim, invalid JSON, wrong ZIP bytes. Total 15 negative executions across three modes, all correctly rejected. Python syntax compilation PASS. No randomness or external services were used.

The actual --root path on a complete authentic checkout, original 83-test suite, full 15-case native negative suite, extracted historical ZIP, and the three real acceptance modes are NOT_RUN in this increment. Therefore no claim of 45 successful authentic negative executions is made. The previous native R272 results remain separately archived evidence, with their own limits.

## Scientific disposition and next gate

Evidence: internal nonblind artificial E1 engineering self-test only. New human E2=0; historical E3=0; external team replication=0. No model or scoring rule was changed. original239 pending net change=0.

A scout scan found the public stratEst documentation of FRD2012 (Fudenberg, Rand and Dreber 2012), listing 13,126 repeated-game observations and participant/game/period/action fields. This is a candidate for independent source and session-identity review; the original file, license and frozen R073 compatibility were not established. Existing DF2011 and Kim 2023 disqualifications are unchanged. New R073 qualified datasets=0.

Next: run this exact candidate on a complete trustworthy checkout, record full stdout/stderr, modes and exit codes, and independently review the runner itself. Then submit a production caller change for authorized maintenance review, with exact reviewed workflow identity, mandatory step, complete trigger coverage, failure propagation, and confirmed no-charge Actions eligibility. A script on main does not prove mandatory adoption. R257 S53 historical blind-order FAIL and R333 to R340 composite acceptance gaps remain open.

No Actions or CI was dispatched, no paid API or cloud resource was used. Actual GitHub account billing and remaining free quota NOT_VERIFIED.
