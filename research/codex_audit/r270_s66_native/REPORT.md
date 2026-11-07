# R270 S66 native replay and independent prefix-state DP

Status: COMPLETE for the pinned engineering replay. S66 scientific status remains PARTIAL_BOUNDED_INTERNAL_EXACT. Date: 2026-10-29 UTC. Observed main: `7c5d5650af12cfdd08e0f2d23b73a49e6f506d29`.

## Target and completed work

Latest R/B reports and E100 still mark the archived R JavaScript native Node entry point NOT_RUN. Ten open Codex draft PRs address other targets, including S67 in PR #10. This increment closes the pinned S66 native replay gap without editing historical sources, protocols or results. Original R270 acceptance, R073 and PESEN v0.1 remain unchanged.

Actual execution used Node v24.19.0 and Python 3.12.14 standard library. The original R Node `--selftest --check` and original portable B Python `--selftest --check` pass on the actual full 7,501-byte archived receipt. Each route rejects its five built-in negative cases. R `--emit` into a fresh temporary directory produces a file byte-identical to the archive, and both original CLIs validate that emitted file. These are five positive CLI invocations. Three executed source/data files match their exact pinned Git blobs before and after execution.

The new independent Python route counts six-bit prefixes by (success count K, adjacent-equality count T, last bit). It extends each state with zero and one, retaining integer multiplicities. This obtains the replicate type table without listing all 64 replicated strings and without B's run-composition binomial-coefficient formula. For posterior integers A,B, each ordered replicate with k successes has mass B(A+k,B+6-k)/B(A,B), calculated using factorials and Fraction. The DP multiplicities weight these masses; summing over T_rep<=T_obs gives each exact lower tail. Observed sequences remain the frozen 64 cases per prior.

All 192 tails and all 27 alarm records agree. The full DP-produced JSON, including every declared field, is also byte-identical to the archived receipt and is retained as `logs/DP_full_receipt.json`. The route checks 192 predictive normalizations and nine generating normalizations. It imports neither original R nor B.

At theta=1/4 or 3/4, risks at alpha=1/20 and 1/10 are 27/2048; at alpha=1/5 the risk is 27/256. At theta=1/2 the corresponding risks are 1/32, 1/32 and 3/16. The original alternating-observation tails 10/429, 7/286 and 16/715 are reproduced. These confirm known artificial-grid results; they do not establish universal conservatism or empirical calibration.

## Controls and representation boundaries

The replay exercises three additional actual CLI controls:

| Input change | Original R JS | Original B Python | New DP typed semantic check |
| --- | --- | --- | --- |
| One exact tail changed to 999 | rejects | rejects | rejects |
| Same values, top-level keys reversed | rejects | accepts | accepts |
| Alarm count 2 written as 2.0 | accepts | accepts | rejects |

The key-order rejection follows R's JSON.stringify comparison, which includes object insertion order. Its persisted receipt passes; this control demonstrates a presentation-dependent rejection, not a wrong numerical result. Python's nested dictionary equality regards 2.0 and 2 as equal; JavaScript parses both as the same Number. The DP requires Python int for count fields. This is a deliberately stricter representation/type policy, not evidence of incorrect risk, false empirical promotion or a uniquely established protocol violation. Preserve this distinction when comparing validators. Byte authentication and semantic/type checking are separate checks in the runner.

Ten oracle tests first failed against an empty stub (ten assertion failures, zero errors). The final normal and optimized-mode suites each pass ten tests. They cover authentic full receipt, DP count edge cases, literal alternating tails, known alarm risks, wrong tails, floating/Boolean counts, missing tails, evidence promotion and key reordering. Raw red/green and final logs are retained. The selftest mutation sets in the original programs are separate from these ten new tests and must not be added as if they were independent scientific studies.

## Reproduce and audit trail

From a repository snapshot with the three pinned original inputs and this directory, using only Python and Node:

```sh
python -B -m unittest discover -s research/codex_audit/r270_s66_native -v
python -B -O -m unittest discover -s research/codex_audit/r270_s66_native -v
python -B research/codex_audit/r270_s66_native/run_native.py . --output /tmp/r270-s66-audit
```

Use a distinct output directory per concurrent run. The runner protects input aliases, invalidates a previous execution.json before checking pins, checks sources again after execution, and publishes a new COMPLETE execution.json atomically after success. A failed protected-alias request preserves input files. No file-system lock is provided; keep the pinned input snapshot stable. `logs/execution.json` records actual commands, temporary paths, versions, hashes and exit codes. The runner's pinned_source_baseline identifies where pins were read, rather than claiming to query Git HEAD. Source manifest records the independently fetched remote HEAD and read ranges.

A fresh engineering reviewer reran all ten tests and the native replay without Critical or Important findings. The Minor operational limitation is that reusing an existing output directory replaces its previous execution/log files. This behavior is retained to invalidate stale successes; use a new output directory for every evidentiary run and preserve prior outputs separately. This is a caller requirement, not an enforced append-only archive. The committed artifacts retain this delivery's actual execution. Review is internal engineering review, not external scientific replication.

## Evidence and limits

All original outputs and protocols were read before new code: NONBLIND internal artificial E1 verification. This closes a native entry-point evidence gap and adds a different exact algorithm. It is not blind confirmation, external-team replication, empirical calibration, a human experiment or historical prediction. New E2/E3/external-team replication all zero. Original R270 bounded acceptance and S66 PARTIAL scientific status are preserved.

Original R270 83-test suites and full repository tests: NOT_RUN. The older nonportable B script writes to `/mnt/data/r270_s66/b_oracle.json`; its native CLI was NOT_RUN, and it was not changed. The archived portable B CLI was the executed source. This environment uses an isolated exact API snapshot, not a full native Git checkout/worktree. Delivery adds only Codex audit/coordination paths in a separate branch and draft PR.

GitHub Actions NOT_RUN for this increment. No paid API, cloud provisioning, purchased data, workflow dispatch or new automation. GitHub account billing and free CI quota NOT_VERIFIED; messages use `[skip ci]`.

Next: fresh main and handoff review, then select a still-open R-series source/receipt gap. Retain the key-order/type boundaries as bounded engineering observations; do not change historical acceptance or duplicate another track's newly completed replay.
