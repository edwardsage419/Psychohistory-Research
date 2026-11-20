# C034 addendum: bounded mismatch between objective calibration offsets

Date: 2026-11-20. Status: SYNTHETIC_ANALYTIC_CANDIDATE. Independent acceptance NOT_RUN.

## Decision gap and prior art

The C034 correlated-clipping supplement assumes exact equality c1=c2 and gives D in [0,0.055]. The independent-offset supplement allows arbitrary c1,c2 in [-0.30,0.30] and gives D in [-0.04,0.09]. Here the new question is whether a *bounded but nonzero* mismatch can preserve the weak or strict preference certificate. This is a project-local algebraic extension, not a claim of external empirical validation. Relevant prior files: C034_ADDENDUM_PERFECTLY_CORRELATED_CLIPPED_OFFSETS_2026-11-20.md and C034_ADDENDUM_EXACT_CLIPPED_OFFSET_BOUNDS_2026-11-20.md.

## Inputs and method

Synthetic scores A=(0.8,0.4), B=(0.5,0.8), first-objective weight w in [0.60,0.65]. Shared-within-objective offsets c1,c2 each belong to [-0.30,0.30], with an additional cross-objective mismatch constraint |c1-c2|<=delta, 0<=delta<=0.10. Clip T(x)=min(1,max(0,x)). Define

D(w,c1,c2)=w[T(0.8+c1)-T(0.5+c1)]+(1-w)[T(0.4+c2)-T(0.8+c2)].

The joint feasible set matters: independent interval arithmetic on the two differences discards the mismatch constraint and may be overly conservative.

## Exact extrema for 0<=delta<=0.10

For any fixed w>=0.60, the first difference f(c1) is nonincreasing, the second difference g(c2) is nondecreasing. Both are piecewise affine, with breakpoints at 0.20. The extrema of D over the clipped polygon are attained at polygon vertices and clipping-line intersections; D is affine in w for fixed offsets, so checking w endpoints suffices. Direct piecewise comparison gives:

min D = -0.4 delta, attained at w=0.60, c1=0.30, c2=0.30-delta.

max D = 0.055+0.35 delta, attained at w=0.65, c1=0.20, c2=0.20+delta.

At delta=0, recover [0,0.055]. At delta=0.05, exact attainable range [-0.020,0.0725]. At delta=0.10, recover [-0.04,0.09], the independent-offset envelope. Continuity of the connected feasible polygon and D gives all intermediate values. The min and max expressions are restricted to the specified delta range, clipping and weight interval.

## Consequences for decision dispatch

For the existing weight lower bound 0.60, any delta>0 permits B to beat A in some allowed realization. Exact equality of offsets yields weak A dominance with a feasible tie; a small positive mismatch eliminates that guarantee. A system must not replace a measured mismatch tolerance with exact correlation.

For generalized w in [p,q] subset [0.60,0.65], a conservative *sufficient* strict A condition under the same delta range is 0.5p-0.3-(1-p)delta>0, using f>=0.2 and g>=-0.3-delta near the minimum witness. For arbitrary p outside the specified weight range, re-optimize rather than extrapolate this condition. This is a candidate routing check, not a universal threshold for other score matrices.

## Baseline, limits and acceptance

Baseline 1: nominal uncalibrated scores yield D=0.7w-0.4 in [0.02,0.055], missing negative witnesses. Baseline 2: independent offsets yield [-0.04,0.09] for every delta and miss the precision gain at delta<0.10.

Inputs required for practical use: confirmed hard-constraint feasibility, cardinal scores, user-approved weight interval, clipping mechanism, both calibration ranges and an evidenced bound on |c1-c2|. If any are unknown, retain UNKNOWN or the wider valid envelope. Do not infer probability of a reversal from the size of the admissible set.

Independent acceptance should: (1) check both witnesses for delta 0, 0.05, 0.10; (2) independently enumerate polygon vertices and clipping intersections; (3) test w endpoints; (4) verify nested envelopes as delta increases; (5) verify a negative witness for any positive delta; (6) test clipping-bound changes; (7) reject treating mismatch tolerance as equality; (8) propagate unknown dependency; (9) verify hard-constraint filtering precedes utility ranking; (10) test floating-point tolerance near D=0.

Evidence: synthetic algebra and exploratory numerical grid only. No original-paper reproduction, independent program test, real-world calibration, predictive validation or scientific acceptance. Independent acceptance track owns isolated reproduction. Data track owns evidence for calibration mismatch. Version development requires separate owner authorization. R073, PESEN v0.1 and all frozen records remain unchanged.
