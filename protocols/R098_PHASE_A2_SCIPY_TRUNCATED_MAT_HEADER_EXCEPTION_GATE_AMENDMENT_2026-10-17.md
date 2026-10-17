# R098 Phase A2 — synthetic truncated MAT exception explicit safe rejection

2026-10-17. First GitHub CI [run 39025491235](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39025491235): **19 synthetic tests attempted**, 18 PASS and 1 ERROR; no actual original 2025 Zenodo file downloaded because real-source job skipped. `scipy.io.whosmat(b"12345")` raises `scipy.io.matlab._miobase.MatReadError` ('Mat file appears to be truncated') not the original list of `ValueError,TypeError,IndexError,NotImplementedError`. This is correct unsafe-header detection but exception was not translated to an explicit safe `R098_PUBLISHED_MAT_HEADER_NOT_SUPPORTED` error.

Narrow amendment before FIRST actual official 2025 source read: add SciPy `MatReadError` to the exceptions caught in `mat_metadata`, and preserve all 19 original synthetic tests. Do not change exact Zenodo publisher file, MD5 `42153952f8e6614d09c2d903fd97af62`, schema, header-only source inspection, dataset admission or any real human behavior; cannot retroactively call failed synthetic job a success.

R098_REAL_ORIGINAL_HUMAN_VALUES_READ=NO
R098_PHASE_A_SOURCE_GATE_FROZEN_UNCHANGED=YES
PESEN v0.1=FROZEN
