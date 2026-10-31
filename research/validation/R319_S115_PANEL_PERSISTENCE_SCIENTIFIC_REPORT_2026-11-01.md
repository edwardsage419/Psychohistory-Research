# R319 S115: exact panel persistence versus independent coefficient redraw

Date: 2026-11-01 Asia/Singapore (2026-10-31 UTC). Frozen protocol commit: 528872dd56d66255014419d1da383de430fc67e7. Target key: (r,R319,original_R319_v1_plus_S115,one_draw_vs_redraw_panel_identifiability).
Scientific status: PARTIAL_E1_EXTENSION. Original R319 PASS_BOUNDED_E1_ONLY remains unchanged. No update to original239 v7.8.

## Research question and source
Original R319 original239 01-007: finite two-point mixed logit, 15 worlds and 84 conditional atoms, original R319 source blob abbc6b79715535bcf0b5d35d7f8c8578c82a2ef6, original marginal JSON blob 5ea1cde7f7f5bad3c0b12bbeee614ac7dda7a947. Author theory: Kenneth Train (2009), Discrete Choice Methods with Simulation, chapter 6, https://eml.berkeley.edu/books/choice2nd/Ch06_p134-150.pdf .

Two new synthetic mechanisms give identical one-occasion marginal choice probabilities. PERSISTENT draws beta once for two independent conditional choices, while REDRAW independently draws beta on each occasion. Fixed original q in {1/4,1/2,3/4}, five original choice sets and beta in {-1,+1}; no new fitted parameters or observed persons.

## Complete exact result
15 worlds, 120 ordered outcome pairs for each mechanism, 240 rational joint probability cells. For all worlds and both occasions, summing the joint over the other occasion reproduces original R319 marginal probabilities exactly. Both joint distributions normalize to one. All 15 worlds have strictly positive total variation between the two mechanisms.

Let a_j=P(j|beta=+1), b_j=P(j|beta=-1). The joint difference is exactly
J_p(j,k)-J_r(j,k)=q(1-q)(a_j-b_j)(a_k-b_k).
TV=(1/2)sum_{j,k}|J_p-J_r|. Equal-prior Bayes mechanism classification accuracy is (1+TV)/2.

| Choice set | q=1/4 TV | q=1/2 TV | q=3/4 TV |
| --- | ---: | ---: | ---: |
| S0 (0,1) | 1/24 | 1/18 | 1/24 |
| S1 (0,1,2) | 27/392 | 9/98 | 27/392 |
| S2 (0,1,1) | 27/800 | 9/200 | 27/800 |
| S3 (0,2,1) | 27/392 | 9/98 | 27/392 |
| S4 (0,2,2) | 25/216 | 25/162 | 25/216 |

The smallest TV is 27/800; the largest is 25/162. For S0 q=1/2, TV=1/18 and classification accuracy=19/36. For S4 q=1/2, TV=25/162 and classification accuracy=187/324. Ten additional q=0 or q=1 boundary controls give TV=0. This establishes that one-occasion equality does not guarantee two-occasion equality when latent taste persists.

## Program, complete data and audit
R generator: research/validation/r319_s115_panel_persistence.js. Exact source: research/validation/R319_S115_ALL_240_PANEL_JOINT_CELLS.csv, SHA256 ac218326bf68d7bd4d6db385921d679ac0706d07ce09130e6458d925dc646531. Summary: research/validation/R319_S115_EXACT_PANEL_SUMMARY.json, SHA256 7509fdbddc82102bbf524a2302c7e84cb83226fc916976c8fa423e83830902b5.
Node v22.16.0 native --emit into isolated directory and --audit of the archived generated files both succeeded locally. Independent Python 3.13.5 Fraction latent pair enumeration checked all 240 joint cells and all 15 summaries. Python normal and -O both passed, including 8 targeted mutations and 10 boundary controls. Remote Git blob readback and CI must be reported separately after commit.

## Scientific boundaries
The same choice set is repeated twice in an artificial panel, with conditional independent Gumbel draws. Classification accuracies are mathematical Bayes optima under equal mechanism priors and complete known distributions; they are not human heldout accuracy, model fit, or causal evidence. No actual person panel, empirical calibration, independent external team, or original-author longitudinal data is used. E1 only; new E2=0, E3=0. R073 model and scoring, PESEN v0.1 remain frozen. Model fusion and personal decision product remain paused.
