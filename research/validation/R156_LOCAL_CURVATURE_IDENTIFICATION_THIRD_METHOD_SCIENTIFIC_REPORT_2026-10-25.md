# R156 third method: exact local capital curvature and parameter identification

Date 2026-10-25 UTC+08. Scientific status: **PASS_BOUNDED_INTERNAL_EXACT_E1**. The original R156 96-world CLOSED_BOUNDED_E1 and its CI acceptance remain intact. This is a project-authored reduced-form mathematical experiment, with no new empirical growth claims.

## Protocol and model
[Prescore freeze](R156_LOCAL_CURVATURE_IDENTIFICATION_PROTOCOL_FREEZE_2026-10-25.md), commit `15fe8c3df41870a02dd537de4a7fbc3e614c6d85`, preceded computation. Original source blob `96ecbc18053cd2f3fcea59a68a753975a471ef66`. Reuse original 96 scenarios exactly: alpha 1 or 1/2; k0 1,4,9; savings 1/10,1/5,2/5,3/5; depreciation 0,1/10,1/5,2/5. The physical stock satisfies `k'=s*k^alpha-delta*k`.

Observe the initial capital level k0, flow `v=k'(0)`, and acceleration `a=k''(0)`. Direct chain rule gives `a=(s*alpha*k0^(alpha-1)-delta)*v`. All calculations are exact rational arithmetic with integer-square-root k0 for alpha=1/2. [Executable source](r156_local_curvature_exact.py), [all 96 exact rows](R156_LOCAL_CURVATURE_96_WORLD_EXACT_RECEIPT_2026-10-25.json).

## Actual results
| Fixed model family | Worlds | Stationary v=0 | Distinct classes with (k0,v) | Distinct classes with (k0,v,a) | Worlds ambiguous under three observations |
| --- | ---: | ---: | ---: | ---: | ---: |
| AK alpha=1 | 48 | 9 | 30 | 30 | 30 |
| Concave alpha=1/2 | 48 | 6 | 35 | 45 | 5 |

For AK, `v/k0=s-delta` and `a=(s-delta)*v`; observing acceleration adds no independent information about the savings and depreciation decomposition. The 48-world finite grid still contains 18 singleton classes; uniqueness within a finite grid does not imply continuous-parameter identification.

For concave alpha=1/2 with v!=0, `s=2*sqrt(k0)*(v/k0-a/v)` and `delta=s/sqrt(k0)-v/k0`. **All 42 nonstationary concave worlds** recover the two parameters exactly. Of six stationary concave worlds, five lie in two multiworld classes (sizes 2 and 3); the remaining stationary world is a finite-grid singleton. In the continuous parameter space, a stationary observation constrains only the ratio of savings and depreciation, so it remains nonidentifying even for the grid singleton.

The frozen off-grid counterexample at k0=1: AK pairs (s,delta)=(1/5,1/10) and (2/5,3/10) both have v=1/10 and a=1/100, and identical complete stock paths. Under alpha=1/2 they retain v=1/10 but acceleration differs: 0 versus -1/100.

## Independent implementation
The B implementation [r156_b_transformed_capital_audit.py](../evidence_audit/r156_b_transformed_capital_audit.py) derives derivatives separately from `x=sqrt(k)` with `x'=(s-delta*x)/2`, `x''=-delta*x'/2`, `k'=2xx'`, `k''=2(x')^2+2xx''`; AK is checked using its exponential growth derivative. All **96 rows matched exactly**, including 15 stationary worlds. A deliberately wrong concave calculation that drops `2xx''` was detected in all 30 worlds with delta>0 and nonzero x'. An initial local test mistakenly hardcoded mutant count 31 and failed; it was corrected to 30 before committing the audit code. No outcome, original grid, or prescore hypothesis changed. [B machine receipt](../evidence_audit/R156_B_TRANSFORMED_CAPITAL_AUDIT_RECEIPT_2026-10-25.json).

## Evidence boundary
Ideal instantaneous flow and acceleration with known model family and known origin are assumed. GDP measurements, time aggregation, noise, policy endogeneity, equilibrium feedback, model uncertainty, heldout prediction, calibration and historical external validation are outside this result. The rich original Romer/Rebelo papers and author data were not newly reproduced. E1 bounded internal pass; new E2=0; new E3=0; external independent team replication=0. Original R156 closure, original239 index and 154-item queue remain unchanged. R073 and PESEN v0.1 remain frozen. No paid resources or requested Actions execution.
