# B independent evidence audit: R147 positive-overlap causal twins

Date: 2026-10-25. Target: new R147 prospective protocol commit 5144933bdee0762e6f3223850222827b0fc85036.

## Independent method and observed checks
The main research used finite elementary-world enumeration in JavaScript (128 S worlds and 512 D worlds). B independently used Python standard-library Fraction to sum exact probability products over hidden U for all eight observed (A,B,C) states. The Python implementation was actually executed locally, exited 0, and reported 11 true checks. Its exact joint probabilities are 7/32 at 000 and 111, and 3/32 at each of the other six states, matching the main receipt. B independently calculated P(B=1|A=1)=5/8, P(B=1|A=0)=3/8, conditional P(B=C=1|A=1)=7/16, covariance 3/64 and S's intervention-invariant P(B=1)=1/2.

The two negative controls were discriminating in this constructed setting. Treating B and C as independent conditional on A incorrectly gives 25/64 rather than 7/16 for P(B=C=1|A=1). Treating S's observational risk difference as do(A) incorrectly gives 1/4 rather than 0.

## Scientific gate and unresolved risks
The positivity claim is limited to the conditional treatment assignment P(A|U). U is unobserved, so ignorability given observed A does not follow. Model D deliberately uses a common W for B and C, and B's algebraic reconstruction checks that modeling choice. Both models have the same full observed eight-cell distribution, but distinct causal graphs. This is an exact internal E1 counterexample to identification from the observed distribution alone.

Leakage: no fitted features or predictive train/test data exist in this synthetic experiment. Baselines, held-out prediction, calibration, cluster bootstrap and uncertainty intervals are not applicable to this deterministic identity proof; none were claimed. An empirical policy diffusion model would require all of them where appropriate. Negative controls pass for the constructed mathematical failure modes only. The result cannot support a real policy intervention estimate.

B independence is algorithmic and language-level within one project, not external investigator replication. No E2 human sample and no E3 historical panel were used. Remote CI for this new audit is NOT_RUN; historical R147 CI cannot certify this addendum. R073 and PESEN v0.1 frozen.

Audit result: PASS_BOUNDED_LOCAL_INTERNAL_B_E1. Remaining gates: remote no-cost CI if verified, external investigator reproduction, and real historical identification data if ever available.
