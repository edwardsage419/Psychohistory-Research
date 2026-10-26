# R178 third method prescore freeze: exact Wilson score coverage under dependence

Date: 2026-10-26. Stage: bounded E1 addendum. This protocol must be committed before reading derived Wilson coverage outcomes.

## Fixed inputs
Repository edwardsage419/Psychohistory-Research, main HEAD at drafting: `1aae82227172f042b9b326ae1b7edf92b52b5886`.
Only source: `research/R178/R178_EXACT_RESULTS.json` at blob `3b4a5abeaa14b5be32fb258a15aa6bf502b2756c`, with exactly 30 `source_worlds`, n in {4,8,12}, marginal p in {1/4,1/2}, five preexisting generating mechanisms. No refitting, parameter changes or new sample draws. The original R178 Wald coverage and frozen E1 conclusions remain unchanged.

## Frozen question and tests
Compare original nominal 95% Wald coverage with a conventional two sided 95% Wilson score interval under the *same assumed IID Bernoulli working model*. Fixed z=49/25 (1.96), not an exact 95% normal quantile.
For each count k, Wilson includes true p iff `n*(k/n-p)^2 <= z^2*p*(1-p)`; Wald includes p iff `(k/n-p)^2 <= z^2*(k/n)*(1-k/n)/n`. Endpoints count as included. Sum the archived full count PMF with exact rational arithmetic. For all 30 worlds, report Wilson and Wald exact coverage, difference, counts with improvement, tie and worsening, count below nominal 19/20, and fixed n=8,p=1/4 five mechanism comparisons. Check PMF sum, support, mean, and equality to archived Wald exact coverage before any scientific interpretation.

## Method independent B audit and controls
Independent implementation must calculate Wilson membership by integer cross multiplication using k,n and reduced p numerator/denominator, and compute weighted excluded mass (one minus excluded mass) instead of summing accepted masses. Compare all 270 binary membership decisions and 30 exact coverage values. Compare original Wald 30 values independently. Negative control must perturb z from 49/25 to 1 and demonstrate a detectable difference; additionally verify a zero or full count is included only when score inversion warrants it. No postscore change to metric or world selection.

## Evidence boundaries
All worlds are artificial E1. The 30 worlds share six (n,p) settings and five related mechanisms and cannot be counted as 30 independent empirical experiments. No observed empirical coverage, E2, E3, R073 transfer, PESEN revision or external independent replication. Wilson remains IID calibrated; correlated worlds may have severe undercoverage. Archive protocol, executable source, exact receipt, scientific report and independent B audit under distinct paths. Avoid modifying crosswalk or other workflows' files. Do not trigger GitHub Actions without verified zero charge; report NOT_RUN when skipped.
