# C034 addendum: exact bounds under shared calibration and clipping

Date: 2026-11-20 Asia/Singapore. Status: SYNTHETIC_ANALYTIC_CANDIDATE. Independent acceptance NOT_RUN. Scope: intelligent decision hub dispatch and robustness certificates. This is a new calculation supplement to the existing clipping counterexample. No historical record or frozen protocol is changed.

## Question and inputs

For nominal scores A=(0.8,0.4), B=(0.5,0.8), user weight w in [0.60,0.65], shared objective offsets c1,c2 independently in [-0.30,0.30], and clipping T(z)=min(1,max(0,z)), find the *exact attainable* range of the weighted difference D=U(A)-U(B). The objective offsets are shared between options within an objective, but independent across objectives. All numbers are synthetic and have no empirical calibration.

## Exact derivation

Write f(c1)=T(0.8+c1)-T(0.5+c1) and g(c2)=T(0.4+c2)-T(0.8+c2). Then D=w f(c1)+(1-w)g(c2).

For c1 in [-0.30,0.20], f=0.3; for c1 in [0.20,0.30], f=0.5-c1. Therefore f ranges exactly over [0.2,0.3].

For c2 in [-0.30,0.20], g=-0.4; for c2 in [0.20,0.30], g=c2-0.6. Therefore g ranges exactly over [-0.4,-0.3].

Since w is nonnegative and no cross-objective offset dependence is assumed, the lower envelope at fixed w is 0.2w-0.4(1-w)=0.6w-0.4; the upper envelope is 0.3w-0.3(1-w)=0.6w-0.3. Both are increasing in w. Hence across w in [0.60,0.65]:

**Exact attainable D range = [-0.04, 0.09].**

Lower witness: w=0.60, c1=+0.30, c2=-0.30 gives D=-0.04. Upper witness: w=0.65, c1=0, c2=+0.30 gives D=+0.09. Continuity over the connected parameter box establishes attainability of intermediate differences. Both rankings are possible; neither option has a universal strict preference certificate. No reversal probability follows from this range.

## Sharp weight threshold and counterfactual scope

If the admissible weight interval is [p,q] with 0<=p<=q<=1, retaining these same score and offset ranges, the exact lower bound is 0.6p-0.4 and the exact upper bound is 0.6q-0.3. Universal strict A preference requires p>2/3; at p=2/3 a tie is feasible. Universal strict B preference requires q<1/2; at q=1/2 a tie is feasible. These statements hold for the specified independent c1,c2 box. They are *not* generic thresholds for other scores, transformation functions, or dependent offsets.

Simple baseline: nominal scores with no offsets yield D=0.7w-0.4, strictly positive on [0.60,0.65]. The baseline can disagree with the robust certificate. An unclipped shared-offset certificate is inapplicable once clipping is present.

## Dispatch, limits and acceptance preparation

Required inputs: confirmed feasible options, user-confirmed cardinal scales and compensatory weights, score transformation provenance, objective-specific shared-offset bounds, and a joint feasible set for offsets and weights. If clipping is confirmed, use clipping-aware joint optimization; if the transformation or dependencies are unknown, do not claim a universal certificate. Hard-constraint rejection remains prior to utility comparison. Do not interpret weight-space proportions as probabilities.

Independent acceptance candidates: reproduce both extrema and their witnesses; verify f and g breakpoints at c1=0.20 and c2=0.20; verify strict equalities at p=2/3 and q=1/2; compare dense sampling with analytic bounds; verify no-offset baseline; reject the unclipped cancellation shortcut; test correlated offsets with an explicitly restricted joint feasible set; propagate UNKNOWN when transformation or calibration bounds are missing; preserve user weight interval and hard constraints.

Failure conditions: changed clipping bounds, option-specific calibration errors, unknown dependence, nonlinear utility aggregation, incomparable objectives, unconfirmed weights, and unresolved feasibility. No original-paper reproduction, independent program verification, real-user calibration, predictive validation, or scientific acceptance is claimed. Independent acceptance track owns isolated computation and boundary tests. Data track owns empirical transformation and calibration provenance. Version development requires separate owner authorization.

Source: project-local exact derivation extending C034_ADDENDUM_CLIPPING_BREAKS_SHARED_ERROR_CANCELLATION_2026-11-20.md.