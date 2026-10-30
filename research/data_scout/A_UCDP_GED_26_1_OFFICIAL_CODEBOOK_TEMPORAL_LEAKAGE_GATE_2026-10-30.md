# A track: UCDP GED 26.1 official codebook temporal leakage and identity follow-up

Date: 2026-10-30 UTC. Independent bounded follow-up to research/data_scout/A_UCDP_GED_26_1_2026_EVENT_HISTORY_SOURCE_AND_ACCESS_GATE_2026-10-30.md. Metadata/codebook-only review, no event-level raw CSV read and no E3 forecasting.

## Primary sources actually checked
1. Official UCDP download centre: https://ucdp.uu.se/downloads/ . GED Global 26.1 CSV link resolves to https://ucdp.uu.se/downloads/ged/ged261-csv.zip . This is a free official ZIP download route separate from the token-protected API. This run inspected the link target but did not download/decompress the binary archive.
2. Official 52-page GED 26.1 codebook: https://ucdp.uu.se/downloads/ged/ged261.pdf . First page: extracted from UCDP systems **2026-03-30**, version 26.1, coverage 1989-01-01 through 2025-12-31. Section 3 variable definitions and sections 4–5 methodology checked.
3. Official API documentation: https://ucdp.uu.se/apidocs/ . API requires x-ucdp-access-token, so it was not invoked. The download centre states free access and CC BY 4.0 with attribution; this does not certify any derivative historical forecasting result.

## New actionable source/identity risks
* Event `id` is the persistent numeric identifier across versions. `relid` can change when an event is updated; do not use relid as the cross-version primary key. Codebook variable table around pages 6–7.
* `date_start`, `date_end`, and `date_prec` represent the reported event interval and temporal uncertainty. A reported event may span multiple days. A strict prediction experiment must specify whether the target is a day-level onset, any-event-in-window, or interval-overlap outcome, and exclude ambiguous intervals or score them separately. A date_end later than a forecast origin cannot be used as a feature.
* `source_date` is publication date information, with **1753-01-01** used as a sentinel when missing. Older events may lack systematic source metadata. Treat 1753-01-01 as missing, not a genuine source-publication timestamp. Avoid using any article or coding information first available after the forecast origin.
* The codebook states revisions can produce discrepancies across UCDP 26.1 products; source extraction date in 2026 means historical events from 1989 onward have retrospective coding. A model trained or evaluated on the 2026 extraction is a **retrospective reconstruction**, not an as-of historical forecast unless historical version snapshots and publication times are reconstructed.
* Actor/dyad ID semantics changed at version 17.1. Joining pre-17.1 releases to 26.1 requires official translation tables. Spatial precision `where_prec` and temporal precision `date_prec` should be reported as separate uncertainty axes.
* Event data concern reported organized lethal violence. Absence of a GED row is not automatically proof that no violent incident occurred; inclusion criteria and reporting delay matter.

## Data gate and next actions
Access: free ZIP endpoint confirmed from publisher, ZIP bytes NOT_DOWNLOADED, CSV columns/row count/hash NOT_VERIFIED, codebook verified. Stable event ID: codebook confirmed; independent episodes, reporting lag, revisions: unresolved. License: publisher CC BY 4.0 attribution. Historical E3: 0.

Next A step: when a free binary transfer is available, save the official ZIP with SHA256, inspect member list, parse CSV header and count valid rows, and check event ID uniqueness, source_date sentinel prevalence, date_prec distribution and duplicate dyad/date clusters. Predefine an as-of reconstruction protocol before any forecast scoring. Never substitute current 2026 hindsight labels for genuine prospective information availability.
