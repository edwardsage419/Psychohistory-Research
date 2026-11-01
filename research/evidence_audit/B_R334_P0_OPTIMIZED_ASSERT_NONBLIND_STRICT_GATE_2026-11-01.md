# B audit: R334 optimized-mode receipt false acceptance

Date: 2026-11-01 UTC. Priority: P0. Track: R/B, with no overlap with Codex PR #1/#3 R257 S53. Scope: finite E1 receipts only. Review mode: same-team nonblind independent arithmetic. No external independent team.

## Exact input identities

Pinned original Python blob `7d232a07d9d2979c2fcc8a407dd8bda18cd8ab93`.
Pinned original CSV blob `6e3bdcc5ca07d1321a651c29b899798a32f7fb72`.
Pinned original JSON blob `02883b6b9cfc22b3b855d8a7cbaa5e5ddf6bd86c`.

The archived original Python was copied without byte changes to a local temporary test directory. Original `render()` reproduced the exact archived CSV and JSON Git blobs. Every mutation was confined to the temporary directory. Original frozen files and main branch source were not modified.

## Actual CLI matrix

Environment: local CPython 3.13.5, standard library, no random seed or external packages. Each row was executed twice using the original CLI `--test --audit` and the new no-import strict receipt checker. Exit codes below are direct subprocess observations.

| Case | Original normal | Original `-O` | Strict normal | Strict `-O` |
| --- | --- | --- | --- | --- |
| Clean pinned files | 0 PASS | 0 PASS | 0 PASS | 0 PASS |
| One CSV model label changed | 1 FAIL | 0 FALSE PASS | 1 FAIL | 1 FAIL |
| JSON schema value changed | 1 FAIL | 0 FALSE PASS | 1 FAIL | 1 FAIL |
| Both receipt files absent | 1 FAIL | 0 FALSE PASS | 1 FAIL | 1 FAIL |
| Source file appended newline | 0 PASS | 0 PASS | 1 FAIL | 1 FAIL |

All original optimized false-positive cases printed `R334 PRODUCTION_REPLAY_PASS` and their five original unit tests reported `OK`. Source-only alteration leaves arithmetic unchanged; original source identity was not a checked predicate. No actual archive tampering is alleged.

## Root cause and repair conditions

Original `audit()` contains only `assert` guards. Python optimization removes those expressions and therefore skips the file reads entirely. The `unittest` harness still executes internal generated-state tests and can report success. The added independent checker uses explicit `ValueError` failures, pinned source/receipt Git blob identities, complete CSV and JSON structure and independently calculated rational values. It does not import the original R334 model.

Reproduction:
```
python research/evidence_audit/test_r334_optimized_gate_20261101.py
python -O research/evidence_audit/r334_strict_receipt_gate_20261101.py
```

The test script regenerates pinned receipts from the original source for fixture setup. The strict checker separately reconstructs all 48 rows and 16 condition records. Tests also check the optimized mode explicitly, preventing a regression that relies on `assert`.

## Status and scope

**COMPLETE:** P0 false acceptance reproduced on the exact archived original source; strict additive checker and four mutation controls executed and passed in local CPython 3.13.5, normal and optimized modes. Independent arithmetic is internal nonblind E1 only.

**PARTIAL:** Original production CLI still has the fail-open condition. No owner-approved replacement or source modification was performed. Native 3.11/3.12 replay of the new checker and independent external-team review are NOT_RUN. Historical R334 CI run 40051279908 remains success for its normal-mode bounded E1 tasks. E2, E3, empirical calibration, causal mechanism identification and cross-experiment prediction are NOT_ESTABLISHED.

**CI:** NOT_RUN for this new work. GitHub Actions free quota and actual account billing were not independently inspected. No paid operation performed.
