# R131 independent absorbing Markov chain scientific audit

Date: 2026-10-25. Existing R131, original239 05-007. Evidence class: E1 synthetic mathematical mechanism. New human E2=0, new historical E3=0.

## Provenance and prespecified test
Freeze protocol: `research/validation/R131_INDEPENDENT_ABSORBING_CHAIN_PROTOCOL_FREEZE_2026-10-25.md`, Git blob `64d984c1a408a23d8f084b7a5a867df8cc91f6c9`, frozen first in commit `6fbce98c8da58b4914b93df254c6d60626f85b25`. Existing original R131 Python source blob `3c61e0c3c0fe7a6d4458eccd8fc18e9714e7152f` and original acceptance blob `3fa4bc6657ae38ee306e106dbd98f21edd48451b` were read before execution and left unchanged.

The R131 paper source is Taylor and Jonker (1978), DOI 10.1016/0025-5564(78)90077-9. The finite Moran illustration is an original project construction, not a Taylor and Jonker empirical experiment. The previously archived R131 source used a forward-difference ratio to obtain the fixation probability of one mutant.

## Independent implementation and actual computation
New script: `research/validation/r131_independent_absorbing_chain_exact.js`, Git blob `db7eed80c4210eec8c9bde1d500952da6a4873d6`. The new algorithm independently enumerates four combinations of fitness-weighted birth type and uniform death type to construct the complete absorbing transition matrix. It solves the interior Dirichlet linear system with exact BigInt rational Gauss-Jordan elimination. The original Python code was not imported by this implementation.

Actual execution of the exact JavaScript program in the current V8 runtime succeeded. All 7 sizes N=2..8 and 3 fixed ordered fitness pairs (3,2), (1,1), (2,3) were evaluated. Results: **84 distinct interior fixation values, 126 stochastic transition rows, 84 exactly zero Dirichlet residuals, 21 exact comparisons against a separately transcribed original forward-difference formula, and 2 rejected negative controls**. The 21 formula comparisons do not constitute execution of the unchanged original Python implementation.

N=5 with one B mutant: B disadvantaged, fitness_A=3 and fitness_B=2, exact probability **16/211**; neutral, **1/5**; B advantaged, fitness_A=2 and fitness_B=3, **81/211**. Under disadvantage, forcing the neutral probability fails; setting the absorbing all-B boundary to zero changes the computed result and is rejected. All interior fixation probabilities lie strictly between 0 and 1 and increase with the initial B count.

Raw output: `research/validation/R131_ABSORBING_CHAIN_84_EXACT_FIXATION_ROWS_2026-10-25.csv`, 84 data rows, Git blob `5d2637d19abac6d963d5bac320d35c16747f4769`. The archived CSV was read back from main and matched the newly executed script output byte for byte. Script and data are new files; no R131 original source, original239 crosswalk, R073, or PESEN v0.1 was edited.

## Independent B-methodology audit and evidence limits
The new linear-system solution differs structurally from the original birth-death forward-difference recurrence. The comparison is **internal methodological independence**, with one shared mathematical model and shared fitness assumptions. It is not independent data collection, external-team replication, or a new prediction exercise.

Leakage: there are no train/test splits or fitted parameters; the finite transition kernel is fixed a priori. Baselines: neutral fixation 1/N is an exact mathematical comparator. Negative controls: two rejected. Uncertainty: all results are exact rational values conditional on the specified artificial process, so resampling intervals are not meaningful here. Calibration, real sample holdout, individual behavior, and historical validity remain untested. An exact E1 result must not be reported as E2 or E3.

## CI, catalogue and disposition
The **older** R131 GitHub Actions run `39360828291` was rechecked: job `118426358465` completed/success. This old CI predates the new audit. **No new GitHub Actions run was requested or verified for the new JavaScript source or CSV**. New local outcome: `PASS_BOUNDED_LOCAL_INDEPENDENT_ABSORBING_CHAIN_E1`. Formal repository CI acceptance of this new method remains open. The global original239 pending count is left unchanged; the previously reported 154-item queue and its separate primary-link accounting are not merged.

No paid APIs, cloud compute, GPU rental, paid datasets, or new GitHub Actions runner were used. Actual account billing was not accessed. R073 and PESEN v0.1 remain frozen.
