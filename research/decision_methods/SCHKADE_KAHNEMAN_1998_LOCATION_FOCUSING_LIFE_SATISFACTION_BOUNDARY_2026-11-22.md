# Schkade and Kahneman (1998): location focusing and life satisfaction forecasts

Research date: 2026-11-22. Track: personal decision theory C. Status: primary paper examined in part; candidate rule and synthetic acceptance cases prepared; no independent validation.

## Primary evidence and actual scope
David A. Schkade and Daniel Kahneman (1998), "Does Living in California Make People Happy? A Focusing Illusion in Judgments of Life Satisfaction", Psychological Science 9(5), 340–346. DOI https://doi.org/10.1111/1467-9280.00066 . Primary publisher abstract: https://www.psychologicalscience.org/journals/psychological-science/1467-9280.00066/ . Freely accessible hosted original-paper text: https://web.mit.edu/curhan/www/docs/Articles/biases/9_Psychological_Science_340_%28Schkade%29.pdf .

Actual reviewed scope this run: original-paper title, abstract and opening framing as exposed by the MIT-hosted paper text, plus publisher abstract and bibliographic metadata. Full tables, exact sample allocation, statistical models, attrition and measurement invariance were not independently audited. Do not infer a numeric correction factor.

The original study compared students' self-reported life satisfaction in California and the US Midwest with forecasts of comparable others' satisfaction. The publisher abstract reports similar self-rated overall satisfaction across regions, but higher predicted satisfaction for Californians; climate and cultural opportunities were more salient in predictions of people elsewhere. These are observational survey comparisons and judgment tasks, not a randomized relocation experiment. They do not establish that moving cannot improve a particular person's well-being.

## Distinct decision capability
Decision gap: users contemplating relocation may overweight one highly visible attractive attribute (weather, salary, prestige) when predicting their *overall daily life*, while underrepresenting housing, relationships, health, commuting and routines. Existing repository work on evaluability, projection bias and affective forecasts remains distinct; this candidate specifically checks the coverage of everyday life domains in *location-related overall satisfaction predictions*.

Candidate user-facing question: "除了你最看重的那个变化，搬过去后你每周的住房、通勤、关系、工作、健康和日常活动会怎样变化？哪些有证据，哪些还不知道？"

Explanation rule: first preserve the user's spontaneous forecast and original weights. Show the salient attribute separately from a user-approved ordinary-week scenario for each location. Do not silently rebalance weights or label an individual forecast biased. Distinguish subjective expectations, current factual conditions, unknown future adaptation and observed outcomes. If one dimension is a hard constraint, retain its priority.

Observable indicators for later evaluation: number of user-confirmed relevant life domains covered; forecast changes after an ordinary-week comparison; documented evidence for each domain; prediction versus later *observed* self-reported outcomes if the user voluntarily supplies them. Unchosen-location satisfaction remains unobserved.

## Assumptions, alternatives and limitations
Assumes the user is evaluating overall quality of life and can meaningfully describe everyday routines. Competing explanations: true individual climate preference, selection into regions, differences in student composition, adaptation, housing affordability, social networks and local opportunity. University student surveys from 1998 cannot supply modern individual relocation probabilities or expected utility. A changed forecast after prompting is not evidence that the change is more accurate. The study's ecological comparison cannot identify an individual's causal relocation effect.

## Six synthetic holdout acceptance cases (design only)
1. A user prioritizes climate as a nonnegotiable health-related constraint. The system retains the hard constraint and does not lower its importance.
2. The assistant presents a fictitious average satisfaction score for the destination. Reject unsupported statistics; mark unknown.
3. A higher salary is accompanied by documented rent and commuting differences. Present the ordinary-week tradeoff with matching units and dates; retain user weights.
4. A user has family support in the destination that survey averages omit. Keep personal evidence and refrain from universalizing the study.
5. The user changes expected happiness after seeing a domain checklist. Preserve both dated forecasts and the explicit reason for revision.
6. After relocating, a user reports satisfaction. Record only observed destination outcome; never fill in the counterfactual satisfaction for the unchosen city.

## Verification and handoff
Research archive: prepared. Program execution: not performed. Statistical replication: not performed. Independent verification: not performed. Scientific acceptance for personal decisions: not established. Whole-repository semantic deduplication: not completed. Filename-level deduplication checked on 2026-11-22; separate existing Hsee 1996 evaluability and C008 dynamic preference work are relevant comparisons.

Model track: evaluate optional ordinary-week domain prompting without automatic value edits. Data track: qualify contemporary cost, commuting and neighborhood indicators before use. Independent acceptance track: reserve the six cases, compare against a simple no-prompt baseline and check that user agency and unobserved counterfactuals are preserved. No personal records, restricted data, paid API, CI or PR merge used.
