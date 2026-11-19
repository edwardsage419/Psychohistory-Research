# C028: Interval hard constraints and unknown feasibility (synthetic method card)

Date: 2026-11-20 Asia/Singapore. Status: SYNTHETIC_ANALYTIC_CANDIDATE. Independent acceptance NOT_RUN. Scope: personal decision workbench feasibility gate. Complements C004 hard-constraint example without altering its evidence status.

## Decision question
When a non-negotiable threshold is specified but an option's measured outcome is an interval, when may a workbench exclude, accept, or defer that option? An unknown outcome must not be silently converted to a safe point estimate.

## Inputs and assumptions
Finite options a; each user-confirmed lower-bound constraint j is x_j(a)>=L_j. For each option and constraint, evidence supports a closed interval [l_j(a),u_j(a)] with l<=u. Bounds are deterministic epistemic bounds, not calibrated probability intervals. Unknown or missing bounds are represented explicitly as UNKNOWN. For upper-bound constraints reverse inequalities. User sets thresholds and units. Each interval and threshold must share units, time horizon, population and scenario. Feasibility across all constraints uses conjunction.

## Three-valued algorithm
For a lower-bound constraint: CERTAIN_PASS if l>=L; CERTAIN_FAIL if u<L; POSSIBLE otherwise (l<L<=u). An absent interval is UNKNOWN, distinct from POSSIBLE. For an option: REJECT if any constraint is CERTAIN_FAIL; ACCEPT only if every constraint is CERTAIN_PASS; otherwise UNRESOLVED. Report which constraint caused each status. A strict > threshold requires separate equality handling. No compensatory weighted score may override REJECT. Only ACCEPT options proceed to guaranteed-feasible ranking. UNRESOLVED may be explored in conditional scenarios but never labeled safe.

## Worked synthetic example
A and B are two hypothetical plans. User-confirmed minimum reserve is L=6 units. A has reserve [5,9], B has [6,7]. A is UNRESOLVED, B ACCEPT. A's nominal midpoint 7 exceeds B's midpoint 6.5, but a midpoint ranking that recommends A as certainly feasible violates the hard constraint gate. If a later valid measurement narrows A to [6.2,7], A becomes ACCEPT; if it narrows A to [4,5.9], A becomes REJECT. These are hypothetical interval revisions, not real data or probabilities.

## Mathematical properties for independent acceptance
P1: For fixed L, shrinking [l,u] to a contained subinterval cannot change CERTAIN_PASS to CERTAIN_FAIL, or vice versa, unless the original evidence was internally inconsistent; an original POSSIBLE can resolve either way.
P2: Adding a hard constraint cannot turn a REJECT option into ACCEPT.
P3: If any constraint is UNKNOWN and none is CERTAIN_FAIL, the option remains UNRESOLVED.
P4: Equality at l=L counts as CERTAIN_PASS for >=, while equality at u=L is POSSIBLE if l<L.
P5: For a conjunction, a known CERTAIN_FAIL dominates any UNKNOWN, with an explicit record of both.
P6: If all options are REJECT or UNRESOLVED, return no guaranteed-feasible recommendation; request the most decision-relevant missing bound or threshold clarification.

## Baseline and failure cases
Baseline: point-estimate midpoint feasibility; it can produce false certainty (A above). Failure conditions: intervals lack defensible coverage, dependence across constraints is ignored in probabilistic claims, thresholds are unconfirmed, units/horizons differ, constraints are nonmonotone, or an outcome changes after action. An interval with no source is UNKNOWN rather than [0,0]. This algorithm makes no causal inference, utility comparison, real-world safety guarantee or empirical forecast. It is a logical decision rule conditional on credible bounds.

## Evidence, provenance and acceptance handoff
Project-local derivation and synthetic arithmetic only; no original-paper theorem reproduction claimed. Context: C004_DYNAMIC_UTILITY_MULTI_OBJECTIVE_ROBUST_2026-10-27.md, section E5 and M2-M5. Independent acceptance track should implement separately and test the six properties, strict versus non-strict threshold, conflicting intervals, missing values, upper bounds, multi-constraint conjunction and label separation. Data track should evaluate whether any real intervals have defensible provenance. Version development may consider an interface after owner authorization. Current status: analytic derivation COMPLETE; software tests NOT_RUN; independent reproduction NOT_RUN; empirical validation NOT_RUN; scientific acceptance NOT_RUN. No private data or frozen protocols changed.
