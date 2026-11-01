# A data scout: Fudenberg and Karreskog Rehbinder (2024), openICPSR E182668 V1
Date 2026-11-01 UTC. Target (A,E182668V1,source_metadata_2024,17_study_lineage_and_R073_eligibility). Status SOURCE_METADATA_VERIFIED / RAW_FIELDS_BLOCKED / E2_NOT_READY.

## Verified English primary sources
Article: Drew Fudenberg and Gustav Karreskog Rehbinder, *Predicting Cooperation with Learning Models*, American Economic Journal: Microeconomics 16(1), 2024, pp.1-32. DOI 10.1257/mic.20220148. Publisher https://pubs.aeaweb.org/doi/10.1257/mic.20220148 . Authors study out-of-sample cooperation prediction in indefinitely repeated Prisoner's Dilemma. Their learning model varies initial-supergame cooperation by experience/game parameters, then uses prior-round outcomes for subsequent actions.

First-party public archive: https://www.openicpsr.org/openicpsr/project/182668/version/V1/view ; DOI 10.3886/E182668V1, published 2024-01-19. Official project description explicitly says compiled data from **17 different experimental papers**, with directories `raw_data`, `clean_data`, `code`, `results_data`, `snippets`, `temp_data`, and README files. A subfolder `raw_data/new_data/Strategy-Choice-in-the-Infinitely-Repeated-Prisoners-Dilemma` lists a 6.3 KB `readme.txt` and a data folder. These are actual inspected archive directory and file metadata, not extracted raw CSV.

## Field and independence gate
Publisher confirms repeated PD, human experimental data and source aggregation across 17 papers. **Actual column names, subject identifiers, opponent identifiers, pair/supergame IDs, period units, missing values, action coding, session split and minimum uninterrupted rounds have not been verified.** The archive readme page was accessible as metadata, while the file content preview did not yield text and download endpoint timed out. Dataset-specific reuse license was not found in the inspected page; journal copyright does not determine archive data redistribution permission.

Important source-lineage risk: aggregation from 17 previously published studies may reuse studies already appearing in R073, R074, R095, NV_games, DF2011, or other registered sources. Source identity requires a 17-paper DOI inventory and raw cohort/sample fingerprints before claiming any independent external sample. The model's stated out-of-sample tests cannot be adopted as R073 frozen-score results without confirming their exact split and target.

R073 frozen gate: continuous >=100-round human-human dyadic sequences with preserved within-match order, player and opponent histories, unique independent experiment identity, and identical frozen R073 scoring. Current eligibility UNKNOWN/BLOCKED, no E2 score, no E3. A complete source-level replay would first require raw-file access, codebook, license, 17-study mapping, stable file hashes, and a prespecified source-exclusive holdout. Do not combine with old data or adjust R073 post hoc.

## Actions and cost
Only official public English article and archive metadata were read. No private data, paid access, raw participant rows, login, purchase, or API billing. Reproduction difficulty MEDIUM_TO_HIGH due to multi-study lineage and unresolved fields. Next: obtain public README text through permitted free access, identify the 17 source papers and cohort overlaps, verify explicit session and player histories, then decide eligibility before scoring.
