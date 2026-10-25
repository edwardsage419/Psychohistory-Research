# R165 exact heterozygosity and stationary autocovariance extension: prospective protocol
Date: 2026-10-25 Asia/Singapore. Track R, subflow main. Observed HEAD at preparation: 83309e920ddb0abbc6b3d71e908d275489193488.
This is an **extension** of R165's previously frozen finite E1 study, with no amendment to the original model, scoring or acceptance. Its results are unknown at freeze time. No E2/E3 claim.

## Fixed input and scope
Use only `research/R165/R165_EXACT_RESULTS.json`, Git blob `8b8a7ca5b6a1d75b3f8464e0eeb1b7b180e4ccf3`, and the model as defined in `research/R165/r165_neutral_drift_exact.py`, blob `b6baec8fd6f6bbfae2df8945b7aaefaaf565ce7f`. N = 4, 6, 8; innovation mu = 0, 1/16, 1/8, 1/4; four original initial counts for each N; horizons 0 to 4. Exactly 48 artificial worlds, 12 kernels, nine positive-innovation stationary laws. Do not change these or the original R165 source files.

## Preregistered algebraic claims and tests
Let p=K/N and H=2p(1-p). Set c=(N-1)/N, a=c(1-mu)^2, b=c*mu*(1-mu/2).
1. Check exact recurrence E[H_{t+1}]=a E[H_t]+b at all 48 x 4 successive time pairs from the frozen result.
2. Check closed form E[H_t]=a^t H_0+b(1-a^t)/(1-a) for t=0..4, all 48 worlds (a<1 for N>=4). This includes mu=0 where b=0.
3. For nine mu>0 stationary distributions, check H_star=b/(1-a) against direct exact weighted stationary diversity from frozen source; check 0<H_star<1/2.
4. For nine mu>0 stationary distributions and lags s in {1,2,4}, check exact stationary covariance Cov(p_t,p_{t+s}) = (1-mu)^s*(1-2H_star)/4. Use a separate direct matrix-power oracle from the frozen Markov kernel for these 27 comparisons.
5. Negative controls: compare correct H_{t+1} against omission of factor c, and against replacing (1-mu)^2 by (1-mu) while leaving b fixed; record applicability counts and actual mismatches. No fabricated universal detection count.
6. Independently verify source row sums, stationary equations, and at least one original mu=0 diversity decay identity.

## Method separation and acceptance
R main uses algebraic moment recurrence with Python Fraction. B audit uses independent exact matrix propagation from frozen kernels and direct sums over states, plus independent stationary joint moments. No import or call from B into R code. Preserve failed checks and document corrections without changing this freeze. Accept finite E1 internal computational verification only when all specified exact comparisons pass. External replication, out-of-sample prediction, E2, E3, and causal identification remain untested.

## Cost, concurrency, provenance
Standard library and existing free GitHub permissions only. Do not launch Actions without confirmed zero additional cost. Write only new paths under research/validation/, research/evidence_audit/, research/data_scout/; do not edit crosswalk v7.8, queue 154, R073 or PESEN v0.1. Recheck main HEAD and target paths immediately before each write. On conflict stop or use a distinct new path, never overwrite.
