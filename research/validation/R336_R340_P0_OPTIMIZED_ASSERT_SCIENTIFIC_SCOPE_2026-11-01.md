# R336 and R340: optimized-mode receipt integrity P0, bounded native reproduction

Date: 2026-11-01 UTC
Track: R main with B independent methods
Baseline main: a84210f0c2974590c85e6ac66a7d6be8e4933c34
Scientific status: P0_FALSE_ACCEPTANCE_CONFIRMED; ADDITIVE_GATE_TESTED; PRODUCTION_INTEGRATION_PARTIAL
Evidence: finite artificial E1 program-integrity audit, internal nonblind only

## Question and frozen boundaries

Determine whether the original frozen R336 and R340 receipt audit entry points reject corrupted or absent persisted CSV and JSON when run under Python optimized mode. Preserve original source, frozen protocol, receipts and historic acceptance records. A positive native reproduction establishes a checker integrity problem only; it does not establish manipulation of the historic archive, falsity of the finite mathematical results, or empirical E2/E3 validity.

Read and byte-reconstructed exact original source blobs:

| Model | Source blob | Archived CSV blob | Archived JSON blob |
| --- | --- | --- | --- |
| R336 | bcbf7b40c1f8ba86d5478d57509a437b5ba0279f | efa20e7d6432a1a6c7bd0abd53384b36e23422e5 | 2704b6066a7f3842c2273c8262d9fd41e2483d73 |
| R340 | 7bd287300825266be1a13fc12229b8c48b01e7a7 | 36ae0a9a11d2f27dacd8948f9617122eade0c40c | e5615c6d99bd79acac5501bda60976b3f7d3cad2 |

Local regenerated receipts matched all four original Git blob identities. Native environment: CPython 3.13.5, standard library, deterministic, no random seed, no paid API or GitHub Actions. Original scripts executed from isolated temporary copies using `--test --audit`. The independent strict checker imported neither original implementation.

## Observed native exit-code matrix

Both R336 and R340 produced the same pattern:

| Input | Original normal | Original python -O | Independent strict normal and -O |
| --- | --- | --- | --- |
| Correct source and receipts | 0, PASS | 0, PASS | 0, PASS |
| CSV appended newline | nonzero, FAIL | **0, FALSE ACCEPT** | nonzero, FAIL |
| JSON appended newline | nonzero, FAIL | **0, FALSE ACCEPT** | nonzero, FAIL |
| Both receipts deleted | nonzero, FAIL | **0, FALSE ACCEPT** | nonzero, FAIL |
| Source-only appended comment | 0, PASS | 0, PASS | nonzero, FAIL |

20 original and 20 strict subprocess executions were actually performed. Across both models, six optimized corruption/missing-file cases were falsely accepted by the original checker; 16 strict negative-control executions were rejected. The four source-only original successes expose lack of source identity binding, not evidence that source edits changed mathematics.

Both originals use bare `assert` expressions for persisted receipt reads. Under `python -O`, these statements are omitted. The originals' `unittest` tests remained green in the false-acceptance cases, while the audit success token was still printed. This is a reproduced conditional P0 integrity failure.

## B independent verification

Added `research/evidence_audit/r336_r340_strict_receipt_gate_20261101.py`, a separate pinned fail-closed verifier. It checks exact source/CSV/JSON Git blob identities, rejects duplicate JSON keys, and independently enumerates the 48 R336 conditions with 96 policy rows and the three R340 generator matrices with 48 entries. It does not import the audited original implementation.

Added `research/evidence_audit/test_r336_r340_native_20261101.py`, a native subprocess negative-control runner, and `research/evidence_audit/B_R336_R340_P0_NATIVE_MATRIX_2026-11-01.json`, the observed exit-code matrix. The complete original local execution JSON (11,625 bytes) has SHA256 `03619291f9d534d3003880133acb9fa4d465ac213a59253a27fef8ee873f886a` and is retained separately as a downloadable artifact; its exact bytes have not been committed to GitHub.

## Scientific scope and remaining work

COMPLETE: two additional original checker P0 false-acceptance reproductions; exact original input identities; bounded nonblind mathematical receipt validation; isolated native negative controls.

PARTIAL: the additive strict checker is available, but original production acceptance entry points remain unchanged. R334 and R335 have separately confirmed this risk. R333, R337, R338 and R339 remain STATIC_RISK_ONLY until native controls are executed. No comprehensive all-model impact audit has been completed.

NOT_RUN: Python 3.11/3.12 native reproduction, external team independent reproduction, any E2 human prediction, E3 historical prediction, CI. No change to original239 itemwise queue or R073/PESEN v0.1 freeze.

Recommendation: establish a mandatory fail-closed scientific receipt acceptance entry point with source and artifact identities; preserve the original historical scripts and their failure behavior as evidence. Then continue native negative controls for the remaining four static-risk models. Avoid claiming the historic E1 mathematical result invalid solely from this checker weakness.
