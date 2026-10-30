# A track: Akata 2024 PD outcome label and opponent group contrast
Date UTC: 2026-10-30. Status: PARTIAL exploratory descriptive source audit.
Target: (A,Akata2024,author-Rmd-ca9991b6+CSV-2dd67c6,PD-cooperation-label-group-direction)
Prior read: earlier A_AKATA_2024_PD_SCORE5_MUTUAL_DEFECTION_OUTCOME_AUDIT, so this is a **nonblind complementary downstream group contrast**.

## Pinned original evidence
Author GitHub: https://github.com/eliaka/repeatedgames
Public CSV: https://github.com/eliaka/repeatedgames/blob/main/human_experiment/analysis/repgames.csv (Git blob 2dd67c6ff80f2d7aa07a70b470e26fe3592c6d95).
Author Rmd: https://github.com/eliaka/repeatedgames/blob/main/human_experiment/analysis/repeated_games.Rmd (Git blob ca9991b6d0917156672e1e2fea923548562d945e).
Previously checked experiment payoff script Git blob 4b7be85e8b3b964bfd0722d796f5ed6c2b8f0a19. J/J yields score 8, F/F yields score 5.
Rmd line 299 sets `cooperated=ifelse(score==5,1,0)`, then line 301 uses `glm(cooperated~opponent, family='binomial')`, and the figure uses "Joint cooperation".

## Actual full CSV read and group count
3900 public rows; 1950 PD rows; 195 PD participants with 10 PD rounds each. Opponent conditions have separate participants.
| condition | participants | PD rows | Rmd score==5 (F/F) | actual score==8 (J/J) |
| --- | ---: | ---: | ---: | ---: |
| Base | 97 | 970 | 362 (37.320%) | 362 (37.320%) |
| Prompted | 98 | 980 | 421 (42.959%) | 356 (36.327%) |

Using original score==5, pooled round-level Prompted minus Base = 5.640 percentage points. Using score==8, Prompted minus Base = -0.993 percentage points. The **descriptive contrast changes sign**.
For a two-condition pooled logistic intercept + group contrast, corresponding raw odds ratios are 1.264927 (score5) and 0.958209 (score8). These are algebraic group odds ratios, **not** independently executed original R `glm` estimates and contain no cluster-robust uncertainty.
One PD row has action=0 and score=0, inconsistent with the displayed deterministic PD payoff matrix; retained. Data redistribution license was not established; raw CSV is not copied into this repository.

## Boundaries
The Rmd's label is inconsistent with the experiment's payoff table. Group contrast reversal is a directly reproducible descriptive result. Author's full R Markdown pipeline, published paper tables, random effects, participant-cluster uncertainty and statistical significance remain NOT_RUN. No causal effect of prompting is claimed. This human versus LLM ten-round design does not satisfy frozen R073 independent human-human 100-round replication. New E2 out-of-sample predictions=0, E3=0. Next: inspect publication outputs, independently run the exact original regression if dependencies are free and available, preserve anomaly and participant clustering.
