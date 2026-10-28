# B track: independent R252 S48 finite information audit

Date: 2026-10-29. Frozen R protocol commit `c57653fe521b9c2bad4da8fce95fa794050e320a`. Audited original nine-world E1 source, deterministic 8x4 subsampling, exact rational and prime-log coefficients, and new machine receipt.

## Actual independent work
The R-track JavaScript route reads the original 576-row GitHub CSV and calculates exact coefficient vectors for H(Y), I(X;Y), I(X;Y|Z), H(Y|X,Z) across 288 cells. B-track independently reconstructs each observable XYZ triple from nine mathematical formulas and the 64 six-bit atoms. It computes entropies directly as numeric `-sum(p*log2(p))`, with its own permutation and count implementation, without invoking R-track entropy functions.

A separate direct read of the **committed GitHub machine receipt** compared all 288 original sample-index arrays, 288 integer XYZ count tables and 1,152 independent numeric metric values. No mismatches; maximum absolute floating discrepancy `5.002e-13`. Independent Python 3 command-line oracle `b_r252_s48_independent_numeric_oracle.py` was executed locally against a separately generated exact-coefficient R receipt with 288 records, 576 index/count checks, 1,152 metric checks and a successful 999-value mutation rejection. The GitHub receipt was separately checked by the independent JavaScript formula implementation; Python command-line execution **against the remote GitHub receipt** is still pending.

## Leakage, controls and inference
The frozen full population gives I(X;Y)=0 in INDEPENDENT_BITS, yet 21/24 deterministic smaller subsamples give positive empirical MI. This is finite sampling sensitivity, not real-world evidence. The full 64-source check matches original exact population. Direct-copy/common-cause alias remains observationally identical across 32 sample pairs, despite different frozen artificial do-oracles. Deliberate target leakage H(Y|X,Z,Y)=0 is rejected as a valid prediction benchmark. There is no IID human sample, independent train/test split, calibration experiment, causal effect identification or external research-team replication. No statistical significance claim.

`B_INTERNAL_FORMULA_AUDIT=PASS`; `B_EXTERNAL_REPLICATION=NOT_ESTABLISHED`; `NEW_E2=0`; `NEW_E3=0`; `CI_NEW_S48=NOT_RUN`. R073 and PESEN v0.1 remain frozen.
