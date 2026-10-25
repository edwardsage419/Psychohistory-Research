# R171 source tree: independent root and four-point audit prescore freeze

Date: 2026-10-26. Track R primary. Baseline main SHA: 851ae260cff4ff61d83176a9aea8ed3818972d51.
Source is the already archived Phlorest gray_et_al2009 published tree, original fixed commit a2e535f07c05d214fe7d36fe03747f4cfd5f9ca5, research/R171/source/summary.trees. Existing R171 full-distance acceptance remains frozen and unchanged.

Question: what can an already fitted source-tree metric identify about root placement, ultrametricity, and zero-length tip equivalence? This is E1 descriptive structural analysis. No independent historical model inference or external E3 validation.

Predeclared tests and gates:
1. Independently parse the original #NEXUS single rooted summary tree. Preserve all leaf labels and exact integer micro-millennia edge lengths; no forced binary resolution, no negative branches. Reconcile 400 tips, 756 nodes, 755 edges, 52 zero-length branches, and original nine named pair distances against frozen R171 results. Fail on mismatch.
2. Calculate every tip depth from the annotated root, report min, max, median, and exact range. Strict ultrametric condition requires all 400 root depths equal; no rounding tolerance. Interpret a failure only as a property of this published source tree, not as proof against biological or cultural clock models.
3. On the original undirected tree, compute pair distances by independent path traversal. Re-root the same unmodified weighted tree at the first lexicographically sorted tip; recalculate all 79,800 unordered tip distances via the new parent tree and LCA formula. Require exact equality for every pair and record root-depth changes. Do not modify source file.
4. For deterministic quartets, take sorted tips and for k=0..1023 choose indices ((k*37+3)%400, (k*71+19)%400, (k*113+41)%400, (k*157+67)%400). Skip repeated indices and report skipped count. For each distinct quartet calculate three sums d(a,b)+d(c,d), d(a,c)+d(b,d), d(a,d)+d(b,c), require two largest sums equal exactly. Record unresolved quartets where all three sums equal. These are internal consistency tests of a tree metric.
5. Identify all distinct-tip zero-distance pairs from the original tree. Zero-length edges can create zero distances; do not infer identical languages. Report count and group-size distribution if any.
6. Execute two explicit negative controls: change one strictly positive original edge length by one micro-millennium and confirm at least one original pair distance changes; perturb one of the three quartet sums by one micro-millennium and confirm the four-point equality fails on at least one previously resolved quartet.
7. Preserve first failures, actual counts, scripts, output, source attribution, limits, and all costs. E1 only. R073 and PESEN v0.1 frozen. No paid CI.
