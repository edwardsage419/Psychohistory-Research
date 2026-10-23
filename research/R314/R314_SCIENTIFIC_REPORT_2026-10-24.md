# R314 Scientific Report: Exact finite preferential attachment E1

Date: 2026-10-24 Asia/Taipei. Original 239 catalogue ID **04-016**, original priority P1, newly assigned research ID **R314**. Explicit scope: **synthetic finite mechanism E1**, with no new measured human E2 or historical E3.

## Frozen first-party mechanism

Primary paper: Barabási and Albert (1999), *Emergence of Scaling in Random Networks*, *Science* 286:509–512, DOI https://doi.org/10.1126/science.286.5439.509 . Follow-up reference for exact rule: https://networksciencebook.org/chapter/5 .

Research protocol frozen in git **before all R314 code, sources or results**: [R314 freeze](../../protocols/R314_BARABASI_ALBERT_THREE_SEED_TWO_ARRIVAL_54_TARGET_SOURCE_PRESCORE_FREEZE_2026-10-24.md), commit `0426722f05cb409655f0bee5897d4b57c87cfa0a`.

The newly arriving vertex attaches exactly one undirected edge to one existing vertex with probability equal to the existing vertex degree divided by the sum of all old vertex degrees. Three labeled, connected seed graphs: P3 path with degrees (1,2,1), K3 triangle with degrees (2,2,2), S4 four-vertex star with degrees (3,1,1,1). Each seed undergoes exactly two arrivals and all paths are enumerated with exact rational probabilities.

## Domain and finite mathematical findings

The first arrival yields 3+3+4=10 potential target atoms; conditional second arrivals 3×4+3×4+4×5=44, for exactly **54 complete original synthetic source rows**, representing **44 complete two-arrival paths**. The full path count is 12 under P3, 12 under K3 and 20 under S4.

For the first arrival:
* P3 targets have probabilities (1/4, 1/2, 1/4).
* K3 targets have probabilities (1/3, 1/3, 1/3).
* S4 targets have probabilities (1/2, 1/6, 1/6, 1/6).

The first-arrival selected old node acquires an additional degree and its relative weight in the next choice updates with the changed total degree. Every conditional target-choice distribution sums to 1, and each seed's complete two-step path distribution sums to 1. At every attachment, exactly one fresh vertex with degree one is added; old selected vertex degree increases by one; all other old degrees remain equal; total degree increases by exactly two. The graph remains simple, undirected, and connected.

These finite calculations distinguish preferential attachment from uniform random target choice. They do **not** test convergence to a power-law, estimate any degree exponent, fit or predict human friendship networks, or reproduce the original paper's large-network scaling simulations. A synthetic target source row is an enumerated alternative, not an empirical node event.

## Auditable output

* [All 54 target choice source atoms](R314_ALL_54_ORIGINAL_TARGET_SOURCE_ATOMS.csv) and [all 44 complete path outcomes](R314_EXACT_44_TWO_ARRIVAL_PATH_RESULTS.json).
* [Pure Python exact generator with unit tests and archive equality](r314_exact_preferential_attachment.py).
* [Independent reimplementation](../catalogue_audit/independent_r314_source_audit.py) reconstructing the source rows and paths without importing the main calculator.
* [GitHub CI](../../.github/workflows/r314-preferential-attachment-exact-e1.yml), to test on Python 3.11 and 3.12, followed by the independent standalone auditor.

The formal limited E1 acceptance should be written **only after verification of the successful live CI run**. R073 and PESEN v0.1 remain frozen. 04-016 is the only permitted new original239 source mapping in any subsequent v3.1 index.
