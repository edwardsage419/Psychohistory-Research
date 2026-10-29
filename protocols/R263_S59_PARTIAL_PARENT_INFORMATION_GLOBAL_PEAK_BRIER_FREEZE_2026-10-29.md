# R263 S59: parent information and one-generation global-peak forecasting prescore freeze
Date: 2026-10-29 UTC. Baseline main HEAD: 731c143bacd51b768701e8d4a133f7cde9ee3ac6.
Target key: (r,R263,S59,conditional Brier risk of next generation reaching global fitness peak).
This is an E1 finite artificial extension of R263 prescore freeze e50f54089dac1bab48bd898b3fc1f1dd89c20ebf. Original nine worlds, 10 independent fair source bits, fixed crossover, mutation, fitness and elitist tie breaking remain unchanged. The R263 source CSV and historical acceptance are immutable.
## Predeclared prediction and design
For every world and each of its 1024 equally weighted 10-bit source atoms, define Y=1 iff the maximum fitness of the two next-generation survivors equals the world-specific global maximum (3 for ONEMAX; 4 for TRAP). Define five nested information sets:
F0: no observations.
FB: original two-parent maximum fitness only.
FP: ordered full genomes of both parents.
FPC: both ordered parent genomes and original crossover-flag bit 6, including disabled crossover worlds.
FF: all original 10 bits.
Use the exact finite-world conditional mean p(Y=1 | F) for every information set, with average squared probability error E[(Y-p)^2]. No train/test split is claimed. All nine worlds times five sets yield exactly 45 rational Brier risks, plus counts of mixed-target groups and strict incremental gains. Tie and repeated genome cases remain in the source universe.
## Locked checks
All 45 scores are exact fractions. Each world must satisfy R(F0)>=R(FB)>=R(FP)>=R(FPC)>=R(FF)=0. All nine source universes have 1024 unique 10-bit identities, no post hoc weighting. R263 frozen 9-world best-gain summary is a source-integrity cross-check, not the S59 forecast result. Verify each world’s 1024 Y labels with an independently implemented integer-mask offspring oracle, without importing R263's tuple-slice generator. Independent oracle must reproduce all five risks for all nine worlds. Reject duplicate or missing source identities, mismatched world labels, a changed target, or evidence-label promotion. Record the first failing counterexample.
## Scope and acceptance
Exact full-population theoretical risks, no human holdout or probability calibration generalization, no biological adaptation or long-run GA convergence, no causal inference from a single fitness outcome. B method independence is internal and nonblind with respect to original R263 world design. New E2=0 and E3=0; R073 scoring and PESEN v0.1 frozen. A-source work must not consume the R-main budget. No paid API or Actions invocation; CI NOT_RUN until free entitlement verified.
