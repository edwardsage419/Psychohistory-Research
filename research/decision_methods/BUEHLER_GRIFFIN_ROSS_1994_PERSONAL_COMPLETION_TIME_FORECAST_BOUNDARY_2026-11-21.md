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
