# R299 S95 prescore freeze: stochastic terminal rewards and independent holdout squared prediction risk

Date: 2026-10-30 UTC. Track R. Key: (r,R299,S95-v1,stochastic-return TD0 versus MC independent holdout risk). Baseline main HEAD: b88df07e72dade9cfbfa8ff2b4f9ef7cbe48e109. This is a prospective frozen extension, not a revision to R299 original protocol or acceptance. Original R299 is CLOSED_BOUNDED_E1 for its deterministic two-step task. R073 and PESEN v0.1 remain frozen. No taxonomy, fusion, or personal decision product.

## Scientific question and source universe

Can Monte Carlo's faster deterministic delayed credit propagation be separated from finite-sample variance when terminal rewards vary independently between episodes? Use the original two-state fixed-policy chain S0 reward0 -> S1 terminal reward R. Training terminal rewards are independently sampled from {0,2}, with P(R=2)=p. This is a fully artificial enumerated E1 task, with no real participants.

Freeze p in {0,1/4,1/2,3/4,1}, discount gamma in {0,1/2}, learning rate alpha=1/2, training episode count n in {2,4}, algorithm in {TD0_ONLINE,MC_FULL_RETURN}. For each factor combination enumerate ALL ordered binary reward histories of length n in lexicographic 0 then 2 order, retaining histories of zero probability. This gives 5*2*2*2=40 group configurations and 5*2*2*(4+16)=400 source histories. Every history probability is p^k(1-p)^(n-k), k counts 2 rewards. Each group's probability mass is exactly one, including zero-weight rows.

Both estimators initialize V0(S0)=V0(S1)=0, observe the identical history, and use the original R299 update order. TD0_ONLINE at episode t first updates S0 using gamma times OLD S1, then updates S1 using observed R_t. MC_FULL_RETURN updates S0 using gamma times current observed R_t after the episode and S1 using R_t. No policy choice, no model learning, no estimated p, no fitted parameters, no peek at holdout rewards.

## Frozen outcomes and evaluation

For every source history, save unique group key, ordered reward string, probability, final V(S0), final V(S1), true mean mu0=gamma*2*p, squared estimation error (V(S0)-mu0)^2, and conditional independent-holdout squared prediction risk (1-p)*(V(S0)-0)^2 + p*(V(S0)-2*gamma)^2. Save all exact rational values.

For each of 40 groups, sum probability-weighted estimation MSE, estimator bias, squared bias, variance, holdout squared risk, oracle holdout risk gamma^2*4*p*(1-p), and zero-estimator holdout risk gamma^2*4*p. Primary contrasts are MC minus TD holdout risk within each (p,gamma,n), 20 pairs. Report sign without presuming a winner. Predeclared decomposition: holdout risk = estimation MSE + oracle holdout risk; estimation MSE = squared bias + variance. S1 final values must match across algorithms for every identical history. At gamma=0, all S0 risks are zero. At p=0, every positive-probability history has zero learned values and zero risk. At p=1, exactly one positive-probability reward history remains and its final estimates reproduce the original deterministic update recurrence at the corresponding n, alpha, gamma. No post-hoc exclusion of zero-probability histories.

## Validation and acceptance boundaries

R route must be a versioned standard-library Python 3.11+ executable generating full 400-row CSV and 40-group JSON plus SHA256 receipt; include --test, --emit, --check commands. First write this freeze as a distinct commit, then calculate. Test exact factor universe, unique ordered histories, complete 400 source rows, group probability sums, all per-source formula fields, exact aggregate identities, negative controls, original R299 deterministic checkpoints, and mutation failures. B route must be a separate no-import independent algebraic/weighted source auditor with recorded mutation controls, preserving nonblind scope. The R and B paths must not silently overwrite each other.

Evidence remains artificial E1. No human E2, animal E2, historical E3, out-of-domain population inference, general TD/MC dominance, or external independent team reproduction is established. New S95 scientific acceptance remains PARTIAL until native reproducibility, archived byte checks, independent audit and relevant CI requirements are actually met. Do not trigger GitHub Actions unless zero-cost eligibility is confirmed. Original239 v7.8, pending154, R073, PESEN v0.1, and original R299 files stay unchanged.
