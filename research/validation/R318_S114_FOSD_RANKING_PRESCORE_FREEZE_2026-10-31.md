# R318 S114 prescore freeze: finite first-order stochastic dominance and signed-tail normalization
Date: 2026-10-31 UTC. Track r. Baseline main b57e34bbc8946125ec2a7ed2ea864589fcff481a.
Status: PRECOMPUTATION_FREEZE. Original R318 E1 bounded acceptance remains unchanged.

## Question and frozen population
Within original R318 18 two-outcome artificial lotteries (six strictly ordered pairs from {-2,-1,1,2}, three low-outcome probabilities 1/4,1/2,3/4), evaluate whether original identity and explicitly noncanonical quadratic asymmetric signed-tail transforms preserve first-order stochastic dominance (FOSD). Also quantify how ranking comparisons differ across the two transforms and under an explicitly incorrect mixed-sign weight normalization.
Fixed original source: research/R318/r318_exact_cpt_rank_sign.py blob cf04581003cc60dde398ee3c557e2d0ea1c60493; frozen original protocol blob ea658979b3d25f1dca1d688c6a6cd8f1f6cd1d03; original 36-outcome JSON blob f70d84f7db8c354cf6f02726dfbab2ddb2cffde3. No changes to these originals or R073/PESEN.

## Deterministic universe and measurements
Assign lottery IDs 0..17 in original PAIRS order and PROBS order, then compare all 18*17=306 distinct ordered (A,B) pairs under each transform: 612 rows. FOSD(A,B) iff CDF_A(t)<=CDF_B(t) for each t in {-2,-1,1,2} and at least one inequality strict. Compute CDFs from raw objective probabilities, not CPT decision weights.
Exact Fraction CPT valuation uses original value v(x)=x if positive, 2x if negative, identity w0(p)=p or noncanonical w1(p)=p^2/(p^2+2(1-p)^2). For all gain lotteries low/high weights are (1-w(1-p),w(1-p)); for all loss lotteries (w(p),1-w(p)); for mixed sign (w(p),w(1-p)). Record FOSD, valuation difference sign, and whether any FOSD pair is wrongly ranked.
For negative control only, define naive normalized mixed-sign valuation V_norm=(w(p)v(low)+w(1-p)v(high))/(w(p)+w(1-p)); pure-sign lotteries use original V. Record its FOSD violations and comparisons with actual CPT. This negative control is an intentionally incorrect model, not a CPT claim.
For each of the 153 unordered distinct pairs, record sign of valuation difference for each transform, and count strict ranking reversals (signs opposite) and ties separately. No selective subsets or post-result threshold choices.
Archive 612-row CSV, exact JSON summary, code, source identities, and independent no-import B audit with at least 8 explicit mutations. Include any failed controls and zero-result counts. No empirical test, calibration, real E2, historical E3, or external independent replication.

## Acceptance and stopping
One deterministic full enumeration only; no tuning or replacing source lotteries. Check exact source JSON values, 612 unique ordered keys, CDF/FOSD algebra, antisymmetry, and per-transform totals. An independently written Fraction calculation must agree on every comparison. FOSD violations, if found, remain visible as negative evidence and must not be silently fixed. Audit checker must reject duplicate, omitted, altered FOSD, altered valuation, swapped transforms, false E2 promotion, and aggregate tampering. Original R318 status stays PASS_BOUNDED_E1_ONLY; S114 remains PARTIAL_E1_EXTENSION unless separately formally accepted. No GitHub Actions until free billing verified. No fee or paid APIs.
