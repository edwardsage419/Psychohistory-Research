# R326 scientific report: finite hierarchical Bayesian cross-group borrowing

Date 2026-10-24. Original239 **02-007 Hierarchical Bayesian Learning** (P2). Scientific grade **PASS_BOUNDED_E1_FINITE_HIERARCHICAL_BAYES_POOLING_ONLY**.

## Original English sources and existing work
Tenenbaum, Kemp, Griffiths and Goodman (2011), *How to Grow a Mind: Statistics, Structure, and Abstraction*, Science 331:1279–1285, DOI 10.1126/science.1192788. Perfors, Tenenbaum, Griffiths and Xu (2011), *A Tutorial Introduction to Bayesian Models of Cognitive Development*, Cognition 120:302–321, DOI 10.1016/j.cognition.2010.11.015. These papers explain hierarchical Bayesian cognitive modeling, with a much broader range of representational assumptions than the finite construction here.

R112 single-group Bayesian belief updating and Beta-Bernoulli conjugacy, and R179 posterior calculations, provide generic probability arithmetic. R301 changepoint inference is a different latent mechanism. No itemwise existing hierarchical cross-group model was verified for 02-007 in original239 v4.3. Exhaustive historical ZIP reuse review remains open.

## Frozen model and original artificial data
[Prescore freeze commit 5be3b4f7](https://github.com/edwardsage419/Psychohistory-Research/commit/5be3b4f7ba1035fb8a655fc8a4a0263e92154cad) preceded [original source and data commit 2eeeb356](https://github.com/edwardsage419/Psychohistory-Research/commit/2eeeb3564886d3d2f3039742bb15b3f0e704cfab).

A global latent regime Z in {L,H} has prior 1/2. Conditional on Z, three independent group probabilities theta_g are each either 1/4 or 3/4, with conditional high-theta probability 1/4 if Z=L and 3/4 if Z=H. Each group generates two iid Bernoulli observations conditional on its theta. All 64 six-bit histories were exhaustively enumerated, each assigned enumeration weight 1/64 solely for exhaustive source coverage. Posterior evidence uses the exact model likelihood, never that enumeration weight. Source contains full exact global posterior, three hierarchical group predictions and three independent-group baseline predictions.

## Exact results
With group1 history (0,1) fixed, groups 2 and 3 all successes give P(Z=H|history)=49/58 and group1 next-success prediction **17/29**. When groups 2 and 3 are all failures, P(Z=H|history)=9/58 and group1 prediction **12/29**. The independent group1 comparator remains **1/2** in both cases. Thus cross-group evidence changes a local posterior prediction under the frozen finite hierarchical prior.

Across 64 artificial histories, the global high-regime posterior ranges from **27/370** to **343/370**, with seven distinct values. All-history exact checks confirm global posterior invariance under group permutation, prediction permutation under group swaps, and complementary posterior/prediction symmetry under flipping all six observed bits. The findings are algebraic consequences of the constructed prior and likelihood.

## CI, independent audit and acceptance
[GitHub Actions run 40022140444](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/40022140444) completed **success**. Three jobs passed: Python 3.11 unit (24 tests), Python 3.12 unit (24 tests), and independent Python 3.11 no-import auditor. The auditor independently enumerated both regimes and eight group-theta assignments for every one of 64 histories, reproduced exact CSV rows, JSON witness and invariances. The machine receipt records source Git blob identities.

## Scientific boundaries
This is a project-defined finite discrete hierarchical Bayes E1 mechanism. No human cognitive observations, inferred actual human priors, original article participant reanalysis, population generalization, independent predictive E2, historical E3 or causal psychological interpretation. The model's cross-group borrowing is conditional on its deliberately fixed shared latent regime. Existing 173 provisional README links and early ZIP content remain subject to separate itemwise audit. R073 and PESEN v0.1 frozen. Taxonomy, fusion and personal decision system deferred.
