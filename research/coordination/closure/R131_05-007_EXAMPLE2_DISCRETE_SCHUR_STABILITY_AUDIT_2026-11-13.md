# R131 / 05-007: independent discrete-time stability gate for example 2

Date: 2026-11-13. Track: closure. Observed main at start: `b25ddca6362d2e3f922c1a7f5a690e9eb9c202cb`.
Source acceptance: `research/R131/R131_FINAL_ACCEPTANCE_STATUS.json`, blob `3fa4bc6657ae38ee306e106dbd98f21edd48451b`.
Prior independent Jacobian report: `research/coordination/closure/R131_05-007_INDEPENDENT_JACOBIAN_BOUNDARY_AUDIT_2026-11-13.md`, blob `803b1ce48bc019f4535722741928ee5f87b61cfb`.
Primary paper: Taylor and Jonker (1978), DOI 10.1016/0025-5564(78)90077-9. The original PDF was not re-read in this audit.

## New exact decision from previously computed Jacobian

For example 2 with alpha=1, payoff matrix `[[2,1,5],[5,1,0],[1,4,3]]` and equilibrium `(3/7,11/35,9/35)`, the prior audit derived the discrete-generation Jacobian with trace `T=224/121` and determinant `D=1268/1331`. Independently check the characteristic polynomial `lambda^2-T lambda+D` with exact fractions. The discriminant is `T^2-4D=-5616/14641 < 0`, so eigenvalues are conjugate. Their squared modulus is `D=1268/1331 < 1`, proving local asymptotic stability of the fixed point for this particular discrete-generation map. The exact second-order Schur checks independently give `1-T+D=135/1331>0`, `1+T+D=5063/1331>0`, and `1-D=63/1331>0`.

Executable standard-library-only verification:

```python
from fractions import Fraction as F
T, D = F(224, 121), F(1268, 1331)
assert T*T-4*D == F(-5616, 14641)
assert 1-T+D == F(135, 1331)
assert 1+T+D == F(5063, 1331)
assert 1-D == F(63, 1331)
assert D < 1
print("example2 discrete: complex conjugate eigenvalues, modulus squared", D)
print("Schur margins:", 1-T+D, 1+T+D, 1-D)
```

Expected output:
```text
example2 discrete: complex conjugate eigenvalues, modulus squared 1268/1331
Schur margins: 135/1331 5063/1331 63/1331
```

This resolves the interpretation explicitly left open in the previous Jacobian audit. It is a bounded local linear stability claim for the project's specified discrete-generation map. It does not imply ESS, global stability, or author-original simulation reproduction. In fact the acceptance receipt records an example-2 mutant with positive invasion advantage `3/350` and ESS=false. Thus local stability of this fixed point is compatible with its failure of the ESS criterion under the recorded model.

## Scientific disposition

The new check is mathematical E1 only. R131 remains CLOSED_BOUNDED, original 05-007 remains PROVISIONAL pending itemwise mainline adjudication. No new E2/E3, no original-author replay, no CI, no external-team validation. No frozen code, crosswalk, or protocol modified. Next: compare the original 1978 paper's example-2 matrix and discrete update definition against the transcribed acceptance source before raising any source-fidelity claim.
