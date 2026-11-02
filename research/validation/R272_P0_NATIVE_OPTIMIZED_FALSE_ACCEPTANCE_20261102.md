# R272 P0: native optimized-mode false acceptance with isolated receipt corruption

Date: 2026-11-02 (Asia/Singapore). Track R, B scientific validation. Starting main `e5d81b59670b51a72be4bf2a8fa89a42ff74ba73`. Scope: original239 `12-002`, R272 finite artificial E1. Status: **OPEN, reproduced in the archived original Python implementation**. No frozen protocol, historical receipt, or original implementation was edited.

## Fixed subject and byte identity

Original source: `research/R272/r272_exact_train_test_prediction.py`, Git blob `13843eecf2f9f05c19ee5545bdb224f58313f367`, 10,677 bytes. Source was reconstructed from the connected GitHub reader into an isolated local directory; `git hash-object` matched the original blob exactly before execution. Frozen protocol: `protocols/R272_OUT_OF_SAMPLE_9_BERNOULLI_WORLDS_576_FULL_SOURCE_PRESCORE_FREEZE_2026-10-23.md`, blob `9fbdb0078a58c4a9c0a548643227e30da5731119`, freeze commit `52f84dbfbe8563cf5c9a491e67d5e320223e0a56`. Historical workflow `.github/workflows/r272-exact-train-test-oos-e1.yml`, blob `3132b08cf4ee64b55f5112d2249894ea0ec9d42d`, uses ordinary Python.

Local environment: CPython 3.13.5, standard library only, no external services or random seed. The exact archived program was run in normal and optimized mode:

| Execution | Observed |
| --- | --- |
| `python research/R272/r272_exact_train_test_prediction.py --test` | 83 tests PASS |
| `python -O research/R272/r272_exact_train_test_prediction.py --test` | 83 tests PASS |
| `python research/R272/r272_exact_train_test_prediction.py --emit` | 576-source CSV and result JSON reproduce historical bytes |
| CSV Git blob | `8fbbc73d239765f5c66395af1bcf9cf7a8df1f41` |
| JSON Git blob | `db3ca11ae224af52c2caf385c898e24aaa0cc54b` |
| CSV SHA256 | `dc40ed773491817caf242ba6416e1bdf98ef2f1a2cd05e1956bdf5aec5801663` |
| JSON SHA256 | `f891df1c4640c2f49a457c436bc043f6bc08b768ac92594050e7e08061495a40` |

## Native error-injection experiment

Reproducible script: `research/validation/r272_optimized_assert_native_injection_20261102.py`, Git blob `185ba3887afeaf743a004ff0ba19eaf285bb866b`. The script imports the exact archived source and injects errors at runtime. It redirects `HERE` into a disposable temporary directory before calling the original `emit()`; original repository data remain untouched.

For each `K` in `mass_zero duplicate_identity oracle_zero`, run both `python research/validation/r272_optimized_assert_native_injection_20261102.py K` and `python -O research/validation/r272_optimized_assert_native_injection_20261102.py K`.

| Injection | Normal CPython | CPython `-O` | Observed invalid acceptance |
| --- | --- | --- | --- |
| `mass_zero`: first source probability in each world replaced with zero | REJECTED, AssertionError | ACCEPTED, `claims_verified=true` | First world probability mass `3367/4096` instead of 1, incorrect weighted score `3367/16384` |
| `duplicate_identity`: first six-bit identity duplicated | REJECTED, AssertionError | ACCEPTED, `claims_verified=true` | Only 63 distinct six-bit sources in first world, despite receipt claiming 576 complete sources |
| `oracle_zero`: independent analytical oracle returns three zeros | REJECTED, AssertionError | ACCEPTED, `claims_verified=true` | Receipt still claims nine independent analytical comparisons although the oracle disagrees |

All six executions completed. The optimized runs emitted machine receipts and JSON with affirmative scientific flags. The `oracle_zero` case is particularly diagnostic: original CSV and result JSON hashes remain identical to the archived valid bytes, while the independently computed oracle has been corrupted. Therefore a matching file hash alone cannot establish that the claimed independent oracle was actually checked.

Root cause: `frozen_claims()` and `exhaustive_moments()` use Python `assert` for mandatory scientific invariants. CPython optimization removes these checks. The original `emit()` then unconditionally sets `all_nine_analytical_binomial_scores_verified=True` and `independent_analytic_comparisons=9` after the skipped validation. Ordinary `unittest` methods use explicit assertion methods and still pass under `-O`, which does not independently exercise these runtime error injections.

## Scope, remediation and closure conditions

This is a **confirmed execution-mode false-acceptance vulnerability** for R272's original generator. No evidence shows that the archived historical CI ran with `-O`, or that its original E1 numerical result was falsified. The historical successful CI remains evidence for its documented ordinary-mode execution only. The earlier independent full-source BigInt E1 replay remains valid within its finite artificial scope.

A future candidate fix should replace all mandatory production scientific `assert` guards with unconditional explicit exceptions, ensure the independent analytical comparisons actually run, and only set positive receipt flags after successful checks. The independent archived-source gate must check world identity, unique six-bit source coverage, probability mass, heldout split, per-row scores, frozen expected values, and receipt identity. Test both `python` and `python -O` with the three injections; all must reject. Verify against frozen archived CSV/JSON hashes, review the workflow caller path, and preserve historical failing evidence. Do not silently rewrite the original frozen protocol or receipts. This report does not claim production adoption or P0 closure.

Evidence level: internal nonblind native Python E1 program audit, not a new E1 model result, human E2, historical E3, or external-team independent replication. No new original239 item closed; R073 and PESEN v0.1 remain frozen. No GitHub Actions were triggered, no paid API was used, and account billing was not independently checked.
