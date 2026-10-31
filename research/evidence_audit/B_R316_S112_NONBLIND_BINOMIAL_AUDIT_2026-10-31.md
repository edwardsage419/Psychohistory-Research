# B R316 S112 nonblind independent binomial audit

Date: 2026-10-31 UTC. Target key: (B,R316,S112_af948405,independent_binomial_source_and_six_observation_receipt). Prescore freeze was committed before R scoring.

## Independence and executed scope
R route aggregates the archived original R316 graph likelihoods in Node. B route uses separate Python Fraction arithmetic, independently reconstructs six Bernoulli factors for every mask and regime, then derives observation probabilities from 2-within and 4-cross binomial combinatorial masses. B imports neither R scorer nor original R316 module. Both routes are within the same research workflow and nonblind: B was able to inspect the R receipt and source.

The original R316 JSON was recreated locally from its archived deterministic generator specification. Its exact Git blob SHA1 equals the remote original `36da587adbc6e1d92824a5fd39516e506569166c`, including the final newline. The remote uploaded R script blob is `379cb2109808f60d41d449638315904b3cb77f4c`, B script blob `3644d1373c08b56aefdacb417020f53f69295c06`, and result JSON blob `410a9c173e020984fa61e7a2420dc0e0e90190ac`. These blobs were fetched from GitHub and matched against the exact locally executed copies.

## Executed tests
Native Node command `node research/validation/r316_s112_observation_coarsening.js --check` returned PASS. The Python B audit returned PASS in normal and `python -O` optimized modes. Source validation checked 64 unique graph masks in each of two regimes, all 128 exact graph probabilities against six Bernoulli factors, edge identities, fixed block assignment and normalization. The B binomial route matched all six receipt cells and confirmed Bayes accuracy=(1+TV)/2.

Eight explicit mutations were rejected in both Python modes: duplicate_mask, missing_mask, wrong_edge_vector, wrong_likelihood, wrong_within_count, false_source_scope, wrong_accuracy, false_E2_upgrade. The negative tests validate semantic coverage without relying only on the Git blob check. No claim of external independent reproduction.

## Preserved development failure
First local B Python script execution raised `SyntaxError: Generator expression must be parenthesized` in the accuracy summation. The expression was fixed before any B PASS claim, then both modes were rerun. The error was a local audit-script syntax defect; it did not alter the original source, frozen protocol or R mathematical receipt.

## Unfinished scientific gates
E1 synthetic exact only. No observed human ties, independent human sample, training/holdout, empirical probability calibration, resampling uncertainty, external team reproduction, historical E3 or causal mechanism evidence. The full local checkout used a byte-identical reconstructed original source and downloaded copies were compared by blob; this is a local native CLI execution, not GitHub Actions CI. The prior R316 acceptance is unchanged. R073 and PESEN v0.1 are frozen.

Commands:
```sh
node research/validation/r316_s112_observation_coarsening.js --check
python research/evidence_audit/b_r316_s112_independent_binomial_oracle.py
python -O research/evidence_audit/b_r316_s112_independent_binomial_oracle.py
```
