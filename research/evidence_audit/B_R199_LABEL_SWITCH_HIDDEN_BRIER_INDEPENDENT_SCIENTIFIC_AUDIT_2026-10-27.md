# B independent audit of R199 hidden-label Brier label-switch experiment

Date: 2026-10-27. Protocol was committed as `08f1a96574f93f296fa4dc461a310198c0d051c2` before computation. Original R199 research and acceptance unchanged.

## Independent calculation and exact checks

R uses forward-backward alpha/beta smoothing to obtain P(Xt=1|Y), then evaluates analytic conditional Brier risk. B constructs every full artificial hidden sequence X and visible sequence Y directly under each source and calculates exact joint P(X,Y). It obtains all time-specific hidden posteriors by summing latent paths and evaluates the actual hidden binary label loss directly, without importing the R forward/backward algorithm or risk expression.

B enumerated 640 full hidden/visible joint atom contributions across BASE/LABEL_SWAPPED and L=3/4. Exact probability mass normalized in all four settings. All 48 full observed-sequence likelihood comparisons were equal across label swaps. All 176 hidden posterior complement comparisons passed. Across four settings, 40 R versus B exact result-field comparisons passed with 0 mismatches.

Negative controls: deliberately using the other label orientation increased true hidden-state Brier in all four fixed settings, even though observed likelihoods remained identical. The exact opposite-minus-true squared posterior gap identity passed in all four. Both archived scripts were retrieved from GitHub and actually replayed, matching the archived JSON rows exactly.

## Scientific limits

These are known-parameter artificial HMMs with artificially known hidden X. The score is for posterior inference conditional on full in-sequence Y, not a prospective test on heldout human data. No probability calibration was measured on real people, and no external team reproduced the result. Programmatic independent enumeration supports internal mathematical correctness only. No inference about actual latent psychological category labels is authorized.

B program: `research/evidence_audit/b_r199_label_switch_hidden_brier_independent_20261027.js`; exact receipt: `research/evidence_audit/B_R199_LABEL_SWITCH_HIDDEN_BRIER_4_EXACT_AUDIT_RECEIPT_2026-10-27.json`. E1 only, E2=0, E3=0, external replication=0. R073 and PESEN v0.1 frozen. No new CI initiated.
