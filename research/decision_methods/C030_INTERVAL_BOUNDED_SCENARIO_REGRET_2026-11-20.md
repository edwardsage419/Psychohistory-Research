# C030: Interval-bounded scenario regret without invented probabilities

Date: 2026-11-20 Asia/Singapore. Status: SYNTHETIC_ANALYTIC_CANDIDATE. Independent acceptance NOT_RUN.

## Decision gap and relationship
C028 gates hard constraints and C029 ranks options with complete point-valued scenario utilities. This addendum covers scenario utilities available only as defensible intervals. It must not convert interval midpoints into observations or assign scenario probabilities. Only C028 ACCEPT options enter guaranteed-feasible comparison; UNRESOLVED options receive separate conditional analysis.

## Inputs and assumptions
Finite feasible options A and scenarios S. Each utility cell u(a,s) is known to lie in a closed interval [L(a,s),U(a,s)], L<=U, on one comparable user-confirmed scalar utility scale. All scenarios share a specified horizon. Bounds describe uncertainty, not confidence intervals or calibrated probabilities. At least one feasible joint realization of the intervals must exist. A rectangular uncertainty set (each cell can vary independently within its interval) is needed for *sharp* cellwise bounds below; if dependence is known, the formulas remain conservative bounds when the joint set is a nonempty subset of that rectangle.

For a realized utility table, regret r(a,s)=max_b u(b,s)-u(a,s) = max(0,max_{b != a}(u(b,s)-u(a,s))). The b != a exclusion is essential because a cannot outperform itself.

For each a,s define lower regret bound:
r_low(a,s)=max(0,max_{b != a}(L(b,s)-U(a,s))).
Define upper regret bound:
r_high(a,s)=max(0,max_{b != a}(U(b,s)-L(a,s))).
For a singleton option, both bounds are zero. For any consistent realization, r_low <= r <= r_high. Under independent rectangular uncertainty these bounds are sharp for the individual (a,s) cell. For the worst-scenario regret R(a)=max_s r(a,s), the enclosing interval is [max_s r_low(a,s), max_s r_high(a,s)]. Under rectangular independence these endpoints are sharp for each individual option, although different options' extreme values need not occur in the same realization.

A cautious upper-bound rule chooses the option(s) with smallest max_s r_high(a,s), explicitly labeled *minimize worst-case regret upper bound*. This is conditional on the supplied scenarios, options, scale, and bounds. Do not call it a unique rational choice. Strong separation of realized worst-regret values can be certified if an option's upper bound is strictly less than every competitor's lower bound. If intervals overlap, display unresolved ordering; the upper-bound rule may still rank candidates, but cannot claim realization-wise superiority.

## Reproducible synthetic case
Two scenarios S1,S2 and three C028 ACCEPT options. A: S1 [7,9], S2 [1,3]. B: S1 [5,6], S2 [5,6]. C: S1 [2,3], S2 [7,9].
For A, S1 regret [0,0] because even A's lower bound 7 exceeds B's upper bound 6 and C's 3; S2 regret [4,8] from C versus A. Worst-scenario regret A [4,8].
For B, S1 regret [1,4] from A versus B, S2 regret [1,4] from C versus B. Worst-scenario regret B [1,4].
For C, S1 regret [4,7] from A versus C, S2 regret [0,0]. Worst-scenario regret C [4,7].
Upper-bound rule selects B (4 versus 8 and 7). Its worst-regret upper bound equals A's and C's lower bound in this example, so strict realization-wise superiority is NOT established. Equality is not strict dominance.

## Baseline, missingness and failure
Simple baseline: choose based on interval midpoints and compute C029 point regrets. It can hide adverse combinations and must be labeled as a scenario assumption. A missing utility interval is UNKNOWN; no finite numerical regret upper bound may be inferred without an independently justified bound. Inconsistent intervals, incomparable utility units, unknown feasible set, unsupported interval coverage, scenario omissions, endogenous scenario changes, or conflicting joint restrictions invalidate a sharp-ranking claim. Narrower utility intervals can tighten regret enclosures but need not preserve the upper-bound winner. Adding feasible alternatives can raise regret bounds; removing alternatives can lower them. A scenario probability, expected regret, causal effect, or real-world accuracy cannot be inferred.

## Candidate independent acceptance
T1: reproduce every synthetic regret interval and the [4,8],[1,4],[4,7] worst-regret intervals.
T2: singleton option yields zero regret.
T3: point intervals collapse exactly to C029.
T4: if every option has the same utility interval in a scenario, the possible regret interval is [0,U-L], not necessarily zero; for identical *point* utilities it is [0,0].
T5: UNKNOWN, invalid intervals and incomparable units fail closed.
T6: distinguish weak equality of bounds from strict superiority.
T7: compare rectangular independent uncertainty with a coupled realization (e.g., all utilities share one additive scenario shock), where rectangle-based upper bounds can be loose.
T8: hard-constraint UNRESOLVED remains conditional and cannot be silently admitted as ACCEPT.

## Evidence and handoff
These are project-local mathematical deductions and synthetic cases, not a reproduction of an external theorem or empirical validation. Source dependencies: C028 and C029 on main, as read 2026-11-20. The research track supplies the candidate card. Independent acceptance track should derive bounds in a separate implementation and test T1-T8. Data track should examine provenance and whether joint restrictions or intervals are defensible. Development requires separate owner authorization. Analytic derivation COMPLETE; local program tests NOT_RUN; independent replication NOT_RUN; empirical validation NOT_RUN; scientific acceptance NOT_RUN. No personal data, paid APIs, CI, or frozen-protocol changes.
