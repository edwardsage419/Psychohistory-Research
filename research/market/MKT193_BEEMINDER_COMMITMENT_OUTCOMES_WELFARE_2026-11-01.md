# MKT193: Beeminder commitment contract, observable goal adherence and welfare evidence

Date: 2026-11-01 UTC
Track: market
Key: (market,Beeminder,official-help-2026-10,goal-adherence-versus-decision-welfare)
Baseline main: 08660ba004d8bb243a9a350c1cdf2e5fa8792ac9
Status: COMPLETE_DOCUMENTARY; PRODUCT_RUNTIME_NOT_RUN; REAL_USER_EFFECT_NOT_VERIFIED
Research mode: public English documentation and independent adjacent academic evidence. No account, card, subscription, API or paid service used.

## Product mechanism observed

Beeminder is a real monetary commitment and quantitative goal-tracking product. The user creates a goal, specifies a target trajectory (the Bright Red Line), and supplies timestamped values and optional comments. Data may be manually entered, emailed or obtained through authorized integrations. A deadline and safety buffer determine whether a goal has derailed. The application can notify users and reconfigure the trajectory after derailment. This is a trajectory adherence and contingent-penalty mechanism, not a disclosed personal-life causal forecasting model or a multiobjective welfare optimizer.

Confirmed product input: date, value, optional comment, goal type, rate/trajectory, deadline, pledge, cap and external source authorizations. Confirmed state/output: historical datapoints, goal graph, safety buffer, deadline risk, derailment notification, pledge escalation and user-initiated adjustment. Official help documents the relevant behavior; exact production implementation, model source, reliability, independent performance and any proprietary algorithms were not inspected.

A documented data integrity boundary is especially relevant: CSV/TSV export and API retrieval are supported, but the official webhook help warns that delivery can fail silently. The existence of a goal datapoint in a remote graph does not by itself establish a complete event history, external outcome truth, or synchronization completeness. The service lists third-party access grants and offers revocation; this does not establish on-device-only processing or deletion from third parties.

## Concrete commercial and safety constraints

The official help article last updated 2026-09-29 states three initial active goals, a required payment card, a possible $5 charge if no goal is created in the first week, a minimum post-trial derailment charge of $5, pledge caps and seven-day delayed pledge decreases. The official pledge ladder includes $0, $5, $10, $30, $90, $270, $810, $2430 and $7290. A derailment notice article updated 2026-10-27 describes a legitimacy-check email and charging after 24 hours, with possible correction of non-legitimate events; No-Excuses Mode changes that policy. These are contractual product rules, not measured causal effects.

Because this project requires absolute zero additional cost and forbids payment registration, the product must remain a documentary research target. No trial or account creation is authorized. Even a nominally free goal would create financial exposure and require a payment card.

## Independent evidence, with explicit transfer limit

Bhattacharya, Garber and Goldhaber-Fiebert, NBER working paper 21406 (2015), report a randomized trial involving more than 4,000 people seeking exercise commitments. Random nudges toward 20-week rather than 8-week contracts changed contract choices and increased attainment of stated exercise goals and subsequent contract uptake. The University of Chicago Becker Friedman Institute's 2017 account explicitly notes that welfare can decrease in some modeled circumstances despite higher goal attainment.

This is independent research about exercise commitment contracts, not an independent Beeminder experiment. It cannot establish Beeminder's effect size, lifetime net benefit, broad cross-domain transfer, or optimal pledge. A separate 2019 randomized field experiment on nonbinding academic commitments (Himmler, Jäckle, Weinschenk, AEJ Applied Economics DOI 10.1257/app.20170288) reports improvement in exam participation and passing relative to controls, while reminders alone did not change behavior. That experiment concerns a different, nonmonetary intervention and population.

## Scientific and design implications as candidates only

Measure (1) prespecified objective completion, (2) missing or disputed datapoint fraction, (3) independently verified outcomes, (4) time/effort and monetary loss, (5) self-reported autonomy and burden, and (6) post-commitment persistence separately. High adherence to a narrow goal can coexist with displacement of other valued goals or financial harm. A credible effectiveness study would predefine endpoints, enrollment and attrition, compare alternatives, account for selection into commitments, and retain adverse effects. No universal life utility weights are chosen.

For future research, prioritize a free, locally simulated, nonfinancial deviation-control benchmark and independently measured net outcomes before considering any monetary mechanism. This is knowledge preparation only; personal decision product development remains deferred.

## Evidence and limits

MARKET-E1: Direct official product help, pricing, data export, API and authorization documentation.
MARKET-E2-ADJACENT: Peer-reviewed/working-paper human randomized evidence for related commitment interventions. Transfer to Beeminder NOT_ESTABLISHED.
MARKET-E3-BEEMINDER: NOT_FOUND in this bounded search. No product-user randomized outcomes, retention-adjusted effect or welfare evaluation independently verified.
R scientific E1/E2/E3: N/A. No R protocol, PESEN v0.1 or R073 changed.
Runtime test: NOT_RUN. Simulations: NOT_RUN. Purchases: NONE. GitHub Actions: NOT_RUN. Account billing: NOT_VERIFIED.

## English sources read 2026-11-01

1. https://help.beeminder.com/article/19-how-much-does-beeminder-cost (last updated 2026-09-29)
2. https://help.beeminder.com/article/17-what-happens-when-i-derail (last updated 2026-10-27)
3. https://help.beeminder.com/article/20-how-much-do-i-pledge-on-my-goals
4. https://help.beeminder.com/article/37-how-do-i-enter-data-to-my-goal
5. https://help.beeminder.com/article/41-can-i-export-my-data (last updated 2026-09-24)
6. https://help.beeminder.com/article/110-apps-and-api (last updated 2026-07-10)
7. https://www.nber.org/papers/w21406 (2015 abstract)
8. https://bfi.uchicago.edu/working-paper/nudges-in-exercise-commitment-contracts-a-randomized-trial/ (2017 author summary)
9. https://pubs.aeaweb.org/doi/10.1257/app.20170288 (2019 independent field experiment)

Next high-value market task: find a product-specific independently collected effectiveness or failure dataset for Beeminder or an open-source nonfinancial deviation-control product. Avoid repeating authentication and witness subtopics without concrete product need.
