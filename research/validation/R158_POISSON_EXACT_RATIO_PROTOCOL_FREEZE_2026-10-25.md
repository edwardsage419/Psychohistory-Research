# R158 additive E1 freeze: exact conditional Poisson likelihood ratios

Date 2026-10-25. Baseline main bae4ca71956c463fb7884ca9c4108b66a0eac6aa. Existing R158 synthetic conditional law and original 60 archived worlds remain frozen.

For each original history H0..H3, each mu in {1/2,1,2}, and each alpha in {0,1/4,1/2,3/4,1}, derive L(mu,alpha)/L(mu,0) using exact rational count terms and an explicit exponential factor, with previous count at t=-1 equal to zero.

Predetermined identity:
L(alpha)/L(0) = R * exp(-alpha*S),
R = product_t ((mu+alpha*n_prev)/mu)^n_t,
S = sum_t n_prev.
All factors in R are exact Fractions. The factorial terms cancel exactly. Compare independently computed log R - alpha*S to differences of the archived rounded total log scores; tolerance 2e-11 due original rounding.

Expected 60 checks; H0 alpha-invariance, alpha=0 ratio one, and 48 nonzero-alpha cases. Negative controls: dropping exp(-alpha*S) must fail on a nonzero-lag history; replacing lagged n_prev by contemporaneous n_t must fail; treating ratio as a causal self-excitation estimate must be rejected as an invalid inference.

Scope: E1 artificial fixed histories only, no observed conflict events, no model fitting or held-out data, no E2/E3, no independent external replication. No changes to R073, PESEN v0.1, original239, or the original R158 frozen outputs. Main result and script must be committed after this freeze.
