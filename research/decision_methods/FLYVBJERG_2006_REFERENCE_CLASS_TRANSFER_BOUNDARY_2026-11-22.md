# Reference class forecasting: historical infrastructure evidence and personal decision transfer boundary

Completed: 2026-11-22. Track: personal decision theory. Status: research candidate, not validated product behavior.

## Decision gap
Users may forecast time, cost or success of career changes, relocation or long projects using an internally constructed plan. A comparable historical distribution can challenge that forecast, but an inappropriate reference class can be more misleading than admitting uncertainty. This note is distinct from the Wiese, Buehler and Griffin (2016) backward-planning note: its focus is the eligibility and transfer limits of historical comparison groups, not planning direction.

## First-hand source and actual reading range
Bent Flyvbjerg (2006), *From Nobel Prize to Project Management: Getting Risks Right*, Project Management Journal 37(3), 5–15, DOI 10.1177/875697280603700302. Reviewed publisher abstract and Project Management Institute's author-associated article abstract, not full empirical tables or raw observations:
https://journals.sagepub.com/doi/abs/10.1177/875697280603700302
https://www.pmi.org/learning/library/nobel-prize-project-management-risks-2545

The author argues that project cost and demand forecasts are frequently inaccurate and presents reference class forecasting using actual outcomes of comparable completed projects. The paper discusses large transport infrastructure and the Edinburgh tram planning example. The paper also distinguishes optimism bias from strategic misrepresentation. These are author claims in the reviewed text; their numerical magnitude and generality were not independently audited.

Related original conceptual source: Kahneman and Lovallo (1993), *Timid Choices and Bold Forecasts*, Management Science 39(1), 17–31, DOI 10.1287/mnsc.39.1.17. Reviewed bibliographic abstract only. It describes internal plan-based forecasts and neglect of historical statistics.

## Candidate rule for a minimal Chinese conversational interface
Provide a preliminary analysis immediately. If forecast uncertainty materially affects a choice, ask at most one optional question:
“有没有与你这件事真正相似、已经完成的案例？如果没有，我会把时间和成本估计标成未知。”
A historical comparison is admissible only if outcome definition, start and end point, relevant context, observation window, selection process, and missing cases are inspectable. Keep the user's own forecast separately. If the comparison is weak, present a scenario range explicitly labeled hypothetical rather than numerical empirical odds. No automatic correction of the user's values or hard constraints.

## Observable acceptance fields
Decision-time user forecast; reference class definition; denominator and completed/failed/censored cases; comparable outcome metric; calendar vintage; data provenance; reason for inclusion/exclusion; empirical distribution when actually supported; user approval of any preference revision.

## Six synthetic failure cases (design only)
1. A user asks about a career change; only megaproject construction data exist. Reject direct probability transfer.
2. Ten successful online testimonials omit unsuccessful attempts. Mark selection bias and unknown denominator.
3. Project costs are measured in nominal currencies across decades. Do not pool without defensible adjustment.
4. A completed project distribution excludes ongoing delayed projects. Flag censoring and possible optimistic bias.
5. A user supplies a non-negotiable deadline. A favorable historical median must not override feasibility or safety constraints.
6. The system finds no comparable sample. Keep outcome probability UNKNOWN and still offer qualitative scenario analysis without inventing quantiles.

## Competing explanations and limits
Project outcomes can differ due to regulatory changes, financing, scale, technology, selection, incentive-driven strategic reporting, and changes in the reference population. Reference class forecasting may improve calibration in suitable project settings, but evidence reviewed here does not establish efficacy for individual career, relationship or health decisions. Historical data do not identify individual counterfactual outcomes. Do not treat descriptive frequencies as personal causal probabilities.

## Handoff and evidence ledger
Theory: scoped source review COMPLETE. Candidate question and six synthetic cases COMPLETE. Original tables and source dataset audit NOT EXECUTED. Program tests NOT EXECUTED. Numerical replication NOT EXECUTED. Independent validation NOT EXECUTED. Scientific acceptance NOT EXECUTED.
Model track: assess optional question and no-data fallback. Data track: assess class comparability, denominator and censoring. Independent acceptance track: hold out the six cases and compare with a no-question baseline. No implementation authorization, no CI, no change to R073, PESEN v0.1 or frozen protocols. Cost: zero additional.
