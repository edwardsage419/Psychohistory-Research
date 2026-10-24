# R128 independent finite Frechet bound audit: scientific report

Date: 2026-10-24. Original239 05-004. Status: **BOUNDED_INTERNAL_E1_COMPUTATION_PASS / NEW_CI_NOT_VERIFIED / NO_GLOBAL_QUEUE_DECREMENT**.

## Source and frozen design

Reused the existing R128 Skyrms (2004) source and prior 70-test research, without modifying the original files. The primary publisher chapter is https://assets.cambridge.org/052182/6519/sample/0521826519ws.pdf . R128 original code Git blob `4695fb1d03fc9e004f91e993907e9b165f90cc52`. This new finite audit follows `R128_THIRD_METHOD_FRECHET_JOINT_BOUNDS_PROTOCOL_FREEZE_2026-10-24.md`, committed **before** the new source and computation. Its n-person all-or-nothing participation rule is a project-created extension, not an empirical rule claimed by Skyrms.

## Actual reproducible computation

The complete source `r128_frechet_joint_bounds_third_method.js` was fetched back from GitHub and executed in an isolated JavaScript V8 environment with its unchanged `runAudit` function. No original R128 Python helper generated its outcomes. Archived source Git blob: `918c24512430bc5a62bcce12bd1d4f9840ed5643`. It generated `R128_FRECHET_JOINT_BOUNDS_42_CASES_2026-10-24.csv`, Git blob `bce009b4a1d5646d68f236de8cd1300e332eb694`. After submission, both files were fetched again and the **entire CSV matched a fresh execution byte for byte**.

For n=2..8 and six frozen marginal probabilities p=0,1/4,1/2,3/4,4/5,1, all **42** cases passed exact integer constructive lower and upper bound tests. Each construction has D equally weighted atoms, with D equal to the reduced denominator of p. Lower constructions place failure sets on consecutive cyclic atoms; upper constructions use perfectly coincident success sets. Exact per-agent marginal checks: **336**. The iid joint success p^(n-1) lay within the bounds in all 42 cases. Two deliberately corrupted counts were rejected.

Decision identification counts across 42 cases: **8 S**, **21 H**, **1 exact TIE**, **12 AMBIGUOUS**. An independent local Python `fractions.Fraction` formula calculation reproduced these four category totals. The separate Python cross-check did not download the archived CSV or execute the JavaScript source; it corroborated the mathematical classification totals by a different implementation.

Frozen examples passed:
* n=3,p=4/5: joint all-stag lower=3/5 and upper=4/5. At the lower bound, expected stag payoff=12/5<3 (choose hare); at the upper bound, expected stag payoff=16/5>3 (choose stag). Same individual marginals allow opposite decisions.
* n=2,p=4/5: lower=upper=4/5, choose stag in either case.
* n=3,p=3/4: lower=1/2 gives hare, upper=3/4 gives exact tie.

The bounds are sharp: for k=n-1 agents with common marginal p, `max(0,k*p-(k-1)) <= P(all k choose stag) <= p`. The two explicit finite constructions attain both endpoints in every tested case. Therefore the 12 ambiguous cells are actual observational nonidentification under the stated marginals, rather than numerical uncertainty.

## Scientific interpretation and limitations

The original R128 had three specific correlated examples for n=3,p=4/5. This extension establishes constructive sharp bounds on the frozen 42-case grid for n=2..8 and identifies where the decision changes as dependence varies. It is a finite mathematical mechanism result, **E1 synthetic only**. It does not estimate human beliefs, population correlations, real-world group cooperation, out-of-sample prediction or causal effects. External-team replication absent. New E2=0 and E3=0. R073 and PESEN v0.1 were left unchanged.

## Acceptance and CI status

Internal computational verdict: `PASS_BOUNDED_INTERNAL_EXACT_FRECHET_CONSTRUCTION_E1`. This verdict is limited to the archived V8 execution, independently generated CSV and local exact-fraction classification cross-check. No GitHub Actions run was initiated for this new script and no CI run ID or job logs exist for this extension. The prior R128 historical CI receipt is a different study and must not be relabeled as a new CI run. Formal CI-backed third-method acceptance remains **PENDING**. The original239 queue stays at 157 because R127 is still pending and R128 has no new CI-backed itemwise acceptance.

No paid services, GPUs, paid runners or proprietary data were used. The project order remains R-series research, then unified classification, then model fusion. Personal decision-product work remains paused.
