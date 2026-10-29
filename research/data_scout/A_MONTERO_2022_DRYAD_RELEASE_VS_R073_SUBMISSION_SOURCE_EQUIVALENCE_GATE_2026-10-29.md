# A track: Montero 2022 official Dryad release versus R073 submission data identity

UTC date: 2026-10-29. Key: `(A,doi:10.5061/dryad.37pvmcvmk,R073-source-lineage,official-release-equivalence)`.

## New official evidence actually inspected

Official English-language Dryad record: https://datadryad.org/dataset/doi:10.5061/dryad.37pvmcvmk (Montero, Eladio; published 2022-05-25). The official page explicitly lists the release files:
* `fix.csv`, 742.09 KB
* `rand.csv`, 796.02 KB
* `README.txt`, 1.52 KB
* `Instructions_of_the_experiment.docx`, 1.05 MB
* `UserInformation.csv`, 6.83 KB

The record states two pairwise iterated Prisoner's Dilemma treatments, six fixed-partner sessions with 92 participants and six shuffled-partner sessions with 96 participants, 188 participants total. Source publication DOI `10.1038/s41598-022-11654-2`. Official data DOI `10.5061/dryad.37pvmcvmk`.

The README download entry `https://datadryad.org/downloads/file_stream/1514376` was actually requested during this cycle; response was HTTP 403 Forbidden. No raw Dryad CSV bytes or README fields were recovered. File-level content, row counts, checksum, exact version correspondence, and dataset-specific license remain `NOT_VERIFIED`. Optional demographic `UserInformation.csv` was not accessed, since this study only requires anonymized repeated decisions.

## Cross-check against the existing R073 study

Project `research/R073/README.md` already documents an author GitHub submission tag at commit `4743f74d8a03a031b8f70aff64956f8ad5155182`, two original `fix.csv` and `rand.csv` files, 12 sessions and 18800 participant actions. The R073 original-source warning explicitly says the author GitHub submission files have not been proved byte-identical to the final Dryad release.

This round confirms the official release has matching file names and experiment design metadata. That is metadata agreement only. It does not prove SHA identity, identical row universe, no later corrections, or independent new participants. The candidate is an `EXISTING_R073_STUDY_FAMILY_WITH_RELEASE_EQUIVALENCE_OPEN` and cannot count as an independent new R073 validation cohort.

## Reproduction readiness

Source DOI and official file roster: `VERIFIED`. Published design, time unit and 12-session cohort: `VERIFIED_AT_DOCUMENTATION_LEVEL`. Original GitHub R073 behavior records: `PREVIOUSLY_VERIFIED`, unchanged in this cycle. Official Dryad behavior bytes and field-level join: `BLOCKED_HTTP403`. Independent new dataset eligibility: `NO`. Release identity: `OPEN`. License for redistribution: `NOT_VERIFIED`.

Next authorized action: retry the public release README/CSV through a permitted no-cost channel, compare exact bytes/hashes and anonymous session/round keys with frozen R073 submission sources, without altering R073 scoring or inspecting optional personal demographic records. No E2 or E3 prediction added. No purchase, paid API, private data, or registration.
