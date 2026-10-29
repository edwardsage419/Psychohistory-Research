# R271 S67 native Node replay and independent run-length oracle

Status: COMPLETE for this bounded native replay. Date: 2026-10-29 UTC. Main observed: `e2614fec5027247de328a5aeef295c4ed3bc9338`. Dedup target: archived S67 native CLI/persisted bytes, explicitly NOT_RUN in the latest R handoff. Previous nine Codex draft PRs concern other targets. Original R271, R073 and PESEN v0.1 remain unchanged.

## Executed evidence

The original R JavaScript generator and original independent B JavaScript validator were executed as native Node v24.19.0 CLIs, with no source changes. Five executed source/data inputs match their pinned remote Git blobs. The actual archived CSV is 1,648,483 bytes, contains 13,584 policy-labelled mathematical source rows, and has SHA256 `9a72624ebcfc77e3eb65cdfe44696efc0d85a282f695a5ad77029753f75db9cb`.

Three positive CLI invocations succeeded: B on persisted archive; R generating into a fresh temporary directory; B on the regenerated files. R's generated CSV, exact-risk JSON and machine receipt each equal the corresponding archived file byte for byte. B verifies all 27 worlds and all 13,584 rows and rejects its six built-in mutations. These six mutation types repeat in the second B invocation; they are not twelve distinct tests.

The independent new Python oracle uses integer path counts for rolling windows. Live states track trailing success lengths zero to three; on each bit an existing hit has two continuations and a live run of three gains one hit. Thus after L=m+3 bits the exact hit probability is hit/2^L. This route neither enumerates primitive strings nor uses B's inclusion-exclusion. Identical-window risk is 1/16; disjoint risk is the independent complement 1-(15/16)^m. Frozen-first and Bonferroni thresholds are then applied with exact Fraction arithmetic. The oracle imports neither archived route and agrees with all 27 archived world risks.

For m=3 flexible reporting, identical=1/16, rolling=1/8, disjoint=721/4096. Rolling m=2 is 3/32; all m=3 Bonferroni risks are zero. These are confirmations of known exploratory results, with all outcomes read before implementation. They do not establish an empirical effect of preregistration policies.

## Counterexamples and failures retained

Two new genuine B CLI negative checks alter a risk and delete a CSV row. Checksums are recomputed to isolate substantive validation. Both exit nonzero, respectively `independent exact risk` and `CSV row count`.

A third sandbox changes only result metadata `R073` from `FROZEN` to `MODIFIED`, updates its receipt checksum, and leaves every mathematical row unchanged. Original B still returns PASS. The new Python oracle rejects it. This is a bounded metadata-coverage gap: B does not validate this result flag. It is not evidence of an actual R073 source modification, corrupt archived risk, or scientific model failure. The correct archived flag is FROZEN. The additional oracle validates identity, evidence and freeze declarations alongside mathematical risks; it is not a replacement for B's full CSV checks or cryptographic source pinning.

Initial source transport failed: GitHub's contents API returned empty content for the CSV larger than 1 MiB. An early B CLI attempt therefore exited ENOENT. `initial_missing_csv.log` and `initial_transport_issue.json` preserve this. Fetching the exact Git blob resource returned the full CSV; local blob and SHA256 checks succeeded before the scientific replay. The model was not blamed for the transfer failure.

Eight new oracle tests first fail against an empty stub (eight assertion failures, zero errors). Final normal and optimized-mode executions each pass eight tests. Cases cover the authentic full universe, literal hand-derived contrasts, duplicate/missing worlds, wrong risk, boolean counts, freeze-flag change and false promotion to blind status. `run_native.py` reproduces the original CLI controls and source pin checks; `logs/execution.json` records exact commands, temporary paths, environments, hashes, exits and outcomes. Temporary full CSV copies are deleted after comparison; no large duplicate dataset is published.

A fresh scoped engineering reviewer reran eight tests and the complete native replay, reporting no Critical or Important finding. A Minor provenance naming issue was corrected: the runner records a `pinned_source_baseline`, rather than claiming to observe Git HEAD itself. Main was independently read through GitHub API; the runner authenticates only the five pinned inputs. After that rename the complete native replay was rerun and execution code hashes regenerated. This is internal code review, not external scientific replication.

## Reproduce

Use an exact repository snapshot containing the five original inputs and this new directory. Python standard library and Node only, with no dependency installation:

```sh
python -B -m unittest discover -s research/codex_audit/r271_s67_native -v
python -B -O -m unittest discover -s research/codex_audit/r271_s67_native -v
python -B research/codex_audit/r271_s67_native/run_native.py . --output /tmp/r271-s67-audit
```

Use a distinct output directory per concurrent run. The runner invalidates an old success before source validation, requires exact input pins, rechecks them after execution, and atomically publishes execution.json on success. Protected input aliases are refused without altering input files. As with any file-based checker, input snapshots must remain stable; this code supplies no concurrent filesystem lock.

## Scientific and operational limits

NONBLIND internal algorithm verification of artificial E1 only. The original S67 design explicitly anticipated overlap effects; STRICT_BLIND_PRESCORE_FREEZE remains NO. No historical result is reclassified as blind. New human E2=0, historical E3=0, external-team replication=0. This closes the archived JS native entry-point gap for the pinned sources, not overall independent scientific validation or real-world causal applicability.

The historical Python programs mentioned by R/B are not archived at the specified S67 repository paths. Their reported 8+7 tests were NOT_RUN this round; the eight tests here belong to the new DP oracle and must not be confused with those historical tests. Original R271's 82-test suites and complete repository tests also NOT_RUN. This environment has isolated API snapshots, not a complete native Git checkout/worktree; only additive Codex files are delivered through a separate branch and draft PR.

GitHub Actions NOT_RUN for this work. No workflow dispatch, new automation, paid API, purchased data or cloud compute provision was used. Billing and free CI quota NOT_VERIFIED; delivery messages use `[skip ci]`. The original S67 documents are dated 2026-10-30; that historical text is preserved. Actual present execution is 2026-10-29 UTC as recorded here.

Next: reread current main/handoffs before closing another active R gap. R270 S66 native Node remains a candidate if not already closed; do not duplicate a later R-track closure. Publication of the originally executed S67 Python programs, if their actual authors can recover them, would strengthen archival provenance; do not reconstruct code and label it their historical source.
