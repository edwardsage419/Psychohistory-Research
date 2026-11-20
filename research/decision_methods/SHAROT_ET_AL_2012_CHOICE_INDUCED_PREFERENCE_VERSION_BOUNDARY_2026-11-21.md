# Sharot et al. (2012): choice-induced preference and versioned review
Actual research date: 2026-11-21. Theory track. Primary-text review completed; independent replication not run.

## Source and scope
Sharot, T., Fleming, S. M., Yu, X., Koster, R., & Dolan, R. J. (2012). Is Choice-Induced Preference Change Long Lasting? Psychological Science 23(10), 1123–1129. DOI 10.1177/0956797612438733.
Free original PDF https://pure.mpg.de/pubman/item/item_2614279_4/component/file_2618847/RD_Is_choice_2012.pdf
Read methods, results and discussion, pp. 1123–1128. This is distinct from earlier outcome-bias and omission-bias entries: it concerns changing *reported preferences* following a choice, rather than judging a decision from its result.

## Published evidence
Initial analytic sample 39 (19 self-choice, 20 computer-choice); only 18 returned after 2.5–3 years (9 per arm). Participants rated hypothetical vacation destinations. For difficult choices between initially equally rated options, selected destinations were rated more favorably after self-choice, immediately and years later. Paper reports task × difficulty × selection interaction F(2,55)=6.33, p<.005, and delayed self-choice interaction F(1,8)=21.1, p<.002. These are author-reported figures, not independently recalculated.

## Assumptions, alternatives and limits
Comparison uses hypothetical travel preferences, not actual long-term life outcomes. Attrition and small follow-up sample constrain inference. The paper considers noisy initial ratings and preexisting preferences, using computer-choice and later free-choice controls. Other plausible accounts include cognitive dissonance, attribute reweighting during comparison, self-perception and memory. Authors note experience of the chosen option may alter preference stability. No claim about an individual user's probability of change or a tool's efficacy is supported.

## Executable question and interpretation
At review ask: “Has your evaluation of each option or the importance of your criteria changed since deciding? What new experience or information explains it, if any?”
Keep timestamped pre-decision ratings and weights immutable; save current ratings, new evidence, realized outcomes and user-confirmed weight revisions separately. A new preference is a present report; it does not retroactively validate the earlier choice or change the original forecast. User controls whether it becomes the weight for future decisions.

## Synthetic acceptance counterexamples, NOT TESTED
1. A and B originally score 7; after selecting A, A is rated 9. Original 7 must remain reproducible.
2. Increased satisfaction rating with no observed outcome must not be presented as increased realized return or improved probability calibration.
3. A weight changes from 30% to 50%. Old comparisons retain 30%; future use of 50% requires confirmation.
4. A computer selects A. Do not automatically attribute later ratings to the self-choice mechanism.
5. A single individual's rating change cannot become a population transition probability.

## Status and handoff
Research source review and candidate acceptance cases COMPLETE. Statistical reproduction, program tests, independent validation, personal effectiveness and scientific acceptance NOT RUN. Acceptance track owns snapshot and retrospective-overwrite tests; model track owns potential implementation; data track owns sampling, timing and attrition qualification. No CI, paid API, personal data, or frozen-protocol changes. R073 and PESEN v0.1 unchanged.
