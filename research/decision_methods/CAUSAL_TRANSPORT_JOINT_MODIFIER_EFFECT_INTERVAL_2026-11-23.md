# Joint uncertainty in target composition and transported subgroup effects

Date: 2026-11-23. Track: decision model learning. Status: synthetic candidate; no scientific acceptance.

## Decision capability and source
When an external study is used for a personal choice, a target population composition interval alone may understate uncertainty if the subgroup-specific causal effects are also uncertain. Extends the already archived Bareinboim and Pearl (2016) transportability candidate, without modifying its source assumptions or frozen records. Primary source: Bareinboim and Pearl, *Causal inference and the data-fusion problem*, PNAS 2016, DOI 10.1073/pnas.1510507113. The transport formula under the specified selection diagram is a weighted target-population average of source subgroup interventional outcomes. The joint interval bounds below are elementary derived arithmetic, not a theorem or empirical claim attributed to the paper.

## Inputs, formula and validity
Let q be the target fraction of pretreatment subgroup Z=1. Let d1 and d0 be causal risk differences under intervention versus control in the two subgroups. Target average effect D(q,d1,d0)=q*d1+(1-q)*d0. Require a valid transport identification graph, comparable treatment/outcome definitions, and justified intervals. The three parameters are assumed independently feasible over their rectangular intervals for the corner calculation. With arbitrary dependence or restrictions, the rectangle yields conservative outer bounds; it need not be sharp. Bounds follow by evaluating all eight corners because D is multilinear. No numerical personal treatment effect is identified.

## Reproducible minimal synthetic example
Assume q in [1/4,2/5], d1 in [3/20,1/4], d0 in [-3/20,-1/20]. Enumerating the eight corners gives D in [-3/40,7/100], namely [-0.075,+0.070]. In contrast, fixing d1=+0.20,d0=-0.10 yields [-0.025,+0.020]. Thus effect uncertainty widens the ambiguity.

Assume instead q in [2/5,3/5] with the same effect intervals. Eight-corner enumeration yields D in [-3/100,13/100], namely [-0.030,+0.130]. The previous fixed-effect interval [+0.020,+0.080] was strictly positive; once effect uncertainty is admitted the robust sign is unknown.

Simple baseline: report the source average effect without transport; fails on population shift. Stronger baseline: transport fixed subgroup point estimates; fails to account for their uncertainty. This candidate reports the joint range and avoids a forced sign.

## Failure cases and acceptance handoff
If Z is posttreatment, hidden effect modifiers exist, source effect identification fails, or study outcome is not the user's objective, these calculations cannot authorize a personal causal recommendation. If the effect intervals are confidence intervals, simultaneous coverage must be addressed; treating marginal 95% intervals as a guaranteed joint 95% region is invalid. If dependence between q,d1,d0 is known, evaluate the feasible joint set rather than assume all corners are possible.

Independent acceptance: enumerate eight corners using exact rational arithmetic; verify the two ranges and the sign reversal of robustness status; test degenerate effect intervals recover the fixed-effect examples; test correlated admissible sets for conservative rather than sharp bounds; block posttreatment modifiers and hidden mechanisms. Data track: qualify sampling uncertainty, causal identification, target modifier prevalence, and simultaneous interval coverage. Product recommendation: present conditional scenarios in natural language, with one targeted clarification only if it can change the decision.

Evidence: derived synthetic calculation and source-linked methodological extension. No real data, software integration, independent scientific validation, CI, paid API or personal data. R073, PESEN v0.1 and frozen protocols unchanged.
