# R313 Scientific Report: Axelrod Cultural Dissemination, exact local-copy E1

Date: 2026-10-24 Asia/Taipei. Catalogue: **04-014, P1**. Research: **R313**. Strict scope: **artificial exact one-step E1**; new human E2 **0**, historical E3 **0**.

## First-party mechanism and fixed protocol

Primary paper: Robert Axelrod (1997), *The Dissemination of Culture: A Model with Local Convergence and Global Polarization*, *Journal of Conflict Resolution* 41(2):203–226, https://doi.org/10.1177/0022002797041002001 . Independent model description: JASSS https://www.jasss.org/12/1/6/appendixB/Axelrod1997.html .

Frozen before creating any result: [R313 prescore protocol](../../protocols/R313_AXELROD_THREE_SITE_TWO_FEATURE_EXACT_ONE_STEP_PRESCORE_FREEZE_2026-10-24.md), Git commit `8b69fc8c73a850279a3fac1a5e9314a3374c6d52`.

Three spatial sites connected in a fixed path 0↔1↔2, two binary discrete features for every site. The model samples an **active** site uniformly and then a neighbor uniformly, whose trait may be copied by the active site. Cultural overlap m is the count of features agreeing. If d=2−m>0, copying any particular differing feature has conditional probability (m/2)/d. If m=0 or d=0, no copying occurs. This is the original similarity-dependent interaction mechanism with one-feature *directional copying*. No real-valued confidence interval, threshold distance update, simultaneous average, or bidirectional midpoint is used.

Enumerate **64 complete artificial initial worlds**, **4 oriented interactions per world** and **2 potential feature atoms per oriented interaction**, thus **256 oriented contacts** and **512 atomic source rows**. Directed contact selection weights: (0,1)=1/3, (1,0)=1/6, (1,2)=1/6, (2,1)=1/3. Exact `fractions.Fraction` prevents floating-point approximation.

## Exact mechanistic findings within frozen finite domain

* 16 of 64 worlds are one-step absorbing. Each adjacent pair must either share both features or none. Two nodes on a connected geographical path can remain completely culturally different because zero-overlap neighbors never copy; structural proximity alone does not force uniformity.
* 128 of 512 potential feature atoms have strictly positive copying probability. Other atoms represent identical/dissimilar or the matching feature for a partly similar pair, whose trait cannot be copied.
* Every full next-state probability distribution has exact mass 1 and no negative entries. An event changes at most one feature of its **active** agent. Copying makes the selected active-neighbor pair one feature more similar and leaves the neighbor untouched.
* Exact witness: world 1 has state `00|00|01`. Its one-step distribution is world 0 `00|00|00` with probability 1/6, unchanged world 1 with probability 3/4, and world 5 `00|01|01` with probability 1/12. The asymmetry comes from differing active-site selection weights, not symmetric dyadic compromise.
* Nonlocal local-edge effect: from world 1, choosing active site 1 and neighbor 2 copies feature 1. The selected edge (1,2) similarity rises from one match to two, while the other adjacent edge (0,1) falls from two matches to one. Pair-level convergence need not improve *all* adjacent relationships.

This finite 2-feature/3-agent case does **not** estimate the paper's long-run cultural-domain distributions, changes in polarization with territory/feature/trait size, convergence time, or any empirically identified causal effect. The specific finite path can impose invariants absent in other graphs. A source record is a synthetic counterfactual potential event, never a human respondent.

## Artifacts and independent verification

* [512 fixed feature atoms](R313_ALL_512_ORIGINAL_FEATURE_SOURCE_ATOMS.csv), every row has source world, actor, neighbor, candidate feature, trait values, overlap, oriented weight, conditional and unconditional copying probabilities and target world.
* [Complete 64 next-state probability distributions](R313_EXACT_64_WORLD_ONE_STEP_RESULTS.json).
* [Main exact generator with 29 named unit tests and full replay](r313_exact_axelrod.py).
* [Independent full-source auditor](../catalogue_audit/independent_r313_source_audit.py), does not import the main model code, independently reconstructs the whole 512-source table and each of 64 outcome distributions.
* [CI definition](../../.github/workflows/r313-axelrod-exact-one-step-e1.yml) executes Python 3.11, Python 3.12 and a third independent audit job.

Acceptance gate requires **all three CI jobs to complete successfully and the archived sources to replay**. The acceptance status is set only after live confirmation; file presence alone is insufficient.

## Boundary to subsequent original239 work

Only 04-014 may receive new R313 provenance if CI passes. The complete original239 scientific closure gate remains OPEN, as do 33 prior source gaps until separately audited. R073 and PESEN v0.1 remain frozen. Complete R series first, then classify, and finally undertake original fusion.
