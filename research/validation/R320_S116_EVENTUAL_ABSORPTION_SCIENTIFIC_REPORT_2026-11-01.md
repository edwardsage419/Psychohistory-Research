# R320 S116: eventual absorption versus six-step censoring

UTC date: 2026-10-31. Scientific status: PARTIAL_E1_EXTENSION. Frozen prescore commit: 2664cca07f969b0e753f3c70886f9ec623b84f58. Original R320 PASS_BOUNDED_E1_DISCRETE_ANALOGUE_ONLY remains unchanged.

## Question, original source and scope

Original R320 studies a six-step discrete two-boundary random walk, a deliberately limited analogue of the drift diffusion model. This extension asks how much probability and expected decision time are hidden by right-censoring at step 6. Frozen worlds: a=4 or 6, start a/2, p=1/4,1/2,3/4, 64 six-bit original exogenous paths per world, 384 source rows. Original source Git blobs: CSV ece51a015bdfeb0a8233f7a24dffe641489e4282, first-hit JSON ec0f3702f956e0075444d1d3efafef0bced1d7a2. The original 385-line CSV and all 6 original JSON worlds were read from main; no original file was changed.

## Exact results

| a | p | eventual upper | E[tau] | six-step survival | E[min(tau,6)] | upper given survival |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 4 | 1/4 | 1/10 | 16/5 | 27/512 | 97/32 | 1/10 |
| 4 | 1/2 | 1/2 | 4 | 1/8 | 7/2 | 1/2 |
| 4 | 3/4 | 9/10 | 16/5 | 27/512 | 97/32 | 9/10 |
| 6 | 1/4 | 1/28 | 39/7 | 81/256 | 1137/256 | 1/28 |
| 6 | 1/2 | 1/2 | 9 | 9/16 | 81/16 | 1/2 |
| 6 | 3/4 | 27/28 | 39/7 | 81/256 | 1137/256 | 27/28 |

All six exact eventual upper and lower masses sum to 1. Each six-step upper/lower hit mass plus survival sums to 1. Eventual-minus-six-step upper/lower residual masses are nonnegative and sum exactly to six-step survival. Every E[tau] is greater than E[min(tau,6)]. All 36 original time/side cells agree with independent forward-state propagation.

## Mechanism result

For the six frozen worlds, P(eventual upper | no hit by step 6) equals the unconditional P(eventual upper). This equality is specific to a centered starting state and symmetric two-boundary random-walk geometry. Reflection pairs at each first-hit time have upper/lower probability ratio (p/(1-p))^(a/2); this ratio is constant over hit times. Consequently right-censoring at a common fixed horizon does not change the upper/lower eventual odds in this fixed family, while it can substantially truncate observed decision times. In the unbiased a=6 world, the true eventual expected steps are 9, compared with 81/16 for the six-step truncated expectation, a difference of 63/16.

This is a falsifiable finite-world mathematical statement. It is not a general claim about arbitrary starting bias, asymmetric boundaries, time-varying drift, continuous-time Wiener likelihoods, nondecision time or human response times.

## Independent audit and reproduction

Primary: research/validation/r320_s116_eventual_absorption.py computes exact gambler's ruin probabilities, expected time and enumerates all 384 six-bit paths. Output: research/validation/R320_S116_EXACT_EVENTUAL_RESULTS.json. Independent B: research/evidence_audit/b_r320_s116_absorption_linear_audit.py solves separate absorbing Markov linear systems by Fraction Gaussian elimination and propagates surviving interior mass, importing no R program. On local Python 3.13.5, primary emit and audit PASS, B normal and -O each ran 11 tests successfully, including 10 mutation rejection tests. The original source JSON and CSV were read from GitHub; no human dataset was used. Archived output SHA256 ab4e22b46b2720e57520d33d2b0e86924c0e9dce45727a26d6d7cc89ca6d59da. Remote Git blob and CI status are separate verification gates.

Evidence: E1 synthetic only. New E2=0, E3=0, external-team replication NOT_RUN. R073 model/scoring and PESEN v0.1 remain frozen. No taxonomy, fusion or personal decision product.
