# B track independent nonblind audit: R309 S105 exact two-step SIR

Date: 2026-10-31 UTC. Target key: (B,R309,S105,independent_microstate_full_coverage). Status: `INTERNAL_NONBLIND_E1_MATH_PASS / EXTERNAL_REPLICATION_NOT_RUN`.

## Read scope and protocol order
Read the original R309 frozen protocol, source code, original scientific report, final machine acceptance, R308 S104 handoff and S105 prescore freeze. The original one-step example and S105 mathematical mechanism were known to this auditor. S105 freeze was committed **a68643bcb79b49f1d96a491d63332a195175cad9** before S105 numerical scoring. This audit is **not blind**, and it is not an independent external team's replication.

## Substantively distinct calculation
R producer reconstructs the original R309 1,134 event CSV from the binomial closed form, verifies exact source bytes and composes a 21-state transition kernel twice. B source `B_R309_S105_MICROSTATE_AUDIT.py` imports neither the R producer nor the original R309 code. B directly enumerates all binary infectious-to-susceptible contact masks and all old-infective recovery masks for each of 189 frozen one-step worlds, assigns exact Fraction probability to each microstate, aggregates the resulting next compartment state, and composes the independently reconstructed kernel twice.

The original archived CSV Git blob is `2d3034e02c83eeaaffeec7cfc704eb48047134f6`; the locally regenerated 91,042-byte original-source CSV has exactly the same Git blob and SHA256 `9470c1e1c880f51da5c11377b6cc8be7f799542d0cebd1f82d4fc3539cabd134`. B was executed locally against that byte-identical reconstructed original file; the archived original-path default CLI on a fresh repository checkout remains **NOT_RUN**. The original one-step study had independently audited 11,664 binary assignments; S105 reuses the same finite mask universe as an internal third calculation route.

## Actual verification
Both Python 3.13.5 commands were executed successfully, first ordinary mode, then `python -O`:

```sh
python research/evidence_audit/B_R309_S105_MICROSTATE_AUDIT.py
python -O research/evidence_audit/B_R309_S105_MICROSTATE_AUDIT.py
```

The commands above are the reproducible repository-checkout equivalents; the actual local runs supplied `--artifacts /mnt/data/s105 --original /mnt/data/s105/R309_S105_RECONSTRUCTED_ORIGINAL_1134.csv`. Both executions returned `status=PASS`, **189 complete worlds, 3,969 exact state cells, all 189 world summaries**, including P(I1=0), P(I2=0), extinction increment, P(X2>0), and E[S2,I2,R2]. All 3,969 cell identities and full source-universe coverage were explicitly checked. The Python receipt output was byte-identical between ordinary and optimized modes; SHA256 `1e097ec5df03e73a97526ef68ca289c147f97883d5a4f7a0d5c3ebfdefb72f9a`.

Eight deliberate mutations were actually applied and **all eight rejected** in both modes: duplicate state cell, missing cell, changed state probability, changed two-step extinction, changed one-step baseline, changed E[I2], false E2 promotion, and corrupted source digest. Receipt validation uses explicit `ValueError` or `RuntimeError` conditions rather than `assert`; Python optimization does not disable them. There were zero final mutation escapes.

R producer output CSV SHA256 `e9734fbe7a9c9ae28431b20295c27cf3d8a860abf49d155f859489b39463d4f6`, JSON SHA256 `8404c0ed201a4b63340decd85d2ce6f1b4ab66413262fc8345021be41857d781`. The remote archived CSV/JSON Git blobs were read back and matched locally generated blob identities `3aefbbc3b5042b6a93ed4e7b8017d9abb7ba9b53` and `6a6c3853de4d557ec4e72ebc647e95272dd9e52d`. B code itself has the same local and remote blob `30bd30cf71839584306b3bb8e0f5560fdbe4b0ca`. Machine audit output: `B_R309_S105_AUDIT_OUTPUT_2026-10-31.json`.

## Scientific audit limits
No training/test split exists for the exact known-parameter artificial law, so there is no empirical leakage or empirical probability calibration result to certify. The one-step extinction baseline is an exact mathematical comparison, not a fitted or out-of-sample predictive baseline. No independent human/clinical data, cluster resampling, uncertainty interval, network heterogeneity or external replication was examined. The 189 parameter-state worlds are not independent experimental units. Evidence class E1 only; new E2=0 and E3=0. S105 acceptance stays PARTIAL, original R309 bounded E1 acceptance remains unchanged. R073 and PESEN v0.1 frozen.

CI `NOT_RUN` this turn; no paid Actions or API use. GitHub billing and free quota were not independently checked. The old R257 S53 PR #1 counterexamples and PR #3 proposed gate remain unmerged and separate from this S105 result.
