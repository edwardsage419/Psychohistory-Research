# Independent bounded integrity review, 2026-11-17

**Final disposition after scoped re-review: no unresolved critical, important, or minor findings. The important source-binding defect below was fixed and its isolated reproduction now executes the genuine source tests in all three optimization modes.**

Scope: actual GitHub Issue #34, current R132 attester and integrity tests, original diff, opt-in R275 archive v2 and its tests. Repository read-only; no comments, commits, agents, CI dispatch, or full-suite reruns. This is an engineering review, not scientific acceptance.

## Critical

None identified within the reviewed scope.

## Important — native test source identity was not bound to executed bytecode (RESOLVED)

`research/R132/r132_phase_b_ci_attest.py:83` uses `importlib.import_module` after hashing source paths. Standard Python imports can execute a timestamp/size-valid cached `.pyc` whose code differs from those source bytes. The imported native test module also imports the mathematical core normally, so both the test and the child-side core have this gap. Comparing source-file hashes before/after and with the parent does not authenticate the loaded code.

Concrete isolated reproduction: `/tmp/r-series-review-20261117/repro_r132_cached_test.py`. In a temporary copy, generate an ordinary bytecode cache for a same-length test module defining 70 no-op tests, then restore the exact original test source bytes and mtime. No repository files or attester functions are modified. Call the real `_run_unit_tests` and `_validate_test_result`.

Observed under normal Python, `python -O`, and `PYTHONOPTIMIZE=1`: 70 cached `CachedNoopTests` run and pass; zero current `Primary1978ReplicatorEquations` tests run; on-disk test source is byte-identical to the repository; reported source SHA256 is `df931f98e5325907509fdb9eb9b0d98438cb028cd42020e6e94367244de195b1`; result validation accepts. This permits a successful receipt's prerequisite to describe a different test implementation from its recorded source. It establishes a current implementation gap, not historical exploitation.

Required fix: in the child, read and hash exact core and native-test source snapshots, compile and execute those bytes explicitly, register the authenticated core under the expected module name before loading the test source, and compare those executed-byte digests against the parent identities. Continue checking source stability. Add a stale-bytecode negative/control covering both native-test and core module identity. `-B` alone does not fix this because it disables cache writes, not cache reads.

## Minor

No separate actionable minor defects identified.

## Checks supporting the rest of the change

- All original 13 R132 acceptance conditions remain explicit and optimization-independent. Count types exclude booleans; numerical error now also excludes negative and nonfinite values; payoff equality requires boolean True.
- Parent math is compiled from the exact bytes whose digest is checked, avoiding the child-side cache defect there.
- Native result validator requires matching run ID/source map, unchanged sources, exactly 70 tests, zero failures/errors/skips/expected failures/unexpected successes, successful return status, and matching optimization level. An isolated direct check rejected 32 invalid type/count/status variants, including boolean counts and skipped/expected-failure results.
- Managed stale output is deleted before source loading or execution. Historical/unowned output is refused; symlink paths are refused. JSON serialization occurs before writing, temporary files are flushed/fsynced, publication uses atomic replace, and temporary cleanup runs on publication failure. Supplied log records all four integrity tests passing, including 72 fault children and historical/publication/source-load controls. I did not rerun those whole suites.
- R275 v2 authenticates bounded source/JSON/CSV snapshots, transforms exactly the pinned original 18 assert conditions into runtime guards in memory, compiles that authenticated AST, and checks authenticated private input copies. No other mathematical AST transformation was found. Public CLI input cannot reach the private semantic engine without passing the frozen input pins. The receipt explicitly retains E1, zero new E2/E3, no workflow adoption, and production blocked; legacy callable remains unchanged.

## Declined to judge

Scientific validity, historical CI exploitation or fresh GitHub CI provenance, empirical predictive validity, production routing/adoption of R275, hostile interpreter/site customization or arbitrary in-process monkeypatching, adversarial concurrent filesystem writers, and cross-PR archival integration. No claim of new science or scientific reacceptance is made. Single-invocation atomic publication does not establish a multi-writer locking protocol.

Reviewed R132 attester SHA256: `de9b608436bcf40626a913649349568c122c370a9b2bed7fc472b8e9f433384e`.
Reviewed R132 integrity-test SHA256: `dcb559dfbd6181aa1072fa921140736d9d3c4b0fa7c36cdbeb1f492906478018`.
Reviewed R275 v2 SHA256: `41d4cf6b0fec28b8da888ac774a41571f8f839c2b107a6080be7691afc11d63e`.

## Scoped re-review of source-byte compilation fix

The child now snapshots each qualified source into bytes and hashes those snapshots, then explicitly compiles and executes both the mathematical core and the native test module. It registers the core in `sys.modules` before the native test executes. Qualified modules no longer use the cache-aware import loader. The before/after identity comparison plus parent digest check binds executed snapshots to the recorded source identity.

Repeated the same isolated cached-70-noop reproduction under normal Python, `-O`, and `PYTHONOPTIMIZE=1`: all three now execute the genuine `Primary1978ReplicatorEquations` suite (70 successful tests), with `cached_noop_tests_executed=false`, `current_source_tests_executed=true`, and the authentic source digest unchanged. Reviewed the added three-mode end-to-end regression that also inspects the published native stderr. No unrelated whole-suite reruns. No remaining blocker found in the scoped fix.

Final attester SHA256: `ba550e569dfe399becdbd6863d6a49e503b9e3db2ed08a9fb6f7020ceebfa495`.
Final integrity-test SHA256: `569118a8d8b1576573a49c25b821f6c4ef227541a9bbb8950724dacff8da6e8f`.
