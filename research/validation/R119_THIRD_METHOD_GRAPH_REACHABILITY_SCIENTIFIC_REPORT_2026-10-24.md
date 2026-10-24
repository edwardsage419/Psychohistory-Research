# R119: independent finite neighbor-network reachability and branching audit

Date: 2026-10-24. original239 item 04-002 Watts Cascade Model. Existing R119 is reused without editing its original source, tests or acceptance.

## Original-language source and frozen audit

Duncan J. Watts (2002), *A simple model of global cascades on random networks*, PNAS 99(9):5766–5771, DOI 10.1073/pnas.082090499, original open text https://pmc.ncbi.nlm.nih.gov/articles/PMC122850/ . The original paper's exact solution on an arbitrary random graph, one-neighbor vulnerability condition and Eq. 5 distinguish the infinite random-network branching criterion from finite network realizations. This run directly reviewed the publicly available English full text.

Protocol frozen at commit `5c56e904701260d4a481c4bf42c0bc3e6b828df1`, before constructing the third-method program or artificial records: `research/validation/R119_THIRD_METHOD_GRAPH_REACHABILITY_PROTOCOL_FREEZE_2026-10-24.md`.

## Reproducible results

An independently implemented bitmask breadth-first search enumerates all possible one-person irreversible activation orders from one externally seeded node. Eligibility uses the exact active-neighbor fraction at each vertex. It never invokes the original synchronous or asynchronous solver while constructing its own result.

For all labeled undirected simple graphs and all threshold vectors in (1/3, 1/2, 2/3) with every seed, n=1,2,3 yields respectively 3, 36, 648 worlds, **687 deterministic constructed worlds**. Every independent terminal reachable set agrees with both original R119 solvers. The complete constructed CSV was independently produced in JavaScript and byte-for-byte replayed by Python in two CI jobs. SHA256 `76c54ccded66df7086067f43de66b9019f3bac1699cb604e600b695a5b585b7f`.

Frozen topology checks: six-node cycle gives six active nodes; two disconnected triangles give three despite identical degree multiset. Four-node diamond with node 3 threshold 3/4 reaches four after two-neighbor exposure. In a four-node graph with only edge (0,1), a seed at 0 activates node 1 while isolated nodes remain inactive, giving two. This last example also exposes an incorrect replacement of local-neighbor fraction by global-population fraction.

Independent exact arithmetic for three Eq. 5 branching configurations gives ratios 2, 0, and 1, respectively. These are infinite locally tree-like random-network regime calculations, not finite-graph cascade guarantees. Two deliberate topology/outcome perturbations were rejected.

Actual CI https://github.com/edwardsage419/Psychohistory-Research/actions/runs/40079302747 completed with `success`: Python 3.11 job 120829303356 and Python 3.12 job 120829303585. Both ran the independent 687-world audit and the original 43 tests, reporting `Ran 43 tests` followed by `OK`. Original R119 source and test SHA1 and SHA256 matched the machine receipt `research/validation/R119_THIRD_METHOD_GRAPH_CI_RECEIPT_2026-10-24.json`.

## Method-independent B assessment

The third algorithm provides internal computational triangulation of the deterministic fixed-threshold finite-network mechanism. The original R119 two solvers already agreed on 21,423 constructed worlds. The new 687 worlds give a different state-space method and explicit raw records; they are a smaller independent method check, not 687 new experiments.

No observed human network topology, measured thresholds, exposure timing, participant identities, true cascade events or external study were analyzed. No train/test split, leakage metric, predictive baseline, probability calibration, empirical bootstrap interval or causal identification is possible. The frozen topology controls are mathematical negative examples. The Eq. 5 calculation remains an infinite-network analytic condition with assumptions absent from individual finite graphs.

Formal bounded grade: `PASS_BOUNDED_INTERNAL_INDEPENDENT_GRAPH_REACHABILITY_E1`. New human E2 = 0; new historical E3 = 0; external independent research-team replication = false.

## Governance and costs

Existing R119, R073 and PESEN v0.1 remain unchanged. Workflow uses standard public `ubuntu-latest` GitHub runners and no artifact upload, GPU, paid API, purchased dataset, larger runner or Chinese-language source. GitHub's official billing policy confirms free standard hosted runners for public repositories: https://docs.github.com/en/actions/concepts/billing-and-usage . Early ZIP reuse and real human network transfer remain open. Only original239 04-002 bounded E1 linkage may be updated after strict crosswalk CI.
