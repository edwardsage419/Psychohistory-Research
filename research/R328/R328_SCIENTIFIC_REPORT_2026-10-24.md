# R328 scientific report: exact scalar precision-weighted predictive error
Date: 2026-10-24. Original239 **02-010 Predictive Processing** (P2). Formal scientific grade: **PASS_BOUNDED_E1_SCALAR_PREDICTIVE_ERROR_ONLY**.

## Original English sources and reuse
Rao and Ballard (1999), *Predictive coding in the visual cortex: a functional interpretation of some extra-classical receptive-field effects*, Nature Neuroscience 2:79–87, DOI 10.1038/4580; Friston (2005), *A theory of cortical responses*, Philosophical Transactions of the Royal Society B 360:815–836, DOI 10.1098/rstb.2005.1622. The first article describes higher-level predictions and lower-level residual signals in a hierarchical visual network, with natural-image simulations. This study is only a scalar project-defined analogue, not a reproduction of those neural architectures or image experiments.

Checked R300 fixed HMM filtering, R112 Bayesian updating, R326 hierarchical Bayesian pooling and R327 costly sensing POMDP. Their checked reports do not verify this exact precision-weighted residual error gradient. Mathematical arithmetic may be reused, but no previous E1/E2 status transfers. Historical ZIP exhaustive content audit remains open.

## Prospective freeze, full artificial source and exact algorithm
Prescore protocol committed first as [cf240df27b0fa1391fb03be2e714e8d498ed83de](https://github.com/edwardsage419/Psychohistory-Research/commit/cf240df27b0fa1391fb03be2e714e8d498ed83de). Code, 120 source rows, 24-world JSON, independent auditor and CI committed later as [5a6a011a359c8528b5443ff61041876250e353fd](https://github.com/edwardsage419/Psychohistory-Research/commit/5a6a011a359c8528b5443ff61041876250e353fd).

Prior m in {0,1}, target y in {0,1,2}, prior precision r in {1,2}, sensory precision p in {1,2} define 24 artificial worlds. Initial estimate x0=m. The objective E(x)=(r/2)(x-m)^2+(p/2)(y-x)^2 is minimized by four exact-rational gradient steps of size 1/4. All five time points t=0..4 in each world are retained, giving 120 complete source rows. Each row records residuals, estimate, energy and analytic optimum. The model is fully deterministic; 120 rows do not mean 120 subjects.

## Frozen counterexamples and exact findings
For m=0, y=2, r=1, p=2, the analytic optimum is **4/3**, and the four-step estimate is **85/64**. For the same m,y with r=2,p=1, the optimum is **2/3**, and the four-step estimate is **85/128**. This finite example demonstrates that precision weights change the estimate toward prior or sensory target. Across all 24 constructed worlds, the objective energy never increases over any of the four gradient updates. When y=m, both residual errors remain zero and the estimate stays at m.

Independent no-import auditor reconstructs all 120 states from the closed-form recurrence x_t=x_star+(m-x_star)(1-(r+p)/4)^t and recomputes every energy and residual. A deliberate changed energy source field is rejected. Production replay reproduces CSV and JSON exact bytes.

## CI and acceptance boundary
[GitHub Actions run 40029363018](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/40029363018) completed success. Python 3.11 and 3.12 each passed seven unit methods plus exact byte replay; the third independent audit job passed. The [machine receipt](R328_MACHINE_RECEIPT.json) pins original source blob SHA identities. [Formal acceptance](R328_FINAL_ACCEPTANCE_STATUS.json) is limited to bounded E1.

This does not establish neural precision weighting, actual human predictive processing, Rao-Ballard visual receptive-field phenomena, hierarchical visual cortical simulation, real human E2, historical E3, parameter recovery or external prediction. R073 and PESEN v0.1 frozen. Original239 taxonomy, fusion and personal decision system deferred.
