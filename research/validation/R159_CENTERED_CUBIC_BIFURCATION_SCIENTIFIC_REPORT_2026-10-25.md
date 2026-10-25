# R159 centered cubic, bifurcation and exact archive replay: scientific report

Date: 2026-10-25. Precomputation protocol: `research/validation/R159_CENTERED_CUBIC_BIFURCATION_PRESCORE_FREEZE_2026-10-25.md`. Original R159 project-authored model is frozen. This report adds bounded synthetic E1 analysis only.

## Exact derivation
The source update is `p'=(1-u)[p+h*p(1-p)(2p-1)]+u/2`. Set `x=p-1/2`. Then `x'=a*x-b*x^3`, with `a=(1-u)(1+h/2)`, `b=2(1-u)h`. For `h>0`, the critical reset probability is `u_c=h/(h+2)`.

When `0<=u<u_c`, the center `p=1/2` is unstable and two attracting outer equilibria exist, `p_*=1/2 ± sqrt((a-1)/b)`. At these equilibria the derivative is `3-2a` and lies in [0,1) on the frozen parameter grid. When `u>u_c`, the unique attracting equilibrium is `p=1/2`, with derivative `a<1`. At equality `u=u_c` and `h>0`, the center is marginal with cubic attraction. This equality case does not occur in the frozen grid. The special `h=u=0` case is an identity map with a continuum of fixed points. The `h=0,u>0` case contracts to one-half.

These are statements about the one-dimensional deterministic synthetic frequency map. The map is monotone on [0,1] for `0<=h,u<=1`; in the present grid trajectories on each side of one-half converge toward the corresponding attracting equilibrium.

## Executed exact checks
Source archive Git blob `c5c38f2a8f6991aac1f7156cb3e9cc6b0baa081d`. A separately written JavaScript BigInt rational evaluator executed against the full 48-world JSON. Verified 336 exact archived frequencies, 336 majority probabilities, 288 exact transitions, 1212 centered-polynomial grid identities and 84 exact mirror equalities. Reset-to-current-p mutant differed in 192 eligible transitions. Unbiased-copying mutant differed in 216 eligible transitions. No post-hoc tolerance was used.

Of 12 distinct `h,u` settings, seven exhibit two attracting outer equilibria, four exhibit one attracting center, and one is the neutral continuum. Representative exact values: `h=1/4,u=1/10` has `x_*²=1/36` and outer derivative `39/40`; `h=1,u=1/4` has `x_*²=1/12` and outer derivative `3/4`; `h=1/2,u=1/4` has center derivative `15/16`.

Full exact receipt: `research/validation/R159_CENTERED_CUBIC_12_CASE_EXACT_RECEIPT_2026-10-25.json`. Executable: `research/validation/r159_centered_cubic_exact.js`. Run `node research/validation/r159_centered_cubic_exact.js research/R159/R159_EXACT_RESULTS.json`.

## Interpretation and limits
Positive symmetric reset can eliminate persistent majority-dependent alternative attractors when it exceeds a threshold; for smaller reset, long-run majority amplification can persist. These equilibrium statements add a longer-run regime analysis beyond the original six transitions. They are E1 mathematical properties of a project-chosen recurrence. No gene state, empirical conformity parameter, genetic-cultural coevolution, original author equation reconstruction, E2 human prediction or E3 historical validation is established. The original R159 CLOSED_BOUNDED_E1 archive remains unchanged. The original239 07-001 scientific source/coverage triage remains open.

The separate B Python enumerator checks 12 regimes, 48 regenerated trajectories, 288 transitions and 84 mirror identities without calling the main JavaScript or R159 polynomial. This is an internal method comparison, not an external-team replication. New CI NOT_RUN; local execution only.
