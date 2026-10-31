# R319 S115 prescore freeze: repeated-choice panel persistence

UTC date: 2026-10-31. Baseline main: faf54ae634622da0d877a0769fbe1361649a1fbf.
Target key: (r,R319,original_R319_v1_plus_S115,one_draw_vs_redraw_panel_identifiability).
Status: FROZEN BEFORE S115 JOINT PROBABILITY COMPUTATION. Original R319 E1 acceptance and original239 crosswalk remain unchanged.

## Original fixed universe
Read the 15 worlds in research/R319/R319_EXACT_15_MIXED_LOGIT_WORLDS.json, from five ordered choice sets S0=(0,1), S1=(0,1,2), S2=(0,1,1), S3=(0,2,1), S4=(0,2,2), each with q=P(beta=+1) in {1/4,1/2,3/4}. Reconstruct conditional probabilities from the original R319 fixed coefficient beta in {-1,+1} and weights 2^(beta*x). Keep all 84 original source atoms, alternative indices and original order. No estimation, observed choices or person identities.

## Two new synthetic mechanisms
For each original world, construct a two-occasion ordered choice outcome (j,k) from the same fixed choice set.
PERSISTENT: draw one latent beta once per artificial panel, then two conditionally independent choices given that beta. Joint Jp(j,k)=q*p_plus(j)*p_plus(k)+(1-q)*p_minus(j)*p_minus(k).
REDRAW: draw beta independently for each occasion with the same q. Joint Jr(j,k)=[q*p_plus(j)+(1-q)*p_minus(j)]*[q*p_plus(k)+(1-q)*p_minus(k)].
Both mechanisms have the same single-occasion marginal probability, exactly equal to original R319. All ordered outcomes must be retained, including repeated alternatives.

## Frozen output and falsification
Produce 15 worlds, 120 ordered outcome pairs per mechanism (3 binary worlds times 4 plus 12 ternary worlds times 9), 240 exact rational joint probabilities. Store a complete 240-row CSV with world_id, choice_set_id, features, q_plus, mechanism, choice_t1, choice_t2, joint_probability. Store 15-world JSON with both exact 2-occasion joint matrices or sufficient exact per-world full statistics: total variation TV=.5 sum_{j,k}|Jp-Jr|, equal-prior Bayes mechanism classification accuracy (1+TV)/2, and same single-occasion marginals. No floating-point approximations in primary outputs. All joint distributions sum to 1, all rows nonnegative, and all single-occasion marginals match original R319 exactly. The registered algebraic identity is Jp-Jr=q(1-q)[p_plus(j)-p_minus(j)][p_plus(k)-p_minus(k)]. Its diagonal must be nonnegative; cross-sign off-diagonal differences must be nonpositive. In S0 with q=1/2, TV=1/18, Bayes accuracy=19/36. For every q in the registered nondegenerate grid, any choice set with distinct beta-conditional distributions has TV>0. Additional q=0 and q=1 boundary controls have TV=0 for each choice set.

## Independent audit and limits
A B-track no-import independent Fraction implementation must independently reconstruct all 240 joint cells and 15 TV/accuracy values using explicit enumeration of beta pair draws and verify every archived row and key, including missing/duplicate coverage. Run >=8 targeted mutations covering deletion, duplication, probability, world/alternative, mechanism, summary, and evidence-label changes; preserve any failed controls. Verify the original R319 84-atom source identity and 15 original marginal vectors when accessible. Record actual runtime, tests, command exit, SHA identities, and CI status. No Actions without verified zero-billing conditions.

Evidence class E1 synthetic mechanism only. These are artificial panel choices, not real longitudinal human behavior or an estimated persistent taste distribution. Bayes accuracy is exact synthetic distinguishability under equal priors, not heldout human accuracy. Real human E2=0, historical E3=0, external independent replication NOT_RUN. R073/PESEN v0.1 frozen; no model fusion or personal decision product.