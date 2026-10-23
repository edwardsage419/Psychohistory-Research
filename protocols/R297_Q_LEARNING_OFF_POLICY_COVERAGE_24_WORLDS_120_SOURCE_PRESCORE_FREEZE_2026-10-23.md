# R297 prospective freeze: Watkins–Dayan Q-learning off-policy backup and unseen-action coverage

Date 2026-10-23 Asia/Taipei. Original 239 model ID **02-003 Q Learning**, P1. Must commit before code/results. Science scope **BOUNDED_E1_SYNTHETIC_DETERMINISTIC_MDP_ONLY**. No human E2, animal E2 or historical E3. R073 and PESEN v0.1 stay frozen. Continue R-series first, then original-wide taxonomy, finally potential fusion.

## First-party original source and earlier R overlap

Watkins, C.J.C.H. & Dayan, P. (1992), "Q-learning", *Machine Learning* 8:279–292, DOI https://doi.org/10.1007/BF00992698 and author's original English manuscript https://www.gatsby.ucl.ac.uk/~dayan/papers/cjch.pdf. Original Q-learning recursively updates Q(s,a) with temporal difference r + gamma max_{a'} Q(s',a') - Q(s,a), including terminal successor value zero. The original paper's asymptotic convergence theorem requires conditions such as persistent visits to every state-action and appropriate learning rates; four or fewer sweeps here do **not** reproduce the convergence theorem. R061/R062/R063 concerned Najar et al. (2020) social imitation VS/metaVS models and research metadata, and did not establish Watkins–Dayan 1992 Q-Learning original-candidate primary research; R065 other models and R073 repeated-games results also cannot be automatically reassigned as new Watkins E2.

## Complete artificial three-state deterministic MDP

States S0 (starting), S1 (second decision), T (terminal). Two available actions at S0:
* SAFE: reward 1 and terminal T.
* EXPLORE: reward 0 and transition to S1.
At S1:
* GOOD: reward 3 and terminal T.
* BAD: reward 0 and terminal T.
Terminal T has Q=0 and no available actions. All Q initially zero.

Frozen parameter grid: gamma ∈ {0, 1/2, 1}; alpha ∈ {1/2, 1}; coverage ∈ {FULL, GOOD_MISSING}; bootstrap ∈ {OFF_POLICY_MAX, BEHAVIOR_BAD}. Each combination forms exactly 3×2×2×2=**24 synthetic worlds**; record epochs t=0,1,2,3,4 for **120 original labeled full Q-vector states**. No randomness or real participants, not 120 individual trials.

At each epoch >=1, execute this order:
1. If coverage FULL, update Q(S1,GOOD) toward terminal reward 3; if GOOD_MISSING, do not visit/update GOOD.
2. Update Q(S1,BAD) toward terminal reward 0.
3. Update Q(S0,SAFE) toward terminal reward 1.
4. Update Q(S0,EXPLORE) toward gamma * max(Q(S1,GOOD),Q(S1,BAD)) for OFF_POLICY_MAX; toward gamma * Q(S1,BAD) for BEHAVIOR_BAD. The latter is a fixed-behavior **sampled-action backup comparator** corresponding to a SARSA-style target under a guaranteed BAD next action, not a claim to implement full SARSA learning or identical optimal policy objectives. GOOD reward transitions may be observed from other offline trajectory episodes even when the fixed next action in the S0 EXPLORE backup is BAD.

All updates use Q_old + alpha * (target - Q_old), exact Python Fraction, terminal target r only. The comparator cannot use Q(S1,GOOD) in its S0 target, even under FULL. No oracle Q* value is allowed in updates.

## Pre-registered exact acceptance checks

For all alpha, gamma, coverage, bootstrap and t, store Q_S0_SAFE, Q_S0_EXPLORE, Q_S1_GOOD, Q_S1_BAD, update target for EXPLORE, chosen S0 action (choose SAFE on exact ties), true optimal Q*(S0,SAFE)=1, Q*(S0,EXPLORE)=3 gamma, and true optimal action (choose SAFE on exact ties). Oracle is evaluation only, never used to fit/update policy.

For t=0..4:
q_SAFE(t)=1-(1-alpha)^t.
q_GOOD(t)=3[1-(1-alpha)^t] under FULL; q_GOOD(t)=0 under GOOD_MISSING.
q_BAD(t)=0.
q_EXPLORE(t) follows q_0=0, q_t=(1-alpha)q_{t-1}+alpha gamma * q_GOOD(t) in FULL+OFF_POLICY_MAX; otherwise q_EXPLORE(t)=0. Independently calculate closed-form q_EXPLORE(t)=3 gamma [1-(1-alpha)^t - alpha*t*(1-alpha)^t] in the FULL+MAX world (for alpha=1 and t>=1 this is 3 gamma; t=0 defined zero; zero-power t=0 0^0 interpreted as 1 only inside the formula). In particular alpha=1/2, gamma=1/2 at t4: q_SAFE=15/16, q_GOOD=45/16, q_EXPLORE=39/32; therefore chose EXPLORE. At epoch1 for that setting: q_SAFE=1/2, q_EXPLORE=3/8, thus chose SAFE; epoch2 exact tie q_SAFE=q_EXPLORE=3/4 and must choose SAFE.

At t=4, all gamma=0 worlds choose SAFE and are oracle-optimal. All positive gamma worlds with FULL+OFF_POLICY_MAX choose EXPLORE and are oracle-optimal. With gamma>0 and either GOOD_MISSING or BEHAVIOR_BAD backup, the learned S0 policy chooses SAFE although the *unconstrained optimal control policy with GOOD available* would choose EXPLORE. The comparator's fixed BAD continuation is itself a different execution policy and it is **not legitimate** to call its SAFE choice suboptimal for the BAD-only behavioral continuation objective. Count exact 24-world final oracle agreement and subgroup disagreements without treating this as human E2 evidence.

Counterexamples: observed GOOD reward need not affect S0 under behavior BAD backup; no coverage of GOOD cannot reveal true value; terminal values never bootstrap future reward; gamma=1 is an episodic acyclic example and not evidence of a general gamma-contraction theorem.

## Independent evidence

Require exact 120 original row CSV, 24-world epoch-level JSON, SHA256 receipt, main >=Python3.11 --test/--emit, independent no-import reconstruction with adversarial source, target, oracle leakage, duplicate/missing and result-tamper cases, three successful GitHub Actions jobs across Python3.11 and 3.12 plus third independent audit, permanent GitHub archival. Only then can add a provenance link for original 02-003 to v1.1 (one candidate changed), queue 52→51, preserving separate original 02-004 Model Based RL and 02-005 Model Free RL R063 scoped status. Scientific acceptance E1 remains separate from any empirical validation.
