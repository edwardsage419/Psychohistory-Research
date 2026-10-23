# R323 prescore freeze: finite value-belief-norm cascade and mediation non-identification

Date 2026-10-24. Original239 **01-015 Value Belief Norm Theory (P2)**. This file is a **prospective protocol only**, before any R323 original artificial source, outcomes, tests, scientific acceptance or original239 link changes.

## Original English references and reuse review

Stern, Dietz, Abel, Guagnano and Kalof (1999), *A Value-Belief-Norm Theory of Support for Social Movements: The Case of Environmentalism*, Human Ecology Review 6(2):81–97. Their original national survey involved 420 respondents, with movement support dimensions, personal norms and constraints; these data are not acquired or replicated here. Stern (2000), *New Environmental Theories: Toward a Coherent Theory of Environmentally Significant Behavior*, Journal of Social Issues 56(3):407–424, DOI 10.1111/0022-4537.00175. These are conceptual/empirical accounts, not a unique deterministic Boolean equation.

Existing R291 Theory of Reasoned Action studies subjective norms/intention/behavior under synthetic DGP; R292 Theory of Planned Behavior studies perceived versus actual control; R308 Collective Efficacy separates beliefs, willingness and resources. Their binary gating algebra is reusable, but they do not establish the VBN-specific value/threat/responsibility/efficacy/personal norm chain. GitHub code search did not surface an exact VBN study. The complete early ZIP and knowledge-card content reuse gate remains open.

## Frozen finite design

Five independent binary artificial exogenous inputs (V,T,R,E,C) in lexicographic order, each of the 2^5=32 input states assigned exact uniform weight 1/32: V=endorsed value, T=belief valued object is threatened, R=ascribed responsibility, E=belief action can help, C=external feasibility. Four **project-defined**, intentionally schematic policy worlds, 128 original source rows:

1. vbn_cascade: latent personal norm N=V*T*R*E; action A=N*C.
2. direct_product: latent personal norm N=0; action A=V*T*R*E*C, representing an observationally equivalent direct mapping without the same mediator.
3. unconstrained_norm: N=V*T*R*E; A=N (ignores C).
4. value_feasible: N=V; A=V*C (omits intermediate beliefs).

CSV columns: world_id,policy,V,T,R,E,C,weight,latent_norm,action. JSON world summary: policy, state_count, personal_norm_positive_count, action_positive_count, personal_norm_rate, action_rate, action_when_C_zero_count, and six pairwise action disagreement counts. All rational exact, no fitted probabilities or real observations.

## Prespecified falsification and negative controls

1. Exactly 4*32=128 unique original source rows, 32 per policy, each row weight 1/32 and mass exactly 1 per world.
2. Under cascade, personal norm is positive in exactly 2/32 states and action in exactly 1/32; action is zero whenever C=0. Under unconstrained_norm action positive in 2/32, including 1 state with C=0. Under value_feasible action positive in 8/32. Under direct_product action positive in exactly 1/32 and latent norm always 0.
3. Cascade and direct_product have **identical action for every one of 32 input states**, despite distinct latent personal norm assignments on exactly 2 states. This is a finite mediation non-identification counterexample from behavior-only outcomes. The project-constructed direct mapping is a mathematical negative control, not a plausible psychological replacement theory.
4. Independent no-import auditor must reconstruct all 128 rows and six pairwise action disagreement counts; byte-for-byte source replay, 25+ stdlib tests in Python 3.11/3.12, independent GitHub Actions job and source blob receipts. Failure -> PENDING.
5. Formal scientific grade can only be PASS_BOUNDED_E1_SCHEMATIC_VBN_MEDIATION_ONLY after 3 green CI jobs and blob verification. No original survey replication, no estimated 1999 survey effects, no observed environmental actions, human E2, historical E3, causal mediation identification or generalized behavioral validity. Original239 01-015 remains pending until that gate. R073/PESEN v0.1 frozen. Finish all R studies before classification and fusion.
