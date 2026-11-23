# Buehler, Griffin & Ross (1994): personal completion-time forecast and deadline boundary
Date actually researched: 2026-11-21 (Asia/Singapore). Track: personal decision theory. Status: candidate rule, not validated product feature.

## Source and actual reading scope
Roger Buehler, Dale Griffin, Michael Ross (1994). *Exploring the “Planning Fallacy”: Why People Underestimate Their Task Completion Times*. Journal of Personality and Social Psychology 67(3), 366–381. DOI 10.1037/0022-3514.67.3.366.
Free institutional-hosted original journal PDF: https://web.mit.edu/curhan/www/docs/Articles/biases/67_J_Personality_and_Social_Psychology_366%2C_1994.pdf
Actually examined: original journal PDF text, opening theory and Studies 1–2 methods/results (printed pp. 366–371), plus opening abstract describing Studies 3–5. No independent inspection or recalculation of all Studies 3–5 statistics. PDF is reading reference only, not redistributed.

## Verified findings and numerical scope
Study 1 enrolled 37 thesis students. Table 1 uses 33 completed cases: mean best estimate 33.9 days, mean observed completion 55.5 days, 29.7% completed by best-estimate date. Four unfinished at record closure were excluded. Mean pessimistic prediction 48.6 days; only 48.7% completed by that date. Mean absolute errors: best 22.6 days, pessimistic 23.2 days. Thus simply requesting a pessimistic date did not improve absolute error in this sample.
Study 2 enrolled 104, followed 101. For completed academic projects n=91: mean predicted 5.8 days, observed 10.7; for completed nonacademic projects n=62: predicted 5.0, observed 9.2. These completed-project analyses do not describe the unfinished tail. Among 62 academic projects with external deadlines, 80.6% met the external deadline while only 38.7% met their own earlier prediction. Original paper: pp. 369–371, Tables 1–2 and accompanying text.
Abstract reports five studies and an intervention in Study 4; full inferential assessment of those later studies remains outstanding.

## Distinct decision gap and operational rule
Gap: a personal decision's time feasibility may be overstated even when its subjective benefit score is sound. This differs from the existing Flyvbjerg 2006 note on transferability of external reference classes and from deferral-option research.
Candidate question: “你预计何时完成？有无不可错过的截止日期？此前三个可比任务分别预计多久、实际多久？哪些尚未完成？如果延期，哪个方案会失效？”
Candidate interpretation: preserve original forecast, external deadline, completion observation and censoring separately. Show personal past completion distribution only if tasks are comparable and unfinished cases are represented. Never turn the observed sample mean ratio into a universal individual correction factor. Distinguish user's desired date from predicted completion date and contractual deadline.

## Synthetic acceptance cases (not observed user data)
1. Deadline 30 Nov; user predicts completion 28 Nov; later completion 3 Dec. System must record forecast miss and deadline miss separately.
2. Five past tasks, two remain unfinished. System must not calculate average duration from the three completed cases and label it the complete historical average.
3. User gives 10 days as optimistic and 20 days as pessimistic. System must not label the latter a calibrated 95% upper bound without coverage evidence.
4. A decision option has a fixed expiry on 1 Dec; forecast completion is 5 Dec. System must flag feasibility conflict, not rank solely by utility.
5. User changes prediction after seeing historical data. Original dated forecast must remain available for subsequent scoring.

## Assumptions, alternatives and limits
Comparability of tasks, observation windows and deadline meaning must be checked. Competing explanations include strategic underreporting, task heterogeneity, incentives, deadlines changing behavior, selection/censoring and recall errors. Study 1 recorded objective submission dates; Study 2 relied on self-reports. Samples were university students and cannot establish a universal correction for career changes, relocation or long-term personal projects. The original evidence supports a candidate clarification and evaluation rule; personal-system effectiveness remains unknown.

## Responsibility and verification
Theory track: source-scope reading, candidate rule and synthetic counterexamples COMPLETE. Original participant-level replication, software tests, independent scientific validation NOT RUN. Cross-repository semantic dedup PARTIAL. Model track: assess forecast/deadline display and versioned forecast input. Data track: verify completion censoring, timestamps and comparable cases. Independent acceptance track: test five synthetic cases with separate held-out scenarios. No CI, paid API, sensitive records, PR merge, R073/PESEN protocol change.

## 2026-11-24 original-paper extension: Studies 4 and 5, directional bias versus accuracy

Actual source inspected: MIT-hosted original journal PDF, printed pp. 374–380, Study 4 Table 4, Study 5 Table 5 and discussion, https://web.mit.edu/curhan/www/docs/Articles/biases/67_J_Personality_and_Social_Psychology_366%2C_1994.pdf . This extends the earlier pp. 366–371 inspection. No participant-level data or independent inferential-statistic replication.

Study 4 distinguished control, recall-only and recall-plus-relevance conditions. Table 4 reports predicted/actual days respectively 5.5/6.8, 5.3/6.3 and 7.0/7.0 (printed table's signed differences -1.3, -1.0, -0.1 after rounding). Absolute errors were 1.8, 2.0 and 1.9 days. Proportions completing by the predicted date were 29.3%, 38.1% and 60.0%. The authors explicitly state that reducing optimistic directional bias did not improve absolute prediction accuracy or correlation. Merely recalling past tasks and actively connecting past obstacles to the current task were different interventions. The causal mechanism of the latter remains uncertain: an alternative future scenario or simple conservative adjustment could explain its effect.

Study 5 used 123 observers to forecast Study 4 actors' tasks. Table 5 reports actor predicted/actual 5.5/6.8 days, with actor mean absolute error 1.8 days; observers' predicted days were 8.0, 8.8 and 8.7 for thoughts, memories and combined information, while actual duration was 6.8 days in each comparison. Observer mean absolute errors were 2.8, 2.7 and 2.6 days. The more conservative observer estimates were not more accurate. This also cautions against automatically replacing the user's estimate with an outsider or reference-class estimate.

**Distinct candidate acceptance boundary:** evaluate separately (a) signed prediction error and optimistic-bias direction, (b) absolute error, (c) on-time coverage relative to the user's original best estimate, and (d) asymmetric costs of early versus late completion. A lower signed group mean error cannot alone pass accuracy acceptance. Before prompting for past cases, check comparability, deadlines and whether the goal is deadline protection or unbiased point forecasting. No universal numeric correction is authorized.

Synthetic holdouts for independent acceptance, NOT_RUN: (1) three groups have signed errors -1.3, -1.0, -0.1 but absolute errors 1.8, 2.0, 1.9; reject a claim that the last group has best absolute accuracy; (2) observer prediction 8.8 versus actor 5.5 with actual 6.8; reject automatic observer superiority; (3) an early-finish penalty exceeds a late-finish penalty; do not optimize only for conservative coverage; (4) recall-only and recall-plus-relevance are labeled separately; (5) unfinished tasks remain right-censored. No implementation, tests, independent replication, or real-user outcome validation performed. Theoretical increment is an extension of this existing method record, new independent method count zero. Data track owns comparability and censoring; acceptance track owns separate scoring and held-out evaluation; model track owns implementation if separately authorized.
