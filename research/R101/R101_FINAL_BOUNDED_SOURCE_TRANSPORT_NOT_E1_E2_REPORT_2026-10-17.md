# R101 formal bounded source result: publisher catalog and signed delivery verified, original raw ZIP E1 remains blocked

Date: 2026-10-17. **R101=CLOSED_BOUNDED_SOURCE_TRANSPORT**, **E0_OFFICIAL_CATALOG_VERIFIED=YES**, **RAW_ZIP_E1=NOT_ESTABLISHED**, **HUMAN_E2=0**, PESEN v0.1 FROZEN.

## Independently proven public data provenance

Stallen et al. (2023), *Nature Communications* DOI 10.1038/s41467-023-42128-2. Official DataverseNL dataset DOI 10.34894/EYFM5L. Dataset API A2 verified nine ZIP public objects with an aggregate publisher-reported size 43,631,177 bytes. A3 separately authenticated nine public filename/file ID pairs from the genuine publisher API. [A3 real source catalog](R101_PHASE_A3_LIVE_CI_OFFICIAL_PUBLIC_ZIP_CATALOG_RECEIPT.json) identifies:

* Exact named original raw-data archive: `3. Raw data files.zip`
* Public numeric dataFile ID: **383977**
* Official catalog registered byte size: **2,247,187 bytes**
* No independently published file MD5 in the verified Dataverse catalog
* Separate source files for raw, processed data, code and study documentation

These are real publication source metadata findings, **not** proof that the archive contains usable actor/opponent/session/round columns. The publication's reported 336 human subjects remain unverified by this project from original actor rows.

## Frozen real original archive access sequence and all negative evidence

A4 first froze only the official `dataverse.nl/api/access/datafile/383977` endpoint and exact file size, double full SHA256, and central directory-only security constraints. Actual first-party download [A4 receipt](R101_PHASE_A4_LIVE_CI_FIRSTPARTY_RAW_ZIP_SHA_DIRECTORY_RECEIPT.json) rejected with `R101_A4_OFFICIAL_FILE_ENDPOINT_NOT_PINNED`, before archive data were accepted.

A5 next froze and ran a nofollow header-only publisher preflight: the actual official API returned **HTTP 303** redirect to `objectstore.surf.nl` and an AWS S3 presigned query; signature/token/full URL contents were never released. [Actual A5 receipt](R101_PHASE_A5_LIVE_CI_REDIRECT_PREFLIGHT_RECEIPT.json). SURF's official documentation independently identifies `objectstore.surf.nl` as its research object-storage endpoint. A6 separately froze a one-hop only, eight presigned-key whitelist, full original 2,247,187-byte double-fetch SHA and ZIP directory-only policy, with 13 extra pure signed URL synthetic tests plus 14 ZIP tests. Actual [A6 receipt](R101_PHASE_A6_LIVE_CI_ORIGINAL_SURF_DELIVERED_ZIP_SHA_DIRECTORY_RECEIPT.json) rejected `R101_A6_ORIGINAL_SURF_PAYLOAD_FINAL_HOST_NOT_VERIFIED`, with zero source model actions scored.

A7 was an independent, no-body diagnostic with the same A6 HTTP request/redirect handler. The real [A7 source response receipt](R101_PHASE_A7_LIVE_CI_FINAL_HTTP_HEADER_DIAGNOSTIC_RECEIPT.json) observed **HTTP 200**, final host **objectstore.surf.nl**, exactly **one** official 303, `application/zip`, Content-Length **2,247,187**, without reading any response body. This confirms at least one eligible final HTTP response was possible in the publisher's delivery chain.

Based exclusively on that evidence, A8 froze **one** unchanged strict replay of the A6 double-fetch source executable, with no altered endpoints or validation. The [actual A8 receipt](R101_PHASE_A8_LIVE_CI_UNMODIFIED_ORIGINAL_ZIP_DOUBLE_SHA_REPLAY_RECEIPT.json), committed at [07a9e6af](https://github.com/edwardsage419/Psychohistory-Research/commit/07a9e6af83dc1a852e00c6ce777182e75ae28ffd), again returned `R101_A6_ORIGINAL_SURF_PAYLOAD_FINAL_HOST_NOT_VERIFIED`. Because the pre-frozen A8 stopping rule allows only one unchanged replay, **the transport branch is now stopped**. All initial failures, response classification evidence, scripts and tests remain separately in main; no source failure was overwritten.

## What does and does not follow

Official first-party catalog identity and actual 303-to-SURF provenance are verified. The final 200 response in A7, by itself, does **not** establish that an exact full source archive was downloaded twice, that project source SHA256 matches, that ZIP members are valid, or that human game data are readable.

True original ZIP file bytes SHA256: **UNKNOWN**. ZIP member count/file schema: **UNKNOWN**. Verified actors/opponents/rounds/independent lab sessions: **0 verified**. New original human behavior model predictions: **0 scored**. None of these can be inferred from reported paper sample size or ZIP filename. Original R073 own/peer history model remains frozen, R095/R096/R099 real E2 results and negative strata remain unchanged. R101 is a **transport/data source eligibility limitation**, not a refutation or confirmation of any learning mechanism.

## Acceptance

A01 author/DOI provenance: PASS_BOUNDED.
A02 real official public nine-ZIP catalog and raw file ID: PASS.
A03 original raw ZIP double authenticated source bytes: BLOCKED.
A04 first-party negative A4/A6/A8 and explanatory A5/A7 evidence retained: PASS.
A05 no invented participant identities, scores, p-values or causal conclusions: PASS.
A06 repository protocols, programs, pure synthetic tests, machine receipts and report archived: PASS.

**Administrative endpoint:** `R101=CLOSED_BOUNDED_SOURCE_TRANSPORT` and `PESEN_v0.1=FROZEN`. Advance to a separate R102 author/data source with explicitly available actor, opponent, round and independent session identities, prioritizing a directly accessible small CSV/TSV to avoid repeating E0 transport failures.
