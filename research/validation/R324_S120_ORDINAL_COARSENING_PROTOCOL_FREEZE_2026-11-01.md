# R324 S120 pre-result frozen protocol: finite ordinal observation and scoring-scale identification

Date: 2026-11-01 UTC. Track r. Baseline main HEAD: 50292a7e2e4d258d3a64c1387dceccda1e743414.
Scope: a complementary bounded E1 extension of original R324 01-017. No original R324 protocol, generator, data, score weights, formal acceptance, original239 crosswalk, R073 or PESEN v0.1 will be changed.

## Prior fixed universe and question
Read original R324 frozen protocol and its four 16-state constructed worlds, with equal state weight 1/16 in each world. Worlds are W0=(3,1), W1=(1,3), W2=(1,1), W3=(2,2), with score=a*(dread1+dread2)+b*(unknown1+unknown2). World prior is exactly 1/4. Enumerate all 64 (world,state) atoms, each mass 1/64. Observers know the four binary hazard descriptors of the sampled state and only the observation specified below. Determine how much mechanism identity remains when absolute ratings are coarsened to ordinal comparisons.

## Observation policies fixed before result computation
P0 state_only: (state).
P1 exact_score: (state, score).
P2 threshold_ge_4: (state, int(score >= 4)), with a fixed absolute threshold 4 in the original score units.
P3 compare_dread: (state, sign(score - score(1,1,0,0) in same world)).
P4 compare_unknown: (state, sign(score - score(0,0,1,1) in same world)).
P5 compare_both: (state, both comparison signs in P3 and P4).
P6 full_ordinal_profile: the complete 16-by-16 weak ordering of the 16 scores for that world, observed as a single full-profile measurement. The profile is not a single sampled-hazard response. This policy is reported separately to avoid conflating observation costs.

For P0–P5, classify the latent world using its known equal prior and 64 equally weighted atoms. Define Bayes-optimal accuracy as sum over observation groups of max number of atoms from one world divided by 64, with ties resolved by the lowest world index only for a deterministic prediction. Report unique observation-group count and accuracy as exact fractions. For P6 classify world using the complete rank profile with prior 1/4 and accuracy as number of distinct rank profiles / 4. Additionally verify W2 and W3 have identical weak rankings on all 16 states, and that W2 and W3 exact scores differ on exactly 15 of 16 states. No fitted parameters or stochastic simulation.

## Required validation and failure gates
1. R script enumerates all 64 atoms, 16 unique states per world, exact prior mass one, and outputs a CSV of per-atom policy observations plus JSON of exact policy results.
2. Independent B script uses a distinct D/U count-multiplicity oracle (binomial multiplicities 1,2,1) to independently reconstruct the policy accuracies and rank profiles. It must avoid importing the R script. Explicitly mark nonblind and shared protocol.
3. At least eight deliberate mutations must be rejected: missing atom, duplicate atom, altered score, altered policy observation, altered world coefficient, altered policy accuracy, wrong profile identity, false E2 evidence tag.
4. Recompute and compare all persisted rows, exact fractions and metadata. Record any failure before repair. Never silently revise this frozen protocol after seeing results.
5. Status can be PARTIAL_E1_EXTENSION only. No claims about original Fischhoff/Slovic factor estimates, empirical human risk prediction, E2/E3, or R073 applicability.

## Stop rule
Complete once all seven policy calculations, 64 original-state bindings, independent mathematical comparison, mutations, report and remote identity checks have been attempted. Any unresolved test or source failure remains OPEN and blocks stronger acceptance. No GitHub Actions without prior confirmation of free execution and billing allowance.
