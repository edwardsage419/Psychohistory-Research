# R299 S95 scientific report: stochastic reward, exact independent holdout risk

Date: 2026-10-30 UTC. R track. Frozen prospective protocol commit: `6a84026ee32039b1e4b256ae46370aee1add11de`. Baseline main before this report: `97f0e078c6994029a21e665a535ef5057a996621`. Original R299 2026-10-23 fixed-policy TD0/MC bounded E1 acceptance stays unchanged.

## Research question and complete artificial source universe

The original deterministic R299 task showed faster delayed reward propagation for Monte Carlo. S95 pre-registered a different question: with noisy terminal reward and independent future test reward, which finite-training value estimate has lower expected squared prediction risk? The fixed policy follows S0 reward0, S1 reward R, terminal. R is 2 with probability p, otherwise 0. Rewards are independent between episodes and independent of test. Alpha=1/2, p in {0,1/4,1/2,3/4,1}, gamma in {0,1/2}, n in {2,4}, TD0_ONLINE or MC_FULL_RETURN. All 400 ordered histories, including zero-probability histories, were retained across 40 groups. There are 20 paired contrasts. No fitted p or policy optimization.

R source `research/validation/r299_s95_stochastic_return_holdout_20261031.js` generates the 400 original exact history rows and 40 group results with rational BigInt arithmetic. Original CSV `R299_S95_ALL_400_STOCHASTIC_TRAIN_HISTORIES.csv` and exact results `R299_S95_EXACT_HELDOUT_RISK_RESULTS.json` are archived. Exact R generator V8 replay regenerated both archived files byte-identically. Git blob identities and independent audit are recorded in `R299_S95_MACHINE_REPLAY_RECEIPT_2026-10-31.json`.

## Exact results

Table below fixes gamma=1/2. Values are independent test expected squared prediction errors. Smaller is better. MC minus TD is positive when TD has lower risk.

| p | n | TD0 holdout risk | MC holdout risk | MC minus TD |
| --- | ---: | ---: | ---: | ---: |
| 0 | 2 | 0 | 0 | 0 |
| 0 | 4 | 0 | 0 | 0 |
| 1/4 | 2 | 15/64 | 1/4 | +1/64 |
| 1/4 | 4 | 229/1024 | 1/4 | +27/1024 |
| 1/2 | 2 | 13/32 | 11/32 | -1/16 |
| 1/2 | 4 | 161/512 | 171/512 | +5/256 |
| 3/4 | 2 | 33/64 | 9/32 | -15/64 |
| 3/4 | 4 | 279/1024 | 129/512 | -21/1024 |
| 1 | 2 | 9/16 | 1/16 | -1/2 |
| 1 | 4 | 25/256 | 1/256 | -3/32 |

All ten gamma=0 paired conditions tie at zero. Across all 20 comparisons: 5 MC lower, 3 TD lower, 12 ties. These counts summarize a deliberately constructed finite parameter grid, without a population interpretation.

The main counterexample is p=1/2: with two training episodes MC risk 11/32 is lower than TD risk 13/32, while with four episodes TD risk 161/512 is lower than MC risk 171/512. Thus the finite-sample ordering reverses as training length changes under the frozen setup. At p=1/4, TD wins for both training lengths. MC propagates the latest realized reward more quickly and therefore carries more sampling variability; TD's delayed credit propagation creates shrinkage and bias. Relative risk depends on both.

## Independent test metric and decomposition

The target is a genuinely new Bernoulli reward R_test, independently drawn from the same frozen p. Each trained estimate V0 predicts gamma R_test. Risk is E[(V0-gamma R_test)^2] over both training histories and the new test outcome. This is an exact hypothetical independent test distribution, not an empirical held-out person or game. Its irreducible oracle risk is 4 gamma^2 p(1-p). The estimator error MSE is squared bias plus variance; total independent test risk is MSE plus oracle risk. All 40 group identities were verified exactly. Zero gamma makes all S0 risk zero; p=0 makes every positive-mass history zero; p=1 reproduces original R299 deterministic n4 gamma1/2 checkpoint TD 11/16 and MC 15/16.

## Scientific verification and scope

B audit used a different closed-form reward-coefficient polynomial, Bernoulli mean/variance identities, and no import of R code. It checked all 400 individual rows, 40 groups, 20 contrasts and rejected eight predeclared mutations. A separate local Python Fraction computation matched eight nontrivial gamma1/2 comparisons. This is an internal nonblind mathematical audit; external independent replication was not performed.

Scientific status `PARTIAL_NONBLIND_INTERNAL_E1`. R299 original bounded E1 acceptance remains unchanged. New E2 human/animal data 0; E3 historical data 0; actual human out-of-sample calibration 0. Original R073 scoring and PESEN v0.1 remain frozen. Original239 v7.8 and pending154 are untouched. Native Node CLI on an independent checked-out archive, full CI and outside-team reproduction remain open. Actions were not started because no-cost eligibility was not verified. No paid service was used.

Primary mechanism sources: Sutton (1988), https://doi.org/10.1007/BF00115009 ; Sutton and Barto second edition Chapter 6, https://incompleteideas.net/book/RLbook2020.pdf . All S95 reward distributions and exact numerical results are project-generated artificial E1.
