# A track: Colman 2018 candidate deduplication against R108 original source

Date: 2026-10-29. This is a repository cross-track correction and source eligibility audit, not a newly acquired study or E2 prediction.

## Cross-track evidence actually read
1. `research/data_scout/A_COLMAN_2018_300_ROUND_FIGSHARE_TITLE_PROVENANCE_AND_RIGHTS_FOLLOWUP_2026-10-29.md` says A-track did not personally obtain the ZIP and marked RAW_UNREAD.
2. Earlier `research/R108/R108_FINAL_ACCEPTANCE_STATUS.json` and `R108_PHASE_B2_LIVE_CI_TRUE_2017_ORIGINAL_SIX_300_BLOCK_CONDITION_SOURCE_ELIGIBILITY.json` establish that the **project had already obtained and validated the original publisher CSV** on 2026-10-18, through first-party delegated download. Original file ID 18370526; 36,526 bytes; publisher MD5 `7afc755c293dc261d696d1b3f9ba796a`; whole SHA256 `e7dbb6ddc96cc5c65368be0d1918c3ebc7a83c14addd03ab44eeb07790575c18`.
3. R108 prior source structural checks established 1,804 five-column logical data rows, four nonnumeric preamble rows, then six distinct condition blocks of exactly 300 sequential rounds, 2-by-3 anonymous condition codes, and predominantly nonbinary numerical fields. They did **not** establish original actor, opponent, or independent session IDs. Source-level analysis was already completed, while A-track's local attempt had no new binary access.

## Data suitability and permissions
University of Leicester original English dataset: https://figshare.le.ac.uk/articles/dataset/Repeated_Prisoner_s_Dilemma_Dataset/10194938 ; peer-reviewed paper DOI https://doi.org/10.1016/j.actpsy.2018.04.014 . Dataset metadata marks All Rights Reserved; the verified original CSV remains outside the public project repository. No private person-level rows or raw source bytes were copied here. The dataset page's prepublication paper title differs from the final paper title; explicit dataset-to-final-DOI version mapping remains a provenance follow-up.

The six 300-round condition traces cannot be interpreted as six independent dyads, 1,800 participant actions, or actor-level 300-round histories. Existing R108 status `CLOSED_E1_ORIGINAL_PUBLISHED_CONDITION_SERIES_NOT_ACTOR_DYAD_E2_ELIGIBLE` remains the correct bounded classification. R073 frozen 100-round actor/opponent-history scoring: DIRECT_REPLAY=NO. No fifth new independent human experiment discovered in this audit. Existing distinct R074/R075/R077 cross-study human evidence is retained and must not be counted again as new evidence.

## Audit outcome
`PROJECT_SOURCE_BYTES_VERIFIED_PREVIOUSLY`; `A_CURRENT_RUN_NEW_RAW_BYTES=0`; `ACTOR_DYAD_SESSION_KEYS=UNVERIFIED`; `R073_DIRECT_REPLAY=NO`; `LICENSE_RESTRICTED`; `NEW_E2=0`; `NEW_E3=0`. This resolves the misleading project-wide interpretation of A-track RAW_UNREAD while preserving the narrow truth of that A-track attempt. Next scout should prioritize a genuinely new actor-level original study and freeze its group/time leakage tests before scoring.
