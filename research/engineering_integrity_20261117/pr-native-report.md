# PR36 / PR37 / PR38 bounded archival review

Reviewed 2026-11-17 against latest main `1e839d3b02cae02833b282c309f5abd58559949e` in `/workspace/Psychohistory-Research`.

**Disposition: all three qualify for archival integration within their stated scope. PR38 does not repair the historical checker on main; its optimization defect remains independently reproducible and needs a separate versioned checker before claiming usable optimized validation.** No workflow, scientific status, frozen protocol, historical source/data/result, index/HEAD/ref or remote was changed by this audit. Initial audit execution was temporary-only. Subsequently authorized engineering preparation added only the two new opt-in helper/test files listed below; their logs remain under `/tmp/r-series-review-20261117/`. No network, human data, dependency install, CI or math campaign was used.

| PR | Exact head | Archive assessment | Separate remaining boundary |
| --- | --- | --- | --- |
| 36 | `211f90b2509a9e958b560780bc30d7a488a518b9` | Qualified: R273 original Python emission, S69 original Node entrypoints and source joins | R077 data/license/session mapping still blocked; no scientific acceptance or production claim |
| 37 | `a6f51d4b4805ce585f791ecb1cade7b6528bd594` | Qualified: S73 original Node R/B native file I/O and bounded controls | S73 frozen text says runnable standard-library Python, archived implementation is Node; scientific owner decision remains necessary |
| 38 | `fbf71dcaee98508a0a861518bfcc6bb768da5a81` | Qualified as defect evidence and explicit-guard candidate only | Historical B checker remains unsafe under optimization; candidate is not deployed |

The cached actual PR records show all three OPEN draft; GitHub reviews/comments arrays are empty. Internal independent reviews are real checked-in artifacts, not GitHub approval events or outside-team replications. Do not present this report as a PR merge, workflow adoption, scientific queue closure or upgrade beyond E1.

## Reused evidence remains applicable to latest main

Read actual PR metadata/file lists, branch objects, reports, implementation, pins, raw stdout/stderr and independent-review notes. Every source/input pin still exactly matches latest main (bytes, SHA256 and Git blob): PR36 18/18, PR37 12/12, PR38 11/11. All executable/package inputs are unchanged since their recorded internal reviews:

- PR36 reviewed `ed56c7e4f1970c1dda66c028daf66d9b4fdea939`; later changes are handoff/report/plan/evidence notes. PR39 subsequently independently accepted the exact final PR36 head. Its `INTEGRATION_REVIEW.md` and actual six-PR integration results may be reused only for the reviewed scope. PR39 explicitly excluded PR37/38.
- PR37 reviewed `f04469d40407b383d4a19bbfc0d8d7400ae12e2a`; final head adds only the review note.
- PR38 reviewed `63c20ef3fe68112de8db37e2d1efb6935a7f7787`; final head adds only DELIVERY and the review note.

Recomputed every recorded stream length/SHA256 (plus Git blobs where recorded): PR36 normal/optimized 32+32=64 streams, PR37 30 streams, PR38 72 streams. All pass. Recomputed PR36's 44 summary source/package identities and PR37/38 harness, pins/package and tar identities; all pass. Established R273/R277 numerical algorithms were not needlessly rerun.

PR36's scope is exactly five artifact byte identities (original 1728-row CSV, 27-world JSON, machine receipt; S69 576-row CSV and JSON), native Node original R selftest/emission and B checks, and the 576 paired-state to 1728 predictor-record join with 27 risk fields. Five new test methods per parent mode and eight listed bad JSON controls per mode are already independently verified. **The original Python emitter ran isolated NORMAL in both parent modes; this is not evidence that its historical assert-based gates survive optimization.** The archived entire original unittest suite was not rerun. R077 source qualifications are historical bounded observations, not a license or data availability requalification.

PR37's 15 native subprocesses are seven positive calls and eight domain-error rejections, not 15 unit tests. Two regenerated artifacts are byte identical: CSV 2449 bytes SHA256 `4e78fd4724011ee6e40f67907dde299fcbf6e3f868efddc2ea48e3529f74d463`, JSON 5349 bytes SHA256 `d8d6e5626996afbe28aba630ad1222dc826738e7896946183a80a162a079e607`. B reads archive, regenerated and reversed-row CSV inputs and returns full 72-probability/27-confusion/9-TV/72-row receipts. The eight negative cases are probability/confusion/TV/evidence/freeze/missing-window/added-row/deleted-row. The last two only show coverage checks reject those cases; they do not establish general CSV schema safety. Original R's two field-difference controls earn no new validator-rejection credit. Protocol language mismatch is explicitly disclosed, and does not invalidate faithful archive execution.

PR38's recorded 36 commands/72 streams include the original Node emitter, patch applicability, eight good archive/generated invocations and 24 negative invocations. Its two regenerated archived artifacts match all frozen bytes; 480 zero-probability placeholder rows remain. The patch preserves all 18 original guard conditions and the entire remaining original AST, adding only explicit require/ValueError behavior. The candidate scope gate rejects both changed-likelihood and disabled-evidence AST mutations. Coverage is six bad-file categories, not independent tests for every guard and not a general malicious-input/schema guarantee.

## Independently reproduced current R275 defect

Source: `research/evidence_audit/b_r275_s71_independent_gate_20261030.py`, latest-main blob `687aebf163193a4fb8f4667ec01774fcc047b2f4`, SHA256 `d6da1a90f84a81a5a0c1a9db252cdb4b977ffa47903a0929ed5281bc604a39ed`.

Lines 30–33 check qualification, including line 31's E1-only evidence. Lines 38–62 contain schema, row identity, probability, posterior and aggregate math assertions. All 18 are erased by Python optimization; line 63 still returns `status: PASS`.

Ran exact latest-main bytes in a disposable temp directory, with ordinary Python, explicit `-O`, and real inherited `PYTHONOPTIMIZE=1` (without `-I`, which intentionally ignores that environment variable). Used Python 3.12.14. Rebuilt actual files for the six existing mutation types. Preserved all stdout, stderr, argv, exit codes and input hashes.

| Input | Original normal | Original `-O` | Original `PYTHONOPTIMIZE=1` | Candidate, all three modes |
| --- | --- | --- | --- | --- |
| unchanged archived JSON/CSV | PASS | PASS | PASS | PASS |
| duplicate source row | AssertionError/exit1 | **wrong PASS/exit0** | **wrong PASS/exit0** | ValueError/exit1 |
| missing source row | AssertionError/exit1 | **wrong PASS/3071 rows** | **wrong PASS/3071 rows** | ValueError/exit1 |
| wrong source probability | AssertionError/exit1 | **wrong PASS/exit0** | **wrong PASS/exit0** | ValueError/exit1 |
| wrong MAP label | AssertionError/exit1 | **wrong PASS/exit0** | **wrong PASS/exit0** | ValueError/exit1 |
| wrong posterior | AssertionError/exit1 | **wrong PASS/exit0** | **wrong PASS/exit0** | ValueError/exit1 |
| JSON evidence changed to E3 only | AssertionError/exit1 | **wrong PASS/exit0** | **wrong PASS/exit0** | ValueError/exit1 |

Independent reproduction: 42 Python subprocesses plus temp patch check/apply. Original: three good passes, six ordinary rejections, **12 optimized false acceptances**. Candidate: three good passes, **18 bad-file rejections** (the six total good passes count both original and candidate). Every genuine rejection has empty stdout and expected AssertionError/ValueError; syntax/import failures are excluded.

Candidate applied only to a temporary source copy and authenticated against the recorded 18-condition AST scope. Candidate remains exactly 3568 bytes SHA256 `27ee7c88b02f70fb989f1dddea23279f7dbd18996c75c73462792e3ceebcacf0`, with zero asserts. This establishes a guard-removal defect, not incorrect historical default-mode results, prior use of optimized mode in formal runs, or human-data impact.

### Bounded implementation recommendation

A separately versioned **archival** checker has now been added after explicit follow-up authorization; see the implementation and verification below. The bounded design recommendation was: add it beside new engineering work. Keep the frozen original checker and original protocol/results untouched. Reuse the exact historical Fraction/K-count mathematics and the 18-condition explicit-guard transformation already independently qualified; pin both the original source identity and transformed candidate identity. Clearly label its receipt as bounded E1 archival validation with no production/workflow adoption. A standalone versioned checker is preferable to editing the historical file or silently applying the old production patch. If the new entry loads/generates a checker, authenticate inputs before executing them and ensure optimization cannot disable any acceptance condition.

Required verification for that entry: good frozen inputs in normal, `-O`, and environment optimization; each six bad-file categories rejects in all three; source/patch/candidate hash mismatch fails closed; guard/likelihood AST tampering rejects; historical source, protocol, workflow and archived results stay byte identical. Broader schema hardening can be a separate task; neither this evidence nor the old patch proves it.

## Current-main dependencies, conflicts and minimal combination checks

All PR36/37/38 changes are additions in distinct B archive directories: 56/7/17 files. Their common merge base is `d4740c2cd999b8da06a25b0ef407aeaf8a56ab6c`. Each classic three-tree Git merge against latest main exits0 with no conflict markers. None intersects paths changed by main since the common base. No path overlaps exist with each other or actual PR30/31/32/33/35/39. None of their pinned input paths is modified by any of those candidate PRs. Thus they add no order dependency and no additional runtime pin conflict to that historical batch. PR30→updated PR31 remains a separate previously established dependency; do not reapply PR35's superseded B pin patch.

Minimal targeted combined-checkout qualification:

1. Overlay actual immutable PR36/37/38 additions on latest-main files in a disposable tree. Authenticate every pinned source and every executable/package artifact, along with raw stream archives. No old candidate patch should be applied to main.
2. When PR30/31 are also included, reuse or rerun source-only B31 capture normally and optimized, with PR30 first; retain A33's expected production-veto status. This does not require new human scoring or R127 math.
3. For these archive additions, fixed-source identity plus existing reviewed native results is sufficient; rerun PR36's five join tests in both modes only if its source/join inputs change. Rerun PR37's single bounded replay only if source/artifact identities change. A combined all-research campaign adds no relevant evidence.
4. If the new versioned R275 checker is included, execute its three-mode good/bad/identity matrix after the actual overlay and ensure it references authenticated historical inputs. Do not conflate its success with fixing or adopting the historical optimized entrypoint.

No real CI, workflow activation, new E2/E3, production acceptance, formal queue update or scientific reacceptance is implied by archival merge. S73 language adjudication, R077 qualifications and externally authorized scientific/production decisions remain separate.

## Authorized versioned archival helper (implemented)

New files only:

- `/workspace/Psychohistory-Research/research/engineering_integrity_20261117/r275_archive_gate_v2.py`
- `/workspace/Psychohistory-Research/research/engineering_integrity_20261117/test_r275_archive_gate_v2.py`

The opt-in public CLI accepts only exact source/JSON/CSV archive byte identities. It reads each once with a bound on size, authenticates SHA256, transforms only the authenticated original 18 Assert nodes to explicit `_require` calls in memory, and runs the original math against private captured snapshot files. No old source or patch is copied wholesale into a new production module. Original AST conditions and duplicate-source message are retained; likelihood/evidence/source truncation changes fail before compilation. Receipt is `PASS_BOUNDED_ARCHIVE_REVALIDATION`, `E1_ARTIFICIAL_NONBLIND`, new E2/E3=0, production_ready=false, workflow_adopted=false and scientific_acceptance=UNCHANGED.

Run from any directory:

```sh
python -B /workspace/Psychohistory-Research/research/engineering_integrity_20261117/r275_archive_gate_v2.py
python -B /workspace/Psychohistory-Research/research/engineering_integrity_20261117/test_r275_archive_gate_v2.py
```

Six unittest methods passed; 43 real subprocesses are fully recorded in `native-audit/r275-v2-matrix.json`. The public CLI passes the good archive in normal, `-O`, and `PYTHONOPTIMIZE=1`; six bad archives reject by identity in all three modes. Separate private-engine tests deliberately bypass only public input-identity qualification to show the actual six semantic guards reject in all three modes (18 domain failures). The CLI has no identity bypass. Three legacy E3 calls preserve normal rejection and both optimized wrong PASSes as explicit RED evidence. Missing-file failure has empty stdout. Source likelihood/evidence-guard/truncation tampering all rejects before execution. Root `git diff --check` also passed at verification time.

**The historical callable STILL REMAINS BLOCKED FOR PRODUCTION until owner-approved routing replaces the old gate.** This new helper is local opt-in archive revalidation only: no workflow, production caller, formal acceptance or historical record was changed. The exact historical source and both archive artifacts still match all three pinned SHA256 identities after testing. Optimization remains unsafe on the legacy callable.

## Local evidence

- `native-audit/identity-stream-checks.json`: latest-main pin equality and PR37/38 raw stream checks.
- `native-audit/pr36-stream-checks.json`: both PR36 stream sets and original summaries.
- `native-audit/package-checks.json`: executable/package/stream-archive and PR36 source identities.
- `native-audit/merge-and-dependency-checks.json`, `native-audit/pr{36,37,38}-merge-tree.log`: latest-main and historical candidate path/dependency checks.
- `native-audit/reproduce_r275.py`, `native-audit/r275-reproduction/summary.json`, `*.stdout`, `*.stderr`: independent current-source reproduction and candidate qualification.
- `pr-native-results.json`: compact machine-readable disposition.

New helper verification: `native-audit/r275-v2-tests.stderr` contains the six passing test methods; `native-audit/r275-v2-matrix.json` contains raw argv, optimization environment, stdout/stderr and exits for every new/legacy subprocess.
