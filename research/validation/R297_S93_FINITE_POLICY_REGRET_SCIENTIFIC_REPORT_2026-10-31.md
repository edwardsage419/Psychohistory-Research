# R297 S93 finite policy regret and sustained-correctness report

Date: 2026-10-30 UTC. Target (r,R297,S93-v1,finite horizon oracle regret and first sustained correct action). Prospective S93 freeze commit: 5ad31ab649e11f7c2147614105661548edf79ca7. Baseline main HEAD 8169d5016f24dc1accee2c4aeaffcb168b1504e9. Original Watkins and Dayan (1992), DOI https://doi.org/10.1007/BF00992698. Source: research/R297/R297_ALL_120_ORIGINAL_Q_LEARNING_Q_VECTOR_SOURCES.csv, pinned SHA256 da5f8af83a4ab28421732e0e6b365b6c9fd99f8de2c85de5270d3a0470cecbc6, 24 artificial deterministic MDP worlds times 5 epochs.

## Exact predeclared results

For each world and epoch, the learned action is evaluated against the original unrestricted continuation oracle: optimal reward max(1,3 gamma), learned action reward 1 for SAFE or 3 gamma for EXPLORE. Exact Fraction regret is their difference. For the fixed BAD backup, this counterfactual assumes the optimal downstream action can be used; its regret is not the loss of the BAD-only continuation policy under its own objective.

| Epoch | Incorrect of 24 | Exact summed regret |
| :---: | ---: | ---: |
| 0 | 16 | 20 |
| 1 | 13 | 31/2 |
| 2 | 13 | 31/2 |
| 3 | 12 | 15 |
| 4 | 12 | 15 |

Total summed regret across 120 artificial labeled states is 81, and across trained epochs 1..4 it is 61. These are unweighted artificial-grid totals, not an estimated population loss or empirical prediction accuracy. At final epoch 12 worlds agree and 12 disagree with the original unconstrained oracle, exactly matching R297 baseline.

Across six FULL plus OFF_POLICY_MAX worlds, final errors are zero, with cumulative regret 6. In three other coverage/backup cells of six worlds each, final errors are four per cell and cumulative regret 25 per cell. Across the eight gamma=0 worlds regret is zero. The eight gamma=1/2 worlds contribute 17; the eight gamma=1 worlds contribute 64.

At gamma=1/2, alpha=1/2, FULL and OFF_POLICY_MAX, the first sustained correct action occurs at epoch 3 after an exact tie at epoch 2, and total regret is 3/2. With alpha=1, sustained correct action begins at epoch 1 and total regret is 1/2. At gamma=1 both FULL+MAX alpha settings begin sustained correctness at epoch 1, with regret 2 from the initial untrained epoch.

## Execution, checks and boundaries

Original source bytes were independently regenerated in a sandbox from the published frozen deterministic recurrence, with SHA256 identical to the pinned original CSV; the GitHub original CSV was also read and its Git blob identified. The archived R script was executed locally with --test (9/9 PASS), --emit and --check (PASS). A separate B script used an analytic closed-form Q formula without importing R code, compared all 120 source rows and 24 summaries, and rejected 8/8 controlled mutations. Generated CSV and JSON Git blob identities were compared byte-for-byte with local outputs before the GitHub commit. This is an internal nonblind reproducibility check, not an external independent laboratory reproduction.

No fitted model, calibration, human holdout, or resampling inference is involved in this exact deterministic E1 grid. Incomplete GOOD coverage and a fixed BAD continuation are two different mechanisms, and the counterfactual oracle presupposes GOOD remains available. There is no claim of asymptotic convergence, empirical policy improvement, human E2 or historical E3. Original R297 scoped acceptance remains unchanged. S93 scientific status PARTIAL pending broader independent reproduction and native remote checkout execution. R073 and PESEN v0.1 remain FROZEN. No CI initiated; no free-runner billing guarantee obtained.

Archived artifacts: research/validation/r297_s93_finite_policy_regret_20261031.py, R297_S93_ALL_120_FINITE_POLICY_REGRET_ROWS.csv, R297_S93_EXACT_POLICY_REGRET_RESULTS.json. B counterpart in research/evidence_audit/. No original source, crosswalk, pending queue, or earlier result was modified.
