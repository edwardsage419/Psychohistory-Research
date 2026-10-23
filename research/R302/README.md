# R302 Multi Armed Bandits: exact Thompson Beta posterior selection, synthetic E1

Original 239 item **02-016**, P1. First-party Thompson (1933), *Biometrika* https://doi.org/10.1093/biomet/25.3-4.285. Related Auer, Cesa-Bianchi, Fischer (2002) https://doi.org/10.1023/A:1013689704352 addresses regret/UCB but **R302 does not implement UCB1 nor prove regret bounds**.

**81 fully artificial success/failure count worlds, 162 source rows** (each world has one A-arm and one B-arm source). Independent Beta(1,1) priors, exact posterior superiority P(theta_A>theta_B) vs deterministic posterior mean greedy with A tie, computed with Fraction. No real arm reward-generating probabilities, reward trajectories, actual decisions, empirical bandit regret, human E2 or history E3.

[Original frozen prescore protocol b3c92f9f](https://github.com/edwardsage419/Psychohistory-Research/commit/b3c92f9f013e795a0db4622dc48613f82eb38bca) | [Full protocol](../../protocols/R302_MULTI_ARMED_BANDIT_THOMPSON_BETA_162_SOURCE_PRESCORE_FREEZE_2026-10-23.md).

* [Executable exact posterior superiority calculator with 660 tests](r302_exact_beta_thompson_bandits.py)
* [All 162 fully labeled artificial original arm source rows](R302_ALL_162_ORIGINAL_BETA_BANDIT_ARM_SOURCES.csv)
* [All 81 world posteriors, variances, greedy actions, Thompson selection probabilities](R302_EXACT_BANDIT_THOMPSON_RESULTS.json)
* [Original source and result SHA256 machine receipt](R302_MACHINE_RECEIPT.json)
* [Independent alternating-polynomial Beta integral reproof and 17 adversarial tests](../catalogue_audit/independent_r302_source_audit.py)
* [Full scoped report with model limitations](R302_SCIENTIFIC_REPORT_2026-10-23.md)
* [Machine final bounded E1 acceptance](R302_FINAL_ACCEPTANCE_STATUS.json)

Illustrations: A1success/no failure vs unobserved B has P_TS(A)=2/3; A2success vs B2failures P_TS(A)=19/20, so B remains 1/20 probability. Equal posterior means do not uniquely characterize posterior variance, and no actual reward has been observed after the artificial decision.

[All three successful CI jobs run39930778614](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39930778614), original synthetic source permanently archived [commit25b895e3](https://github.com/edwardsage419/Psychohistory-Research/commit/25b895e30416f109d38e6bd083163ff08d0d5dd0). R073/PESEN v0.1 remain frozen, all R-series before catalogue-wide taxonomy/fusion.
