# Hogarth and Soyer (2015): uncertainty display and simulation boundary
Actual research date: 2026-11-23 Singapore. Theory candidate; no product validation.

## Primary evidence and reading range
Robin M. Hogarth and Emre Soyer, “Providing information for decision making: Contrasting description and simulation,” Journal of Applied Research in Memory and Cognition 4 (2015), 221–228. DOI 10.1016/j.jarmac.2014.01.005. Free institutional original: https://repositori-api.upf.edu/api/core/bitstreams/d8fdb583-1667-4280-93fe-6b68e808f503/content . Inspected abstract, introduction and opening of p.222, not full paper. Discusses description, simulation and hybrid communication of forecast uncertainty, and open questions. Methodological discussion, not direct product-effectiveness evidence.

Companion first-hand source: Hogarth and Soyer, “Experiencing Simulated Outcomes,” BSE Working Paper 470, September 2015, https://bse.eu/research/working-papers/experiencing-simulated-outcomes . Abstract inspected only. Two experiments concern probabilistic inference tasks and regression/investment interpretation; authors report improvement after sequential simulated experience. Full experiment and statistics not audited; transfer to real personal choices unproven.

## Candidate conversational rule
Give an initial short natural-language comparison with assumptions, outcomes and unknowns. If a credible probability distribution is available and distribution comprehension matters, offer optional frequencies or simulation with the original probabilities and time horizon visible. If probabilities are unknown, show explicitly hypothetical scenarios without assigning frequencies or invented likelihoods. Keep hard constraints and rare severe outcomes visible. Do not require the user to navigate charts before receiving useful advice.
Conditional question: “你想先看简短结论，还是看几种可能结果的图示？”

## Synthetic counterexample
Hypothetical option: 90% chance of +10 and 10% chance of -100. Expected outcome = -1. Under independent draws, ten simulations omit the adverse event with probability 0.9^10 = 34.8678%. A ten-outcome visualization can therefore misleadingly show only gains. These probabilities are stipulated assumptions, not real estimates. If the real probabilities are unknown, this simulation cannot establish them.

## Ten proposed acceptance cases, unexecuted
1. Verified distribution: show provenance, units, event definition and horizon.
2. Unknown probabilities: no numeric likelihood invented.
3. Small simulation omits rare loss: disclose complete assumed distribution.
4. Conflicting sources: preserve separate estimates.
5. Quick advice requested: concise answer without mandatory chart.
6. Detailed view requested: show scenario assumptions and allow concise mode.
7. Irreversible harm: preserve user hard constraints despite high mean.
8. Undefined event denominator: ask only if decision-critical.
9. User rejects graph: preserve user preference without diagnosis.
10. Deterministic comparison: prefer exact calculation over sampling.

## Competing explanations and limits
Comprehension differences might reflect visualization, repetition, numerical literacy, clearer event definitions or user self-selection. Stylized inference results cannot establish welfare gains or improved life decisions. Random samples are not causal evidence. Simulation must not manufacture confidence.

## Dedup, responsibility and status
Read latest main, formal v3.0 workflow, open PR and full repository tree (10,158 entries; 142 decision-method files). Adjacent prior research: Hertwig 2004 on description/experience and rare-event sampling; McNeil 1982 on framing; Hsee 1996 on presentation; C023/C026 on forecast scoring. This candidate concerns presentation-mode selection and misleading simulation graphics. Filename-level dedup complete, full semantic review incomplete.
Model track: optional presentation rules. Data track: distribution provenance and calibration. Independent acceptance track: held-out comprehension versus concise text baseline and rare-event omissions. Product track: minimal UI.
Archived research candidate only. No implementation, program test, numerical independent reproduction, real-user validation or scientific acceptance. No CI, paid API, sensitive data, PR merge or frozen-protocol changes.