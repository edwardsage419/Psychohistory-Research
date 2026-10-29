# B: R276 S72 nonblind independent count and remote-source audit

Date: 2026-10-30 Asia/Singapore. Target key (B,R276,S72,ordered-Z-primitive-vs-binomial-count-and-persisted-receipt). Original R276 and m=2 result 11/16 were read in advance. Internal NONBLIND procedural replication, not external-team or blind replication.

## Independent calculation actually executed

The independent Python 3 standard-library file `b_r276_s72_independent_binomial_20261030.py` was executed locally. It computes nine 3x3 confusion matrices by Binomial(m,theta1) counts k=0..m and compares them against an independent ordered-bit route for each m=0..8. All 81 confusion entries agree exactly. All row masses sum to one. It confirms macro values 1/3, 7/12, 11/16, 71/96, 605/768, 103/128, 1687/2048, 41321/49152, 55271/65536. Local output was rerun and matched byte for byte. Local JSON output SHA256 9f42f8263885fbabb5181714c8fbc58bdeb0c874d71f9fed2f78c4fcd9517972. Local Python source Git blob f3a41ce21d132a0985590f67410ef017f7c10e13 equals the remotely archived B source blob.

## Remote persisted-source validation actually executed

The exact remote GitHub CSV and JSON were read back from main after upload. CSV blob 08dbd0c57ea2f18749d05fe953b2ed907de9cbdd, JSON blob 51eb669c9150b6c90ac81c3ab8cf5f91030f9d0b. An independent V8 exact rational verifier checked:

* 1533 complete unique (m,true-model,ordered-Z) keys and source masses.
* 1031 positive-mass source types.
* Every MAP selection, correct flag, and all three exact posterior probabilities.
* All 81 confusion probabilities, nine macro accuracies, nine source-row totals, all conditional mass normalizations.
* Frozen protocol identity and E1-only scope, with E2/E3 prediction counts zero.

Six deliberately altered inputs were tested and all rejected: duplicate row, missing row, changed primitive probability, changed posterior, E3 scope promotion, changed macro accuracy. No numerical disagreement found. The V8 source checker was run in the execution environment; it has not been separately archived as a standalone JS program. The archived R Python executable is present but its native CLI and full byte regeneration against persisted GitHub receipts are NOT_RUN. Do not treat the independent B Python execution as an R native CLI execution.

## Scientific boundary

Exact finite model verification establishes consistency under the specified artificial Bernoulli observation law and fixed prior. There is no training/test leakage in this complete enumerated probability calculation, but there is also no real out-of-sample prediction, probability calibration on humans, external validation, or historical E3 inference. The 9/10 threshold was frozen before S72 scoring and not reached by m<=8. The original R276 formal bounded E1 acceptance remains unchanged; S72 is an exploratory extension. R073 and PESEN v0.1 remain frozen. GitHub Actions not triggered; billing/free quota NOT_VERIFIED. No new chargeable operations.
