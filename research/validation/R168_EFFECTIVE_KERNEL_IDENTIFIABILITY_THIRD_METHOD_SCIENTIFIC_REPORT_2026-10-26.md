# R168 third-method scientific report: complete kernel observational equivalence

Date: 2026-10-26. Evidence E1 synthetic only. Additive study after the existing bounded R168 E1 acceptance. Protocol: [frozen audit](../../protocols/R168_EFFECTIVE_OPPORTUNITY_KERNEL_IDENTIFIABILITY_AUDIT_FREEZE_2026-10-26.md), commit `8cc8f44bf64bc630874f12c540c64e1a2ced0c4d`. Original frozen data: `research/R168/R168_EXACT_RESULTS.json`, Git blob `053c7fb851638e4ec4f0838afff7ee78603d2818`. No original human data or original-author equations were analyzed.

## Mathematical result
In the project-authored 3-level group-maximum process, let m be the effective number of independent copying opportunities (m=N for full_pool; m=1 for single_channel). Let individual fidelity f and innovation probability u be as in the original frozen program. Define the two **effective** parameters

`A=(1-u)^m`, `B=(1-f)^m`.

The entire observable transition matrix, with rows and columns indexed by skill frontier 0,1,2, is exactly

```
        [ A,     1-A,      0 ]
K   =   [ A*B,   A*(1-B), 1-A ]
        [ 0,       B,     1-B ]
```

Thus even complete knowledge of the one-step 3x3 group transition kernel determines at most A and B. If m is unknown, a continuum of (m,u,f) combinations with the same effective parameters generates identical kernels whenever transformed parameters remain admissible. Any finite-length sequence of group-frontier observations from the same starting state then has identical likelihood under those equivalent kernels. This is a **structural** nonidentifiability result for this invented model. No claim is made about individual human learning or the disputed original Derex group-size experiment.

## Executed checks
The exact BigInt rational replay independently reconstructed all 32 archived transition matrices from (f,u,m) through the two effective parameters, verifying **288 of 288 cells**. It also propagated the 64 archived worlds through all five archived timepoints and compared **960 of 960 state probability cells**, exactly. The 32 parameter rows yield **16 distinct full kernels**, identical to the 16 classes induced by (A,B). **23 of 32 parameter rows** lie in non-singleton equivalence classes; **9 are singleton rows**. Class sizes: `[5,4,4,4,2,2,2,1,1,1,1,1,1,1,1,1]`. Across 64 initial-state worlds there are 27 distinct complete five-time probability paths.

The zero-innovation counterfactual `(m=2,f=1/2,u=0)` versus `(m=1,f=3/4,u=0)` produces exactly the same entire matrix, extending the previously documented equality of one retention statistic. With positive innovation `u=1/8` and `f=1/2`, m=1 versus m=2 produces different matrices. The 16/23 counts were **seen in exploratory archive inspection before the audit freeze**, so they are reported as confirmed descriptive counts, not prospective discoveries.

Executable program: [third method](r168_effective_kernel_third_method_20261026.js). [Full machine receipt](R168_EFFECTIVE_KERNEL_THIRD_METHOD_EXACT_RECEIPT_2026-10-26.json) includes every kernel equivalence class and original source identity. An independently coded, parameter-blind observable-matrix reconstruction is archived under `research/evidence_audit/`.

## Scientific boundaries and disposition
These are 32 parameter rows representing a finite synthetic design, not 32 independent human experiments. The complete-kernel assumption is idealized; estimation uncertainty from finite human observations would add difficulties. No new out-of-sample predictive scores, probability calibration, session-level bootstrap, human E2, historical E3, or external independent replication was produced. Existing R168 `CLOSED_BOUNDED_E1` is preserved. Human data access remains blocked and source-independent causal claims remain unresolved. R073 and PESEN v0.1 remain frozen. The original239 v7.8 crosswalk and 154-item audit queue were read and left unchanged. No paid compute or GitHub Actions was started.