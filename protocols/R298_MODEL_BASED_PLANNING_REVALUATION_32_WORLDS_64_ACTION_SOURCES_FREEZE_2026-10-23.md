# R298 prescore freeze: Model-Based Reinforcement Learning, notified revaluation and transition remapping

2026-10-23 Asia/Taipei. Original 239 model 02-004 (P1). Must commit before R298 code or results. Bounded **E1 entirely artificial deterministic planning submechanism**, E2/E3 zero. R073/PESEN v0.1 frozen, finish all original R series before taxonomy and original-model fusion.

## Original model-based reinforcement learning anchors

Sutton, R. S. (1990), "Integrated Architectures for Learning, Planning, and Reacting Based on Approximating Dynamic Programming", ICML 1990:216–224, DOI https://doi.org/10.1016/B978-1-55860-141-3.50030-4 ; original conference entry https://mlanthology.org/icml/1990/sutton1990icml-integrated/ . Sutton (1990), "Integrated Modeling and Control Based on Reinforcement Learning and Dynamic Programming", NeurIPS 1990 official proceedings https://papers.nips.cc/paper_files/paper/1990/hash/d9fc5b73a8d78fad3d6dffe419384e70-Abstract.html . Dyna can integrate learned world-model updating, direct trials and planning; this **finite study only tests one-step planning with a known or newly communicated model**, not world-model learning.

Daw, Niv & Dayan (2005), "Uncertainty-based competition between prefrontal and dorsolateral striatal systems for behavioral control", *Nature Neuroscience* 8:1704–1711 DOI https://doi.org/10.1038/nn1560; Daw et al. (2011), "Model-based influences on humans' choices and striatal prediction errors", *Neuron* 69:1204–1215 DOI https://doi.org/10.1016/j.neuron.2011.02.027. These are first-party model-based/model-free scientific motivation, **none of their human subject trials, fMRI or parameter fits are included or replicated here**. R297 Q Learning 02-003 model-free off-policy backups is distinct, and original 02-005 Model Free RL remains earlier R063 scoped only until separate primary evidence is established. Do not double count adjacent original items.

## Entire fixed synthetic decision universe

Two-stage episodic deterministic MDP: at S0 action LEFT L or RIGHT R, immediate reward0 and transition to terminal-reward state S1 or S2. From S1 collect one terminal reward r1; from S2 collect one terminal reward r2, end. Baseline transitions L->S1, R->S2, baseline rewards r1=2, r2=1. Discount γ∈{1/2,1} applied once.

Four externally defined environmental conditions:
- BASELINE: mapping L->S1, R->S2; r1=2,r2=1.
- REWARD_SHIFT: same mapping, new r1=0,r2=3.
- TRANSITION_SWAP: mapping L->S2,R->S1; r1=2,r2=1.
- BOTH: swapped mapping and shifted rewards r1=0,r2=3.

Every original condition is crossed with notification N∈{0,1} and controller C∈{MODEL_BASED_PLANNER,CACHED_VALUES} for exactly 4×2×2×2=**32 complete synthetic worlds**. Each world has precisely **two fully labeled original action-level source rows**, for **64 exact original sources**, all positive determinism and Fraction calculations. Neither 32 worlds nor 64 rows are people.

The model-based planner uses only baseline transition/reward beliefs unless explicitly NOTIFIED. If N=1 it directly receives updated environment model before choice and recomputes expected gamma-discounted outcome value for each action. This exogenous perfect message is a **precondition** and not inferred via unobserved experience. The cached value controller always retains the baseline action values Q_cache(L)=2γ and Q_cache(R)=γ since no postchange reward/transition experience is given. Both controllers have identical full baseline knowledge and zero postchange direct experience, but different update/computation interfaces. Importantly model-free algorithms could adapt after observing new transitions/rewards, which is outside this no-postchange-experience test.

Source fields per (world,action): scenario, γ, notification, controller, action, actual successor and actual reward, reported/assumed successor and reward, actual Q value, predicted Q value, tie priority (LEFT on exact equality), current chosen action, unconstrained actual-optimal action, action-level oracle regret (max actual Q−actual Q chosen); no real learning trajectories.

## Frozen confirmatory expectations

Action prediction:
- BASELINE: actual L=2γ, R=γ, optimal LEFT.
- REWARD_SHIFT: actual L=0,R=3γ, optimal RIGHT; under uninformed or cached prediction remains baseline, chooses LEFT.
- TRANSITION_SWAP: actual L=γ,R=2γ, optimal RIGHT; under uninformed/cached predicts baseline, chooses LEFT.
- BOTH: actual L=3γ,R=0, optimal LEFT; for uninformed/cached predicts baseline and also chooses LEFT (negative control: model alterations do not always imply preference reversal).

Expected finite world-level results:
* Exactly **20/32** controller-worlds choose the real-environment optimal action (8 BASELINE + 8 BOTH + 2 REWARD_SHIFT with NOTIFIED planner + 2 TRANSITION_SWAP with NOTIFIED planner), and **12/32** disagree; these are unweighted artificial settings, not human percentages.
* NOTIFIED+MODEL_BASED_PLANNER matches the actual optimal action for all 4 scenarios ×2 gamma =8.
* NO_NOTIFICATION+MODEL_BASED_PLANNER agrees only in BASELINE and BOTH, so 4/8. Under no announcement, a planner cannot infer changes by magic.
* NOTIFIED+CACHED_VALUES agrees in BASELINE and BOTH only, 4/8 (identical 4/8 under no notice), showing a cached comparator with no direct experience does not replan merely from notified information.
* For both γ, in REWARD_SHIFT when wrongly selecting LEFT regret is 3γ; in TRANSITION_SWAP selecting LEFT regret is γ. In BASELINE and BOTH realized regret always 0. For informed planner regret zero.
* Actual and assumed successor/reward state transitions must each agree exactly with frozen complete constants. Oracle values may be used only for evaluation and **must never leak into predicted action value**.

Do not claim convergence, a fit of Sutton Dyna-Q, learnt transition-estimation fidelity, or empirical individual goal-directedness.

## Auditing and acceptance gates

Require Python >=3.11 executable --test and --emit, 64 complete action sources, 32 world-level predicted and actual values, exact per-world agreement and regret, SHA256 receipt, independent no-production-imports original-source audit and malicious-tamper checks, actual three-green-job GitHub Actions matrix for Python3.11+3.12 and third independent full replay, then report and bounded machine-scientific acceptance. Only thereafter add a *single* original-catalogue provenance link 02-004 to R298 v1.2 from v1.1, reduce pending51→50. Original 02-005 prior R063 scoped status remains unchanged. R073/PESEN v0.1 frozen.
