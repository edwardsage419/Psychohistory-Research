# A data scout: Basel Risk Norms and alternate zoonoses psychometric data

Date: 2026-11-01 UTC. Track r A subflow. Scope: public source verification only, no human rows accessed or scored.

## Primary candidate: Basel Risk Norms
Hussain, Mata and Wulff (2024), *Novel embeddings improve the prediction of risk perception*, EPJ Data Science 13:38. DOI 10.1140/epjds/s13688-024-00478-x.
Official article: https://link.springer.com/article/10.1140/epjds/s13688-024-00478-x
Official article data availability: https://osf.io/gu9df/ (Semantic Accounts of Risk Perception).

Actually inspected the English full-text methods and data-availability statement. Paper reports 1004 distinct risk sources, nine psychometric attribute ratings and a separate riskiness rating. Two human samples: 1506 people for riskiness ratings (each assigned 100 risks on a -100 to 100 scale), 2360 people for psychometric ratings (each assigned 20 risks with 1 to 7 response scale for each item). Study collected multiple sessions over two consecutive weeks, finishing 2022-10-10. These are paper-reported sample sizes and assignment designs, not independently counted raw rows. Unit of observation is participant by hazard by rating item; identity and repeated-rating linkage keys are NOT_VERIFIED. The two participant samples must remain separate in modeling.

The authors report nine psychometric attributes and two-factor discussions. Their paper explicitly notes that the classical dread/unknown factor division is imperfect for these data. The current R324 artificial two-axis equation must not be treated as estimated from these ratings. For later empirical work, freeze hazard-level splits before fitting and check whether participant-level splits are also needed. Prevent leakage of the same hazard across training and test sets. Compare intercept-only, attribute-only, dread/unknown and richer nine-attribute baselines; report held-out risk rating error and calibration where applicable. This is a future design suggestion, not a frozen empirical evaluation.

Availability gate: the paper states that study data, code and supplementary materials are available at OSF except full SWOW data and participant-identifying information. Direct OSF page access in this run returned HTTP 403. No files, row counts, column headers, IDs, missingness, exact time field, file hashes or reuse licence for the individual datasets were verified. The article itself has CC BY 4.0 rights; dataset reuse terms require separate verification. Status: PUBLIC_METHODS_VERIFIED; RAW_FILE_ACCESS_BLOCKED; FIELD_SCHEMA_UNVERIFIED; LICENSE_DATA_UNVERIFIED; EMPIRICAL_REPRO_NOT_READY.

## Secondary candidate
Spence, Jenkins and Osman (2022), *Impact of disease characteristics and knowledge on public risk perception of Zoonoses*. Dryad DOI 10.5061/dryad.dncjsxm32. https://datadryad.org/dataset/doi:10.5061/dryad.dncjsxm32 . Official Dryad listing: UK public survey n=727, 11 zoonotic diseases, 12 qualitative risk attributes, files README_SPENCE_BIO_LETTERS_DATASET.txt (1.26 KB) and Spence_Data_Sub.xlsx (332.10 KB). Direct download attempts for both files returned HTTP 403. Spreadsheet field names, participant IDs, dates, consent/privacy, reuse licence, missingness and raw observations remain UNVERIFIED. No raw personal data accessed.

## R073 compatibility and next
Both sources concern risk ratings, not continuous dyadic repeated-game decisions. R073 frozen independent dataset gate: HARD_NO_BY_TASK. No R073 model or scoring changes, no E2 scoring. Next attempt no-cost public raw access via alternate official mirrors and explicit dataset licence, then verify schema and hazard/participant identity before any model comparison. No paid account, paid API, purchased data or nonpublic data used.
