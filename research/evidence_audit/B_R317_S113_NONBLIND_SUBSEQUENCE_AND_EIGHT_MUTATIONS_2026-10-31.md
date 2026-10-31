# B: R317 S113 independent exact subsequence audit and eight mutation gates

UTC date 2026-10-31. Target key: (B,R317,S113_d01a9696,source_label_group_exact_nonblind). Read scope: main at ce5d443b90e2d0fc3e78865e131e02fac7938e4f before freeze, original R317 2026-10-24 prescore/source/81 outcomes/report/status, original239 v7.8 crosswalk blob 36f24235901172642c46853298aebb421f1a3552 (239 original catalogue records), 154 pending queue blob 3b96d46b3d88ccafd779a08509c3cfd0e435772f, R316 S112 handoff, E146 cross-track compensating-likelihood note, open Codex PRs including #1/#3. All verification nonblind.

## Frozen independent verification

B Python independently enumerates all time-increasing contact subsequences, with no import of the R JavaScript scorer. It checks 27 schedule identities, the original 81-row contact source Git blob 926c1fee6a473da6bbedb9746cf109f5a3a3eb16, 162 exact directed target labels and arrival times, seven observation partitions, integer correct counts and Fraction Brier. The independent source-origin audit through GitHub connector also checked all 81 original R317 outcome arrays and 12 original static-overstatement pairs.

Results: all 162 labels PASS; 7 observation-map exact scores PASS. Full exact oracle accuracy 162/162 and Brier 0. Static and multiset exact accuracy 150/162, Brier 4/81; no-event baseline 138/162 and Brier 92/729. B code: research/evidence_audit/b_r317_s113_independent_subsequence_oracle.py. Primary receipt: research/validation/R317_S113_OBSERVATION_MAPS_EXACT.json. Primary labels: research/validation/R317_S113_ALL_162_DIRECTED_LABELS.csv.

## Eight prespecified corruption classes

1. Duplicate and missing schedule: REJECT.
2. Missing schedule: REJECT.
3. Changed contact identity: REJECT.
4. Flipped reachability label: REJECT.
5. Changed observation-group count: REJECT.
6. Changed static-map accuracy: REJECT.
7. Changed static-map Brier: REJECT.
8. Invalid evidence promotion to human E2: REJECT.

Python 3.13.5 standard and Python -O each exit 0 for the test harness, all eight invalid cases raise explicit validation exceptions. Both modes produced identical audit JSON SHA256 5a0bd527e08f0f89207ba71aa40446f3fe93bcfc5f04ef0726447a426a99c2d5. No hidden failing mutation is reported. No use of Python assert for acceptance checks.

Archived B script Git blob 106bed78447ded90b020eb20e651a19c4d60f679 matches the locally executed script byte-for-byte. Archived labels Git blob 306ab736a9cefc95c6941538593d047fb7ff5fc7 and receipt blob 4b339ca2676e7b61d1b30a60876b672ab9e1b404 match local executed outputs byte-for-byte. Archived R scorer Git blob 3442f3a46688b933f06c4161d1585457bed04674 was executed in a V8 adapter, which reproduced archived labels and receipt exactly; the adapter simulated Node crypto SHA1, so archived scorer's native Node CLI execution is NOT_RUN. A separately authored native local Node script with the same recurrence and source Git blob passed before archive. The archived R native CLI remains an open verification gate.

## Scientific evidence and risk review

The score is an in-sample Bayes oracle over all 27 artificial schedules, so there is no train/test split, no human calibration and no independent held-out observation. The seven maps were frozen before scoring, so postscore map selection is not used. The complete synthetic universe needs no resampling uncertainty interval; a real contact dataset would require independent time blocks or units, baseline comparison, calibrated probabilities and appropriate uncertainty. The labels are E1 artificial only. No external blind team has replicated the result.

E146 independently reported an R316 S112 function-level compensating-likelihood mutation; its original full Node CLI still has a Git blob guard, and the B R316 exact Bernoulli check covers each likelihood. This is a distinct target, remains read-only, and is not claimed fixed by S113. Codex PR #1 R257 S53 comparator counterexamples and #3 candidate fix are unmerged; no main adoption.

Status: PASS_INTERNAL_NONBLIND_EXACT_E1_AUDIT; scientific S113 acceptance remains PARTIAL_E1_EXTENSION. E2=0; E3=0; external replication NOT_RUN. No Actions dispatched, new commit CI NOT_RUN, billing/quota UNKNOWN.
