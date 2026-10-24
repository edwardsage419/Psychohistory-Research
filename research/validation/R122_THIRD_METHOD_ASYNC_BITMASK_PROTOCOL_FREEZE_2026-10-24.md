# R122 04-005 next-queue reuse preaudit and independent audit freeze

Date: 2026-10-24. Parent main HEAD: `85270e7ae68858249663be1b109232398e59abc2`. Status: **PROTOCOL_FROZEN; EXECUTION_NOT_STARTED**. Do not change original R122 or its 2026-10-19 protocol.

## Original source and reuse finding

Centola and Macy (2007), *Complex Contagions and the Weakness of Long Ties*, American Journal of Sociology 113(3):702–734, DOI 10.1086/521848. Original publisher article: https://www.journals.uchicago.edu/doi/10.1086/521848 ; University of Pennsylvania hosted original journal PDF: https://ndg.asc.upenn.edu/wp-content/uploads/2016/04/Centola-Macy-2007-AJS.pdf . The original distinguishes distinct reinforcing sources from repeated exposures by the same source. The limited graph rule here requires at least a distinct active neighbors.

Existing `research/R122` already contains the original 2007 source review, two independent algorithms, 51 original tests, 16930 finite n<=4 undirected graph/threshold/seed cases, a six-node two-community bridge counterexample, a formal bounded E1 acceptance and a preserved correction history. Original failed run `39258433825` and corrected successful run `39258676907` were both checked. Strict reuse is preferred over a duplicate R identifier.

## Falsifiable independent third-method protocol

Implement a new standard-library Python auditor using a bitmask graph of reachable asynchronous single-vertex additions, with explicit adjacency masks. From each active state, add one currently inactive node whenever it has at least a **distinct** active neighbors. Explore all reachable states via BFS, assert that all terminal states converge to the same least fixed point, and compare the exact terminal mask with both original R122 algorithms. No calls to the original solvers during third-method BFS.

Freeze the full test universe to all n=1,2,3,4 labeled undirected simple graphs, all seed sets and all legal a in {1,2} intersect [1,n], exactly 2+32+512+16384 = **16930** constructed cases. Store one raw result row per case with graph mask, n, a, seed mask, terminal mask and reached-state count. Require exact source Git blob identity for original source/test/report and re-run all 51 original tests on Python 3.11 and 3.12.

Negative controls: repeated exposures from one active neighbor must never count as two distinct sources; three dispersed intercommunity edges must not be confused with three reinforcing edges that converge on the same initially inactive vertex. The frozen six-node bridge witnesses must match original R122: one bridge and three dispersed bridges both stop at 3 active nodes for a=2, three reinforced edges activate all 6; all reach 6 for a=1. Altering one CSV result and supplying a wrong source blob SHA must both be rejected.

An executable free standard public Ubuntu CI run, a raw CSV, an independent scientific report and separate scoped acceptance are required before updating original239 from its present 162 pending links. An actual failure remains visible; no retrospective change of this protocol to fit a result. Maximum grade `PASS_BOUNDED_INTERNAL_ASYNC_REACHABILITY_E1`. No real human E2, historical E3, external team reproduction, large rewired-lattice simulation or empirical bridge-width identification. R073 and PESEN v0.1 frozen. Personal decision product and fusion postponed.
