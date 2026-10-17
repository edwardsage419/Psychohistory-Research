# R101 Phase A8: single unchanged original full-ZIP source replay after bounded A7 HTTP proof

Date: 2026-10-17. Evidence before execution:

* Actual A4 original raw ZIP source attempt rejected with a strict hostname mismatch.
* Actual A5 nofollow official DataverseNL HTTP 303 redirect verified host `objectstore.surf.nl`, a signed S3 path with no credential disclosure.
* Actual A6 strict one-hop source delivery attempt rejected with `R101_A6_ORIGINAL_SURF_PAYLOAD_FINAL_HOST_NOT_VERIFIED`; genuine failure receipt remains archived.
* Actual A7, using precisely the same original GET headers, same A6 redirect handler and no response body reading, then obtained one successful **HTTP 200**, final host **`objectstore.surf.nl`**, **one** publisher 303, `application/zip`, and **Content-Length 2,247,187**. The first-party [A7 receipt](../research/R101/R101_PHASE_A7_LIVE_CI_FINAL_HTTP_HEADER_DIAGNOSTIC_RECEIPT.json) confirms this. An intermittent delivery response or network variation may explain A6, but has not been conclusively established.

Therefore, the narrowly justified next step is a **single unchanged strict replay of the exact A6 source executable** `research/R101/r101_phase_a6_dataverse_surf_signed_zip_sha_only.py`. NO source-code changes, no additional permitted host, no looser path, no new signature assumptions, no removal of SHA or ZIP safety checks, no access to ZIP members. Run exactly the same 13 SURF signing and 14 ZIP safety pure synthetic tests first; then one workflow run of the source auditor that itself requires **two** separate acquisitions and exact full-file SHA256 equality. Distinct workflow and permanent source receipt path: `research/R101/R101_PHASE_A8_LIVE_CI_UNMODIFIED_ORIGINAL_ZIP_DOUBLE_SHA_REPLAY_RECEIPT.json`. Keep original A6 source result unchanged.

This is one authorized bounded re-evaluation justified by a genuine no-body A7 success, not indefinite retrying or changing behavior models. If it fails, record its unchanged real error class and stop further automatic source transport retry within R101 until a new independent reason is available. If it succeeds, grant E1 only to this exact downloaded ZIP and anonymous central-directory metadata; author names, participant actor/opponent labels and behavior values remain unread; E2 still zero. PESEN v0.1 FROZEN.
