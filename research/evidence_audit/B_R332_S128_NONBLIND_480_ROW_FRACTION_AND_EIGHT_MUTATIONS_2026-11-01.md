# B-track independent scientific audit: R332 S128, full constructed source and mutation controls

Date 2026-11-01 UTC. Target key: (b,R332,S128-v1,nonblind_complete_480_row_reconstruction). Status PASS_NONBLIND_INTERNAL_E1. This is a procedural and mathematical second implementation by the same research workflow, not external blind reproduction.

## Frozen inputs and read scope
Read original R332 protocol blob 17d2022bece9d78a011796e61b581bf172b0c04a, original R332 Python solver blob fd468b3177c98c59a4612ac9ce5b719ad11398d4, original 14-world JSON blob 5d7c162c968171f0bb45320ffde835035ed46486, new S128 preregistration commit b203dc38183c1cdbabf8082d8c4927217b7b05e8, and complete newly persisted S128 CSV/JSON and primary JavaScript. Reviewer was already aware of the new result summaries and source design. BLIND=NO.

## Independent computation
A standalone Python standard-library auditor was written without importing the R332 original Python or S128 JavaScript. It uses itertools.product to reconstruct every task subset and both realized payoffs, computes integer weighted expectation for each of 60 worlds, selects lexicographic maxima, and checks exact ordered row dictionaries and 60 full world dictionaries. Source file `research/evidence_audit/b_r332_s128_independent_audit.py`, exact Git blob 14297c39f33f24e221c030d157ab372de68b161b. It was executed in the available local Python interpreter in ordinary and optimized (-O) modes, with result `PASS_NONBLIND_INTERNAL_E1: 60 worlds, 480 rows, 8 live mutations rejected` in both modes.

The separately reconstructed complete CSV has Git blob `6f60aeb788a81f935caaec470a80e1ce3bbb87e1`, identical to the remote persisted CSV; 22,703 bytes, FNV32 d406adb3. The separately reconstructed complete JSON has Git blob `a94076add723eaf85eb50bb5955049dce1f4a6d5`, identical to the remote persisted JSON; 16,816 bytes. Git blob identity compares full bytes and guards against partial-row-only verification. Remote exact archived JS source (blob b3c82120fb80975f426259adab6a8ce04f27afa1) was executed with a V8 Node-module shim against the actual fetched remote CSV/JSON; returned `R332 S128 exact finite E1 checks PASS`. A deliberate persisted JSON world-count mutation was rejected by this replay. This V8 shim is NOT a native Node CLI run.

## Eight live Python mutation controls
1. Remove one CSV row.
2. Duplicate one CSV row.
3. Change one task cost.
4. Change one candidate expected utility.
5. Change one winning subset in the JSON receipt.
6. Promote JSON model identity to E2_HUMAN.
7. Duplicate one JSON world.
8. Corrupt one information-value gap.

All eight were verified non-no-op and rejected by the independent auditor in both Python modes. The independent check uses explicit ValueError paths rather than assert statements, so -O does not disable it. This tests bounded source and receipt coverage; it is not eight independent scientific replications.

## Scientific validity checks
Data leakage: N/A for fully enumerated artificial deterministic worlds; no training or test subjects. Baselines: robust low-capacity allocation and best precommitment, both fully enumerated; capacity-aware oracle is an upper bound, not a deployable predictive model. Out-of-sample prediction, probability calibration, bootstrap uncertainty and independent participants: NOT_APPLICABLE to E1 artificial exhaustive enumeration; empirical claims remain OPEN. Negative results: 36/60 worlds have exactly zero information value; 24 positive; 20 have precommitment strictly outperform robust baseline. Endpoint k=0/4 all have zero information gap. Recoding never decreases any optimal expected value under the fixed cost assumption. The all-or-nothing infeasibility payoff is an explicit modeling choice, not a measured human penalty. There is no causal identification, human E2, historical E3 or external independent replication.

## Execution, scope and remaining gates
Archived R332 S128 primary native Node CLI: NOT_RUN. Full repository regression and new GitHub Actions: NOT_RUN. Historical R332 CI success is archival context and does not apply to S128. GitHub account billing/free quota: NOT_VERIFIED. No chargeable resources used or triggered. Preserve R073, PESEN v0.1 and original R332 statuses; no claim of upgraded scientific acceptance. Next B target: prioritize an unfilled native execution gate in R329 S125 or R330 S126 after verifying live main and other-track activity.
