# R065 Phase I — Fixed-sample beta-profile robustness protocol

Date: 2026-10-16. Submitted before any Phase I numeric calculations. This is **post hoc** to R065 H; **not an independent study**.

Sources: preserve exactly the ten raw author files, paths, individual Git blob SHA1s, upstream commit and objective function semantics already frozen in `protocols/R065_PHASE_H_MODEL3_SENSITIVITY_2026-10-16.md`. Sample selection cannot change. The two reset rules are fixed: author [23,45,67,89,111] and task-block boundary [18,35,52,69,86,103,120]. Observe/play handling is exactly model_3_objective with its available-boat check, raw softmax scores [1,0] when last observed boat available, otherwise uniform. No trial exclusions and no parameter changes other than β.

**Data-reducing representation:** For each participant and reset scheme, count scored play choices as MATCH (recent observed action available and selected), MISMATCH (recent observed action available but unselected), UNIFORM (no relevant observed action). The original per-play likelihood for parameter β with these counts is fully determined by these counts:
NLL(β) = MATCH * log(1 + exp(-β)) + MISMATCH * log(1 + exp(β)) + UNIFORM * log(2), with the exact original `+1e-10` probability floor applied when reporting source-objective NLL. This is an analytic equivalence, not a new model.
We will publish **only totals across all ten participants for each reset scheme**, and optionally aggregate leave-one-participant-out metrics, not participant-level count vectors, experiment rows, survey fields or IDs.

**Four analyses:**
1. Verify ten fixed raw source identities; derive MATCH/MISMATCH/UNIFORM counts in the GitHub-connected execution environment. Compare β=5 NLL to Phase H at tolerance 1e-8; fail closed if inconsistent.
2. Produce objective profiles for the preselected β in [0,0.5,1,2,3,5,10,20,30], identical in both schemes, reporting per-play mean NLL, and selected trial proportions.
3. Optimize β independently for each reset rule on all ten using β∈[0,30], minimizing exact original `-log(p+1e-10)` sum, deterministic bounded scalar minimization; also report analytic unconstrained optimum `log(MATCH/MISMATCH)` clipped to [0,30] as a cross-check. If MISMATCH=0 or MATCH=0 handle boundaries. In-sample optimized comparison is not valid generalization evidence.
4. **Leave-one-person-out** (ten folds): separately fit β on nine other participants' sufficient counts under each rule, compute heldout source-objective NLL on the tenth, accumulate overall per-play NLL; do not use heldout labels in the fitted β. Never claim independent model selection, random sample, significance, or seven-model refit.

**Safeguards:** Report β=0 degeneracy (all play choices uniform) as a common anchor; if two fitted schemes select β≈0, report information collapse rather than misrepresenting it as recovered cognitive mechanism. The source code's transform restricts β to [0,30] but uses numerical constraints; mark any boundary solution. Test locally using synthetic subject-level count vectors and an exhaustive formula vs per-trial softmax comparison. Python code must fail closed on wrong source Git blob for raw-file mode and on malformed counts for count-only test mode. Raw individual CSV not redistributed.

Evidence class: `CONNECTOR_RAW_MODEL3_COUNTS + LOCAL_AGGREGATE_REPLAY`, not author native code or fit. `R065_FULL_GATE=OPEN`, `PESEN_v0.1=FROZEN`.
