# A track: Akata 2024 PD participant-cluster uncertainty and label scope
Date UTC: 2026-10-30. Status: COMPLETE descriptive aggregate calculation; published-paper causal/replication gate PARTIAL. Target key: (A,Akata2024,author-Rmd-ca9991b6+CSV-2dd67c6,PD-score-label-participant-level-uncertainty). NONBLIND follow-up after earlier source and sign-reversal reports.

## Sources actually read
Original public CSV https://github.com/eliaka/repeatedgames/blob/main/human_experiment/analysis/repgames.csv ; Git blob `2dd67c6ff80f2d7aa07a70b470e26fe3592c6d95`; 3900 rows, of which 1950 PD rows, 195 distinct participants, 10 PD rounds each. Original author analysis https://github.com/eliaka/repeatedgames/blob/main/human_experiment/analysis/repeated_games.Rmd ; blob `ca9991b6d0917156672e1e2fea923548562d945e`. In its PD behavior section, `cooperated <- ifelse(score==5,1,0)`, followed by a row-level `glm(cooperated~opponent,family='binomial')` and plot labeled `P(Cooperation)` with a fixed `BF=6.5` annotation. Previously read original game payoff script establishes score=5 as mutual defection, score=8 as mutual cooperation. Source data license for participant-level redistribution remains UNKNOWN; no raw participant data copied.

## New actual aggregate calculation
Read all 3900 CSV rows and grouped all PD records by participant ID and opponent condition, then computed each participant's fraction of 10 PD rounds with score=5 and with score=8. Compare independent participant means between Base (97 people) and Prompted (98 people). Standard error is sqrt(s_Base^2/97+s_Prompted^2/98) using unbiased between-participant variances, with descriptive normal 1.96 SE intervals. This is an exploratory participant-level uncertainty calculation, not the author's exact R glm, mixed-effects fit, randomization-based causal inference, or formal published Bayes factor reproduction.

| Metric | Base participant mean | Prompted participant mean | Prompted minus Base | Participant-level SE | Descriptive normal 95% interval |
| --- | ---: | ---: | ---: | ---: | ---: |
| score=5, mutual defection mislabeled cooperation in Rmd | 0.373196 | 0.429592 | +0.056396 | 0.046562 | [-0.034866, 0.147658] |
| score=8, mutual cooperation per payoff table | 0.373196 | 0.363265 | -0.009931 | 0.061851 | [-0.131159, 0.111298] |

Between-participant sample variances: score5 Base 0.097399055, Prompted 0.114063749; score8 Base 0.183857388, Prompted 0.189152114. Each participant contributes exactly ten PD rounds. The two intervals include zero. The previously observed descriptive sign reversal survives participant-level aggregation because group sizes per participant are equal, while uncertainty is much wider than a naive independent-round calculation would imply. This cannot establish a statistically reliable direction of the effect. The original plot's fixed BF annotation has NOT been recomputed, and its scientific scope is unresolved.

## Gates and next
No independent 100-round human-human repeated PD experiment suitable for frozen R073 found here; this is ten-round human-LLM interaction. Real participant observations were read for measurement auditing only; new E2 out-of-sample prediction=0, E3 historical prediction=0. The raw participant file is not redistributed. Re-run the author's exact Rmd in a zero-cost local environment if dependencies are available, and compare participant-clustered models and the published figure before claims about paper conclusions. R073/PESEN v0.1 remain frozen. No paid service or CI used.
