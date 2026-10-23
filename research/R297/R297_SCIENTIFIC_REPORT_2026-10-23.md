# R297 Scientific Report: Watkins–Dayan Q-Learning, off-policy bootstrap and incomplete action coverage

Date 2026-10-23 Asia/Taipei. Original-239 candidate 02-003 (P1), research ID R297. Scientific conclusion **CLOSED_BOUNDED_E1_ARTIFICIAL_R297_OFF_POLICY_Q_AND_COVERAGE**, synthetic finite deterministic MDP only. No new human/animal E2, no real historical E3.

## Primary source and earlier-study separation

Watkins, C.J.C.H. & Dayan, P. (1992), *Q-learning*, *Machine Learning*, 8:279–292, https://doi.org/10.1007/BF00992698 and original author-hosted English paper https://www.gatsby.ucl.ac.uk/~dayan/papers/cjch.pdf . Q-learning incrementally updates an action value using immediate reward and the maximum forecast successor-action value. Original convergence result requires sampling and step-size hypotheses, and these **cannot be proven by a four-epoch synthetic run**. Van Hasselt (2010), *Double Q-learning*, https://papers.neurips.cc/paper_files/paper/2010/hash/091d584fced301b442654dd8c23b3fc9-Abstract.html is related but a distinct original model not implemented here.

The original-239 2026-10-18 provenance overlay had no verified 02-003 source. Direct earlier R063 code audit concerns Najar et al. (2020) metaVS imitation/social reinforcement learning rather than independent Watkins–Dayan original research. R065 human models and R073 repeated-game held-out prediction remain separately accepted at their existing scope; **none is promoted or double-counted as this synthetic Q-learning E2 proof**. Earlier RL work may share individual mathematical terms.

[Prospective full R297 frozen protocol](../../protocols/R297_Q_LEARNING_OFF_POLICY_COVERAGE_24_WORLDS_120_SOURCE_PRESCORE_FREEZE_2026-10-23.md) committed as [fd66badd](https://github.com/edwardsage419/Psychohistory-Research/commit/fd66badd5a110b36cc97564f7e1a29daba4298ba) before executable/results.

## Entire original artificial data universe

Finite three-state deterministic MDP: S0 with SAFE (reward 1 to terminal) or EXPLORE (reward 0 to S1); S1 has GOOD (reward 3 to terminal) and BAD (reward 0 to terminal). Terminal has successor value zero. All Q initialized to 0.

Cross four prospectively frozen factors: discount γ∈{0,1/2,1}, step size α∈{1/2,1}, observed GOOD action coverage FULL vs GOOD_MISSING, backup OFF_POLICY_MAX vs BEHAVIOR_BAD. Each of **24 artificial worlds** is evaluated at exactly five epochs 0..4 for **120 complete labeled original state vectors**, not 120 original paper samples.

At each epoch≥1, update (when observed) S1 GOOD toward reward3 and S1 BAD toward 0; update S0 SAFE toward1; finally S0 EXPLORE toward γ times maximum successor learned Q for OFF_POLICY_MAX, or γ times learned S1 BAD Q for BEHAVIOR_BAD. Identical observed state/action/reward definitions, no source randomness, zero terminal continuation. BEHAVIOR_BAD represents a fixed BAD successor-action sampling target for *one update*, not a complete model of optimal SARSA control. Under that forced-BAD continuation the choice may be rational for the *behavior policy* even when it disagrees with the more permissive, optimal free-action benchmark.

The benchmark oracle uses the environment equations **only to evaluate choices**, never to train: true optimal Q*(S0,SAFE)=1, Q*(S0,EXPLORE)=3γ. Tie policy chooses SAFE.

## Recurrent update and independent exact formula

All predictions use Fraction exact rational arithmetic. After t observed epochs, for either coverage:

* Q_SAFE(t)=1−(1−α)^t.
* Q_GOOD(t)=3[1−(1−α)^t] under FULL, otherwise 0.
* Q_BAD(t)=0.
* Under FULL and OFF_POLICY_MAX only, Q_EXPLORE(t)=3γ[1−(1−α)^t−αt(1−α)^t], including t=0 at 0; in other worlds Q_EXPLORE(t)=0.

The implementation checks independent discrete recursive update against each analytic formula for all 120 source states. A **separate, no-production-imports independent auditor** reconstructs all 120 state rows and all 24 × 5 complete result records; includes adversarial tests of wrong learned action, wrong bootstrap value, invalid coverage, unearned oracle, incomplete states, result tampering and digest changes.

### Frozen counterexample

For γ=α=1/2, FULL, OFF_POLICY_MAX:
- Epoch 1 Q_SAFE=1/2, Q_EXPLORE=3/8. Learned choice SAFE.
- Epoch 2 both Q_SAFE and Q_EXPLORE=3/4. Strict tie chooses SAFE.
- Epoch 4 Q_SAFE=15/16, Q_GOOD=45/16, Q_EXPLORE=39/32. Learned choice EXPLORE, matching unconstrained optimal action.

With FULL coverage but **BEHAVIOR_BAD** sampled-action backup, Q_GOOD still learns from the other observed episodes; S0 EXPLORE bootstrap remains 0 because the target successor BAD has value 0. Thus the same underlying high-reward action evidence need not enter that one-step behavior-conditioned value backup. With GOOD_MISSING, no learner can infer the unobserved positive GOOD reward from the other fixed artificial experiences; the S0 EXPLORE value likewise remains 0. No optimistic unobserved action value is hallucinated.

At epoch4: of 24 fixed worlds, **12 learned S0 actions agree** with the oracle under free optimal downstream action and **12 disagree**. The 12 disagreements are tied to positive γ and the absence of FULL+MAX. This count is unweighted grid arithmetic, not population error and not estimated generalization. In particular it would be **incorrect** to call BEHAVIOR_BAD SAFE action suboptimal with respect to the fixed BAD-continuation policy's own reward objective.

The Γ=1 setting is finite and acyclic, with all trajectories terminating. No proof is offered of generic undiscounted Bellman contraction. Constant α and four updates are not the conditions of the original asymptotic stochastic Q-learning theorem. Neither an original real-human dataset nor animal-learning behavior was used.

## Original sources, machine verification and formal gate

* [Executable exact Q-learning model and 611 true unit tests](r297_exact_q_learning.py)
* [All 120 original artificial Q-vector states](R297_ALL_120_ORIGINAL_Q_LEARNING_Q_VECTOR_SOURCES.csv)
* [24-world complete epoch0..4 and counterfactual-oracle result JSON](R297_EXACT_Q_LEARNING_OFF_POLICY_RESULTS.json)
* [Original CSV/JSON SHA256 machine receipt](R297_MACHINE_RECEIPT.json)
* [Independent no-import 120-source/24-world recomputation and 16 adversarial tests](../catalogue_audit/independent_r297_source_audit.py)

[GitHub Actions run39924889538](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39924889538) completed/success with three jobs: Python 3.11 and 3.12 each passed 611 exact model tests and 16 independent auditor tests, with third job redoing source verification and permanently archiving original source/results/receipt in main [commit6d3b0496](https://github.com/edwardsage419/Psychohistory-Research/commit/6d3b0496111d58c03983941480398c1fd4bff85f).

Scientific status: **CLOSED_BOUNDED_E1_ARTIFICIAL_R297_OFF_POLICY_Q_AND_COVERAGE**. No E2 (human or animal); no E3. Historical R073 and PESEN v0.1 remain frozen. Remaining original 02-004 Model Based RL and 02-005 Model Free RL require separate provenance and scope handling before any shared mechanics could be treated as new primary research.
