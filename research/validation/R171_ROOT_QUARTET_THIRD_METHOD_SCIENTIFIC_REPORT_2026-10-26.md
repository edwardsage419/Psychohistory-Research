# R171 third-method source-tree root and quartet audit

Date: 2026-10-26. Frozen protocol commit 13b9538f5c118378f7f9df0e8f496aeacb5ae88d. Original source is archived Phlorest Gray et al. (2009) summary tree, source upstream commit a2e535f07c05d214fe7d36fe03747f4cfd5f9ca5, licensed CC-BY-4.0. Source location research/R171/source/summary.trees.

## Exact executed findings

Original tree: 400 labeled tips, 756 nodes, 755 edges, 52 zero-length edges. All 79800 unordered pairwise patristic distances agree exactly after rerooting the same weighted undirected tree at Agta. The nine original frozen named-pair distances agree exactly.

Annotated-root tip depths in micro-millennia: min 1733214, median bounds 4633214 and 4633214, max 4633215, range 2900001. Strict ultrametricity fails for this previously estimated tree. This alone cannot reject a real linguistic clock, because source outgroups, historical taxa, and original calibration may create noncontemporaneous tips.

Deterministic quartet check: 1024 attempted, 16 skipped duplicate indices, 1008 valid; 951 resolved and 57 metric-unresolved. Every valid quartet satisfied exact four-point equality. Rerooting leaves tip distances unchanged, so unrooted pairwise distances alone cannot determine the original root.

Distinct-tip zero-distance pairs: 10. Nontrivial zero-distance component sizes: [2,2,2,2,2,2,2,2,2,2]. These represent zero-length source-tree paths, not evidence of identical languages.

Both executed negative controls passed: perturbing a positive edge by one micro-millennium changed the crossing pair Agta / SquliqAtayal by exactly one unit, and perturbing one maximal quartet sum by one unit violated four-point equality.

## Execution disclosure and limits

First execution failed at Newick position 1260 because the initial parser omitted valid scientific-notation edge length 1e-06. The parser was corrected to accept scientific notation and enforce integer micro-millennia before the successful execution. This failure is retained in the audit record. The frozen protocol remained unchanged.

Scientific status PASS_BOUNDED_INTERNAL_E1_SOURCE_DESCRIPTIVE. This is a new descriptive mathematical consistency and identifiability audit on a previously inferred published tree. No new independent Bayesian tree fitting, migration hypothesis validation, E2 human forecast, E3 independent historical forecast or external independent replication. The new parser and reroot routines share one implementation and do not qualify as external independent verification. The original R171 bounded acceptance remains unchanged. R073 and PESEN v0.1 remain frozen.

Primary sources: https://doi.org/10.1126/science.1166858 and https://github.com/phlorest/gray_et_al2009 . No paid resources or CI triggered. Account billing not independently checked.
