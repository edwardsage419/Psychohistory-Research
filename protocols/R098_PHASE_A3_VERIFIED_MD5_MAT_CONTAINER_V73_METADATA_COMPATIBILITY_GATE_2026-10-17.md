# R098 Phase A3 — publisher original MD5 passed, MAT header reader compatibility only

2026-10-17. After [CI run39025545307](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39025545307), all **19 synthetic tests PASS**; the real original full Zenodo MAT file **passed published publisher MD5** `42153952f8e6614d09c2d903fd97af62` and byte cap, then `scipy.io.whosmat` rejected parsing source with `R098_PUBLISHED_MAT_HEADER_NOT_SUPPORTED`; **no actual human contribution values read, zero real scores**. Previous [CI39025491235](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39025491235) failed one synthetic due unhandled truncated MAT exception, then corrected without changing source identity.

Freeze amendment **before new original reread**:
1. Keep EXACT original source Zenodo v2 URL, publisher MD5, 100000-byte cap and resulting whole-source SHA256 strict and unchanged.
2. Diagnostic may inspect only up to first 128 bytes **after MD5 verification** to identify container signature `MATLAB 5.0 MAT-file`, `MATLAB 7.3 MAT-file`, `HDF5 signature`, `UNKNOWN`; report one of these static enumerated strings only, not original header payload.
3. Allow HDF5 MAT v7.3 files by listing only top-level HDF5 object names, shape/dtype/number of items; use `h5py.File(io.BytesIO(raw),"r")` (never `object[...]` or `loadmat`), check every published schema key safe ASCII. Some structures are MATLAB metadata groups, preserve as static class `group` and shapes [].
4. SciPy legacy path still whosmat only. In case of unsupported container: fail closed but print safe static class of exception, not any value, and never claim source structs verified.
5. Test both synthetic MAT v5 and synthetic HDF5 headers with ≥5 tests, including value privacy, plus all 19 old cases; ensure full downloaded source not written to GitHub and no results fabricated.
6. No human model score, no `Contribution` field access beyond top-level name as schema. Original same humans participate Session1 and Session2; cross-session independent participant claims prohibited.

R098_AUTHOR_ORIGINAL_FULL_MD5=VERIFIED_BEFORE_MAT_DIRECTORY
R098_SOURCE_SHA256_PUBLIC_RECEIPT=NOT_YET_AVAILABLE
R098_HUMAN_E2_SCORE=ZERO
PESEN_v0.1=FROZEN
