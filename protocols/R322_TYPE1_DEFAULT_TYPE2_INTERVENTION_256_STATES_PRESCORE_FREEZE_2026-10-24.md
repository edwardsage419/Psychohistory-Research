# R322 prescore freeze: default/intervention and observational equivalence

Date 2026-10-24. Original239 01-012 Dual Process Accounts (P2). **PRESCORE ONLY**, before any generated R322 source or outcomes.

## Original English source and reuse

Evans & Stanovich (2013), *Dual-Process Theories of Higher Cognition: Advancing the Debate*, Perspectives on Psychological Science 8(3):223–241, DOI 10.1177/1745691612460685. The authors describe autonomous Type 1 default responses and Type 2 higher-order intervention drawing on working memory; they explicitly warn against treating every intuitive answer as wrong or every analytic answer as correct, and against treating the family as one unique theory. This finite exercise is a **project-constructed schematic truth table**, not their fitted original model, replication or general proof of two psychological systems.

R295 habit cue/revaluation, R289 satisficing search and R303 Bandura acquisition/expression contain gate or choice components but no verified equivalent Type1 default, Type2 intervention, one-process observational-equivalence experiment. Reuse only finite binary gate arithmetic. Repository code search returned no matching dual-process source; full early ZIP review is still OPEN.

## Frozen universe and mechanisms

All 2^6=64 ordered artificial binary exogenous states (h,a,y,d,r,w) where h=autonomous default response, a=analytic proposed response, y=externally designated correct answer, d=conflict detection availability, r=working memory resource, w=intervention willingness. Uniform weight 1/64. Four deterministic policy worlds (256 rows total), in order:
* default_only: output=h, intervention=0.
* gated_intervention: if h!=a and d=r=w=1, output=a, intervention=1; otherwise output=h, intervention=0.
* analytic_only: output=a, intervention=1 (even if a=h).
* lookup_equivalent: a single direct Boolean lookup output=h XOR ((h XOR a) AND d AND r AND w), intervention label set to 0 (one-stage observational equivalent by construction).

Each source row stores world_id,policy,h,a,y,d,r,w,weight,output,correct,intervention. Outcomes store counts and exact fractions of correct, output differs from default, intervention labels, and pairwise output disagreement across policies. The lookup model is an explicit **identification counterexample** only, not a realistic cognitive mechanism or evidence that real people use a single process. All states are artificial, not subjects.

## Frozen falsifiable claims

1. 256 rows exactly, 64 per policy, all distinct state keys within policy, uniform weights sum 1 each; all outputs binary.
2. gated_intervention changes the default response on exactly 4/64 states, since h!=a has 1/2 probability and d=r=w=1 has 1/8; analytic_only changes it on 32/64. The direct lookup produces exactly the same 64 output values as gated_intervention, while its intervention labels differ.
3. Across full uniform y, every policy has accuracy exactly 1/2. Type2 intervention is therefore **not sufficient to guarantee improved accuracy** in this constructed universe.
4. Conditional on a=y and h!=a, gated override happens on exactly 1/8 of the states; in these cases the gated response is correct, otherwise the default remains wrong. This is an algebraic witness, not empirical evidence.
5. Independent no-import source audit must reconstruct 256 rows and verify output truth table and exact summary independently. 25+ stdlib tests under Python 3.11/3.12 plus independent GitHub Actions job. Byte replay and Git blob source receipts. Any failure -> PENDING.
6. Formal grade only PASS_BOUNDED_E1_SCHEMATIC_DEFAULT_INTERVENTION_IDENTIFICATION_ONLY after three green jobs and verified blobs. No human E2, historical E3, working-memory manipulation evidence, causal identification, normative superiority, original Evans-Stanovich empirical replication, or proof of two systems. Only after acceptance update original239 01-012. R073/PESEN v0.1 remain frozen; no classification or fusion.
