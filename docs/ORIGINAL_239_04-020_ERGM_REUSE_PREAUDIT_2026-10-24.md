# Original239 04-020 ERGM: original-source and strict-reuse preaudit

Date: 2026-10-24. State: OPEN_STRICT_REUSE_SCOPE. Next pending item after 04-007 SIS. This preaudit does not grant E1 acceptance.

## Original non-Chinese literature
Frank and Strauss (1986), *Markov Graphs*, *Journal of the American Statistical Association* 81(395):832–842, DOI 10.1080/01621459.1986.10478342, https://www.tandfonline.com/doi/abs/10.1080/01621459.1986.10478342 . They describe log-linear random-graph models with dependence and sufficient graph statistics such as triangles and stars. Wasserman and Pattison (1996), *Logit Models and Logistic Regressions for Social Networks: I. An Introduction to Markov Graphs and p* *, *Psychometrika* 61(3):401–425, DOI 10.1007/BF02294547, https://doi.org/10.1007/BF02294547 .

## Existing R reuse audit
R316 covers exact independent dyadic probabilities for known-block SBM on four artificial nodes. R314 covers finite degree-proportional attachment. R317 covers time-respecting paths on a fixed contact sequence. Their archived READMEs do not show a normalized exponential-family graph distribution with an explicit triangle interaction. GitHub indexed searches for 'ERGM', 'exponential random graph', and 'triangle statistic' returned no matches. This is a bounded search; early R001–R064 binary ZIP member-level reuse audit remains OPEN. Full historical novelty is unverified.

## Proposed bounded mechanism
A new R341 may enumerate all eight undirected three-node graphs and exact weights proportional to a^(edge count) b^(triangle indicator). The b=1 world is an independent-edge baseline; b=2 provides a constructed closure interaction. Exact enumeration can check normalization and conditional odds, while keeping inference, large-network degeneracy, human network E2 and historical E3 outside scope. Reuse R316 only for conceptual dyadic probability contrast. R073 and PESEN v0.1 remain frozen. Complete R series and itemwise audit before classification and fusion.
