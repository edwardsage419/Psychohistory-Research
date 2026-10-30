# R281 S77: 极端概率裁剪与有限样本对数评分互补研究，计算前冻结

date_utc: 2026-10-30
baseline_main_head: 7ebb2ee6012775d3859fea293fc7b95ac735ed9d
target_key: (r,R281,original-cbf8eec7+S77-v1,epsilon-clipping-boundary-forecast-finite-sample-ranking)
evidence: E1 artificial, internal nonblind exploratory
original_protocol: protocols/R281_LOG_SCORE_15_WORLDS_240_COMPLETE_SOURCE_SYMBOLIC_FREEZE_2026-10-23.md
original_R281: CLOSED_BOUNDED_E1, unchanged
R073: FROZEN
PESEN_v0.1: FROZEN

## Problem and legal boundary
Original R281 uses q=0 and q=1 with genuinely infinite expected log loss for interior Bernoulli p. This independent extension asks what happens when a forecast implementation explicitly clips those two boundary reports to epsilon or 1-epsilon. It does not modify original 15 worlds, original raw sources, or their infinite-score convention. The clipping is a separate, named policy.

## Fixed worlds and exact measurements
p in {1/4,1/2,3/4}; boundary b in {ZERO,ONE}; epsilon in {1/16,1/4}. Thus 12 policy worlds. In each, enumerate all 16 ordered four-bit Bernoulli(p) sources, 192 world-labeled atoms, with exact Fraction masses p^k(1-p)^(4-k). q=epsilon if b=ZERO, q=1-epsilon if b=ONE. q is fixed before observing any outcome.

For each source record p,b,epsilon,q,fourbit,k,mass, exact mean loss in rational coefficients of ln2,ln3,ln5, and the indicator of strictly lower sample mean log loss than truthful q=p. Equal losses count as TIE, never as strict wins. Every comparison uses the same four-bit source. All 12 expected log scores and strict-win/tie probabilities are mass-weighted. Retain un-clipped b=0/1 theoretical infinite expected risk as a separate analytic reference, with probability of an infinite four-bit score 1-(1-p)^4 or 1-p^4. Do not silently clip the original R281 policy.

Exact finite loss basis:
q=1/16: L(y=1)=4ln2; L(y=0)=4ln2-ln3-ln5.
q=15/16: L(y=1)=4ln2-ln3-ln5; L(y=0)=4ln2.
q=1/4: L(y=1)=2ln2; L(y=0)=2ln2-ln3.
q=3/4: L(y=1)=2ln2-ln3; L(y=0)=2ln2.
q=1/2: both outcomes ln2.
Exact expected risk is p times success loss plus (1-p) times failure loss, in the same basis. The strict-win decision uses the exact rational inequality between products q^k(1-q)^(4-k) and p^k(1-p)^(4-k), avoiding floating-point threshold ambiguity.

## Independent B route and rejection controls
B computes each expected risk from one-step Bernoulli expectation and each strict-win/tie mass from five Binomial(4,p) counts, without invoking R's ordered-source generator. Compare all 12 worlds. Check 192 unique keys, 16 keys per world, total mass 1 per world, 12 analytic risk coefficient triples, exact win/tie fractions, symmetry p↔1-p and b↔1-b, and zero score-tie when q!=p. Reject duplicate/missing atom, modified mass, modified coefficient, incorrect evidence label, and treating an un-clipped infinity as finite. Keep failed controls and negative findings.

## Interpretation and stop rule
Compute and archive a standard-library Python R script, full atom CSV, exact JSON, a method-independent B script/audit, A data audit and scientific report. No paid services or GitHub Actions. Do not claim E2, E3, external replication, scientific confirmation or a change to original R281 status. This is nonblind: original R281 results and theoretical form were read before the new freeze. Any discovered error is retained with a correction artifact, not rewritten as preregistered success.
