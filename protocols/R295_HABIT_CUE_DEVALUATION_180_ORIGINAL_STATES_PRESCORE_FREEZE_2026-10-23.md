# R295 prospective freeze: Habit formation, cue-triggered autonomy and outcome devaluation

2026-10-23 Asia/Taipei. Original 239 catalogue P1 item **01-019 Habit Formation**. This freeze precedes all R295 executable/results. Explicit scientific scope: **E1 finite artificial mechanism only**. No Lally automaticity time-series reproduction, human questionnaire fitting, brain experiment, animal devaluation replication, or historical prediction E2/E3. R073 and PESEN v0.1 frozen; complete all R-series before taxonomy and model fusion.

## Direct scholarly anchors and boundaries

Dickinson (1985), "Actions and habits: the development of behavioural autonomy", *Philosophical Transactions of the Royal Society of London B* 308:67–78, original English manuscript https://www.princeton.edu/~yael/LearningCourse/Targilim/Dickinson1985.pdf. The goal revaluation distinction motivates the bounded negative controls; model quantitative rates below are our invention.

Wood and Neal (2007), "A New Look at Habits and the Habit-Goal Interface", *Psychological Review* 114(4):843–863, DOI https://doi.org/10.1037/0033-295X.114.4.843, original author PDF https://dornsife.usc.edu/wendy-wood/wp-content/uploads/sites/183/2023/10/wood.neal_.2007psychrev_a_new_look_at_habits_and_the_interface_between_habits_and_goals.pdf. Context-response repetition and goal interaction motivate candidate architecture.

Lally et al. (2010), "How are habits formed: Modelling habit formation in the real world", *European Journal of Social Psychology* 40(6):998–1009, DOI https://doi.org/10.1002/ejsp.674, archived original English article https://repositorio.ispa.pt/server/api/core/bitstreams/370f1dca-cc04-4d3d-a0f0-36d16109ec37/content. Empirical 96 recruited, 82 analyzable and varying automaticity growth do not imply that our artificial training rates match participants. The original paper's observed measures are not read for fitting.

Historical overlay 2026-10-18 lists original 01-019 without first-hand source; earlier ZIP scan metadata has no modelwise 01-019. Existing R learning of RL or repeated actions may have conceptual overlap, so no general never-studied claim. This is a tightly scoped mathematical bridge from context cue to valuation-sensitivity, not proof of automaticity in a person.

## Full fixed finite synthetic source universe

One learned action A vs alternative B. Fixed value V of action A after possible revaluation is 1 (VALUED) or 0 (DEVALUED), alternative B benchmark=1/2. Cue c is SAME_CONTEXT=1 or CHANGED_CONTEXT=0. Training repeats n∈{0,1,2,3,4}; artificial learned context-action strength H_0=0 and H_{n+1}=H_n+alpha*(1-H_n), with alpha∈{0,1/2,1}, so H_n=1-(1-alpha)^n. Controller habit share λ∈{0,1/2,1}. All five factors crossed exhaustively: 3 alphas × 3 habit shares × 2 contexts × 2 outcome valuations × 5 training stages = **180 labeled original deterministic decision source rows**, grouped into 36 world IDs each with five training stages. This is exact enumeration, not 180 humans/experiments.

One explicitly **synthetic hybrid decision score**: U_A=(1−λ)*V+λ*c*H_n. Compare U_B=1/2. Choose A if U_A>1/2; exact ties choose B. All Fraction math. Every source row records full factors, H_n, goal contribution, habit contribution, outcome utilities, tie, selected option and the independently computable negative-control checks. The context cue is the post-training retrieval switch, not an estimate of real cue generalization; the outcome value V is a controlled switch in the constructed world, not a measured subjective devaluation effect. The mixing score is not falsely attributed as a literal formula from Dickinson, Wood/Neal or Lally.

## Frozen confirmatory exact criteria

1. For each alpha,n verify H_n=1−(1−alpha)^n and recursive increments α(1−H_n), bounds [0,1], non-decreasing with n. For α=1/2,n=4 obtain H_4=15/16.
2. At λ=0 (GOAL_ONLY), with either cue, either alpha and any training n, action matches current valuation: V=1 selects A, V=0 selects B. Devaluation changes choice A→B independent of cue or training.
3. At λ=1 (HABIT_ONLY) for same cue and α=1/2,n=4, H=15/16>1/2, A is chosen regardless of valuation. For a changed cue c=0, HABIT_ONLY selects B irrespective of valuation. Under α=0 no habit can form and both cues result in B; under α=1 and n≥1 H=1 and same cue selects A.
4. At λ=1/2, α=1/2,n=4 and cue SAME, valued action score (1/2)+15/32=31/32 >1/2 and devalued score 15/32<1/2, showing goal sensitivity despite a substantial habit trace. The same trace gives habit-only behavior insensitive to outcome value. Context shift can disrupt retrieval even without H decay.
5. Paired devaluation classification for each α, λ, context and n: sensitivity=1 iff valued A and devalued B, otherwise 0. Count all 90 matched comparison pairs, report by controller. There must be no B→A reversal after reducing V since U_A is nondecreasing in V.
6. Independent third-party audit never imports the primary implementation: parse 180 frozen rows, verify exact H recursion, source completeness (36 worlds ×5), score components, decisions, all paired sensitivity and CSV/JSON SHA256. Include adversarial tamper tests for source score, cue, training level, missing combinations, reported sensitivity and digest.
7. Produce bounded research package, machine receipt, audit, three-job GitHub Actions matrix using Python3.11 & 3.12 and independent auditor, and only after observed success permit original 239 crosswalk v0.9 one-row amendment (01-019). Original 239 entries, P1/P2 status, earlier R references and E2/E3 claims must remain honest.

## Scope guard

A repeated response or mathematically devaluation-insensitive artificial choice does not constitute psychological habit identification in humans, absent experimental manipulation, action devaluation checks, measurement quality, competing RL explanations and out-of-sample data. The R295 formula is one constructed possible account, and is not an independent real replication of the cited sources.
