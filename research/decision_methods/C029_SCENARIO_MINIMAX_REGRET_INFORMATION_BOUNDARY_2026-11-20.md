# C029: Scenario regret without invented probabilities (synthetic method card)

Date: 2026-11-20 Asia/Singapore. Status: SYNTHETIC_ANALYTIC_CANDIDATE. Scope: personal decision workbench, conditional on user-confirmed hard-constraint feasibility. Independent acceptance NOT_RUN.

## Decision gap and relation to existing work
C028 handles feasibility with epistemic intervals; C004 discusses robust multiobjective preferences and uncertain weights. This card treats a different downstream question: when the user supplies mutually exclusive scenarios without justified probabilities, how can the workbench compare the cost of choosing a plan that turns out suboptimal? Do not assign probabilities or describe scenario regret as expected loss.

## Inputs, assumptions, algorithm
Inputs: finite feasible options A, finite scenarios S, scenario-specific scalar utility u(a,s) on a single explicitly confirmed comparable scale, with higher better. Each scenario must have a defined time horizon and common utility normalization. User-confirmed hard constraints are evaluated before this method. The scenario list must not be presented as exhaustive unless evidence supports completeness.

For each scenario s compute M(s)=max over feasible b of u(b,s). Define regret r(a,s)=M(s)-u(a,s), and worst-case regret R(a)=max over s of r(a,s). Candidate minimax-regret choices minimize R(a); ties remain ties. Report the full regret matrix, worst scenario, scenario-wise best option, and every tie. Compare with maximin utility and a user-chosen reference option. Minimax regret is a descriptive decision rule conditional on the supplied scenario set, not a normative requirement or probabilistic forecast.

## Fully worked synthetic case
Two equally plausible-looking but **unweighted** scenarios S1 and S2. Utilities: A=(8,2), B=(5,5), C=(2,8). In both scenarios the oracle maximum is 8. Regret vectors are A=(0,6), B=(3,3), C=(6,0). Worst-case regrets: A=6, B=3, C=6. Minimax regret selects B; maximin utility also selects B in this particular case, which does not establish their general equivalence.

If S1 were learned perfectly before an irrevocable decision, A would be chosen; if S2, C. Relative to committing to B, perfect scenario identification would improve utility by 3 in either scenario. This 3 is a conditional synthetic gain, **not** a monetary price, expected value of information, or probability-weighted value. The real benefit of a measurement also depends on whether it arrives before commitment, its errors, costs, delay and whether actions can be changed.

## Distinguishing regret from maximin: counterexample
Two scenarios, X=(10,0), Y=(6,5). Oracle maxima are (10,5). Worst regrets X=5, Y=4, so minimax regret selects Y. Minimum utilities X=0, Y=5, so maximin also selects Y. To demonstrate a genuine divergence instead use X=(100,0), Y=(55,40): oracle maxima (100,40); worst regrets X=40, Y=45, so minimax regret selects X, while maximin utilities are 0 and 40, so maximin selects Y. A ranking label must state which rule generated it.

## Failure modes and acceptance properties
F1: Adding a new feasible option can change the scenario-wise oracle maxima and therefore every option's regret; old regret matrices must be recomputed.
F2: Adding a scenario cannot decrease any existing option's worst-case regret, though the winning option can change.
F3: Adding the same constant to all utilities within one scenario leaves that scenario's regrets unchanged; multiplying every utility by the same positive constant scales all regrets without changing minimizers.
F4: Missing scenario utility is UNKNOWN; no numeric ranking until the required cells are resolved or explicitly bounded.
F5: If a hard constraint is unresolved under C028, show conditional exploration separately from guaranteed-feasible ranking.
F6: Show tie cases and counterexamples for regret versus maximin; do not silently choose one.
F7: If probabilities are absent, do not display an expected regret, probability of best option or expected value of information.
F8: A hypothetical measurement with cost or timing cannot be recommended merely because perfect foresight has positive conditional benefit.

## Evidence and handoff
All arithmetic is project-local synthetic derivation. Context: C004_DYNAMIC_UTILITY_MULTI_OBJECTIVE_ROBUST_2026-10-27.md and C028_INTERVAL_HARD_CONSTRAINT_FEASIBILITY_2026-11-20.md. No original-paper theorem reproduction or empirical calibration claimed. Independent acceptance track: implement separately and test matrix arithmetic, F1-F8, unknown propagation and feasibility gate. Data track: examine provenance and coverage of real scenarios. Version development requires separate owner authorization. Analytic examples COMPLETE; software testing NOT_RUN; independent replication NOT_RUN; empirical validation NOT_RUN; scientific acceptance NOT_RUN. No private data, CI, paid API or frozen protocol changes.
