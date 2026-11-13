# R183 oracle null control: independent BigInt rational recheck

Date: 2026-11-14. Scope: postfreeze R183 supplementary exact Fisher audit only.

## Source identity

At read time, main HEAD was `9d52f9ede7bee60736575367a629218580987da1`. The 15-world original JSON at `research/R183/supplementary_exact_fisher_type1_20261113/R183_FISHER_NULL_EXACT_RESULTS_20261113.json` had Git blob `9eec0c72b5c4c14d8091a5d0993b5fab57fafc90`.

## Independent calculation performed

A standalone JavaScript BigInt rational implementation, separate from the source Python program, evaluated all 15 oracle null rejection probabilities. Fractions were normalized by Euclidean GCD at every arithmetic step. For each source and n=4,8,12, the implementation formed the exact count PMF using binomial, rising-factorial beta-binomial, or zero-inflated binomial mixture formulas, then independently formed the distribution of absolute count difference by double convolution. For each integer distance d, it computed the inclusive survival probability Pr(|K1-K0| >= d). The oracle rejection probability was the sum of probabilities at distances whose survival probability was at most 1/20.

All **15 exact rational outputs matched** the archived `known_full_null_PMF_oracle_type1` fields with zero mismatches. This includes the zero-rejection case for n=4 and beta-binomial concentration 2. The calculation does not import or execute the original Python implementation. It checks oracle calibration arithmetic, not the Fisher rejection calculations or external real-world predictive validity.

## Scientific limits

Evidence: bounded internal E1 arithmetic replication. No E2/E3 promotion, no original frozen source/protocol modifications, no itemwise scientific closure. The oracle assumes the full null source mechanism and p=1/4 are known. It is not an operational test for unknown dependence from one cluster per arm. Historical 239-item queue remains uncounted in this audit. No CI or paid services executed.

## Reproduction specification

For each of 15 source/n pairs: compute PMF P(k), k=0..n; compute D(d)=sum over k,j with |k-j|=d of P(k)P(j); compute T(d)=sum over e>=d D(e); sum D(d) where T(d)<=1/20. Compare reduced rational string to archived JSON oracle field. Arithmetic uses arbitrary-precision integer numerator/denominator throughout. The independent check found 15/15 matches.
