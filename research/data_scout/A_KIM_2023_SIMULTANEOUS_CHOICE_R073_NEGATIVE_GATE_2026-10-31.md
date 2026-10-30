# A data scout: Kim 2023 repeated PD design and R073 negative eligibility gate

Date: 2026-10-30 UTC. Target key: (A,Kim_2023_openICPSR_E152261V1,source-design-v1,prospective-history-availability-negative-gate). This is a distinct eligibility check following the earlier A_KIM_2023_OPENICPSR_E152261_REPEATED_PD_SESSION_GATE_2026-10-31.md. No original file is overwritten.

## English-language source evidence inspected

Official openICPSR V1 project: https://www.openicpsr.org/openicpsr/project/152261/version/V1/view . Published 2023-01-25, DOI https://doi.org/10.3886/E152261V1 . The official data_code listing: https://www.openicpsr.org/openicpsr/project/152261/version/V1/view?path=/openicpsr/152261/fcr:versions/V1/data_code . The official temp directory: https://www.openicpsr.org/openicpsr/project/152261/version/V1/view?path=/openicpsr/152261/fcr:versions/V1/data_code/temp . The original journal paper is https://doi.org/10.1257/mic.20200195 .

Official description explicitly states subjects make all stage-game decisions at once, with payments delivered over weeks or months. Three randomized treatments have four sessions each, with 14 to 20 subjects per session. The official temp directory displays 12 CSV files and 12 corresponding Stata files, with session-like date/time filenames, including 160929_1539_mod.csv (660.3 KB) and 161019_1537_mod.csv (316.4 KB). The data_code directory also lists readme.txt (3.6 KB), time_coop.dta (1.4 MB), and Stata scripts. These are visible metadata, not parsed rows.

## Specific R073 frozen-design decision

R073 requires prospective next-action conditional prediction from genuinely observed earlier personal and opponent moves, and its existing protocol uses 100 sequential rounds per person in the original Montero-Porras fixed/shuffled experiment. Kim's all-at-once elicitation cannot provide contemporaneous feedback from previous realized opponent actions within the same precommitted choice sequence. Thus **R073 unchanged historical-opponent-feedback mechanism replication is DESIGN_INELIGIBLE on the published description**, irrespective of whether the raw data later reveal many nominal rounds. Retrospective strategy-contingent choices would be a different estimand and need a separately frozen study. This negative design gate is stronger and more specific than the prior NOT_ESTABLISHED raw-schema gate. It does not prove the dataset is unusable for other real human E2 studies.

## Field, identity, licensing and access gates

Verified: project DOI/version, publication, real human lab source, three treatments, twelve session files, dated session file names, experimental choice elicitation, week/month payoff timing. Unverified: raw column names, participant and dyad identifiers, whether all choices were contingent strategies, individual actual round counts, observed opponent actions, missingness, file digests, per-file redistribution permission, and exact original source license. Official file preview page shows the filename and a download link but does not expose the raw content through the available public reader. No original CSV bytes were obtained. No login, paid account or private data accessed. Do not infer data reuse permission from project visibility.

Next source priority: a genuinely independent experiment with sequential within-dyad action histories, stable participant/session IDs, and at least 100 consecutive rounds under R073 frozen conditions. Preserve Kim as a separate time-preference/cooperation candidate with SOURCE_BYTES_BLOCKED and R073_DESIGN_INELIGIBLE. New E2=0 and E3=0.
