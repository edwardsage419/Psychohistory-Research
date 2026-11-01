# R257 ninth nonconvex world: independent exact fraction audit

track: R/B
subflow: independent scientific verification
run_date_utc: 2026-11-01T22:44Z
observed_main_before_write: 8a88b82d23c1d15843840ce0d622ca3749ee1837
target_key: (R/B,R257 original source 225,2026-10-23 prescore freeze,nonconvex ninth-world 25-row arithmetic)
status: COMPLETE_BOUNDED_INTERNAL_E1; FORMAL_R257_S53_ACCEPTANCE_PARTIAL
ci_status: NOT_RUN
billing_checked: ACCOUNT_NOT_VERIFIED
original239_queue_change: 0

## Frozen scope and exact sources

Read the original R257 prescore freeze, R257 original source README, original CSV and JSON, prior R257 S53 source-link audit and its independent checker, and current original239 v7.8 and pending154 identities. Prior R257 S53 independent source-link checker verified all 225 grid identities, but explicitly left the ninth nonconvex world's objective and gradients as structure-only. This run fills that narrow gap without repeating its 200 convex-row checks or Codex PR #3 strict S53 KKT work.

Inputs read through the connected GitHub repository at the checked main state:

* `research/R257/R257_ALL_225_ORIGINAL_GRID_CANDIDATE_SOURCE_ATOMS.csv`, Git blob `63dc333cf4c4206fa466e0c0f33e3b079f4dc01b`.
* `research/R257/R257_EXACT_RESULTS.json`, Git blob `55c00defa893ba3ed36cc5d3a6b0144953f16301`.
* `protocols/R257_OPTIMIZATION_9_TRIANGLE_KKT_WORLDS_225_CANDIDATE_ATOMS_PRESCORE_FREEZE_2026-10-23.md`, Git blob `925be58bac3b9dfe045959f9bfaf5b2fe7889d35`.
* `research/validation/r257_s53_original225_source_link_gate_20261102.js`, Git blob `a4dfac449371aa259bcdabf4cc73c88e7e014135`, read only for prior coverage and nonduplication.
* original239 v7.8 crosswalk blob `36f24235901172642c46853298aebb421f1a3552`; pending154 queue blob `3b96d46b3d88ccafd779a08509c3cfd0e435772f`.

## Actually executed independent calculations

A fresh, in-memory JavaScript V8 BigInt rational evaluator was used, without importing the original Python R257 implementation or prior JavaScript source checker. Exact fraction comparison used cross multiplication, with no floating-point tolerance. It filtered the ninth world `NONCONVEX_KKT_NOT_SUFFICIENT` from the complete 225-row CSV.

For each of 25 original grid rows, independently calculated `f(x,y)=-(x-1/2)^2+(y-1/2)^2`, `grad=(-2(x-1/2),2(y-1/2))`, `slack=1-x-y`, `feasible=(x+y<=1)`, and checked design mass and nonconvex identity. All 25 objective values, both gradient components, feasibility flags, slack values and convexity labels agreed with the original archived CSV; 15 grid rows were feasible. Distinct grid positions: 25. Error count: 0.

Exact feasible grid minimum: `-1/4`, uniquely at `(0,1/2)`, matching archived JSON. Independent continuous global bound: for `0<=x<=1`, `-(x-1/2)^2>=-1/4`, while `(y-1/2)^2>=0`; the feasible point `(0,1/2)` attains the bound. The feasible stationary point `(1/2,1/2)` has zero gradient and value `0`, providing the archived nonconvex KKT insufficiency counterexample. Hessian `diag(-2,2)` and archived certificate values were checked.

Seven isolated in-memory negative controls were correctly rejected: changed objective, gradient, feasibility flag, capacity slack, convexity label, duplicate grid position and altered JSON stationary objective. All original source bytes remained unchanged. No random seed was used.

Actual run: connected JavaScript V8 in-memory independent calculation. Standalone native Node CLI on a complete local checkout: NOT_RUN. This report records the explicit formulas, source identities, tested controls and results. No claim is made that an independently archived executable was run.

## Scientific and operational disposition

`R257_NINTH_WORLD_25_ROW_EXACT_ARITHMETIC = PASS_BOUNDED_INTERNAL_E1`.
`R257_S53_ORIGINAL225_SOURCE_LINK_GAP_NONCONVEX_ARITHMETIC = ADDITIONAL_COVERAGE_COMPLETE`.
`R257_S53_HISTORICAL_B_BLIND_ORDER = FAIL` remains unchanged.
`R257_S53_FORMAL_FROZEN_ACCEPTANCE = PARTIAL`; Codex PR #1/#3 remain unmerged at initial review.
`original239_pending_net_change = 0`; no scientific itemwise closure was adjudicated.
`new_E2 = 0`; `new_E3 = 0`; `external_team_replication = NOT_RUN`.

A-track short scan: Zenodo record 10.5281/zenodo.10246248 describes 45,686 Axelrod-Python computer tournament results. It is generated agent data, so it cannot qualify as an independent human R073 E2 test cohort. No new original human data file was downloaded, schema-qualified or scored. R073 and PESEN v0.1 remain frozen.

No Actions, paid API, GPU, subscription, data purchase or cloud runner was initiated. Actual GitHub account billing and free quota were not independently inspected. Next P0 task remains full authentic R333 to R340 composite native receipt and mutation execution plus mandatory caller binding; R257 S53 requires a separate blind-order failure disposition.
