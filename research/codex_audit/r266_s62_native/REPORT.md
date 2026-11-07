# R266 S62 native archival replay and complete source reconstruction

Status: COMPLETE for this engineering replay. Scientific verification remains PARTIAL; original R266 bounded E1 acceptance is unchanged. Date: 2026-10-29 UTC. Observed main: `3d5349f5505679492ee324f8b47d028476b1fc7b`.

## Task and completed evidence

R266 S62's R/B reports and E096 explicitly leave native execution of the two archived JavaScript programs and the exact archived Python source-rebuild script open. Existing Codex PR #1–#11 address other targets. This increment uses those original scripts without edits, reads the actual original CSV and baseline JSON, and adds isolated Codex-owned code/logs. It does not change protocols, R073, PESEN, original results or acceptance.

The native original R Node CLI produces 7,423 stdout bytes equal to the entire persisted S62 receipt. The original B Node CLI checks all 18 rows and 180 fields and rejects its five built-in mutations. The original Python rebuild CLI reports 5,328 rows, 419,791 bytes and the historical source SHA256. A separate clearly identified byte-export adapter calls that same original regenerate() function, exposes its full byte output in a temporary directory, and confirms exact equality against the actual remote-fetched original CSV. This adapter is additional to the original native CLI invocation, not a substitute for it. B also checks the replayed R output. Overall: four positive original CLI invocations plus one byte-export adapter.

All six executed source/data inputs match exact Git blob pins before and after execution. The CSV SHA256 is `5e0aac41c960ee21b54d3266064793a7e9a2454dbb4493ae8e4451591d48587a`, Git blob `53a808994300f85826a18723146fdb2fea7c6db2`. This round reads the persisted CSV bytes; it does not infer source identity solely from a newly generated dataset.

## Added independent source-row checks

The Python source auditor imports neither archived R nor B. For every primitive tuple it independently applies each frozen event function, reconstructs IID or antithetic success counts, estimates, source masses, true means and squared errors, and checks all 11 CSV fields. It checks tuple bounds, uniqueness, complete finite source coverage and mass normalization for all 18 world/design groups. Total: 5,328 rows and 58,608 field checks; the tuple itself is an input whose validity and complete coverage are checked, not a new independent observation.

It accumulates exact source-weighted means, second moments and expected IID plug-in variance. It computes actual estimator variance from the moments and Wilson z=2 coverage using n*(estimate-p)^2 <= 4*p*(1-p), including equality. The derived 18 means, variances and source counts agree with their baseline reference, and all 180 S62 metric fields agree. This is not a full audit of every field or PMF in the original baseline JSON; baseline authenticity is separately pinned by bytes.

The previously known SYMMETRIC_EXTREMES_N6 counterexample is confirmed: IID coverage 31/32, antithetic coverage 3/4, antithetic expected naive/actual variance ratio 1/3. Zero true variance in THRESHOLD_HALF antithetic cases retains a null ratio. These frozen mathematical results were read before implementation and are not counted as new discoveries or empirical observations.

## Tests, review and failure record

Eight tests total comprise two positive cases and six mutation rejection cases: missing source, duplicate source, coherently altered hit/estimate/error fields for an unchanged primitive tuple, changed baseline variance, wrong coverage, and replacing an undefined variance ratio with zero. The coherent-hit mutation ensures that checking only algebraic consistency of the derived columns cannot pass the source audit.

All eight tests initially failed against an empty stub (eight assertion failures, zero errors). Final normal and optimized-mode runs each pass eight tests, zero failures/errors. The five B built-in mutation types are separate original checks, not eight additional studies. A fresh engineering reviewer reran all eight tests and the native runner, found no Critical/Important issue, and confirmed the current code hashes. Review corrected test-count wording to distinguish eight total tests from six mutation cases. No numerical inconsistency or new historical protocol violation was found within this scope. Red failures are intentional test-development evidence and are retained alongside final green logs.

## Reproduce

Use Python standard library and Node, with the six pinned original inputs and this new directory present:

```sh
python -B -m unittest discover -s research/codex_audit/r266_s62_native -v
python -B -O -m unittest discover -s research/codex_audit/r266_s62_native -v
python -B research/codex_audit/r266_s62_native/run_native.py . --output /tmp/r266-s62-audit
```

Use a fresh output directory for every evidentiary run. Reusing a directory replaces previous logs; preserve old runs separately. The runner refuses protected input aliases, invalidates an old execution.json before pin validation, checks original input identities after execution, and publishes COMPLETE atomically only after success. Input snapshots must stay stable; no filesystem lock or permanent concurrency guarantee is supplied. Exact commands, temporary paths, environment, versions, hashes and output filenames are in logs/execution.json. The pinned_source_baseline is the remote version from which pins were read; the runner does not itself query Git HEAD.

## Scientific and operational boundaries

NONBLIND internal computation on exhaustive artificial E1 probability spaces. The original R266 result, S62 result and protocol were viewed before the new implementation. No external research-team replication, blind confirmation, actual stochastic experiment, human prediction, historical prediction or general interval-calibration claim. New E2/E3/external-team replications all zero. The native archival execution gap is closed for these pinned sources; full independent scientific validation is not declared.

Original R266 Python 3.11/3.12 136-test suites, full repository tests and historical CI reruns: NOT_RUN. Existing CI claims in the original acceptance file were read as historical claims; they were not newly verified. The environment uses an isolated exact API snapshot rather than a native full checkout/worktree. Delivery adds only new Codex files in an independent branch and draft PR.

GitHub Actions for this increment: NOT_RUN. No paid API, cloud provisioning, workflow dispatch, new automation or data purchase. Account billing/free CI quota NOT_VERIFIED; delivery uses [skip ci].

Next: refresh main/PRs/handoffs and select another still-open R source/receipt gate. R267 S63 may warrant a native replay if still open, while its historical FAIL_TIMING must remain failed; computational agreement cannot repair the protocol order.
