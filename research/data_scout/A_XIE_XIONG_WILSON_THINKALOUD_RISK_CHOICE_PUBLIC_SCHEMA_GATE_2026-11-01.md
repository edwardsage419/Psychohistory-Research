# A track public empirical candidate: Xie, Xiong and Wilson think-aloud risky-choice trials
Date: 2026-11-01 UTC. Track A. Status: PUBLIC_SOURCE_SCHEMA_LICENSE_VERIFIED; RAW_ROW_REPLAY_NOT_RUN; EMPIRICAL_SCORING_NOT_RUN.

## Fixed upstream identity and actual inspection
Upstream English-language public repository: https://github.com/xhb120633/think-aloud-language-models
Main commit observed: d4e5d3db9f16dbc7049e82665eb2fc217641245b
Read actual README blob 3bd1235535a3c2a01a0c8bcca25876c9efbf8498, data dictionary blob 9de80ba40f11c3152b216bca5f2a9803bfa68a80, data license blob a994bf4e452579ab890c482b24b2697ddf027bef, FILE_MANIFEST blob 8f1a825b07578fcac0e841f260aafbf985fb7ceb, data directory listing and CSV header only. The transcript-bearing data rows were deliberately not opened. No personal or nonpublic data accessed.

Research reference: Xie, H., Xiong, H.-D., and Wilson, R. C. (2025), *Rethinking Think-Aloud in the Age of Language Models*, PsyArXiv DOI 10.31234/osf.io/6ta3z_v2. This citation and counts are the upstream authors' claims; no original paper replication was executed.

## Public data objects
* Experiment 1 prospect-theory design: data/behavioral_text_data.csv, Git blob 54a9333b1a1e4f7cd62c99cc0d3e45c2f90458e3, 427115 bytes, upstream-reported 1368 trials, 72 participant keys.
* Experiment 2 Choices13k design: data/behavioral_text_data_expanded.csv, Git blob 3421a0c79721aaf14c05e3d5f0f0f7e8aa9295c4, 9652294 bytes, upstream-reported 44308 trials, 641 participant keys.
* Total upstream-reported 45676 trials. SHA256 values claimed in upstream FILE_MANIFEST: 9997fbef97a69969034a36c366a58a1e7907c65e44a8a08072b388ccb843b82a and b3ba4fdbaa9625b779a9d3a9c4dc756c2283cbcc86800c5f6b3e73db3bc48e08. Those SHA256 values were READ from a manifest, not independently recalculated from downloaded CSV bytes.
* Actual CSV header verified for first file: 0,1,2,3,4,5,6,7,8,9,10. Data dictionary maps to exported row index, anonymized participant sub_id, binary choice, probability and outcome lists for two gambles, problem_id, rt, think_aloud transcript, word_count.
* Unit of observation is a single risky-choice trial. RT is stimulus-to-choice elapsed milliseconds and includes concurrent speech. It must not be treated as a pure nonverbal motor response time. A sequential trial timestamp, game round, opponent identity and continuous dyad identity are not documented.
* Upstream counts 1323 nonblank transcripts in Experiment 1 and 36967 in Experiment 2. Data dictionary explicitly flags a four-record discrepancy versus the paper's 1327 valid-transcription count; unresolved.

## Rights, privacy and readiness
The data/LICENSE.md explicitly states CC BY 4.0 for the two CSV datasets; repository code LICENSE is MIT. The data license does not waive participant privacy/personality rights. Public anonymized free download is advertised with no registration. Do not copy transcripts into project archives or publish unreviewed excerpts; start with numeric fields only and use privacy-minimizing local checks.
Potential R318 risk-choice relevance: YES, subject to a separately frozen human measurement and grouped holdout protocol. Keep participants grouped across folds and problem_id grouped across repeated items; experiment 2 reuses a Choices13k design and is not automatically an independent population for any previously fitted Choices13k benchmark.
R321 S117 direct validation: NO. Its seven-bit Bernoulli evidence sequences and exact stopping thresholds are absent. A new behavioral mapping would be required. R073 frozen 100-round human-human dyad eligibility: HARD_NO_BY_TASK_TYPE.
Remaining: complete raw CSV parse and SHA256, actual participant uniqueness, trial ordering and missingness, problem overlap, privacy review, and independent E2 holdout protocol. No raw data fit or human score performed. No paid API, purchase or cloud computation.
