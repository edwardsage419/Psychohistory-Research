# R284 S80: pre-score protocol for selective-publication high-positive alarm

Date UTC: 2026-10-30. Track: r. Baseline main HEAD: cedfa8eaf8de88d7678db9e832a15d744f309896.
Target key: (r,R284,original-freeze-0a6eccd2+S80-v1,finite-four-study-publication-alarm-vs-complete-registry).
Previously read: original R284 frozen protocol, exact results, original Python source, scientific report and acceptance. Existing R284 CLOSED_BOUNDED_E1 remains unchanged. This is a nonblind internal complementary E1 extension, with original policies already known.

## Fixed question and full source
Retain the original four independent hypothetical studies, Y_i and R_i independent fair bits, 8-bit order Y1R1Y2R2Y3R3Y4R4. Exactly 256 equally likely ordered sources per policy, 768 policy-labelled rows. Preserve the original three policy rules COMPLETE_REGISTRY, POSITIVE_ONLY, POSITIVE_PREFERRED without changing any inclusion or outcome. All original 8-bit sources, including K=0 and K=1, must be retained with probability 1/256.

Define K as published count, J as published positive count, T as true positive count across the four registered studies. The *published high-positive alarm* is 1 exactly when K>=2 and J/K>=3/4; otherwise 0, including K=0 and K=1. Define the *complete registry alarm* as 1 exactly when T/4>=3/4. The fixed 3/4 threshold and K>=2 minimum are descriptive decision rules, not a p-value, significance test or real-world selection detector.

Compute per policy with exact rational probabilities: P(K>=2), P(published alarm), P(published alarm | K>=2), P(complete-registry alarm), P(published alarm and not registry alarm), P(registry alarm and not published alarm), and the paired 2x2 alarm table on identical 8-bit sources. Report zero-publication probability and retain it in denominators of unconditional probabilities. Compare the original R284 publication conditional positive-rate anchors 1/2, 1 and 2/3 without reinterpreting those anchors as this alarm probability.

## Verification and stop rules
R route enumerates 256 original ordered eight-bit sources per policy and records source, Y bits, R bits, inclusion flags, K, J, T, both alarms and 1/256 source mass; aggregate exact fractions.
B route independently derives the alarm and paired table using multinomial counts of published positives i, published negatives j and unpublished negatives l with i+j+l=4, masses 4!/(i!j!l!)a^i b^j c^l. Per-policy single-study category probabilities (a,b,c) are (1/2,1/2,0), (1/2,0,1/2), (1/2,1/4,1/4), respectively. For these specific frozen policies, T=i because positives are always published. The independent route must not import the R enumeration code.
Both routes must match all 2x2 cells, mass, P(K>=2) and conditional probabilities. Negative controls: duplicate, missing source, mass mutation, alarm mutation and evidence-grade mutation must be rejected by B checks. Any disagreement is FAIL and remains recorded. Do not retroactively revise this freeze.

## Evidence and operations
All worlds are E1 artificial. No real publications, human E2 or historical E3 inference. Internal nonblind replication is distinct from external-team replication. R073 model and scoring and PESEN v0.1 remain frozen. Use new append-only paths only, check current HEAD and target existence before each write. No Actions dispatch without verified zero additional billing.