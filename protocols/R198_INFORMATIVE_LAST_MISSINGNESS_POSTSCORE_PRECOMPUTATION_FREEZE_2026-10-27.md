# R198 informative missingness: third-method prescore freeze

Date: 2026-10-27. Scope: additive E1 artificial state-space analysis. The original R198 acceptance and its deterministic last-missing observation design remain frozen and unchanged.

## Frozen source universe and observation channel

Use all 4 original symmetric hidden-state stay probabilities a in {1/2, 3/4, 1/4, 11/18}, both sensor accuracies r in {3/4, 7/8}, and both original history lengths T in {4,5}: 16 parameter settings. X0 is Bernoulli(1/2); X1..XT follow symmetric Markov transition P(Xt=Xt-1)=a; Yt equals Xt with probability r, independently conditional on X. Observe the ordered prefix H=(Y1,...,Y[T-1]). At T, generate YT and missingness indicator M with a fixed observation-dependent mechanism. When M=0, YT is observed; when M=1, YT is concealed, and the fact of concealment M=1 is observable.

Predeclare two missingness mechanisms, never chosen by results: MCAR: P(M=1|YT=1)=P(M=1|YT=0)=1/2; INFORMATIVE: P(M=1|YT=1)=3/4, P(M=1|YT=0)=1/4. M is conditionally independent of other variables given YT. The observation mechanism and all a,r values are known to the oracle. The future target is a fresh Y[T+1] after a new hidden-state transition and new sensor emission. Do not use Y[T+1] for model selection.

## Frozen predictors and scores

AWARE: the exact conditional P(Y[T+1]=1|H,M,observed YT when available), including the missingness likelihood. IGNORE_M: when M=1, use P(Y[T+1]=1|H), ignoring information in the missingness indicator; when M=0, use the correctly observed YT. Both use the same known a,r, and both are fixed before scoring. Evaluate Brier loss for the new binary observation, integrated over all original hidden states, sensor histories, M and future outcome. Primary effect: source-marginal Brier(IGNORE_M) minus Brier(AWARE). Secondary effects: probability of missingness, Brier conditional on M=1 for each predictor, and positive/zero effect counts. Also record a missing-case risk identity: weighted excess risk equals the source-weighted squared difference between the two predictive probabilities. Each of 16 parameter settings is evaluated for both MCAR and INFORMATIVE, 32 comparisons in total.

## Validation and negative controls

Main calculation uses forward hidden-state filtering and explicit missingness likelihood; independent B audit must enumerate complete hidden-state paths and observation channels and future outcome probabilities without calling the main filter. Compare all 32 settings, with rational arithmetic and zero numeric tolerances. MCAR must have exactly zero excess risk in all 16 settings. For a=1/2, both schemes must have exactly zero excess risk; informative missingness may help for dependent a. Verify 0<=all predictive probabilities<=1, positive normalized observation masses, and exact total probability one. Introduce deliberate missingness-channel reversal as a negative control in B audit and check that it is detected for dependent worlds.

No additional sources, hyperparameters, model selection, new R073 scores, or original R198 status changes are permitted. This is an internal E1 mathematical addendum only, with no E2 human or E3 historical evidence. R073 and PESEN v0.1 remain frozen. No CI or paid computing may be triggered without confirmed zero cost.
