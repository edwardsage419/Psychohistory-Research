# R252 S48: finite source information estimates and observational equivalence

Date: 2026-10-29 (Asia/Singapore). EVIDENCE=E1 artificial mathematics only. Original R252 formal acceptance remains unchanged.

## Freeze and source
Protocol `protocols/R252_S48_FINITE_SOURCE_SUBSAMPLE_INFORMATION_PRESCORE_FREEZE_2026-10-29.md`, commit `c57653fe521b9c2bad4da8fce95fa794050e320a`, precedes this scoring. Original R252 source SHA256 `febd739ed17cbdac2dff13e32429e8250bfc13f067b31bf641c9679c241d3061`, Git blob `d830affa2734305c113bea37d32c4a4b44c45ca0`. Exactly 9 artificial worlds, 64 original six-bit atoms per world, 576 total; no human participants. Original source not modified. Full sample index, exact rational and prime-log coefficients, integer XYZ counts, and numerical approximations are in `R252_S48_FINITE_SAMPLE_INFORMATION_RECEIPT_2026-10-29.json`. Reproducer `r252_s48_exact_source_information_20261029.js` requires Node.js and validates source SHA256 before producing receipt.

## Locked 288 finite-population sensitivity cells
Eight deterministic shuffle replicates for each sample size 8,16,32,64 and each world. The source indices are sampled without replacement from the same finite artificial 64-atom population. Replicates are a deterministic design grid, **not** IID human subjects, and no sampling p-values or confidence intervals are claimed. All entropy quantities retain exact rational plus prime-log2 coefficients; decimal bits are presentation approximations.

| n | INDEPENDENT_BITS mean absolute error in I(X;Y), bits | mean absolute error in I(X;Y given Z), bits | positive empirical I(X;Y) among eight replicates |
|---:|---:|---:|---:|
| 8 | 0.148033370512 | 0.258816545575 | 6 |
| 16 | 0.062141835826 | 0.122498338400 | 8 |
| 32 | 0.012101006091 | 0.033894970891 | 7 |
| 64 | 0 | 0 | 0 |

Population I(X;Y)=0 in INDEPENDENT_BITS. Nevertheless, 21 of its 24 deterministic subsamples at n<64 produce strictly positive plug-in I(X;Y). The empirical dependence arises from finite sample cell imbalance; it is **not** evidence of actual information transmission. The eight replicates are not independent replications.

For XOR_SYNERGY, full-source I(X;Y)=0 and I(X;Y given Z)=1 bit. Mean absolute conditional-MI errors across eight deterministic replicates are 0.146418898702, 0.021418898702, 0.022008703445, and 0 bits for n=8,16,32,64. Thus errors need not decrease monotonically for a fixed small deterministic replicate grid.

All 32 sample-pair comparisons between DIRECT_COPY and HIDDEN_COMMON_CAUSE_ALIAS have identical observed XYZ integer counts and exact empirical information, yet original artificial intervention oracles differ. XOR_SYNERGY and XOR_MASK_REPARAM agree in full observed joint distribution at n=64, with different sourcewise representations. Neither plug-in information nor complete observation determines causal direction.

## Integrity, negatives and boundaries
The Node script was evaluated against the original GitHub blob in an isolated JavaScript environment; 288 records generated. A separate Python Fraction implementation reconstructed the original 24,414 source bytes and reproduced the original SHA256 exactly. An independent numeric implementation reconstructed all nine source formulas and compared 1,152 metric values from the GitHub receipt, maximum absolute discrepancy `5.002e-13`, and independently compared all 288 XYZ cell tables and 288 sample-index arrays. A Python command-line implementation also passed 1,152 comparisons against its separately generated exact-coefficient receipt, including a deliberate 999-value mutation rejection. These are internal procedural checks, not external research-team replication.

The deliberately leaked conditioning set containing Y gives H(Y|X,Z,Y)=0 by mathematical identity for all 288 cells. This is a leakage negative control, excluded from legitimate predictive performance. No train/test partition, calibration, new E2 or E3 validation, or real-world mechanism identification is claimed. R073 and PESEN v0.1 remain frozen. No paid compute, data, or GitHub Actions were initiated; CI for new S48 code is NOT_RUN.
