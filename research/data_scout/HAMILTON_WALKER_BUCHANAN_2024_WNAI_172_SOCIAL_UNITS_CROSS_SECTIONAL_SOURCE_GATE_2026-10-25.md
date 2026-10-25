# A data scout: WNAI 172 societies, verified public rows and independence gate

Date: 2026-10-25. Scope: public historical/ethnographic institutional data candidate, no model scoring. Candidate for future R140/R149/R171/R173 research, not an R161 finite cultural-fixation dataset. No R073 evaluation.

## Source and deduplication

Primary research: Hamilton, Walker and Buchanan (2024), *Institutional complexity emerges from socioecological complexity in small-scale human societies*, Proceedings of the Royal Society B, DOI 10.1098/rspb.2024.0246.

Primary data repository: Dryad DOI 10.5061/dryad.gb5mkkwz3, published 2024-04-18, README.md and WNAI_data.xlsx. Dryad explicitly links the authors' public source repository `RobertSWalker/wnai_bayesnet`. An additional Zenodo record 10.5281/zenodo.10868982 references the same underlying study. These are not independent datasets. Do not count Dryad, Zenodo and GitHub as three samples.

The GitHub author repository was actually fetched at fixed commit `5f3a074b190415a35cd678caf6c57b54980720ab` (2023). Text CSV `df.csv`, Git blob `8d70b2ab96d7541dcae14179299dad600c1d4edc`, is 38,269 bytes according to GitHub metadata. The connector returned 38,241 decoded text characters. The author README blob is `9027d2dba4e2b6be84cbdb2b6a77e9765eb0a416`; analysis script `wnai submit.R` blob `3d233999d947d8842f64b4a5ed94e124b46ef8c7`. GitHub has no top-level declared license. The 2023 GitHub CSV and 2024 Dryad XLSX have **not** been established as byte-equivalent or row-equivalent. The original Dryad XLSX bytes were not retrieved this round.

## Actual CSV audit

Parsed the fixed author CSV with an RFC-style quote-aware reader; actual header and all records were read. Results:
* 172 data rows and 62 columns; zero malformed row widths.
* 172 distinct society-name strings; 156 distinct society-ID strings, 133 distinct language glottocodes and 23 distinct language-family strings. One row has an empty society ID and name. The distinct counts are descriptive; repeated IDs may reflect source mappings and must be reviewed before grouping.
* 37 empty or `NA` cells over the 10,664 row-by-column cells; 14 rows contain at least one such cell. This is the **published derived CSV**, not a calculation of the missingness in the source ethnographic traits.
* No explicit year, observation wave, trial, or generation column. Unit of observation is an ethnographic society in a cross-sectional table, with language and location descriptors. No person-level actions, no repeated observations, no experimentally independent sessions.
* Examples of present variables: `society_xd_id`, `language_glottocode`, `language_family`, `Lat`, `Long`, `technology`, `Subsistence`, `Politics`, `material_culture`, `div_of_labor`, `econ_dist`, `property`, `marriage`, `war`, `phyla`. No observed action histories or direct measures of cultural copying probability.

The primary Dryad README states 172 selected societies, 13 derived trait categories and 258 cleaned binary traits. It also reports **5.4% missing source traits imputed by missForest** before aggregation. The GitHub CSV's 37 empty cells therefore do not represent the source missingness rate. The original 172 societies were selected from about 250 groups for high-quality ethnographic information, so selection bias must be addressed.

## Legal and methodological gate

Dryad's published terms (updated 2025-05-20) say submitted datasets are released under a CC0 instrument. The GitHub mirror itself has no declared license. To avoid assuming the mirror is covered identically, do not republish its full CSV until the Dryad original file is checked. Access and analysis of the public text source required no registration or purchase.

Important limitations: historically reconstructed pre-contact traits are cross-sectional and often derived from later elder recollections; no observed time axis. Spatial and linguistic autocorrelation violate naive independent-row assumptions. The author R script explicitly models language phyla and geographic spatial structure. Its `bnlearn`, `brms` and `cmdstanr` dependencies may require environment setup, but no paid service is required in principle. Original authors' bootstrapped network edge direction is not automatically identified causal direction. Any future prediction audit must group by language/spatial cluster, freeze holdouts before fitting and use negative controls. Cross-sectional data cannot test R161 fixation times or R073 repeated PD predictions.

Status: `PUBLIC_AUTHOR_CSV_ROWS_VERIFIED_172x62 / CROSS_SECTIONAL_ONLY / ORIGINAL_DRYAD_XLSX_EQUIVALENCE_OPEN / NO_E3_SCORED`.

Source links:
* https://datadryad.org/dataset/doi:10.5061/dryad.gb5mkkwz3
* https://github.com/RobertSWalker/wnai_bayesnet/blob/5f3a074b190415a35cd678caf6c57b54980720ab/df.csv
* https://github.com/RobertSWalker/wnai_bayesnet/blob/5f3a074b190415a35cd678caf6c57b54980720ab/README.md
* https://datadryad.org/terms
