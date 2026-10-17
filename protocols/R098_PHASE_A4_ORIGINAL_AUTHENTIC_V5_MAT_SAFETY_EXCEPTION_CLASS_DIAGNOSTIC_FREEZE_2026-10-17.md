# R098 Phase A4: original publisher MD5 verified, MATLAB legacy v5 directory still unsupported; safe diagnostic only

2026-10-17. [CI39025710365](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39025710365): all **24 pure synthetic** tests PASS; real original 2025 Zenodo MAT publisher MD5 passed byte-complete authentication. Re-running `scipy.io.whosmat` after classifying file by safe first-byte signature as MATLAB_LEGACY_V5 **still** returned `R098_PUBLISHED_MAT_HEADER_NOT_SUPPORTED_MATLAB_LEGACY_V5` and **0 human source actions/metrics**. Unchanged published MD5 `42153952f8e6614d09c2d903fd97af62`; no model results.

Before next source access freeze only **safe exception diagnosis**:
- preserve exactly source URL, publisher MD5, byte cap, 24 synthetic + new pure test; no `scipy.io.loadmat`, no original numeric/actor/session values accessed.
- On whosmat error publish only static exception type from enumeration `MatReadError, ValueError, NotImplementedError, TypeError, IndexError, Other`, not raw Python exception message, traceback contents, or any original data values.
- Publish the MD5-passed full original source SHA256 and byte size **even when MAT metadata cannot be parsed**, as proof of authentic access but NOT successful data inference.
- Diagnostic may include MAT header version two bytes at offsets [124:126] in hex as container-format metadata **only**, not any source content outside first 128 byte metadata header; if unusual header data reveals anything untrusted, emit SHA256 of first128 only rather than literal.
- No training or scoring, no other source files yet.
- If the actual published file is unreadable by SciPy, preserve E1 original source authenticity and stop instead of claiming behavior analysis; alternative original published files are separate source candidates/protocols.

PESEN v0.1 remains FROZEN.
