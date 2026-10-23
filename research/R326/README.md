# R326 Hierarchical Bayesian Learning: finite three-group pooling E1

Original239 **02-007**, P2. [Frozen protocol](https://github.com/edwardsage419/Psychohistory-Research/commit/5be3b4f7ba1035fb8a655fc8a4a0263e92154cad) preceded [source and 64 artificial histories](https://github.com/edwardsage419/Psychohistory-Research/commit/2eeeb3564886d3d2f3039742bb15b3f0e704cfab). Three groups each with two Bernoulli observations, two global regimes and two group theta values. Exact full hierarchical posterior and independent-group baseline for every one of 64 six-bit histories.

Group1 fixed 01 with other groups all successes yields hierarchical next-success prediction **17/29**, with other groups all failures **12/29**. Independent group1 prediction remains **1/2**. All 64 histories pass complement and group-permutation checks.

**PASS_BOUNDED_E1_FINITE_HIERARCHICAL_BAYES_POOLING_ONLY**, after [three green CI jobs](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/40022140444): Python 3.11/3.12 each 24 tests and independent no-import enumeration.

[Scientific report](R326_SCIENTIFIC_REPORT_2026-10-24.md), [formal acceptance](R326_FINAL_ACCEPTANCE_STATUS.json), [machine receipt](R326_MACHINE_RECEIPT.json), [source](r326_hier_bayes.py), [64 original artificial histories](R326_ALL_64_ARTIFICIAL_GROUP_HISTORIES.csv), [exact results](R326_EXACT_HIERARCHICAL_PREDICTIONS.json).

Replay `python research/R326/r326_hier_bayes.py --test`, `--audit`, and `python research/catalogue_audit/independent_r326_hier_bayes_audit.py`. Project-defined finite E1 only, no human E2, historical E3 or actual cognitive model fit. R073/PESEN v0.1 frozen.
