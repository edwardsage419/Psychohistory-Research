# B audit: R329 S125 no-import independent KL check
Date: 2026-11-01 UTC. Status: PASS_NONBLIND_INTERNAL_E1; external independent replication NOT_RUN.

## Prespecified audit target
Target (b,R329,S125-v1,source_atom_score_policy_identity_and_negative_controls). The protocol was frozen at 84161eebcee14924d58df49874f21262f20525fb before new scores. The B auditor was implemented independently of primary source. Previously read materials include the original R329 scientific report, original 18-world JSON and original R329 code; this is NONBLIND. This work is not a blind replication.

## Inputs and independent route
Actual remote files fetched and checked:
* primary JS blob 0d3428a8dcfad1113e19d2e19ae39bd4c8d02ef8
* 720-atom CSV blob 6c65f8aedf27fb45c6933d143a66fe29478defcf
* 90-world JSON blob b002eafb9efdfbdf4b0fc21b2f4a0dc40bf4f1e3
* original R329 18-world JSON blob 19218910a5b59e222f2b7f4ae64b7fc88f4b2eb8
* final independent B source blob 17d2fc9645cb7793dd39804e38529849f84c2c50.

Primary archived JavaScript source was executed in the V8 environment; its full generated CSV and JSON strings matched both persisted artifacts exactly. B used separately written rational arithmetic to reconstruct all 720 joint atoms and calculate G as KL(predicted observation||preference)+conditional observation entropy+cost, without importing primary code. All 90 world keys, 90 choices, both scores, both information quantities, six accuracy series, 18 original q=3/4 score/choice records, 36 zero-mass atoms and evidence-grade labels passed. An additional local Python Fraction and entropy computation reproduced the six advantage series and 45/45 policy counts.

## Negative controls
Ten actual source/receipt mutations were executed against the independent auditor. Missing row, duplicated row, joint mass tamper, likelihood tamper, flipped policy, score tamper, E2 grade promotion, advantage-series tamper, zero-mass atom tamper, and reordered rows were all rejected. Initial development produced an ineffective policy mutation that replaced an already NOISY label with NOISY, hence the first trial was ACCEPTED (no actual mutation). That failure is retained. The test was corrected to flip the label dynamically; the actual mutation was then rejected. The zero-mass control was further corrected to target a real q=1 zero-mass joint atom. Final corrected source and rerun passed.

## Scientific gates
No leakage or calibration claim is possible from this synthetic finite distribution; all 90 worlds are enumerated, not held-out human samples. Baselines are the frozen NOISY policy and original q=3/4 R329 records. No sample-out human E2, no historical E3, no independent outside-team replication, and no neural mechanism evidence. Full original-author simulation reproduction remains open. Native Node CLI execution of archived scripts was NOT_RUN; V8 execution and separate local Python are the observed execution modes. CI and billing status are checked separately. Passing these internal mathematical checks does not automatically constitute new formal R-series scientific acceptance.
