# R266 S62: finite score interval coverage and naive variance audit, prescore freeze

Date: 2026-10-29 UTC. Track: R. Base main at planning: `a005e7890997d3881ce6b9ec994cd17710b559f5`.
Target key: (r,R266,S62,finite-score-coverage-and-naive-independence).
This is a new, bounded E1 extension of original R266, which remains CLOSED_BOUNDED_E1_EXACT_FINITE_MONTE_CARLO. No existing R266 protocol, source, result or acceptance file is modified.

## Frozen source and comparison
Read exactly the original nine worlds, IID and ANTITHETIC designs, and all 5,328 primitive source atoms from `research/R266/R266_ALL_5328_FINITE_MONTE_CARLO_ORIGINAL_SOURCES.csv`. Verify source SHA256 equals `5e0aac41c960ee21b54d3266064793a7e9a2454dbb4493ae8e4451591d48587a`. Use the original R266 result JSON as a separate variance reference. Each atom within a world/design is equiprobable, but atoms are alternative exhaustive source outcomes, not observed humans or 5,328 independent trials.

## Prespecified metrics
For each of 18 world/design combinations, calculate exact coverage of the nominal two-sided Wilson score interval with z=2, treated as if all n function evaluations were IID Bernoulli trials. Use the score-inversion identity
`n * (p_hat - p)^2 <= 4 * p * (1-p)`.
Here n is function evaluation count, k is event_success_count, p_hat=k/n, p is the original frozen exact integral. Equality counts as covered. Compute exact coverage as covered atom mass / total atom mass, and exact miscoverage as its complement. No normal approximation is used to estimate coverage.

Also compute the exact expectation of the usual IID plug-in variance estimator `p_hat*(1-p_hat)/n`, the actual frozen estimator variance, and their ratio when actual variance is positive. When true variance is zero, ratio is null and must not be interpreted as a numerical value.

## Frozen falsifiable checks and boundaries
For SYMMETRIC_EXTREMES_N6, the IID score coverage must equal 31/32 and ANTITHETIC score coverage must equal 3/4, hence the latter is 7/32 lower despite the same six function evaluations. Both designs must be unbiased for p. THRESHOLD_HALF antithetic has true variance zero; a plug-in ratio is undefined. All 18 rows, source uniqueness, masses, and all exact rational calculations are required. A duplicate or missing source row, wrong SHA, wrong evidence grade, or altered variance reference must fail closed.

The z=2 score interval has nominal Gaussian reference level about 95.45%, but this is only a reference, not an exact finite-sample promise. Source enumerations are artificial E1; no actual pseudo-random draws, real-world probability calibration, human E2 or historical E3 evidence. This is not an assessment of general interval performance or an externally independent replication. B independent route must be a separately implemented binomial/convolution calculation, with nonblind scope recorded if original R266 was read. R073 and PESEN v0.1 stay frozen. No paid services or GitHub Actions runs are authorized.
