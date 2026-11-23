# C036: Two-stage adjustable feasibility and information timing (synthetic method card)

Date: 2026-11-23. Status: ANALYTIC_CANDIDATE. Independent acceptance NOT_RUN.

## Decision gap and de-duplication
C035 classifies environmental states in a joint uncertainty set. When resource allocations are controlled by the decision maker, its universal-state CERTAIN_PASS test is not a substitute for existence of a feasible action. This card isolates the distinct decision-policy question: what can be committed before a scenario is observed, and what may be adjusted afterwards? It extends the previously documented C035 counterexample without modifying C035, C028, C034 or frozen R results.

## Applicable decisions and inputs
Use for budgets, time slots or staffing with future scenarios and conditional reassignment. Inputs: scenario set S and evidence; fixed budget B; precommitment action a in admissible set A; scenario-specific post-observation action x_s in X(a,s); per-scenario hard constraints g_j(x_s,s)>=0; maximum allowed reassignment k; observation time, action deadline and authority to reallocate. Record whether k is confirmed or hypothetical.

## Three distinct queries
(1) Existence for a known scenario: for a given s, does there exist x_s satisfying all constraints?
(2) Fixed robust decision: does there exist a single a that satisfies constraints for every s?
(3) Adjustable robust decision: does there exist an a such that for every s, an admissible x_s depending only on information observed by its action time satisfies constraints? A policy cannot depend on an unobserved future scenario. An unsupported scenario set or unknown adjustment authority yields UNKNOWN, not CERTAIN_PASS.

## Exact synthetic example and reproducible arithmetic
Two accounts A and B share B=10 units. Scenario 1 requires final allocation (at least 7, at least 3); scenario 2 requires (at least 3, at least 7). With conservation, the only feasible final A allocations are 7 and 3 respectively. Let a be the initial A allocation, and k the maximum number of units transferred in one direction after observing the scenario. The adjustable constraints are |a-7|<=k and |a-3|<=k. Their intersection is nonempty iff k>=2 (by triangle inequality; a=5 witnesses equality). For integer units, k=0 and k=1 fail, k=2 admits a=5, k=3 admits a=4,5,6. A fixed allocation without adjustment fails because A>=7 and B>=7 imply B>=14, exceeding 10. Counting both the reduction in A and increase in B as two transfers would incorrectly double the physical transfer volume.

A simple reproducible Python baseline:
```python
for k in (0, 1, 2, 3):
    witnesses = [a for a in range(11) if abs(a - 7) <= k and abs(a - 3) <= k]
    print(k, witnesses)
```
Expected output:
```
0 []
1 []
2 [5]
3 [4, 5, 6]
```

## Failure conditions and counterexamples
If the scenario cannot be observed before reassignment, adjustable feasibility must not be asserted. If transfers have cost, delay, losses, minimum increments or different directional limits, recalculate the actual post-observation feasible set. Scenario-wise feasible solutions do not prove a shared feasible precommitment. If constraints and budget evidence contradict, report EVIDENCE_CONFLICT. Probabilities are unnecessary for feasibility and must not be invented. A satisfying policy is a mathematical conditional certificate, not proof that an actual institution permits transfers.

## Conservative baseline and acceptance handoff
Baseline: C035 joint-state gate, explicitly marked as insufficient for controlled actions. Independent acceptance should test fixed versus adjustable quantifier order, k=1/2/3, scenario observation after deadline, nonanticipativity, budget conservation, and transfer volume definition; compare an independent enumeration with analytic inequality. Data track validates timing, permission and costs. Product track explains the distinction in natural language. Version development needs owner authorization.

## Evidence and status
The example is synthetic and follows elementary inequalities. Original-paper replication NOT_CLAIMED. Local Python enumeration EXECUTED for k=0,1,2,3. Independent implementation verification NOT_RUN. Real-world data NOT_RUN. Scientific acceptance NOT_RUN. No private records, paid APIs, CI, or changes to frozen protocols.
