# A track: Pereda et al. 2019 public goods longitudinal action data source gate

Date: 2026-10-30 UTC. Target key (A,Pereda2019,Zenodo-2590686-v1,public-CSV-schema-and-independence-gate).
Status: PUBLIC_SOURCE_SAMPLE_VERIFIED; FULL_FILE_ROW_LEVEL_AUDIT_NOT_RUN; R073_NOT_ELIGIBLE.
No original human records are redistributed in this repository.

## Fixed public provenance
English-language official Zenodo record https://zenodo.org/records/2590686 ; DOI https://doi.org/10.5281/zenodo.2590686 ; version v1, published 2019-03-11. Accompanying article DOI https://doi.org/10.1038/s41598-019-50964-w . The public downloadable original file is https://zenodo.org/records/2590686/files/2017A2ECOCOOPANSA01ONL0000ESPMAD.csv?download=1 . The Zenodo record reports 612.2 kB and MD5 626c61c2c18a114a5b92a7d2b7e46558. This MD5 was read from the record and has NOT been independently recomputed. The record's rendered Rights/License section does not expose an identifiable license value, so raw data redistribution permission remains UNKNOWN.

## Actual source inspection
Read the English record's field dictionary and multiple noncontiguous windows of the actual public text CSV, including first rows, lines around 10,459 and 10,500, and final lines around 21,094 through 21,195. The displayed file has eight columns: participant_id, player_alive, group_avg_contribution, player_contribution, round_number, gender, age, treatment.
Observed treatment labels include PGG100, PGG1000, PGG_H2. Round indices are actual game rounds, not calendar dates. Individual contribution is the behavior variable; group_avg_contribution is an aggregate and should not be treated as independent individual behavior.
The public CSV includes rows with eight empty fields (for example near displayed line 101 and 10,459), #N/A demographic fields, and player_alive=0 rows that still have a contribution field. These are concrete parsing and missingness hazards. Displayed participant_id values restart from 1 across treatments and rounds, so participant_id alone is not a globally unique longitudinal identity; at minimum treatment and source session need consideration. No explicit session or interaction group ID appears among the eight columns. Group membership, repeated identities across sessions, and independent unit definition require paper/code corroboration.
The web text viewer reports 21,196 lines including header and blank separators. This is a viewer line count, NOT a verified count of valid human action rows; no full raw-file byte download, checksum recomputation, or full CSV parser run occurred. The sampled lines establish a real public behavioral file and concrete schema hazards only.

## Eligibility and reproducibility decision
Suitable as a candidate for longitudinal public goods contribution dynamics and information/treatment contrasts after independent-unit reconstruction. Not directly suitable for the R073 frozen 100-round two-person repeated prisoner's dilemma test: this is a public goods design and dyadic opponent actions are not present in the inspected schema. No R073 fitting or score was attempted.
Before empirical analysis: (1) fetch exact public file and recompute MD5/byte hash using free local tools, (2) parse eight columns and separator rows, (3) audit treatment x round x participant uniqueness, dropouts and player_alive, (4) determine sessions/groups and round maxima from original paper, (5) verify license explicitly before any redistribution, (6) prefreeze unit-aware split and held-out evaluation. Never use demographic values for personal identification.
Evidence: PUBLIC_REAL_SOURCE_METADATA_AND_SAMPLED_ROWS, E2_PREDICTION=0, E3_PREDICTION=0. Access is open without payment or registration; actual full reconstruction remains OPEN. No paid resources used.
