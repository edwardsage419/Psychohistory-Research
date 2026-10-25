# A data source gate: Cason et al. 2026 real human indirect reciprocity experiment

Date: 2026-10-26. Baseline HEAD 01b14fb848ed1b645d39212ead1d9a928f7d5c75. Track A, public-data scout. Source official English-language Dryad: https://doi.org/10.5061/dryad.mcvdnckd6 (published 2026-01-20). Primary authors Cason, Riedl, Schram and Ule, *Local competition promotes hurtful behavior towards unknown others*. Source DOI and file inventory verified from official Dryad page; raw CSV byte retrieval was NOT performed.

## Directly verified documentation and design

Official files: CRSU_rawdata.csv (2.75 MB shown), README.md (7.57 KB), Strategy_Class.csv, strategy scripts and ethics approval. Official README explicitly documents these original raw fields: ida, idb, round, adecision, group, session, cohort, indivIDa, indivIDb, R1dum, R2dum, bluedum, purpledum, plus lagged help, snub, hurt and optional information-click fields. A recipient has no action in that round; only donor A chooses among help, snub, hurt. The source reports 156 human subjects, 100 rounds per experimental session, 6 subjects per cohort, 3 randomly formed donor-recipient pairs per cohort per round, and anonymized participation. It reports one session per subject. The study compares local versus global competition; the authors treat each six-person cohort as an independent observation. The same session may contain multiple cohorts, so a more conservative independent unit may be session if shared session effects matter.

Observed fields permit an eventual time-ordered actor/recipient history reconstruction, but need raw-row verification of whether cohort and individual identifiers remain stable across all rounds, exact missingness, event ordering, role assignment, and whether information-click fields are pre-decision. Source README says lagged behavior was visible to donors; leakage prevention must use only information available before donor decision. Cohort and session grouping should be preserved across splits. Never split individual rounds at random.

## Suitability and exclusions

This is a real human repeated indirect-reciprocity experiment with observed behavior, session, cohort, and person IDs. High value for R135 indirect reciprocity, R136 direct reciprocity contrast, social learning, and longitudinal decision research. It is **not** a two-person simultaneous binary iterated prisoner's dilemma: R073 frozen model/score is not directly compatible and must not be silently recoded or tuned. The original paper's strategy classification table is derived from outcomes and must not be fed as pre-decision features.

Source-identity check against existing scout filenames found no prior Cason/CRSU registration at baseline. A distinct original experiment is plausible, but deduplication against all original R studies is pending. Counts of actual CSV rows, 26 cohorts inferred from 156/6, and 15,600 subject-round opportunities are design-based implications, not observed raw-row counts. Do not present them as verified CSV row totals.

## Rights, access, and replication gate

Dryad openly exposes downloadable raw CSV and README. Dryad site has a general reuse notice; a file-specific license identifier and terms were not independently read in this run. Do not redistribute raw data until checked. Download and hash of the actual 2.75 MB CSV, exact field parsing, missingness, cohort/session stability, and legal reuse remain PENDING. Stata version 19 is reported for original analysis; a future Python standard-library reader can validate the CSV without purchasing Stata. A prescore protocol must be frozen before any future E2 prediction. No paid resources, no nonpublic data, no person-level reidentification.

Status: PUBLIC_SOURCE_AND_README_SCHEMA_VERIFIED; RAW_BYTES_PENDING; LICENSE_FILE_SPECIFIC_PENDING; SESSION_AND_COHORT_SPLIT_PENDING; R073_NOT_COMPATIBLE; NEW_E2=0; NEW_E3=0.

Primary source: https://datadryad.org/dataset/doi:10.5061/dryad.mcvdnckd6 . Current R171 mathematical research is unaffected. R073 and PESEN v0.1 remain frozen.
