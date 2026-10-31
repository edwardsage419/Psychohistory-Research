# R323 S119 prospective freeze: structural mediator intervention and action identification

UTC date: 2026-10-31. Baseline main HEAD: 2cfd3d2c7959de1f8db2e0f8467abed158b96463.
Research target key: (r,R323,original_R323_v1,do_N_mediator_identification_S119).
Status: PRECOMPUTATION_FREEZE. This document is written before generating any S119 numerical results or audit scores.

## Historical fixed inputs
Original R323 2026-10-24 protocol and original 128-row CSV (Git blob 1b92efb314aae036e773be92e28793f8fcd60809), four worlds, exact 32 uniform exogenous configurations V,T,R,E,C. Original outcome rules and original E1 acceptance remain unchanged. Original original239 v7.8 crosswalk blob 36f24235901172642c46853298aebb421f1a3552 and 154 pending queue blob 3b96d46b3d88ccafd779a08509c3cfd0e435772f are read-only.

## New bounded question
Do two project-defined VBN policies with identical observational action mapping become distinguishable when an idealized, surgically set latent personal norm is observed and assigned? Evaluate identification solely in the finite artificial structural models. This is a hypothetical intervention on an abstract variable, not a feasible human norm manipulation or evidence of a causal effect in real people.

## Frozen structural intervention
For each original exogenous state x=(V,T,R,E,C), independently enumerate do(N=0) and do(N=1), exactly 64 rows per policy and 256 total. Each x has exact probability 1/32 and intervention assignment 1/2, yielding row weight 1/64 within a policy. The intervention replaces only the mediator equation, leaving exogenous inputs and downstream equations intact.
1. vbn_cascade: A = N_do * C.
2. direct_product: A = V*T*R*E*C (independent of N_do).
3. unconstrained_norm: A = N_do.
4. value_feasible: A = V*C (independent of N_do).
The original natural mediator N_original is retained as a provenance field, alongside assigned N_do and intervened action. No fitted parameters, real subjects or stochastic behavior are introduced.

## Prespecified tests and scores
1. Strict uniqueness and complete 4*32*2 coverage; all binary fields and policy names validated; weight 1/64 and mass 1 per world; original CSV all 128 rows checked against original source and natural actions reconstructed.
2. Each policy: count of positive action under each do(N) assignment; conditional average intervention effect E[A|do1]-E[A|do0] as exact Fraction; original observational actions never rewritten.
3. All six pairwise policy disagreement counts across the 64 equally weighted intervention states. Special focus cascade vs direct_product: observational action disagreement zero, intervention disagreement positive; report separately for do0 and do1.
4. Total variation distance between fully observed joint distributions (X,N_do,A) for cascade vs direct_product, equal-prior optimal binary classification accuracy 1/2+TV/2; additionally conditional on do0 and do1. Exact fractions only.
5. Boundary and negative controls: C=0 must suppress cascade under both interventions; direct_product action invariant to N_do; value_feasible action invariant; unconstrained action equals N_do; changing any original natural action or world identity is forbidden.
6. Independent no-import Python audit independently derives all counts from the structural equations and reads the complete persisted S119 CSV/JSON. It must reject at least six targeted mutations including omission, duplicate, incorrect assignment, incorrect action, weight, and evidence-grade upgrade. All audit code and test cases archived. A genuine outside-team replication is NOT_RUN.
7. S119 status only PARTIAL_E1_EXTENSION even if exact checks pass. No E2 or E3 evidence, no real causal mediation, no generalization, no R073/PESEN v0.1 changes. CI only if cost can be positively verified free; otherwise NOT_RUN.

## Stop rules
Any source identity mismatch, failed exact check, incomplete audit or conflicting concurrent GitHub edit blocks acceptance and is recorded as failure. New outputs go only to unique S119 files under research/validation, research/evidence_audit, and research/coordination/r. Recheck main HEAD, target paths and other tracks before writes; no overwrites or status-only commits.
