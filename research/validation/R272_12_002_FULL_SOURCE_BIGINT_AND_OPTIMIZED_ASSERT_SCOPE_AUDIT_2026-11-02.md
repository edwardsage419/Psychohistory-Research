# R272 / original239 12-002: complete source BigInt cross-language audit and optimized-assert scope

Date: 2026-11-02 (Asia/Singapore). Track: R; subflow: B independent scientific verification. Run baseline main: `768e07a91560aa50252531dce198fd2bef5d5c94`. Audit implementation commit: `fb97706ff04c6c5151b6786232907a2574896d7c`. This is an additive nonblind internal E1 audit; the frozen R272 protocol and original receipts remain unchanged.

## Locked subject and inputs

Subject: original239 item 12-002 Out of Sample Prediction, R272. Original frozen protocol: `protocols/R272_OUT_OF_SAMPLE_9_BERNOULLI_WORLDS_576_FULL_SOURCE_PRESCORE_FREEZE_2026-10-23.md`, blob `9fbdb0078a58c4a9c0a548643227e30da5731119`, frozen at commit `52f84dbfbe8563cf5c9a491e67d5e320223e0a56`.

Archived CSV: `research/R272/R272_ALL_576_ORIGINAL_TRAIN_AND_TEST_SOURCES.csv`, Git blob `8fbbc73d239765f5c66395af1bcf9cf7a8df1f41`, 61,489 bytes. Archived JSON: `research/R272/R272_EXACT_RESULTS.json`, Git blob `db3ca11ae224af52c2caf385c898e24aaa0cc54b`, 4,402 bytes. Original Python source `research/R272/r272_exact_train_test_prediction.py`, blob `13843eecf2f9f05c19ee5545bdb224f58313f367`. Read these from GitHub main using the connected repository reader. Do not mistake the three predictors applied to the same 64 sources per p for independent experimental units.

## Executed independent arithmetic

An independent JavaScript V8 BigInt rational implementation was run against the full remote CSV and JSON content. It did not import or execute the original Python implementation. It reconstructs all ordered six-bit strings, the four-bit train / two-bit test split, success counts, Bernoulli source masses, three prespecified predictions, all six individual Brier losses, train/test means, and the unfloored infinite-log-loss event. It independently aggregates each world with exact rational weights and compares all nine archived result records.

Results: **576/576 source rows PASS, 8,640/8,640 CSV fields PASS, 9/9 complete world summaries PASS**. Exact train/future Brier pairs:

| p | Constant half | Train MLE | Laplace Beta(1,1) |
| --- | --- | --- | --- |
| 1/4 | 1/4 ; 1/4 | 9/64 ; 15/64 | 11/72 ; 31/144 |
| 1/2 | 1/4 ; 1/4 | 3/16 ; 5/16 | 7/36 ; 5/18 |
| 3/4 | 1/4 ; 1/4 | 9/64 ; 15/64 | 11/72 ; 31/144 |

Unfloored MLE infinite-loss event mass: 291/2048 for p=1/4 and 3/4, 3/32 for p=1/2. The other predictors have zero such mass.

Seven in-memory negative controls were executed against the same independent verifier: wrong source mass, altered test split, wrong forecast, altered test Brier, source identity duplication, false E2 grade, and altered world-level score. **7/7 rejected**. These mutations were applied to copies held in memory; no historical artifact was changed. No random sampling or seed was used.

Reproducible new verifier: `research/validation/r272_independent_full_576_bigint_gate_20261102.js`, Git blob `0833c476f233899f528b300e5219a9579e336002`. Its exported `verify` and `selftest` functions were executed in the JavaScript V8 tool environment with the exact content submitted. Native Node.js CLI execution on a complete local checkout remains **NOT_RUN**. When the complete repository is available, run:

```sh
node research/validation/r272_independent_full_576_bigint_gate_20261102.js research/R272/R272_ALL_576_ORIGINAL_TRAIN_AND_TEST_SOURCES.csv research/R272/R272_EXACT_RESULTS.json --selftest
```

The CLI checks both exact historical Git blob identities before semantic verification. The in-memory negative controls intentionally bypass the blob precondition to exercise semantic guards.

## Additional P0 candidate: optimized assertions in the original producer

Static source inspection found that the original R272 Python producer's `exhaustive_moments` and `frozen_claims` use bare `assert` for key mass, universe, analytical equality, frozen score, and infinite-event checks. `emit()` calls `frozen_claims()`. CPython removes those assertions under `python -O`. A local CPython 3.13.5 minimal counterexample (`assert 1==2`) raised AssertionError in ordinary mode and printed PASS in optimized mode. This proves the language-mode risk; the complete original R272 program was **not** executed with mutated inputs in optimized mode during this run.

Risk status: **OPEN_STATIC_SCOPE**. A future optimized invocation of the original emitter cannot rely on those assertions as acceptance guards. This does not establish any error in the archived original results or the historical normal-mode CI. The new BigInt verifier provides independent, explicit checks of the pinned archived CSV/JSON, and is not yet a mandatory production caller.

## Historical CI and current scientific boundary

Original R272 historical run `39903106107` was re-read from GitHub: completed/success, push at head `99ef67439e988a5f04b3a9482e85ad1509c97574`, with three successful jobs (Python 3.11, Python 3.12, independent-sources-and-archive). This historical CI predates this new audit and does not certify it.

Scientific evidence: **internal nonblind E1 artificial only**. New genuine human E2=0; historical E3=0; independent external-team reproduction=NOT_RUN; R073/PESEN v0.1 remain frozen. The original239 itemwise queue is unchanged by this additive audit. The latest read queue was `docs/ORIGINAL_239_PENDING_154_ITEMWISE_EVIDENCE_TRIAGE_QUEUE_2026-10-25.csv` (blob `3b96d46b3d88ccafd779a08509c3cfd0e435772f`), 154 items: P0 27, P1 82, P2 45. The latest crosswalk file remains v7.8, blob `36f24235901172642c46853298aebb421f1a3552`.

## A data and coordination

A quick English-source revisit of Romero and Rosokha (2023), *Econometrica*, DOI `10.3982/ECTA17482`, confirmed the previously recorded mixed-strategy elicitation design and publisher's 197 MB supplemental package. No new file, permission, participant/session dictionary, or R073 frozen-protocol qualification was obtained. Data candidate status: **PARTIAL**, qualified new R073 data=0, scored new E2=0. Codex PR #1 and #3 remain open, as do 12 open PRs at the observed read; no changes to Codex paths.

## Cost, failures, and next action

No new paid services, paid APIs, datasets, GPU, or Actions dispatch. New CI: **NOT_RUN**. Account billing/free quota: **NOT_VERIFIED**. Container Git network clone failed due to DNS resolution of github.com; full native repository replay remains **BLOCKED**. The independent arithmetic ran through the existing connected GitHub read access and V8 execution environment.

Next: independently reproduce the optimized-mode false-acceptance condition against the original R272 producer in a read-only complete checkout, then decide whether an R-owned strict gate can become a mandatory acceptance dependency. Continue the higher-severity R333–R340 composite gate native and caller-adoption investigation when full repository access is available. No original239 closure or scientific grade promotion is requested.
