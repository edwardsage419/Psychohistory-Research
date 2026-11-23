# C035: Joint hard-constraint feasibility under coupled evidence (synthetic method card)

Date: 2026-11-23. Scope: personal decision workbench feasibility gate. Status: ANALYTIC_CANDIDATE. Independent acceptance NOT_RUN.

## Decision gap and relationship to existing work
C028 tests each lower or upper bound separately and returns UNRESOLVED when every bound is individually possible but none is certain. This is a sound conservative three-valued gate. A known joint physical or budget identity can sometimes prove that all hard constraints cannot hold together even though each one separately could hold. This card is a narrow extension for a verified joint feasible set; it does not revise C028 or any frozen R result. Distinct from C034, which compares soft utility scores after feasibility filtering, and from causal transport parameter dependence.

## Inputs and method
Given user-confirmed hard constraints g_j(z)>=0 and a defensible nonempty joint uncertainty set S of simultaneously possible states z, classify:
CERTAIN_PASS iff every z in S satisfies every g_j(z)>=0;
CERTAIN_FAIL iff there exists no z in S satisfying every g_j(z)>=0;
UNRESOLVED otherwise.
An empty S due to contradictory measurements is EVIDENCE_CONFLICT, not CERTAIN_PASS or CERTAIN_FAIL. If S is missing or unsupported, return UNKNOWN. With linear constraints and linear coupling, use a linear-feasibility solver or exact rational elimination. Report the joint identity, evidence, units and a witness state when feasible. These are logical certificates conditional on S, not empirical probabilities.

## Minimal exact counterexample
Two nonnegative resources x,y are jointly constrained by x+y=10, x in [4,6], y in [4,6]. The user requires x>=6 and y>=6. Individually, each interval [4,6] is POSSIBLE under C028, so C028 returns UNRESOLVED. Jointly, x>=6 and y>=6 imply x+y>=12, contradicting x+y=10. Thus CERTAIN_FAIL is mathematically established if the joint identity and both requirements are valid. This result can be verified by integer arithmetic; no numerical optimization is needed.

For a boundary check, replace the total with 12 while retaining x,y in [4,6]: the only joint state is x=y=6, so both requirements CERTAIN_PASS. For an unresolved case, use total 13 with x,y in [4,9]: (6,7) satisfies both requirements, while (4,9) violates x>=6. Thus the joint result is UNRESOLVED. At total 12 with x,y in [4,8], both (6,6) and (4,8) are possible, so the result remains UNRESOLVED.

## Baseline, counterexamples and acceptance
Baseline: C028 per-coordinate interval gate. It correctly avoids false safety, but can leave jointly impossible options unresolved. The joint method may resolve more cases when the coupling is documented.
Acceptance cases:
1. total 10, x,y in [4,6], both >=6: CERTAIN_FAIL with inequality contradiction.
2. total 12, x,y in [4,6], both >=6: CERTAIN_PASS with unique witness (6,6).
3. total 13, x,y in [4,9], both >=6: UNRESOLVED with satisfying witness (6,7) and violating witness (4,9).
4. total 12, x,y in [4,8], both >=6: UNRESOLVED with witnesses (6,6) and (4,8).
5. inconsistent S, such as x+y=3 with x,y in [4,6]: EVIDENCE_CONFLICT, never vacuous CERTAIN_PASS.
6. unknown coupling or units: UNKNOWN; do not assume x+y=10.
7. strict inequalities, equality endpoints, multiple simultaneous constraints and user-edited thresholds must be separately tested.
8. Adding a genuine constraint can only shrink the satisfying subset; tightening the supported state set can change UNRESOLVED to either CERTAIN_PASS or CERTAIN_FAIL.
9. A weighted utility score cannot reinstate CERTAIN_FAIL.
10. A state coupling inferred from observed correlation alone is not a deterministic identity.

## Failure conditions, provenance and handoff
All numerical inputs are synthetic. The method assumes the joint set contains every genuinely possible state and uses compatible units, times and measurement definitions. If the coupling is approximate, represent a tolerance explicitly and recompute; if it lacks evidence, return UNKNOWN. Nonlinear or integer-valued constraints require an appropriate certified solver; no generic implementation is claimed here.
Project-local exact inequality proof completed; original-paper theorem reproduction NOT_CLAIMED; program execution NOT_RUN; independent verification NOT_RUN; real data validation NOT_RUN; scientific acceptance NOT_RUN. Independent acceptance track owns an implementation-independent feasibility test suite. Data track owns evidence for joint identities and uncertainty sets. Product track owns natural-language explanation. Version development requires separate owner authorization. No CI, paid API, personal records or frozen protocols involved.
