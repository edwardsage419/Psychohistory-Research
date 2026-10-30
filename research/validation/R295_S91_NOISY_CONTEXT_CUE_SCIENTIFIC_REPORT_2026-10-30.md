# R295 S91 scientific report: noisy context cue, finite artificial habit control

UTC 2026-10-30. Research track r. Original R295 item 01-019 Habit Formation, original formal acceptance CLOSED_BOUNDED_E1 remains unchanged. This extension is E1 synthetic only and PARTIAL scientific acceptance.

## Prescore binding

The new protocol was committed before any S91 results at commit 4b67e0dd172f6633a37c4ba65f12e7b5269856b2: [freeze](R295_S91_NOISY_CONTEXT_CUE_PRESCORE_FREEZE_2026-10-30.md). Original source blob c8400ce907e2f09734bbdf5f018074ce73d0b130. Primary implementation: [script](r295_s91_noisy_context_cue_20261030.js), corrected exact numerator assertion in a separate pre-scoring commit 97a2c7fbe2a2a41ec1f8f52821f64e7627a1f263. The correction is preserved in commit history and preceded the first S91 result calculation. No original R295 code or source changed.

## Finite world and exact results

Preserve R295's H_n=1-(1-alpha)^n and deterministic A choice iff (1-lambda)*V+lambda*c*H_n>1/2, exact tie selects B. Fixed 90 alpha/lambda/V/n settings, three independent binary observation error rates e=0,1/4,1/2, and each true cue C and observed cue Z pair. Enumerated 270 settings and all 1080 probability atoms, including 180 zero-mass atoms. Source CSV and complete 270-setting JSON are persisted alongside this report.

Exactly 22 of 90 settings are cue-sensitive, distributed as lambda=0:0/30, lambda=1/2:8/30, lambda=1:14/30. These are artificial grid counts, not people. For any cue-sensitive setting, no-cue Bayes Brier=1/4; observed noisy-cue Bayes Brier=e*(1-e); true-cue oracle Brier=0. The remaining 68 settings have all three Brier risks zero. This is prediction under the known data-generating mechanism, not fitted or learned out-of-sample human prediction.

| Cue error e | Sensitive settings | Total baseline Brier over 90 settings | Total noisy cue Brier | Total information gain |
|---|---:|---:|---:|---:|
| 0 | 22 | 11/2 | 0 | 11/2 |
| 1/4 | 22 | 11/2 | 33/8 | 11/8 |
| 1/2 | 22 | 11/2 | 11/2 | 0 |

For each cue-sensitive setting, improvement is 1/4 at e=0, 1/16 at e=1/4 and 0 at e=1/2. For lambda=0 all settings are cue-insensitive by the original construction. Observing a noisy cue helps only where the synthetic action actually depends on cue. No additional causal effect or real human habit mechanism is established.

## Executed evidence and limits

R route read the persisted 180-row original CSV from GitHub and generated 1080 labelled atoms and 270 result settings in V8, with fixed original Git blob identity recorded. The archived standalone Node CLI was not run in a native Node checkout; container download was blocked by DNS, so native replay remains NOT_RUN. B route independently reconstructed the deterministic action using integer-scaled habit strength, audited the persisted 1080 atoms and 270 results, and rejected eight of eight deliberately malformed controls. A separate local Python Fraction computation independently confirmed 22 cue-sensitive settings and the three exact risk formulas. All such checks are internal nonblind procedural replication; no external independent team.

No probabilistic calibration on real people, no external holdout sample, no E2 or E3. No original R295 formal status update, no original239 catalogue changes, no R073 or PESEN v0.1 changes. New S91 scientific acceptance=PARTIAL. Future work: native Node CLI execution on a real checkout and, separately, pre-registered real-world cue measurement evaluation if legally available and scientifically comparable.
