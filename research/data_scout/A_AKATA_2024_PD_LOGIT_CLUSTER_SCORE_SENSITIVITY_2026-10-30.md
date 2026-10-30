# A track Akata 2024 PD published-score label and cluster-logit sensitivity
Date UTC: 2026-10-30. Target: (A,Akata2024,author-Rmd-ca9991b6+CSV-2dd67c6,PD-score5-score8-GLM-cluster-robust-and-one-anomaly). Status: COMPLETE_DESCRIPTIVE_ANALYTIC_REPLAY / PAPER_CONCLUSION_PARTIAL. NONBLIND follow-up to existing A reports, no raw participant records republished.

Read the full 3900-row original public CSV, 1950 PD rows, blob 2dd67c6ff80f2d7aa07a70b470e26fe3592c6d95, https://github.com/eliaka/repeatedgames/blob/main/human_experiment/analysis/repgames.csv . Read the author Rmd, blob ca9991b6d0917156672e1e2fea923548562d945e, https://github.com/eliaka/repeatedgames/blob/main/human_experiment/analysis/repeated_games.Rmd . Rmd PD chunk defines score==5 as 'cooperated', fits glm(cooperated~opponent, family='binomial') on all PD rows, then displays an explicitly hard-coded BF=6.5 annotation in the figure. The code shown in that chunk does not calculate BF=6.5. The original payoff script previously verified J/J=8 mutual cooperation and F/F=5 mutual defection.

Reconstruct the two-group binomial GLM coefficient exactly as logit(p_Prompted)-logit(p_Base). Compute standard row-level GLM SE and a participant-cluster sandwich SE using per-person scores, treating the 97 Base and 98 Prompted people as independent clusters. The latter uses G/(G-1) within each group, without claiming experimental randomization or exact original R package execution.

| Outcome | Base positives/N | Prompted positives/N | log odds contrast | OR | naive SE | participant-cluster SE | descriptive cluster 95% OR interval |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- |
| score=5 (mutual defection) | 362/970 | 421/980 | 0.235014 | 1.264927 | 0.092582 | 0.194253 | [0.864398, 1.851044] |
| score=8 (mutual cooperation) | 362/970 | 356/980 | -0.042689 | 0.958209 | 0.093908 | 0.265924 | [0.568985, 1.613688] |

One anomalous PD row (anonymous id153, Base, action=0, score=0) violates the deterministic payoff mapping; ordinary score=0 with action=1 is valid and must remain. Excluding only the anomalous row yields score5 OR 1.262846 and score8 OR 0.956633. The direction reversal and wide cluster intervals persist. No statistical significance or causal effect inferred. The author Rmd complete pipeline, published paper figure and reported Bayes factor have NOT been natively reproduced.

The root LICENSE.md blob 108cffb7c9fcd38dadc419f4c18e4e3e0afb4407 is MIT and describes 'Software and associated documentation'; independent participant-level data redistribution permission remains UNKNOWN. No raw data copied. This human versus LLM ten-round experiment is ineligible for the frozen R073 100-round human-human protocol. Prior project R074/R075/R077 already contain separate original human experiments; do not describe R073 as lacking all second-source evidence. New E2 out-of-sample prediction=0, E3=0.

Reproducible analytic source: research/data_scout/a_akata_pd_logit_cluster_gate_20261030.js . Next: exact author Rmd environment and figure/BF trace, separate subject-level randomization and data license audit.