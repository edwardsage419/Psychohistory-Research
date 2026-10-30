# R298 S94: noisy communicated scenario and exact planning regret

Date 2026-10-30 UTC. Track R. Prospective freeze commit `479b96c37c53c4d5f62503f308ab2067daa26933`, before any S94 computation. Original R298 scoped E1 acceptance and 64 original sources remain unchanged. Extension status **PARTIAL**.

## Research question and sources

The original R298 [known-model planning protocol](../../protocols/R298_MODEL_BASED_PLANNING_REVALUATION_32_WORLDS_64_ACTION_SOURCES_FREEZE_2026-10-23.md) fixes four deterministic scenarios, two discount factors and a baseline cached-value comparator. S94 introduces a five-level symmetric scenario-label communication error channel, no fitted parameters or direct postchange experience. Model-based planner recomputes Q from received label, cached comparator retains baseline Q. Evaluation oracle sees the actual scenario only after prediction. All examples are artificial E1, no human E2, historical E3 or external replication.

Scientific anchors: Sutton (1990) https://doi.org/10.1016/B978-1-55860-141-3.50030-4 ; Daw et al. (2011) https://doi.org/10.1016/j.neuron.2011.02.027 . Neither original empirical dataset was reproduced.

## Exact frozen universe

4 actual scenarios x 2 gamma values (1/2,1) x 5 error probabilities (0,1/4,1/2,3/4,1) x 2 controllers = **80 worlds**. Each has four received-message branches and two action sources, yielding **320 branches and 640 complete action rows** including zero-probability branches. The error channel is P(correct label)=1-e, P(each incorrect label)=e/3. All arithmetic is exact rational. Equal weighting of the four scenarios is an artificial reporting convention.

For gamma=1, equal-scenario expected regret:

| Error e | Replanning on message | Fixed baseline cache |
| --- | ---: | ---: |
| 0 | 0 | 1 |
| 1/4 | 1/3 | 1 |
| 1/2 | 2/3 | 1 |
| 3/4 | 1 | 1 |
| 1 | 4/3 | 1 |

For gamma=1/2 all regrets are halved. Exact planner wrong-action probability across every true scenario is 2e/3. Cache is wrong in REWARD_SHIFT and TRANSITION_SWAP and correct in BASELINE and BOTH. In each actual scenario, planner regret equals (2e/3) times the true action gap, while cache expected regret is 0, 3gamma, gamma, 0 respectively. Equal-scenario planner regret is 4e*gamma/3, cache gamma. Thus planner has lower risk when e<3/4, equal risk at e=3/4, higher risk when e>3/4. With e>0, false messages can damage BASELINE and BOTH, where a cached baseline action is correct. This is a finite exact counterexample to the claim that using an updated communicated model must improve decisions.

## Execution and independent checks

R JavaScript source `r298_s94_noisy_scenario_notification_20261031.js` was executed in V8; all 80 worlds, 320 message branches, 640 action rows, 20 summaries and per-world probability mass passed internal exact checks. Persisted CSV Git blob `3d4d044817fb3b752f52f41d9e528532ca73b3ca` and JSON Git blob `bd908d7efd46dd69b2f07e5626d972c6e676f441` were read back from GitHub. B separate no-import V8 oracle verified all 640 rows, 80 worlds, 20 summaries and 64 original R298 rows; eight controlled mutations were rejected. Independent local Python Fraction implementation separately reproduced all ten gamma/error average-regret pairs, with no R code import. This is nonblind internal checking, no external independent study.

Native Node CLI `--test`, `--emit`, `--check` in a repository checkout **NOT_RUN**. CI **NOT_RUN** pending cost-safe eligibility. No real-data out-of-sample prediction, uncertainty inference, probability calibration or E2/E3 transfer. Do not interpret 3/4 as an empirically estimated communication error threshold. Exact deterministic E1 arithmetic has no sample-based confidence interval.

## A01 to A06 acceptance

A01 PASS scoped finite problem and negative controls. A02 PASS original R298 repository source identity and pinned version metadata; full native SHA256 source verification OPEN. A03 PASS V8 exact computation and persisted-source B audit; native Node checkout and external reproduction OPEN. A04 PASS eight controlled mutation rejections; broader adversarial review OPEN. A05 PASS E1-only reporting, no human generalization. A06 PARTIAL: archived scientific report, receipt and handoff; native execution and cost-safe CI OPEN. S94 status **PARTIAL**, original R298 CLOSED_BOUNDED E1 unaffected.

Next R mainline: inspect R299 model-free TD versus Monte Carlo and select a distinct, frozen bounded question. R073 model/scoring and PESEN v0.1 frozen. No taxonomy, fusion or personal product implementation.
