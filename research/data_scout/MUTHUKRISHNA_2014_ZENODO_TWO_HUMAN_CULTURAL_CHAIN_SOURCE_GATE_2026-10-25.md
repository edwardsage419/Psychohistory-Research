# A data scout: Muthukrishna et al. cultural transmission, two human experiments

Date: 2026-10-25. Source: Muthukrishna, Shulman, Vasilescu and Henrich, *Sociality influences cultural complexity*, publisher-linked public dataset DOI 10.5061/dryad.8th12; accessible mirror https://zenodo.org/records/4973326. Original source record describes two distinct laboratory tasks. The linked original article DOI is 10.1098/rspb.2013.2511.

## Actual publicly visible source rows and schema
Zenodo published two CSV assets: `Experiment1.csv` 3.1 kB, publisher MD5 `12910570ff595db1e0694ffe0afbd4d1`; `Experiment2.csv` 3.5 kB, publisher MD5 `e0263cda7e01b6913a529e4f10784a4d`. Both complete plaintext CSV bodies were accessible through the public Zenodo file views on 2026-10-25, each displaying one header and 100 data lines. The actual bytes have not been independently downloaded and hashed locally, so these MD5s remain publisher-reported only.

Experiment 1 visible header: `ID,ImageEditExpScreen,ImageEditSkillScreen,Generation,GroupCondition,Age,Male,Ethnicity,Algorithm,Rating`. Visible design: 10 generations with five participant records per generation for each of two GroupCondition values, totaling 100 records. No explicit independent chain identifier or direct teacher-student edge is present in this file. `Algorithm` and `Rating` are performance-related outcomes; they are not binary cultural trait A decisions.

Experiment 2 visible header: `ID,Chain Number,GroupCondition,Generation,Age,Male,Ethnicity,Exp. Sailing,Sailing.Deg.Of.Exp,Exp. Climbing,Climbing.Deg.Of.Exp,Score`. Visible design: 10 labeled chains, 10 generations per chain, five chains in each condition, totaling 100 records. Chain identifiers contain whitespace inconsistencies (e.g. `Chain4 `, `Chain 7`); any normalization must be documented before evaluation. `Score` is a performance outcome, not a binary cultural majority vote. The participant `ID` field is pseudonymous; do not redistribute personal-level source rows unnecessarily.

## Deduplication and evaluation gates
The repository DOI dedup registry `research/SOURCE_PROVENANCE_DOI_DEDUP_REGISTRY_2026-10-18.json` does not list this dataset; the original239 07-001/R159 reference covers a synthetic majority-copying model. This is a candidate distinct from the already registered dyadic R073/R096 studies. Full literature-wide and cohort-wide deduplication remains pending.

Experimental unit for experiment 2 should be the whole transmission chain, not each participant row or each generation. A chain-held-out design might be feasible for a future separately frozen performance model, after confirming generation-specific teacher links and task instructions. Experiment 1 requires explicit independent chain/source identities before valid cluster-independent claims. Neither CSV provides the R073 frozen dyadic action, opponent and session fields. R073 scoring is ineligible. These are human E2 source records, but no E2 predictive scoring was executed.

License field on the accessible Zenodo landing page is blank. Redistribution rights are unverified. No paid account or private data was accessed. Source body was viewed publicly; exact raw byte checksum, full missingness audit, linkage and reuse license remain OPEN.

## Access and evidence state
`PUBLIC_HUMAN_ROW_SCHEMA_VISIBLE / ORIGINAL_BYTES_HASH_PENDING / EXP2_CHAIN_ID_VISIBLE / R073_INELIGIBLE / LICENSE_PENDING / E2_SCORE_NOT_RUN`.

Source URLs:
https://zenodo.org/records/4973326
https://zenodo.org/records/4973326/files/Experiment1.csv?download=1
https://zenodo.org/records/4973326/files/Experiment2.csv?download=1
