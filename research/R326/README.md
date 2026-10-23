# R326 Hierarchical Bayesian Learning: finite three-group pooling E1

Original239 **02-007** (P2). [Prescore freeze](https://github.com/edwardsage419/Psychohistory-Research/commit/5be3b4f7ba1035fb8a655fc8a4a0263e92154cad). Three groups, each with two Bernoulli observations, two global regimes, two possible group theta values and **64 original artificial histories**. Exact full hierarchical posterior compared with independent group baselines. The group1 01 observation has different hierarchical predictions when groups 2/3 switch from all failures to all successes, whereas independent group1 prediction remains 1/2.

Replay `python research/R326/r326_hier_bayes.py --test`, `--audit`, and `python research/catalogue_audit/independent_r326_hier_bayes_audit.py`. CI and formal acceptance pending. Project-defined artificial E1 only, no human E2 or historical E3. R073/PESEN v0.1 frozen.
