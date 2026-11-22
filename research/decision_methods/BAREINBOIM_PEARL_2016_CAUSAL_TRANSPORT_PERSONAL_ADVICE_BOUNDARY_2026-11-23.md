# Causal transportability of external advice to an individual: theory candidate

Date completed: 2026-11-23 (Asia/Singapore)
Track: personal decision theory. Status: candidate, not scientifically accepted.
Capability gap: deciding whether published effects from a different population justify a numerical personal recommendation.

## Primary source and actual scope read
Elias Bareinboim and Judea Pearl (2016), "Causal inference and the data-fusion problem", PNAS 113(27), 7345–7352, DOI 10.1073/pnas.1510507113. Read publicly available author paper text, specifically introduction and Fig. 1, pp. 7345–7346, and "Transportability and the Problem of Data Fusion", Fig. 5 and equations (15)–(17), pp. 7350–7351. URL: https://pubmed.ncbi.nlm.nih.gov/27382148/ ; freely accessible PDF https://bpb-us-w2.wpmucdn.com/u.osu.edu/dist/7/36891/files/2021/01/BareinboomPearl2016Causal-inference-and-the-data-fusion-problem-7345.full_.pdf-copy.pdf

The authors distinguish observational, intervention, sampling-selection and cross-population questions. In Fig. 5A, where only the distribution of pretreatment Z differs between source and target, equation (15) identifies the target intervention outcome as sum_z P_source(y | do(x), z) P_target(z), conditional on the selection diagram assumptions. Fig. 5D supplies a case in which the target effect is not transportable from the available information. Eq. (17) demonstrates that posttreatment variables require a different formula; naive reweighting is invalid.

## Proposed conversational rule
When citing an external study as support for an individual's choice, present its observed study population and intervention, and label the transfer to the user's situation as conditional. If population differences could reverse the recommendation, ask one targeted question: "研究对象和你最可能不同、又会影响结果的条件是什么？" If the differences or causal structure are unknown, avoid claiming a personalized causal effect. Retain a useful conditional scenario analysis.

## Synthetic illustration (not empirical estimates)
Assume an intervention improves success by +0.20 for subgroup Z=1 and decreases success by -0.10 for Z=0. In source population P(Z=1)=0.8, average effect = 0.8*0.20 + 0.2*(-0.10) = +0.14. In target population P*(Z=1)=0.2, transported effect = 0.2*0.20 + 0.8*(-0.10) = -0.04. This sign reversal holds only if subgroup-specific intervention effects are stable and Z captures all relevant cross-population effect modification. No personal effect is identified from this example.

## Competing explanations and limitations
Observed source-target discrepancies may reflect baseline risk, effect modification, selection into studies, confounding, measurement differences, treatment implementation, or sampling noise. Merely reweighting observed covariates does not repair an unknown causal mechanism or hidden effect modifiers. Transporting a population average does not identify an individual's potential outcomes. The source provides theoretical identification conditions; it does not validate this conversation rule or demonstrate personal decision benefit.

## Candidate acceptance cases (theory handoff only)
1. Identical populations and valid randomized source: allow a labeled population effect, no individualized certainty.
2. Known pretreatment modifier with different prevalence and valid selection diagram: calculate Eq. 15 and show assumptions.
3. Synthetic sign reversal (+0.14 source versus -0.04 target): prohibit unqualified source recommendation.
4. Modifier distribution unknown: show conditional ranges, no invented target weights.
5. Posttreatment Z: prohibit blindly using Eq. 15; require graph-specific derivation.
6. Hidden target-specific outcome mechanism (Fig. 5D): mark transport blocked.
7. Observational association only: distinguish association from intervention effect.
8. User declines to provide target modifiers: give conditional explanation without pressure or false precision.
9. Source measures surrogate outcome rather than target value: prohibit conflation.
10. Single individual versus population average: mark individual counterfactual unobserved.

## Dedup and handoff
Repository decision_methods directory checked at 2026-11-23, HEAD 8a575972dc7791f4e099791a68f5438e22e631da. Existing C014 covers within-study causal positivity and censoring, C028 covers unobserved alternatives, and Flyvbjerg covers reference class forecasting. This note isolates causal effect transport across populations; full semantic repository dedup remains pending.

Model track: evaluate eligibility gate for using externally estimated effects. Data track: source/target population, modifier measurement, design and licensing qualification. Independent acceptance track: held-out sign reversal and Fig. 5D nontransportability, compare to a naive external-average baseline.

Evidence status: primary source equations reviewed; synthetic arithmetic specified; no software implementation, independent execution, real-world validation or scientific acceptance. No personal data, paid API or CI. R073, PESEN v0.1 and all frozen records untouched.
