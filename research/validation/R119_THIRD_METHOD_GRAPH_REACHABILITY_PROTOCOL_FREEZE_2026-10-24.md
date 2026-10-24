# R119 original239 04-002 third-method graph reachability audit protocol freeze

Date: 2026-10-24. Observed main HEAD `437f7db1988f01081140c004c5c534896759eb93`. This protocol precedes any new R119 independent-audit implementation and is not itself a result.

## Existing source and strict reuse

Existing primary R119 is `CLOSED_BOUNDED`, with original source `research/R119/r119_watts_2002_fraction_neighbor_cascade.py` Git blob `91d1853638fe5f3b3fe241d5fc952cceaee882a4` and test blob `2e2209cddb0bd8f6654390c6ceee7cecc3354a27`. Original CI https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39251971404 reports 43 mathematical tests and 21,423 enumerated synthetic graph/threshold/seed configurations. No original source or test is to be changed.

First-party non-Chinese publication: Duncan J. Watts (2002), *A simple model of global cascades on random networks*, PNAS 99(9):5766–5771, DOI 10.1073/pnas.082090499, https://pmc.ncbi.nlm.nih.gov/articles/PMC122850/ . The original article distinguishes a sparse random-network infinite branching criterion from deterministic finite-network cascade outcomes. This distinction is a required audit guard.

## Falsifiable independent method

1. Build an independent one-node-at-a-time bitmask reachability graph from a single seed on a simple undirected graph. For every inactive node, activation requires degree>0 and exact rational active-neighbor count / degree >= its threshold. No original R119 synchronous, asynchronous or eligibility function may be called to construct expected outcomes.
2. Enumerate all labeled simple undirected graphs, all 3^n threshold vectors from (1/3,1/2,2/3), and all n seed choices for n=1,2,3. Counts must be 3,36,648 respectively, total 687 artificial worlds. Every reachable terminal subset must be unique and must equal the original synchronous and fair asynchronous final membership. Fail on any mismatch.
3. Frozen topology negative controls: six-node cycle and two disjoint triangles have the same degree multiset but final active sizes 6 versus 3 from seed 0 at threshold 1/2; four-node diamond with threshold 3/4 on node 3 reaches four active nodes after two active neighbors; isolated non-seed nodes never activate. Explicitly reject replacing local-neighbor thresholds with global population fractions.
4. Independently calculate three exact branching ratios for degree distributions concentrated at degree 3 with rho3=1 (2), degree 3 with rho3=0 (0), and degree 2 with rho2=1 (1). This infinite locally tree-like approximation must never be asserted to predict deterministic finite graph outcomes.
5. Two deliberate tamper controls must be rejected: alter a frozen expected cascade size, and replace a cycle with disconnected triangles while falsely retaining the cycle result. Check original Git blob identities and re-run the existing 43 tests under Python 3.11 and 3.12.
6. Produce deterministic raw artificial records, an independent replay script, a scoped report, CI receipts, and strict original239 catalogue update only after all gates pass.

Maximum evidence grade `PASS_BOUNDED_INTERNAL_INDEPENDENT_GRAPH_REACHABILITY_E1`. No original human network, external research group replication, new human E2, historical E3, independent causal estimate, probabilistic calibration or held-out generalization is established by these deterministic worlds. Original R073 and PESEN v0.1 remain frozen. Use only standard free public GitHub runners, no paid resource, no Chinese-language sources, no classification, fusion or personal decision product.
