# R320 Drift Diffusion Model: exact six-step absorbing-walk analogue (E1)

Date 2026-10-24. Original239 01-009, P2. **Scientific status: finite computation complete; CI and source identity verification pending**. Prescore protocol committed first at `ff112a92d32fd07695c77c6d6010cf121bfd8e8a`, before the path source and outcomes.

## Original mechanism and reuse

Ratcliff (1978), *A theory of memory retrieval*, *Psychological Review* 85(2):59–108; Ratcliff and McKoon (2008), *The Diffusion Decision Model: Theory and Data for Two-Choice Decision Tasks*, *Neural Computation* 20(4):873–922, DOI 10.1162/neco.2008.12-06-420; author manuscript https://pmc.ncbi.nlm.nih.gov/articles/PMC2474742/ . The original DDM describes continuous noisy evidence accumulation to two absorbing boundaries with reaction-time and accuracy implications. This finite study is a **discrete random walk analogue only**. No Wiener-process likelihood, nondecision-time component, continuous parameter fit, human reaction times or original 1978 experimental replication.

Repository tree and code-search review found finite evolutionary/cultural drift R131/R165, diffusion R147/R174, sequential offers R289, with different mechanisms. No strict equivalent original two-threshold decision-time study was verified in those checked sources; full historical ZIP scan is still open.

## Complete frozen artificial sample

Two absorbing boundary widths a=4,6, starts z=a/2, three independent step-up probabilities p=1/4,1/2,3/4, six time steps, all 64 exogenous step strings per world: **6 worlds and 384 complete artificial original source rows**. First boundary hit defines the decision; paths without a hit by step 6 are right censored. Bits after a hit are counterfactual labels for exhaustive sample-space accounting, never observed actions. Each row is weighted by exact p^up(1-p)^down; the original source contains every row.

For a=4,p=1/2, hit by step6=7/8, survival=1/8 and each decision boundary has probability 7/16. Complement symmetry swaps upper/lower hit-time probabilities under p=1/4 vs 3/4. At p=1/2 the wider a=6 has greater six-step survival than a=4. Full joint hit-time and side distribution, conditional mean decision time among hits and expected truncated decision steps are retained as exact Fractions.

Independent no-import audit reconstructs the 384 path labels and probabilities, then verifies each six-world first-hit distribution with an independent interior-mass dynamic program. The DP sums only surviving states at each step and therefore provides an independent computation of first-passage outcomes.

[Prescore protocol](../../protocols/R320_FINITE_BOUNDED_RANDOM_WALK_DDM_ANALOGUE_384_PATHS_PRESCORE_FREEZE_2026-10-24.md), [384 original path CSV](R320_ALL_384_ORIGINAL_SIX_STEP_PATHS.csv), [6-world result JSON](R320_EXACT_6_FIRST_HIT_WORLDS.json), [generator and 35 tests](r320_exact_absorbing_walk.py), [independent DP audit](../catalogue_audit/independent_r320_absorbing_walk_audit.py), [three-job CI](../../.github/workflows/r320-absorbing-walk-384-paths-e1.yml).

Scientific evidence level: only finite **E1 mathematical analogue**, no human E2, historical E3, original model empirical validation or external forecasting. R073 and PESEN v0.1 remain frozen.
