# R341 scientific report: exact three-node edge-triangle ERGM

Date: 2026-10-24. Original239 **04-020 Exponential Random Graph Model**. Grade **PASS_BOUNDED_E1_CONSTRUCTED_THREE_NODE_EDGE_TRIANGLE_ERGM_ONLY**.

## Literature and reuse
Frank and Strauss (1986), *Markov Graphs*, *Journal of the American Statistical Association* 81(395):832–842, DOI 10.1080/01621459.1986.10478342. Wasserman and Pattison (1996), *Logit Models and Logistic Regressions for Social Networks: I*, *Psychometrika* 61:401–425, DOI 10.1007/BF02294547. See [strict reuse preaudit](../../docs/ORIGINAL_239_04-020_ERGM_REUSE_PREAUDIT_2026-10-24.md). R316 provides an independent-edge blockmodel contrast only. Early R001–R064 ZIP strict reuse remains OPEN.

## Frozen protocol, source and results
[Prescore protocol](../../protocols/R341_ERGM_THREE_NODE_32_ARTIFICIAL_GRAPH_ATOMS_PRESCORE_FREEZE_2026-10-24.md) was committed at [67d74d18](https://github.com/edwardsage419/Psychohistory-Research/commit/67d74d18b90d8c435f39d32270da2b7b77667d74), before the first R341 source commit [253dda50](https://github.com/edwardsage419/Psychohistory-Research/commit/253dda5063adf103f0bda0c45d7e9c297194ab85).

The model enumerates all eight labeled undirected three-node graphs. Exact probability is proportional to a^(edge count) b^(triangle indicator). Four artificial parameter worlds, 32 source atoms, rational normalization.

| (a,b) | Z | P(edge 0,1) | P(triangle) | closure odds ratio |
|---|---:|---:|---:|---:|
| (1,1) | 8 | 1/2 | 1/8 | 1 |
| (1,2) | 9 | 5/9 | 2/9 | 2 |
| (2,1) | 27 | 2/3 | 8/27 | 1 |
| (2,2) | 35 | 26/35 | 16/35 | 2 |

All frozen falsifiers F1–F9 passed: 4 worlds, 8 graphs, 32 atoms; exact Z and unit probability; exact marginals; exact triangle probability; exact conditional closure odds; frozen checks; independent byte replay and two tamper controls; three green CI jobs; prescore protocol preceding source.

## CI and provenance
[GitHub Actions run 40063471750](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/40063471750) concluded success with python311, python312, independent all success. Production runs eight unit tests per interpreter. Independent auditor independently enumerates all graphs and recreates CSV and JSON bytes without importing production.

Protocol blob 6d1d2afb4763f94848a052ffdf01811153989b34. CSV blob 41c7df1e190bdd5e4985fe0d4586cbb9d3365325. JSON blob c7cb9c0e981f3f45ff2c80f1a3fac82900dc072b. Production blob c0e0e30e2e030bc0d63a7491b76c09a47d82e0d9. Independent auditor blob a215576698153f0105ca1f0bc6c5f45b4f6471df.

## Evidence boundary
The increased triangle probability under b=2 is an algebraic consequence of the imposed interaction. This finite graph model does not estimate parameters from observed networks, identify social motives, establish large-network mixing or degeneracy, or replicate original empirical work. Human E2: NOT_ESTABLISHED. Historical E3: NOT_ESTABLISHED. Catalogue linkage is provenance only. R073/PESEN v0.1 frozen. R-series evidence audit precedes taxonomy and fusion; personal decision system deferred.
