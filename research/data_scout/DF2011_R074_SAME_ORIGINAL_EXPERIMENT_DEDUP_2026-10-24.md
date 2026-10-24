# A data scout: DF2011 is the R074 original study, source deduplication

Date: 2026-10-24. Track A, public data scout. Status: **SOURCE_STUDY_DUPLICATE_CONFIRMED; R073_NEW_INDEPENDENT_EXPERIMENT_INELIGIBLE**.

## Study identity cross-check

The decoded public `cran/stratEst` `data/DF2011.rda` has 7,358 rows and six fields, with fixed upstream blob `52e216b02e1a7ab7fb1a6e335b5f7e2ef6b7f5a0`. The previously archived source audit is `research/data_scout/DF2011_FIXED_BLOB_ROW_DECODE_REPORT_2026-10-24.md`, with successful GitHub Actions run 40083592838.

The original article is Dal Bó and Fréchette (2011), *The Evolution of Cooperation in Infinitely Repeated Games: Experimental Evidence*, American Economic Review 101(1):411–429, DOI **10.1257/aer.101.1.411**. Source: https://pubs.aeaweb.org/doi/10.1257/aer.101.1.411 . The public package documentation and license are in https://github.com/cran/stratEst .

The pre-existing **R074** research uses the **same article, same authors, same DOI** and its first-party text data at https://gfrechette.com/data/Dal_Bo_2011a_data.txt . See `research/R074/README.md`, `research/R074/R074_FINAL_ACCEPTANCE_STATUS.json` and its pre-score frozen protocol. R074 has already evaluated a real original-author human repeated-game source across 18 experimental sessions. The earlier source record reports 37,042 individual actions and 15,338 eligible t>=3 decisions. The smaller `DF2011.rda` row count indicates a distinct curated representation or subset; the precise row correspondence has **not** been established.

## Scientific decision

A new format or subset of the **same original experiment** cannot count as another independent experimental replication of R073. This source is now marked `INELIGIBLE_AS_NEW_INDEPENDENT_EXPERIMENT`. No R073 model, scoring rule or frozen parameter is changed. No DF2011 predictions have been scored. The published R074 human evidence is not duplicated in E2 or E3 counts.

This deduplication supersedes the *independent-study-candidate* wording in the earlier DF2011 scout notes, which remain preserved as historical evidence of what was known at that time. The binary decode and field-quality checks remain valid.

## Remaining uses and limits

DF2011 may still be useful for a **within-study source reconciliation** against the R074 first-party archive, conditional on a predeclared row mapping and explicit analysis of treatment, subject, supergame and period keys. It offers no new study independence. Avoid redistributing human row-level data. Source licensing for the curated DF2011 package is described as CC BY 4.0 in the upstream copyright file; no private data or paid service is needed.

Next A priority: identify an **experiment not already represented by R073, R074, R075, R076 or later human R-series studies**, and verify its original author, DOI, data dictionary, partner identifiers, independent sessions, time semantics, permission and frozen R073 feature compatibility before any scoring.

Scope: provenance deduplication only. New E1=0, new E2=0, new historical E3=0. No external-team independent replication claimed.
