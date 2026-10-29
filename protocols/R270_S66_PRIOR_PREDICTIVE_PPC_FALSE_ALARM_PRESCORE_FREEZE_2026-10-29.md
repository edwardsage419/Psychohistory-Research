# R270 S66: posterior predictive tail alarm repeated-sampling calibration, prescore freeze

Date: 2026-10-29 UTC. Track R. Initial main HEAD: 617f7e38d45aa16b7cb09cb5984df66ff6b277e0. This protocol is prospective for S66 endpoints only; the investigator has read R270 original nine-world results, so the study is nonblind with respect to R270. Do not modify original R270 frozen results or acceptance.

## Frozen universe and data-generating assumptions

Length n=6, all 64 ordered binary observed sequences. Fixed generating Bernoulli(theta) independently across six positions with theta in {1/4,1/2,3/4}; these are mathematical artificial mechanisms, not human trials. Fit the original Beta(a,b) model with priors {(1,1),(2,2),(1,3)} and posterior Beta(a+K,b+6-K) for each observed sequence. For each observed sequence, compute the exact posterior predictive probability over all 64 ordered six-bit replicated sequences using rising-factorial Beta integration, with the same K_count and T_adj=sum_{i=1}^5 1[y_i=y_{i+1}] definitions as original R270.

## Frozen endpoints, alarm rule, and controls

Primary statistic is lower-tail posterior predictive p_lower(y)=P(T_adj(y_rep)<=T_adj(y)|y) including equality. Define alarm as p_lower(y)<=alpha, with alpha exactly {1/20,1/10,1/5}. No randomization at equality, no multiple-testing adjustment. For each (prior, generating theta, alpha) of 27 combinations, calculate exact repeated-sampling alarm probability by summing theta^K (1-theta)^(6-K) over all 64 observed sequences satisfying the alarm. Report the number of alarming sequences, exact probability, difference probability minus nominal alpha, and the 64-sequence p_lower table per prior. Report both anti-conservative and conservative cases without selective suppression. This is a fixed-theta repeated-sampling diagnostic of the posterior predictive tail rule, not a claim of posterior predictive p-value uniformity.

Controls: 64 observation coverage per prior, 64 posterior predictive replicate coverage per observation, exact predictive mass normalization, generating probability normalization, monotonicity of alarm sets across alpha, exchange symmetry theta=1/4 versus 3/4 when prior is symmetric, and strict JSON type/identity checks. Negative tests must reject changed probability, omitted row, duplicate row, false evidence category and Boolean masquerading as integer.

## Independent calculation routes and evidence

R route directly enumerate 64 observations and for each enumerate all 64 replicates using exact Fraction arithmetic. B route independently derive each T_adj conditional probability by counting ordered sequences by (K,T_adj) using run-composition binomial coefficients, then integrate Beta posterior mass; compare all 192 per-observation tail values and 27 final alarm probabilities. Persist full results, scripts, checks and a scientific report as new paths. Prior protocol commit must exist before any S66 score is computed. All evidence E1 artificial; no E2 human, E3 historical, external-team replication or R073/PESEN promotion. GitHub Actions only if no additional cost can be confirmed; otherwise NOT_RUN. Avoid overwrites and recheck HEAD/target blobs before each write.
