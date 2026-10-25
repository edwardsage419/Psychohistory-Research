# B scientific audit: R167 critical reweighting threshold

Date: 2026-10-26 Asia/Singapore
Status: PASS_BOUNDED_INTERNAL_E1
Preregistered design: [R167 critical-threshold freeze](../../protocols/R167_KAPPA_REVERSAL_CRITICAL_THRESHOLD_THIRD_METHOD_FREEZE_2026-10-26.md), commit `3ff757de60838bb742fe5347c94f2a3a0a935fea`, prior to either calculation.

## Independently executed method

The main R167 extension used JavaScript BigInt and the algebraically factorized two-group between contribution. The B route uses Python standard-library Fraction, directly normalizes the post-reweighting group masses, and solves the affine numerator of the net change in kappa. It does not import the original R167 program or the main R167 extension. Both routes share the fixed synthetic model specification and initial grid, so this is internal method-level corroboration.

Actual local Python execution of [committed B source](r167_b_independent_threshold_20261026.py) returned:
```json
{
  "worlds": 72,
  "delta_positive_worlds": 24,
  "finite_threshold_worlds": 12,
  "impossible_threshold_worlds": 12,
  "positive_reversal_worlds": 5,
  "boundary_tests": 36,
  "controls": 42,
  "example_nets": ["-1/192", "0", "1/64"],
  "status": "PASS_BOUNDED_E1"
}
```

The local executed Python source had SHA256 `9e2845e93e513d45d7a421260c980473c1e22a94b626680459165ae0a881595b` and Git blob SHA1 `f6d9e03cbc8af38fe0ab57c3860e265dcb82f32f`. The remotely committed Python source was re-fetched and its Git blob SHA1 matched exactly. Local full 72-record JSON receipt SHA256 was `5106a116c964b7682e63938a4577dc2d31b3b18ae1fc1f9ca71a12189be4cab9`; the full local receipt is not currently included as a GitHub file. This report preserves its actual stdout summary and source identity.

The 72 ordered records from the local Python run and the [committed main execution receipt](../validation/R167_KAPPA_REVERSAL_CRITICAL_THRESHOLD_72_WORLD_EXACT_RECEIPT_2026-10-26.json) were each independently reduced to the identical 1598-byte ASCII canonical sequence `id|net|critical_kappa\n`. Their 64-bit FNV-1a fingerprint is `39e5a121a6c8a286` on both sides. This is a complete-grid comparison fingerprint, with the ordinary non-cryptographic collision limitation; it is stronger than comparing only aggregate counts.

## Audit gates and limitations

* **Data leakage:** no human data, training or model selection; 72 grid worlds were frozen in the 2026-10-21 R167 protocol and the extension's new threshold tests were committed before execution.
* **Baselines and negative controls:** kappa=0, equal-frequency groups, and exact kappa-critical boundary; 42 fixed-grid controls and 36 off-grid boundary evaluations passed.
* **Uncertainty and resampling:** no statistical sample is involved. Sampling confidence intervals, probability calibration and resampling are inapplicable to this exact algebraic identity. They remain required for any future E2/E3 predictive study.
* **Independent sample:** no new independent human sample. No evidence for social welfare, actual group reproduction, culture-level causation or historical dynamics.
* **Execution limits:** local Python actually executed; no remote Actions were started. Repeated same-project scripts do not constitute external independent replication.
* **Preservation:** no existing frozen file, R073 model, PESEN v0.1 or original239 queue was modified.

Verdict: exact conditional E1 theorem corroborated in two languages and two computational forms; `E2=0`, `E3=0`, `EXTERNAL_INDEPENDENT_REPLICATION=0`.
