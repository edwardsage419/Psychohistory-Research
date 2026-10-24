# A data scout: Dal Bo and Frechette 2011 repeated PD candidate

Date: 2026-10-24. Status: **SOURCE_SCHEMA_LICENSE_BLOBS_VERIFIED; BINARY_NOT_DECODED; R073_REPLICATION_BLOCKED**.

## Primary provenance

Original human repeated prisoner's dilemma experiment: Dal Bó and Fréchette (2011), American Economic Review 101(1), 411–429, DOI 10.1257/aer.101.1.411. Official AEA page: https://pubs.aeaweb.org/doi/10.1257/aer.101.1.411 (replication package listed). Public CRAN mirror: https://github.com/cran/stratEst . Directly inspected source documentation Git blobs `man/DF2011.Rd` SHA1 `0554f7f3d2d7a313b058265ab53e8150b5f559f4`, `man/data.DF2011.Rd` SHA1 `bc7d21de9994ffe1332a9b1339f6c4a0bb2c458f`. The upstream copyright file explicitly assigns **CC BY 4.0** to Dal Bo and Frechette (2011) data, copyright American Economic Association 2011. Copyright source: https://github.com/cran/stratEst/blob/master/inst/COPYRIGHT.txt . Software GPL-3 licensing is distinct from the embedded data license.

## Actual source inspection

The raw `data/DF2011.rda` file is listed at Git blob `52e216b02e1a7ab7fb1a6e335b5f7e2ef6b7f5a0`, size 3298 bytes. The derived `data/data.DF2011.rda` file is at blob `4c2586af1a5465a9e690b41e6f839c33096a4903`, size 5082 bytes. The connector successfully retrieved the original binary in base64 form but no validated RDA-to-tabular decode was completed. No row-level assertions are claimed.

The upstream **raw** documentation declares 7358 rows, six variables: `treatment`, `id`, `game`, `period`, `choice`, `other.choice`. The upstream **derived** documentation declares 7358 rows, seven variables, adding `input`, the previous-round own/other action pair. The first period's `input` is NA. These counts and semantics are upstream declarations pending direct row verification.

Time unit is the round `period` within supergame `game`. Participant ID is `id`; the document does not establish independent laboratory session IDs, opponent pair IDs, or whether IDs are globally unique across treatments. Splitting by `game` alone is prohibited because an individual can contribute to multiple supergames. The raw `other.choice` is contemporaneous, so a predictor must shift it within verified individual-supergame boundaries; using it as same-round predictor leaks the outcome. Derived `input` may be used only after independently validating that it contains strictly lagged actions.

## R073 compatibility and barriers

Potentially valuable as a second independent human repeated-game study. Required gates: decode exact fixed blobs, verify 7358 raw rows and types, validate key uniqueness and game chronology, confirm partner pairing and independent sessions or an acceptable identity-disjoint split, distinguish action implementation noise and intended actions, check R073 frozen feature and scoring compatibility before any score. No parameter fitting, model selection or threshold tuning on this dataset. Until these conditions are met, new E2=0, new E3=0 and external R073 score is **NOT_RUN**.

No private data, registration, purchase, paid API or redistribution was used. A separate FRD2012 registry already exists; this is a distinct candidate and does not duplicate its experiment.
