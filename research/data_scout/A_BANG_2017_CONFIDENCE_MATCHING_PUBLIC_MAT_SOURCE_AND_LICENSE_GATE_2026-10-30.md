# A data scout: Bang et al. 2017 confidence matching in group decision making

Date: 2026-10-30 Asia/Singapore. Track: r/A. Evidence type: public source registry and schema metadata only. Status: PARTIAL, binary raw-record gate BLOCKED in this execution environment.

## Primary sources actually read

Author GitHub repository: https://github.com/danbang/article-confidence-matching (master). Paper: Bang et al., *Confidence matching in group decision-making*, Nature Human Behaviour (2017), https://doi.org/10.1038/s41562-017-0117. Author README Git blob 0515aaa51c88f2f10c63e2658ec8d52df95c4793. Repository MIT LICENSE Git blob 6c4b7f2dabab291c71346be66ff73ac8dea08db4, copyright 2018. Author README explicitly says the data are released under a permissive open-source license. This is a repository-level license observation, not a separate per-participant consent audit.

Read the author README and LICENSE, enumerated the Data directory through GitHub API. Fourteen MATLAB .mat files are publicly listed. Particularly relevant: Data/exp2-S.mat, 41,674 bytes, Git blob fe5138ffc6625a3eda042cef133b9167ce0d7bac; Data/exp3-S.mat, 80,270 bytes, Git blob 604b3605a799a1b316c2e1fb7c0ef10b89f42ae8. These are public file identities and advertised sizes, not locally decoded data.

## Reported design and fields

Author README reports six experiments. Experiment 2 social task: 384 trials; Experiment 3 social task: 384 trials, continuous confidence. Experiment 1 isolated and social tasks: 160 trials each. Experiment 4 includes social runs with virtual partners; experiment 5 social task 160 trials with a strictly proper scoring rule. Experiment 6 has isolated/social/observe tasks.

Author README names group, sbjID, trial, stimInterval, stimContrast, sbjConfidence, sbjChoice, sbjAcc, otherConfidence, otherChoice, otherAcc, dyadChoice, dyadAcc. The README also documents order, noise, bias, condition, session for applicable experiments. This is a genuine repeated individual/group perceptual decision source, potentially useful for longitudinal social influence and confidence calibration. It is not a prisoner's dilemma dataset and is not R073 frozen 100-round dyadic PD replication evidence.

## Actual access attempt and missing checks

The GitHub blob fetch for exp5-S.mat (8,270 bytes, blob a6af47ac0e4f18a78307bb2a9c4dd71fa1e38220) returned UnicodeDecodeError because the connector expects UTF-8. Binary MATLAB content was not materialized or parsed. Therefore observed row counts, participant counts, trial continuity, group identifiers, repeated pair identities, missingness, individual trial timing, calibration target semantics, and file-level consent/reuse conditions remain UNVERIFIED. The README's 384 trials are experiment-design metadata and must not be reported as 384 verified rows or independent participants.

## Reproduction readiness

SOURCE_DISCOVERED=YES; README_SCHEMA_DOCUMENTED=YES; REPOSITORY_LICENSE_READ=YES; RAW_MAT_BYTES_DECODED=NO; SUBJECT_AND_DYAD_KEYS_VALIDATED=NO; TIME_UNIT_VERIFIED_FROM_RECORDS=NO; R073_ELIGIBLE=NO; HUMAN_E2_PREDICTION=NOT_RUN. Next: use a free binary-capable download path and scipy.io.loadmat or HDF5 parser as appropriate, then validate keys, actual trial counts, group pairing, privacy and reuse terms before any E2 analysis. No private data or paid account used. No raw participant records republished.

Deduplication: current source ID (Bang2017, Git blob fe5138ff, 384-trial social perceptual confidence matching) is separate from previously registered Mao2017, Akata2024 and R073 PD experiments. Future overlap must be checked before new analysis.
