# A track: SocioPatterns HighSchool2013 metadata identity delta

Date: 2026-10-31 UTC. Track key: (A,SocioPatterns_HighSchool2013,official_public_metadata_v1,metadata_id_universe). Status: `METADATA_TEXT_ACTUALLY_READ / CONTACT_GZ_NOT_PARSED / NO_E2_SCORE`.

## Prior work and distinct question
Read existing `research/data_scout/SOCIOPATTERNS_MASTRANDREA_2015_HIGHSCHOOL2013_TEMPORAL_NETWORK_R169_SOURCE_GATE_2026-10-26.md` (Git blob `ebbec52419b72f3669fbff7041f99828b6833f34`). That prior report established official schema, license, five-day time window and explicitly left unique metadata person count unverified. This delta checks the **actual publicly readable metadata file** and its identity/class completeness; it does not repeat the prior source-gate claim.

## Original public evidence
Dataset-maintainer English source: https://github.com/SocioPatterns/sociopatterns.github.io/blob/main/_datasets/high-school-contact-and-friendship-networks.md (Git blob `1ee86219e7f7d21d3d17e964a56c24f2b230e933`). Primary public site: https://sociopatterns.org/datasets/high-school-contact-and-friendship-networks/ . Underlying study: Mastrandrea, Fournet and Barrat, PLOS ONE 2015, DOI 10.1371/journal.pone.0136497.

**Actual text file fetched and parsed**: `SocioPatterns/sociopatterns.github.io/assets/data/HighSchool2013_metadata.txt`, Git blob `50b7012ada20f2c9277d5c0eefe83f5d45b932c4`, 3,574 bytes. Each line contains exactly three tab-separated fields `anonymous_id, class, reported_gender`. There are **329 rows, 329 distinct anonymous IDs, zero malformed three-field lines**, and nine class codes. Class counts: 2BIO1 36, 2BIO2 35, 2BIO3 40, MP*1 29, MP*2 38, PSI* 34, PC 44, PC* 40, MP 33; total 329. Third-field codes: F 146, M 176, Unknown 7. These are counts of records in the public metadata text only; **the number of distinct IDs in the actual contact stream remains unverified**. No person-level rows are copied into this repository.

GitHub directory metadata confirms the source-maintained binary `HighSchool2013_proximity_net.csv.gz` exists, size 653,252 bytes, Git blob `9ad96b3e331a6744efdf198a1c2c94a0fe6b226d`. The compressed contact stream was **not decompressed or row-parsed**. Its actual row count, timestamps, edge IDs, contact-to-metadata join coverage, missingness and file SHA256 remain OPEN. Other compressed files are also not parsed.

## Design, license and applicability
Official contact schema is `t i j Ci Cj`: one active proximity contact per 20-second interval, anonymous IDs and class codes, five days in December 2013. These are observed **contacts**, not observed infection, norm adoption, opinion changes or repeated prisoner's dilemma actions. The same school and repeated timestamps imply dependence. A five-agent homogeneous independent-contact SIR model cannot be calibrated or scientifically validated by merely attaching a contact edge list. A future network-only E2 descriptive analysis would require a separately frozen question, privacy screening and time-blocked holdout.

Official source explicitly lists **CC BY-NC-SA 3.0**, with attribution, noncommercial and share-alike conditions. This audit only stores aggregate checks and original links, avoiding raw student-level records. Source has no R073 paired C/D choices, so `R073_DIRECT_TRANSFER=INELIGIBLE`. R309 S105 remains artificial E1; E2/E3 newly scored 0.

## Next reproducibility gate
Obtain the already public compressed bytes through a lawful free route, verify compressed digest, decompress in a local sandbox, check five-field row schema and unique contact IDs, and calculate metadata join coverage. If blocked, preserve the blocker. Never infer disease or opinion outcomes from physical proximity alone.
