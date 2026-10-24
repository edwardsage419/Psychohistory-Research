# Original239 04-024 Heterogeneous Network Models: source and strict reuse preaudit

Date: 2026-10-24. State: OPEN_STRICT_REUSE_SCOPE. Next pending original239 item after 04-023 multiplex. No scientific E1 acceptance in this document.

## Original non-Chinese literature
Sun, Han, Yan, Yu and Wu (2011), *PathSim: Meta Path-Based Top-K Similarity Search in Heterogeneous Information Networks*, *Proceedings of the VLDB Endowment* 4(11):992–1003, DOI 10.14778/3402707.3402736, https://doi.org/10.14778/3402707.3402736 . Sun and Han (2013), *Mining Heterogeneous Information Networks*, *SIGKDD Explorations* 14(2):20–28, DOI 10.1145/2481244.2481248, https://doi.org/10.1145/2481244.2481248 . These explicitly preserve multiple node/relation types and meta-path semantics.

## Reuse boundary
R316 is an exact known-block undirected SBM on a fixed four-node assignment; it demonstrates heterogeneous edge probabilities but does not provide typed meta-path similarity. R343 has two relation layers among the same three nodes and exact union/intersection projections, but does not distinguish actor versus object node types. R341 ERGM counts edges and triangles in one undirected graph. Strict full meta-path reuse is unverified in the checked artifacts; earlier R001–R064 binary ZIP member audit remains OPEN. Broad 04-024 cannot be declared exhaustively new.

## Proposed R344 limited scope
Two type-A nodes and two type-B nodes, binary A-B incidence matrix. Enumerate all 16 typed bipartite graphs. Compute A-B-A length-two path counts and exact PathSim-style normalized similarity for all four ordered A-node pairs. Check symmetry, zero-degree behavior and loss of B-node identity under same-type projection. No original benchmark reanalysis, large-scale embedding, human E2 or historical E3. R073/PESEN v0.1 frozen. Complete R series and evidence audit before classification and fusion.
