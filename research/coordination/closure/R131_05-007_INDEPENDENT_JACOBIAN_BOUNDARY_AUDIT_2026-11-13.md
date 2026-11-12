# R131 / original 05-007: independent exact Jacobian audit

Date: 2026-11-13. Track: closure. Starting observed recent main commit: `cf6d56ced27d7b7b04e2e6d9bfc6f678bb94d9d0`. Source: `research/R131/R131_FINAL_ACCEPTANCE_STATUS.json`, blob `3fa4bc6657ae38ee306e106dbd98f21edd48451b`. Primary reference: Taylor and Jonker (1978), DOI 10.1016/0025-5564(78)90077-9. This is a fresh algebraic check of receipt values, not an independent original-author simulation reproduction.

## Reproducible exact calculation

Use Python 3 with SymPy installed in an existing local environment. Let `z=1-x-y`, `v=(x,y,z)`, `f=A*v`, and `avg=v.T*f`. Compute the two-dimensional continuous replicator field `g_i=v_i*(f_i-avg)` and the discrete-generation map `h_i=v_i*(1+f_i)/(1+avg)` for i=0,1. Differentiate each with respect to x,y and substitute the stated equilibrium.

```python
import sympy as s
x,y=s.symbols('x y')
v=s.Matrix([x,y,1-x-y])
cases=[
 ('example1',s.Matrix([[-s.Rational(1,2),1,-1],[-1,-s.Rational(1,2),1],[1,-1,-s.Rational(1,2)]]), (s.Rational(1,3),s.Rational(1,3))),
 ('example2',s.Matrix([[2,1,5],[5,1,0],[1,4,3]]),(s.Rational(3,7),s.Rational(11,35)))
]
for name,A,(px,py) in cases:
 f=A*v
 avg=(v.T*f)[0]
 g=s.Matrix([v[i]*(f[i]-avg) for i in range(2)])
 h=s.Matrix([v[i]*(1+f[i])/(1+avg) for i in range(2)])
 for label,field in [('continuous',g),('discrete',h)]:
  J=s.simplify(field.jacobian([x,y]).subs({x:px,y:py}))
  print(name,label,J.tolist(),'trace',s.trace(J),'det',s.factor(J.det()))
```

## Actual independent output

* Example 1 continuous: J = [[1/6,2/3],[-2/3,-1/2]], trace -1/3, determinant 13/36.
* Example 1 discrete: J = [[6/5,4/5],[-4/5,2/5]], trace 8/5, determinant 28/25. The determinant exceeds 1, so the fixed point is linearly unstable in discrete time, despite the continuous-time trace being negative with positive determinant.
* Example 2 continuous: J = [[-291/245,-60/49],[2013/1225,33/49]], trace -18/35, determinant 297/245.
* Example 2 discrete: J = [[556/847,-300/847],[183/385,92/77]], trace 224/121, determinant 1268/1331. These two discrete numbers are additional bounded diagnostics, absent from the referenced final acceptance summary.

All six continuous and example-1 discrete trace/determinant quantities match the referenced acceptance JSON exactly. Example-2 discrete trace and determinant are new exact diagnostics and require separate interpretation before inclusion in any formal acceptance claim. Both cases use the original-source matrices transcribed in the receipt; upstream paper typesetting was not independently re-read in this run.

## Scientific disposition

R131 research status remains CLOSED_BOUNDED. Original 05-007 itemwise status remains PROVISIONAL pending mainline disposition. Evidence is constructed exact algebra E1 only; no new human E2, historical E3, author simulation replay, or independent external-team replication. No frozen protocols, crosswalk, CI, or core code changed. No paid computation used. Next: verify original 1978 source page transcription and audit the 05-007 itemwise source coverage against the formal gate.
