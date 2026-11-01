# A: Romero and Rosokha 2023 directly elicited repeated-game strategies, source gate

track: A
run_date_utc: 2026-11-01
observed_main_before_write: 88a5d492293a30c0a24f4e799f35fb4dd2aa8513
status: PARTIAL_SOURCE_METADATA_ONLY
source_candidate: Romero, Julian; Rosokha, Yaroslav (2023), Mixed Strategies in the Indefinitely Repeated Prisoner's Dilemma, Econometrica 91(6), 2295-2331
doi: https://doi.org/10.3982/ECTA17482
publisher: https://onlinelibrary.wiley.com/doi/full/10.3982/ECTA17482
publisher_supplement: https://onlinelibrary.wiley.com/doi/abs/10.3982/ECTA17482
source_access_checked_utc: 2026-11-01
R073_frozen_eligibility: UNKNOWN
R073_score: NOT_RUN
PESEN_v0_1: FROZEN
new_E2_E3: 0
CI: NOT_RUN
billing_checked: NOT_VERIFIED

## Actual source check

Read the publisher's English full-text article and supporting-information listing. The paper was first published 2023-12-07. The main treatment reports six Purdue laboratory sessions in April 2018, each with 60 supergames. Participants directly constructed probabilistic action rules, including cooperation probabilities conditional on prior CC/CD/DC/DD outcomes. This makes the data conceptually useful for comparing observable action histories with elicited strategies, and for examining whether an action-only model confuses mixed and pure mechanisms.

The publisher lists `ecta200610-sup-0002-dataandprograms.zip` as a 197 MB Data and Programs supplement and a separate 891.1 KB appendix. The existence of the listed supplement is confirmed at the publisher metadata level only. Neither ZIP nor data dictionary was downloaded or opened. Participant IDs, within-supergame round fields, partner pairing, treatment separation, full sample identity, raw file hashes, file-level license and permission to redistribute remain UNKNOWN. No executable code from the archive was run.

## Deduplication and frozen test gate

The current R073, R074, R075, R096 and DF2011 evidence cannot be assumed independent of this candidate solely from a different article title. The 2023 paper discusses earlier Romero and Rosokha experiments and comparisons with prior studies. Before any scoring, verify session collection dates, participant/sample identity, treatment, original source lineage and overlap with all already registered studies. A GitHub default-branch code-search query for `Romero Rosokha` and `ECTA17482` returned no hits, which is insufficient to prove the repository has no prior record.

The main treatment uses repeated supergames and elicited strategies. It is not yet established that it supplies the same fixed-pair continuous sequence unit and prespecified action fields required by R073's frozen external evaluation. If the unit differs, retain as a distinct exploratory E2-method candidate without changing R073 or PESEN v0.1.

## Next executable low-cost check

If publicly accessible without new fees, inspect only the publisher's supplement manifest and metadata, without executing bundled code. Record archive SHA256, license, session/person/opponent/supergame/period columns and exact repeated-pair semantics. Deduplicate before any outcome access. Freeze a separate source and score plan before any new prediction if the original R073 protocol cannot apply unchanged.

No purchase, paid API, cloud compute, CI dispatch, restricted-data upload or new subscription. No raw experimental data was archived or redistributed.
