# R323 scientific report: finite value-belief-norm mediation identification counterexample

Date 2026-10-24. Original239 **01-015 Value Belief Norm Theory (P2)**. Scientific grade **PASS_BOUNDED_E1_SCHEMATIC_VBN_MEDIATION_ONLY**.

## English original sources and reuse audit

Stern, Dietz, Abel, Guagnano and Kalof (1999), *A Value-Belief-Norm Theory of Support for Social Movements: The Case of Environmentalism*, Human Ecology Review 6(2):81–97, including a reported national survey of 420 respondents. Stern (2000), *New Environmental Theories: Toward a Coherent Theory of Environmentally Significant Behavior*, Journal of Social Issues 56(3):407–424, DOI 10.1111/0022-4537.00175. These are empirical and conceptual sources; the R323 Boolean cascade is **project-created**, not an original fitted equation or a reproduction of the original survey.

R291 has a synthetic subjective norm/intention/behavior model, R292 perceived versus actual control, and R308 collective efficacy and resources. Only finite gate arithmetic was reusable. No identical original VBN mediation model was verified in those studies; full historical ZIP scan remains open.

## Prescore source and complete artificial sample

Protocol frozen at [54aee0ea](https://github.com/edwardsage419/Psychohistory-Research/commit/54aee0ea3e5153396b167249ce7f75afa95a6756) before generated source [0e560dc9](https://github.com/edwardsage419/Psychohistory-Research/commit/0e560dc9be36534a65e8325dcc18d06adb12a341). All 32 combinations of five exogenous binary values V,T,R,E,C are enumerated under four project-defined policies: cascade, direct product, unconstrained norm, value plus feasibility. Exactly **128 artificial original source rows** at exact weight 1/32 each per world.

Cascade assigns latent norm N=V*T*R*E and action A=N*C. Direct product sets N=0 but A=V*T*R*E*C. Unconstrained policy ignores C; value-only policy A=V*C. These schematic rules deliberately isolate a mediation identification issue.

## Frozen exact results

Cascade has personal norm positive in **2/32** states and action in **1/32**. Direct product has norm positive in zero states and action in **1/32**. Their observed actions are **identical on all 32/32 states**, even though the latent norm differs in two states. Therefore complete behavior-only mappings in this artificial universe do not identify the proposed mediator. Unconstrained norm has action in **2/32** states, including one state with C=0; value plus feasibility has action in **8/32**. Action disagreement counts: cascade vs direct product 0, cascade vs unconstrained 1, cascade vs value feasible 7. The result is an algebraic identification counterexample, not a claim about actual personal norms or environmental behavior.

## Independent audit and formal acceptance

[GitHub Actions run 40015028540](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/40015028540) completed three successful jobs. Python 3.11 and 3.12 each executed 30 stdlib tests and byte-for-byte source replay; independent no-import audit reconstructed all 128 CSV rows and six pairwise policy comparisons. [Source generator](r323_vbn.py), [independent auditor](../catalogue_audit/independent_r323_vbn_audit.py), [machine receipt](R323_MACHINE_RECEIPT.json).

## Evidence limits

No original 1999 survey reanalysis, real norm measurement, environmental action observation, fitted effect size, causal mediator identification, human E2, historical E3, or external forecast. This is a bounded artificial E1 teaching and falsification case only. R073/PESEN v0.1 frozen. Existing 173 provisional original239 README associations remain provisional; classification and model fusion deferred.
