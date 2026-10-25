# R147 positive-overlap observational twins: prospective E1 protocol

Date: 2026-10-25. Parent evidence: R147 source report and frozen 2026-10-20 protocol. This is an additive new bounded experiment. Do not edit earlier frozen files or reinterpret original authors' city observations.

## Claim to test before writing computation
Construct two distinct three-jurisdiction structural causal models with exactly the same observed eight-cell joint distribution P(A,B,C), strictly positive P(A=a|U=u) for all four (a,u) pairs, and different effects of intervening on A. This tests whether replacing the previous R147 perfect A=U relationship with positive conditional assignment probabilities removes observational ambiguity.

All variables binary. U ~ Bernoulli(1/2). In BOTH models, P(A=1|U=1)=3/4 and P(A=1|U=0)=1/4, implemented by an independent four-outcome draw.

Model S: conditional on U, B and C are independent Bernoulli(3/4) when U=1, Bernoulli(1/4) when U=0. A has no causal influence on B or C.

Model D: conditional on A, the joint pair (B,C) is generated from a fresh exogenous uniform integer W in [0,63], independent of U and A. The conditional four-cell probability P(B,C|A=a) is fixed from Model S's exact eight-cell observational distribution. This intentionally preserves B,C residual dependence given A. Under do(A=a), override A's equation, preserve the distributions of U and W, and recompute B,C. Do not condition on A to approximate the intervention.

## Prespecified independent computations
1. Enumerate S using all 2*4*4*4=128 equally weighted elementary worlds and D using all 2*4*64=512 equally weighted worlds. Cross multiply the eight observed cell counts to compare exactly.
2. Derive a separate symbolic eight-cell table by summing over U and multiplying conditional Bernoulli probabilities. Require equality to enumeration.
3. Check positivity: all P(A=a|U=u) are 1/4 or 3/4 and all eight observed P(A,B,C) are positive. Require total probability one.
4. Compute observed P(B=1|A=1)-P(B=1|A=0), and two do(A) risk differences in D and S. Prespecified expected values: observational 1/4; D 1/4; S 0.
5. Independent residual-dependence check: P(B=1,C=1|A=1) must equal 7/16 and its covariance must equal 3/64.
6. Negative control 1: replace D's joint (B,C)|A with independent Bernoulli marginals and REQUIRE mismatch in at least one observed cell.
7. Negative control 2: replacing do(A) by observation conditioning in S must yield an incorrect nonzero effect, which must be flagged.

Outputs: self-contained standard JavaScript (Node/V8), deterministic JSON receipt, separate scientific report and B evidence audit. Abort scientific PASS if any prespecified check fails. Scope E1 mathematical counterexample only. E2=0; E3=0; external independent replication=0. R073 and PESEN v0.1 remain frozen. No paid compute or GitHub Actions unless zero-cost billing verified.
