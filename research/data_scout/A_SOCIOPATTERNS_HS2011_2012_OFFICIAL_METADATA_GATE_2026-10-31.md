# A track: 2011 and 2012 SocioPatterns high school contact source and identity gate

Date: 2026-10-31 UTC. Target key: (A,SocioPatterns_HS_2011_2012,official_public_metadata_v1,real_temporal_contacts_and_R073_gate).

**Primary public source:** https://sociopatterns.org/datasets/high-school-dynamic-contact-networks/ (published 2014-08-24). Official maintained source description: https://github.com/SocioPatterns/sociopatterns.github.io/blob/main/_datasets/high-school-dynamic-contact-networks.md , Git blob `1ed091519eff29aaf30858ce3ef83daaad904c80`.

This is an independent earlier cohort relative to the 2013 high school metadata examined in the prior R309 S105 A track. Do not mix participant IDs across years or assume the same individuals. 2011 comprises three student classes plus a teacher metadata category, four collection days in December 2011; 2012 comprises five student classes and seven collection days in November 2012.

## Actually read and verified
* 2011 official public text metadata `assets/data/highschool_2011_metadata.txt`, Git blob `b24abfebefee837206563141ca3f7d3452d903bc`: 126 records, 126 unique anonymous IDs, 3 tab-delimited fields per row, no repeated IDs; class values PC, PSI*, PC*, teacher; gender labels F, M.
* 2012 official public text metadata `assets/data/highschool_2012_metadata.txt`, Git blob `b5e6ebe0413b3e8985fccaf6983eb1754cd37518`: 180 records, 180 unique anonymous IDs, 3 fields per row, no repeated IDs; classes PC, MP*2, PSI*, PC*, MP*1; gender labels F, M.
* Public raw contact files are listed as `assets/data/highschool_2011.csv.gz` and `assets/data/highschool_2012.csv.gz`. Official documentation specifies contact rows `t i j Ci Cj`, with 20-second active-contact intervals, anonymous pair IDs, and two class labels. 2012 t uses Unix seconds. The 2011 time origin and exact timestamp semantics must be checked before cross-year alignment.
* Official page licenses the published data CC BY-NC-SA. The license permits attributed noncommercial research under its conditions; it does not grant unrestricted commercial redistribution.

## Reproduction gate
Actual compressed contact bytes, row counts, unique contact dyads, timestamp range, overlap with metadata IDs, duplicate intervals and file SHA256 are **NOT_VERIFIED**. Metadata counts do not establish the number of people appearing in the contact stream. An accessible metadata file is not evidence that contact behavior has been parsed. No row-level human records were copied into the research repository. This is a public-source/identity gate, not a human prediction experiment.

R314 eligibility: observed temporal proximity contacts are neither new-vertex single-edge attachment histories nor a confirmed growth-only network. A network edge at time t may disappear. BA-versus-uniform mechanism E2 test **NOT_READY**; requires independently specified arrival definitions and outcomes, with no post hoc choice of time ordering.

R073 eligibility: **HARD_NO_BY_TASK**. These files contain contacts, not paired sequential prisoner-dilemma actions with fixed frozen scoring. E2 model scores=0.

Next: obtain the two publicly licensed compressed contact files without payment; verify bytes and schema in an isolated environment; preserve 2011/2012 and 2013 provenance separately. If inaccessible, retain BLOCKED status. No purchase, account registration, or private data access.
