# Gibson (2000): delayed feedback and attribution in personal decision reviews

Actual review date: 2026-11-23 (Asia/Singapore). Track: decision theory only. Status: candidate, not product validation.

## Question and source
How should a personal decision assistant interpret outcomes that arrive long after an action, when intervening actions and environmental changes may affect them?

Faison P. Gibson (2000), “Feedback Delays: How Can Decision Makers Learn Not to Buy a New Car Every Time the Garage Is Empty?”, Organizational Behavior and Human Decision Processes 83(1), 141–166. DOI: 10.1006/obhd.2000.2906. PMID: 10973786. Public primary abstract reviewed at https://pubmed.ncbi.nlm.nih.gov/10973786/ ; bibliographic cross-check https://ideas.repec.org/a/eee/jobhdp/v83y2000i1p141-166.html . Full article pages and computational model equations NOT inspected. The published abstract reports human-subject comparisons with two computational models: a no-memory model treating feedback as immediate and a with-memory model representing task history. In the examined dynamic tasks, delayed feedback impaired learning, and history display helped; these are study-specific findings, not validated effect sizes for personal life decisions.

## Proposed minimal interaction
When reviewing an earlier decision, offer an initial account distinguishing recorded actions, observed outcomes, and unknown effects. Ask only if attribution could change the conclusion: “这个结果是什么时候出现的？期间有没有其他重要行动或环境变化？”

Proposed rule: Store or display decision time, action time, expected outcome horizon, observation time, intermediate actions, outcome status, and unknown counterfactual separately. If an outcome arrives before the expected observation horizon, mark it provisional. If later actions overlap the outcome window, mark attribution uncertain. Do not treat missing outcome as failure or assign a delayed outcome automatically to the most recent action. Do not infer the unchosen option’s result.

## Competing explanations and limits
A delay may be an expected causal lag, measurement/reporting delay, selection bias in follow-up, changing environment, or a different action's effect. The abstract does not isolate these mechanisms for individual cases. Experimental repeated dynamic tasks may not generalize to unique career, relationship, health, or financial choices. Historical display may improve comprehension without establishing causal attribution or predictive improvement. Evidence status: primary abstract only; original model details, sample sizes, effects, and statistical tests not verified.

## Synthetic acceptance proposals (NOT executed)
1. A job change on Jan 1 with an agreed six-month outcome horizon: a Feb 1 salary observation is interim, not final success.
2. Training started Jan 1, job change on Mar 1, income increases in June: do not attribute full gain to training.
3. Decision recorded but outcome not yet observed: mark pending, not failure.
4. User reports an outcome without a timestamp: ask timing only if necessary; do not invent one.
5. One observed improvement with no comparable control: avoid claiming individual causal effect.
6. An unchosen alternative has no observed outcome: preserve unknown.
7. Feedback arrives after environment changed: flag transport/attribution uncertainty.
8. User declines follow-up: present conditional review without fabricated certainty.
9. Recorded negative outcome despite a well-calibrated ex ante decision: separate process quality from outcome quality.
10. Multiple actions within overlapping windows: avoid assigning the outcome to the latest action by default.

## Handoff
Model track: decide whether timing fields and minimal follow-up belong in the candidate method interface; no implementation authorized here.
Data track: evaluate time-stamped evidence quality, censoring, intervening actions, and observation rights.
Independent acceptance track: hold out variants, compare with a simple timestamp-only baseline, check false causal attribution and extra-question burden.

No real personal records, paid API, CI, scientific acceptance, or frozen-protocol changes. Deduplication: repository code search for “Feedback Delays”, “Sterman”, “delayed outcome”, “feedback delay” returned no matches at time of writing; semantic completeness unknown. Related prior theory: Dawid 2000 prospective vs retrospective causal questions; distinct focus here is feedback timing and review chronology.
