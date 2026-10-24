# A source deduplication: Montero-Porras 2022 is already R096

Date: 2026-10-24. Evidence type: provenance correction; no new E2.

## Previously registered candidate

The registry `research/data_scout/MONTERO_PORRAS_2022_LONG_IPD_DRYAD_SOURCE_REGISTRY_2026-10-24.md` described the 2022 long iterated Prisoner's Dilemma as a potentially independent experiment and reported Dryad HTTP 403 for direct raw CSV. The publication is Montero-Porras, Grujić, Fernández Domingos and Lenaerts (2022), Scientific Reports 12:7589, DOI 10.1038/s41598-022-11654-2; Dryad dataset DOI 10.5061/dryad.37pvmcvmk.

## Repository prior-work match

The same publication and experimental population are already explicitly covered by `research/R096/R096_MONTERO_2022_12_REAL_LAB_SESSIONS_188_HUMANS_100ROUND_FPSP_BINARY_LOSO_E2_SCIENTIFIC_REPORT_2026-10-17.md`. R096 records 12 actual sessions, 188 participants, 18,800 person-round source records and 18,612 scored next-round targets, using the author's fixed Git submission source commit `4743f74d8a03a031b8f70aff64956f8ad5155182`. R096 has source Git blob checks, session-wise leave-one-session-out M0/M1/M2 Brier scoring, and two archived CI reruns `39023796827` and `39023880006`. R096 explicitly records that the official Dryad CSV bytes were not acquired and were not proven byte-identical to the author's Git processed files.

## Decision

`SAME_ORIGINAL_EXPERIMENT_AS_R096 = YES`. Remove Montero-Porras 2022 from the list of newly independent experimental sources. Keep the earlier Dryad 403 report as an honest source-specific limitation. Do not count the Dryad landing page and the author's Git copy as two distinct experiments. Do not rescore under R073 or adapt its frozen model/score rules. The existing R096 E2 is a separate, bounded retrospective within-experiment held-out-session analysis with M0/M1/M2, not a newly executed exact R073 external replication. No new human data were accessed and no new E2 or historical E3 result is asserted.

## Next scout gate

Seek a genuinely different laboratory experiment or longitudinal source after checking DOI, original author datasets, and all existing R073 through R110 source reports. Require session and identity boundaries, row-level schema, lawful license, frozen model compatibility and time-aligned lag features before any new score. No paid access or non-public data.
