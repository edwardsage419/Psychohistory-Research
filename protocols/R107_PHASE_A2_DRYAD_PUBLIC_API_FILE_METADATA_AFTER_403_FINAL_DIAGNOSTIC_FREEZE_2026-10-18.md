# R107 A2 original Dryad public API delivery diagnostic freeze (after first-party 403)

Date 2026-10-18. Original Dryad stream file 296893 official GET first failed HTTP403 in GitHub Actions run 39128368647 after all 16 source synthetic tests passed. No original human source body read and no E1/E2.

Freeze one final public Dryad **metadata-only** source check. Only the two URLs:
https://datadryad.org/api/v2/datasets/doi%3A10.5061%2Fdryad.7fq25s8
https://datadryad.org/api/v2/files/296893
Only GET over exact HTTPS datadryad.org origin, exact path, empty query, redirects **DENIED**, no credentials, max 256KiB per response. Access only JSON object metadata and export no arbitrary source text, email, individual data, or URL destinations.

Publish sanitized numeric HTTP response categories, exact official DOI match boolean, official filename DataSet.csv match boolean, published file byte size if integer and file publisher-reported digest only when formatted as a 32-hex MD5 or 64-hex SHA256. A published digest in metadata is not yet verification of actual source bytes. Inspect any metadata-declared links only to distinguish whether exact original publisher path or an alternate official path is advertised, no other URL content released, no redirect followed, never perform a source file GET during A2. For response without metadata, only code and safe failure reason, no guess.

Before real API: pure synthetic source host/URL safety, strict JSON digest and link schema, and no human field leakage. Archive immutable response research/R107/R107_PHASE_A2_LIVE_CI_DRYAD_OFFICIAL_PUBLIC_API_METADATA_DIAGNOSTIC.json. A2 cannot establish E1. If public metadata cannot authorize a precise accessible first-party file, bound R107 at E0 and move to new R108 dataset instead of unbounded exception chasing. R073 and PESEN v0.1 frozen.
