# B independent method audit of R148 first-ruin evidence
Date: 2026-10-25. Pre-execution B protocol: `research/evidence_audit/B_R148_PYTHON_FIRST_RUIN_REPLAY_PROTOCOL_FREEZE_2026-10-25.md`.

## Independent recomputation performed
The committed Python 3 standard-library script reconstructs the full state-mass recursion from the original R148 equations. It does not import the Node path enumeration or its transition implementation. It reads the separate integer receipt CSV only for comparison after computing the expected values. At q=f=1/4, eight periods and nine stock states, it obtains exact first-ruin probabilities, cumulative harvest, original net and terminal survival. All 24 year-by-policy first-ruin bins, three terminal survivals, three harvest sums and three net sums agree with the separately executed Node enumeration. All three archived R148 survivor and net checks agree. The local audit returned `checks_passed=40`.

The original Node source was locally executed, and the uploaded Git blob `aac9200fe9bd724fba9130c11df8ad4c7698d4e1` matches that source exactly. The Python B source was locally executed and uploaded without byte differences: Git blob `c62564dc1bbefc3fb0958b85be2ce6a8c1d152db`, local SHA256 `098d3f1a9e41287cfb0b5b63be94d5d06e4d98b4d94db4059b2f685e8431d382`. Machine audit summary and source are archived under this directory.

## Adversarial controls and interpretation
An explicit defective transition that resurrects S=0 to S=1 is rejected by the absorbing-state invariant. A second alternate fee ledger that stops charging after first extinction is distinguishable for QUOTA and ADAPT. This is a sensitivity test only. The frozen eight-year fee ledger must be retained when reporting original R148 net harvest.

The synthetic first-ruin ordering of ADAPT and QUOTA is a within-model result at one specified q/f point, not a claim of causal effects in real ecosystems. No human participants, independent sessions, historical records, held-out sample, calibrated ecological parameters, or external laboratory were involved. Data leakage, predictive calibration, resampling and out-of-sample evaluation are inapplicable to these closed-form synthetic trajectories. Scientific evidence E1 only. Do not count 196608 possible event paths as 196608 independent empirical samples.

## Limits and disposition
`PASS_BOUNDED_LOCAL_INTERNAL_TWO_LANGUAGE_E1`. Remote CI `NOT_RUN`; prior R148 historical CI success does not validate this new code. No change to original R148 acceptance, original239 queue, R073, PESEN v0.1 or external E2/E3 counts. No extra paid compute.
