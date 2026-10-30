# A track: UCDP Candidate monthly event overlap and as-of preparation

Date 2026-10-30 UTC. Evidence class: historical data source discovery only, E3 prediction NOT_RUN.

## First-party source checks and new methodological finding

Revisited official UCDP current downloads https://ucdp.uu.se/downloads/ and historical versions https://ucdp.uu.se/downloads/olddw.html. The current page identifies September 2026 version 26.0.9 as a monthly candidate CSV and January to September 2026 version 26.01.26.09 as a separate aggregated CSV. The official historical page lists monthly and quarterly vintages for 2024, 2025 and 2026. The official candidate codebook version 1.4 at https://ucdp.uu.se/downloads/candidateged/ucdp-candidate-codebook1.4.pdf explains that candidate events with date_start or date_end in a release month may appear in both adjacent monthly releases when an event spans a month boundary. Its cover identifies data extraction around the 20th of each month. The current official page links codebook 1.5; whether that later version changes the exact overlap or extraction convention is NOT_VERIFIED.

**New audit consequence:** blindly concatenating monthly Candidate CSVs can double-count spanning events, even before cross-vintage revisions are considered. The monthly 26.0.9 and cumulative 26.01.26.09 releases also represent different coverage windows. They must be registered as distinct versions, never summed without a documented event-identity and time-window rule.

Preliminary deduplication protocol for future frozen E3 preparation: retain source version, file SHA256, verified public availability date, original event ID, start/end dates and source date; distinguish duplicate event identity within a prediction window from a revised event record across vintages. Explicitly preserve conflicting revisions and missing IDs as exceptions. Do not collapse repeated events based solely on geographic coordinates, actor pair or calendar date. Verify publication timestamp separately from codebook extraction day. Train and score only against a version demonstrably available by the prediction cutoff.

## Actual access and limits

Official CSV links were reattempted through the available web reader. The 26.0.9 endpoint returned unsupported content-type text/csv; local runtime has no outbound DNS. No bytes were downloaded, no CSV schema, identity or event counts were independently verified, and no historical forecast was run. The current official download page states free CC BY 4.0 access with attribution. The UCDP API requires a token; none was requested. This candidate does not satisfy R073's independent hundred-round human dyadic-game gate.

SOURCE_METADATA=PASS; VINTAGE_CATALOG=PASS; MONTH_OVERLAP_RULE=HISTORICAL_CODEBOOK_SUPPORTED; CURRENT_V1_5_RULE_PARITY=UNKNOWN; RAW_BYTES=BLOCKED; LICENSE=OFFICIAL_CC_BY_4_0; COST=ZERO_NEW_SPEND; E2=0; E3=0.

Next: obtain two official monthly CSVs through an allowed free route, verify stable IDs, duplicate spans, release times and revision semantics before proposing any E3 evaluation.
