# R298 Scientific Report: notified model-based replanning vs cached model-free values

Date 2026-10-23 Asia/Taipei. Original 239-candidate 02-004 Model Based Reinforcement Learning, P1. Scientific scope **BOUNDED_E1_ARTIFICIAL_R298_KNOWN_MODEL_REPLANNING**. The original 239-candidate catalogue itself remains unchanged. No new animal/human E2 or historical E3.

## Original primary literature and limits

Richard Sutton (1990), *Integrated Architectures for Learning, Planning, and Reacting Based on Approximating Dynamic Programming*, *ICML* 1990:216–224, original DOI https://doi.org/10.1016/B978-1-55860-141-3.50030-4; Sutton (1990), *Integrated Modeling and Control Based on Reinforcement Learning and Dynamic Programming*, original NeurIPS volume https://papers.nips.cc/paper_files/paper/1990/hash/d9fc5b73a8d78fad3d6dffe419384e70-Abstract.html; Daw, Niv & Dayan (2005), *Uncertainty-based competition between prefrontal and dorsolateral striatal systems for behavioral control*, https://doi.org/10.1038/nn1560; Daw et al. (2011), *Model-based influences on humans' choices and striatal prediction errors*, https://doi.org/10.1016/j.neuron.2011.02.027.

These sources distinguish representations of the world, model-free value caching, and planning. R298 constructs **one known-or-notified model planning calculation**, and does **not learn a transition model, implement full Sutton Dyna-Q, reproduce the Daw 2011 human sample/fMRI, or test real-world model identification**. No real data introduced or reclassified from R297 or R063.

[Prospective protocol, frozen before code](../../protocols/R298_MODEL_BASED_PLANNING_REVALUATION_32_WORLDS_64_ACTION_SOURCES_FREEZE_2026-10-23.md) commit [24cdb311](https://github.com/edwardsage419/Psychohistory-Research/commit/24cdb3119991c7233ee02fdad271d74881ab8825).

## Exact original artificial environment and information assumptions

A two-stage episodic deterministic MDP. S0 chooses LEFT or RIGHT; baseline known model LEFT→S1, RIGHT→S2, with downstream terminal reward S1=2, S2=1. Immediate S0 reward0 and gamma ∈{1/2,1}. Baseline action values are Q(L)=2γ and Q(R)=γ.

Prospectively frozen scenarios:
* BASELINE: original transitions and rewards; true best LEFT.
* REWARD_SHIFT: terminal rewards change to S1=0,S2=3 with original mapping; true best RIGHT.
* TRANSITION_SWAP: LEFT→S2, RIGHT→S1 with old terminal rewards2/1; true best RIGHT.
* BOTH: swapped transition plus terminal rewards0/3; true best LEFT, crucial negative control that two changes can cancel action preference reversal.

Cross 4 scenarios × 2 gamma × 2 externally supplied information states notified=0/1 × 2 controllers MODEL_BASED_PLANNER / CACHED_VALUES ⇒ **32 worlds**, with **64 original fully labeled action source rows**.

If and only if the planner is notified, it receives the exact new transitions/rewards and recomputes both Q predictions before taking action without new direct experience. The cached controller retains baseline Q and never learns from the external announcement. If neither controller received new direct experience or model notification, their choice remains baseline LEFT. Note: this does not prove real model-free systems ignore reward shifts after experience; such adaptation is excluded by design.

Original source labels per action contain true and believed successor, true/believed terminal reward, original world factors, actual vs predicted discounted Q values, selected and optimal action, source-backed regret. The true optimal oracle is evaluation-only; cannot enter the beliefs used to select actions.

## Exact independent findings

| Scenario | True terminal reward / transition change | Actual optimal action | With notified planner | With cached or uninformed planner |
|---|---|---|---|---|
| BASELINE | none | LEFT | LEFT | LEFT |
| REWARD_SHIFT | S1=0,S2=3 | RIGHT | RIGHT | LEFT |
| TRANSITION_SWAP | LEFT→S2, RIGHT→S1 | RIGHT | RIGHT | LEFT |
| BOTH | rewards shifted and transitions swapped | LEFT | LEFT | LEFT |

Both γ values preserve these strict orderings. Therefore exactly **20/32 artificial controller-worlds** agree with the full actual-environment optimal action, **12/32** disagree. Breakdown: notified model-based planner 8/8 correct; unnotified model-based planner 4/8; notified cached comparator 4/8; unnotified cached comparator 4/8.

When a controller incorrectly persists with LEFT in reward shift, its exact actual-model regret is 3γ; in transition swap it is γ. BASELINE and BOTH always have regret zero regardless of notification. Crucially BOTH shows that **true environment structure can change while original action remains optimal**; counting action switches alone as evidence of revaluation sensitivity would misclassify this condition.

The 20/32 result is an unweighted count of chosen *model configurations*, not a behavior frequency, human planning accuracy, or learned transition model fit. Exogenously perfect notification is a strong information assumption; any real learner with imperfect observations, mislearned transitions, insufficient working memory or changing preferences can deviate. No empirical causal inference is made.

## Actual independent source verification

* [Runnable complete E1 planning program and 269 unittest checks](r298_exact_model_based_revaluation.py).
* [All 64 exact source-level action rows](R298_ALL_64_ORIGINAL_REVALUATION_ACTION_SOURCES.csv).
* [Every scenario, predicted/actual action values and 32 verdicts](R298_EXACT_MODEL_BASED_REVALUATION_RESULTS.json).
* [SHA256 original source/result receipt](R298_MACHINE_RECEIPT.json).
* [Entirely separate no-import audit, 17 independent tests and adversarial tamper checks](../catalogue_audit/independent_r298_source_audit.py).

[CI run39925393352](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39925393352) all three jobs completed/success, Python3.11 and3.12 each ran 269 main model tests and 17 independent source tests; third independently recomputed all 64 exact source rows, 32 action decisions and SHA256 before permanently committing full sources and results to main [commitbea6bf4f](https://github.com/edwardsage419/Psychohistory-Research/commit/bea6bf4f6b3b95db05b2ba1efe5f9d96fa4d2794).

Formal scientific status **CLOSED_BOUNDED_E1_ARTIFICIAL_R298_KNOWN_MODEL_REPLANNING**, original-human/animal data replication=false, E2=0, E3=0, and 239 scientific completion NOT_ESTABLISHED. Original 02-005 Model Free RL must remain separate prior R063 scoped only. R073 and PESEN v0.1 frozen; continue R studies first, categorization and fusion later.
