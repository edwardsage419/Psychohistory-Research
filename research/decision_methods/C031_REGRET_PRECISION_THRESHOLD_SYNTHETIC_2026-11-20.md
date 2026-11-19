# C031: Precision threshold for certifying scenario regret ranking

Date: 2026-11-20 Asia/Singapore. Status: SYNTHETIC_ANALYTIC_CANDIDATE. Independent acceptance NOT_RUN.

## Decision gap and provenance
C029 gives point-valued scenario minimax regret. C030 gives interval regret bounds and a sufficient condition for realization-wise strict superiority. This card asks how narrow defensible utility bounds would have to become before that sufficient condition holds. This is a project-local algebraic exercise using C030 definitions, not an empirical information-value estimate or an external theorem replication.

## Inputs and scope
Assume three C028 ACCEPT options A, B, C; two fixed scenarios S1, S2; one comparable user-confirmed utility scale; and independent rectangular utility uncertainty. Point centers are A=(8,2), B=(5.5,5.5), C=(2.5,8). Each of the six cells has interval [center-e, center+e] for a common nonnegative uncertainty radius e, restricted here to 0<=e<=1. No probabilities are assigned. This uniform radius is an artificial measurement design, not a claimed attainable accuracy.

For a realized table, r(a,s)=max_b u(b,s)-u(a,s). Compute C030 bounds using competitors b!=a:
r_low(a,s)=max(0,max_{b!=a}(L(b,s)-U(a,s)));
r_high(a,s)=max(0,max_{b!=a}(U(b,s)-L(a,s))).
Worst-scenario interval for a is [max_s r_low(a,s),max_s r_high(a,s)].

## Analytic calculation
For 0<=e<=1, the worst-scenario regret intervals are:
A: [6-2e,6+2e].
B: [max(0,2.5-2e),2.5+2e].
C: [5.5-2e,5.5+2e].
All lower bounds are positive in the stated e range, so B simplifies to [2.5-2e,2.5+2e].

B's upper bound is strictly below both competing lower bounds exactly when
2.5+2e < min(6-2e,5.5-2e),
which reduces to e<0.75.

At e=0.5: A [5,7], B [1.5,3.5], C [4.5,6.5]. The strict separation test succeeds.
At e=0.75: A [4.5,7.5], B [1,4], C [4,7]. Equality with C's lower bound means strict separation is not certified.
At e=1: A [4,8], B [0.5,4.5], C [3.5,7.5]. The upper-bound rule still selects B, but strict realization-wise superiority is not certified.

This threshold certifies a sufficient robust comparison within the supplied rectangular set. It is not a necessary condition for B to win in a particular realized table. Dependence constraints may make C030 bounds loose and permit stronger certificates. Changing options, scenario coverage, utility scale, feasibility, or cell-specific precision requires recalculation.

## Decision workbench recommendation
Show (1) upper-bound rule winner, (2) whether strict separation is certified, (3) the specific inequality that would need to hold, and (4) the utility precision needed under an explicitly labeled hypothetical uniform-radius design. The numeric 0.75 is in synthetic utility units. It must not be presented as a required survey sample size, real-world measurement error, probability, causal benefit, or monetary value of information. Missing bounds remain UNKNOWN; C028 unresolved feasibility stays in a separate conditional comparison. The user retains value scale and decision authority.

Simple baseline: C029 on point centers, yielding worst regrets A=6, B=2.5, C=5.5 and choosing B. This baseline hides whether its ranking is robust to interval uncertainty.

## Candidate independent acceptance
T1 reproduce all three symbolic worst-regret intervals for 0<=e<=1.
T2 reproduce e=0.5, 0.75, and 1 tables independently, including equality at the threshold.
T3 test e=0.749 and e=0.751 on either side of the strict certificate.
T4 verify e=0 collapses to C029 point regret.
T5 check that changing any one center or radius invalidates reuse of the 0.75 threshold without recalculation.
T6 coupled-shock joint uncertainty: verify rectangle bounds remain conservative and can be loose.
T7 reject missing bounds, incomparable utilities, and C028 UNRESOLVED options from guaranteed-feasible ranking.
T8 distinguish the sufficient strict certificate from a claim of empirical validity or expected information value.

## Execution and handoff
Analytic derivation COMPLETE. Local independent arithmetic spot check for e=0,0.5,0.75,1 COMPLETE (not a formal automated test suite). GitHub archive status depends on successful commit and readback. Independent replication NOT_RUN. Empirical calibration NOT_RUN. Scientific acceptance NOT_RUN. Independent acceptance track owns isolated T1-T8 tests; data track owns whether real utility intervals and their dependencies are defensible. Version development requires separate owner authorization. No frozen R/PESEN changes, personal data, paid APIs, or CI.
