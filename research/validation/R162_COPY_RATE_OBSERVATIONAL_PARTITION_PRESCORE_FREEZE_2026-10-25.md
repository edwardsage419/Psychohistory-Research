# R162 observational equivalence third method: prescore freeze
Date: 2026-10-25. Track R. Parent main HEAD eafd890d01994bc2fe8a04e07abf79152ccd25c7.
This is an additive E1 identification analysis of the already frozen R162 72-world attention-ticket experiment, NOT a change to the R162 protocol, R073 or PESEN v0.1.

## Frozen universe and input identity
Use precisely the 72 worlds in research/R162/R162_EXACT_RESULTS.json at Git blob aa6fd210a803d0914b5d18692f9a49c86f9b3009. Original patterns (000,100,011,111), favored index (0,1,2), extra tickets (0,1,3), artificial correctness (0,1). No fitting, sampling, or new parameters. Validate the original 72 unique IDs and the frozen probability formula before analysis.

## Prespecified observability partitions
Compute exact rational equivalence classes of 72 worlds under:
P0: copying probability P(A) only.
P1: copying probability plus the full ordered triple of demonstrator actions.
P2: P1 plus the artificial correct action.
P3: P2 plus extra attention ticket count.
For each partition report number of distinct classes, class-size histogram, maximum class size, and number of worlds belonging to non-singleton classes. Under P0/P1/P2 count classes whose members disagree in the sign of artificial success advantage versus neutral; use exact Fraction arithmetic. P3 is an additional diagnostic, not a guaranteed complete identifier.

## Counterexamples and negative controls
A: pattern 100, favored 0, extra 3, c=1 yields p(A)=2/3 and advantage +1/3.
B: pattern 011, extra 0, c=1 yields p(A)=2/3 and advantage 0. The P0 observational likelihood is identical at every independent Bernoulli copying trial.
C: same A pattern and cue but c=0 yields advantage -1/3 and unchanged p(A).
Mutant 1: replace weighted attention copying with neutral copying; must differ in at least one nontrivial world.
Mutant 2: reverse the artificial correct token without changing copying probability; must reverse advantage sign whenever advantage nonzero.
No posterior inference, real-person calibration, true prestige measurement, external prediction, or causal claims.

## Independent audit and acceptance
Primary R script: exact rational class partition and explicit full 72-world frozen JSON equality checks. Independent B script: independently generate 72 worlds and use a different method to group by observables; compare counts and counterexamples. Record failures transparently. Require all 72 source matches, complete partitions and counterexamples, both mutants executed and detected. B audit is internal methodological cross-check only. No GitHub Actions unless confirmed free; local tests preferred.
Evidence E1 synthetic only. E2=0; E3=0. Keep original239 v7.8 and 154 pending queue unchanged.