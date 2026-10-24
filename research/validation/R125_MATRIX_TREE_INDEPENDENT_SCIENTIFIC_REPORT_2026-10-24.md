# R125 exact matrix-tree independent method: bounded scientific report

Date: 2026-10-24. Original239 candidate 04-018, existing R125. Scope: constructed finite undirected labeled graphs, n=1..5. Evidence grade: E1 only.

## Prior original sources and strict reuse

Existing R125 directly reviewed Erdős and Rényi (1959), *On Random Graphs I*, original pp. 290–291, https://www.cse.cuhk.edu.hk/~cslui/CMSC5734/erdos-1959-11.pdf, and Gilbert (1959), *Random Graphs*, original pp. 1141–1142, DOI 10.1214/aoms/1177706098. The original fixed-m model and independent-edge model differ in edge-count variance and unconditional connectivity. Existing R125 already enumerated 1099 graphs, checked 4396 G(n,p) weighted cases, 25 fixed-m buckets and 54 unit tests. Original successful run: https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39345096433. Its historical failed runs remain on record.

The additional Matrix-Tree Theorem provides an independent algebraic connectivity route. Frozen protocol: `research/validation/R125_THIRD_METHOD_MATRIX_TREE_CONNECTIVITY_PROTOCOL_FREEZE_2026-10-24.md`, blob `1d03c1020e89b8ce74fed76c12c401af36700f63`, committed before the new code or results.

## Method, complete artificial raw rows and exact results

For each n=1..5, construct the lexicographic potential-edge mask. Form the integer graph Laplacian. Calculate the principal (n-1) minor determinant by the full Leibniz signed-permutation expansion. The empty n=1 minor is 1. Kirchhoff's theorem equates this determinant to the spanning-tree count. Compare `count>0` to the unchanged original R125 DFS. Every graph is archived as one raw CSV row with n, mask, m, spanning-tree count, determinant connectivity and original DFS connectivity.

Counts: n=1:1, n=2:2, n=3:8, n=4:64, n=5:1024; total 1099 rows. All 1099 connectivity classifications agree. The exact G(n,m) roster comprises 25 edge-count buckets. In G(4,m=3), 16/20 graphs are connected. In G(4,p=1/2), 38/64 graphs are connected. Six frozen controls pass: singleton 1 tree, n2 empty 0, four-vertex path 1, C4 cycle 4, K4 complete 16, two disjoint edges 0. All exact G(n,p) connectivity sums at p=0,1/3,1/2,1 for n=1..5 match unchanged Gilbert Eq.(4) recurrence, including endpoints.

Independent additional local arithmetic cross-check used Bareiss fraction-free determinant elimination on all 1099 graphs; it found connected graph counts by n of 1,1,4,38,728 and 25 fixed-m buckets. This additional local check is project-internal and has no separate GitHub CI.

Raw CSV: `research/validation/R125_MATRIX_TREE_1099_CONSTRUCTED_GRAPHS_2026-10-24.csv`; SHA256 `a76ae80e35a545cc91a0cd19f0a90d92c1e160b2fcf7f1cfe10f2674ebe773fa`. Reproduction script: `research/validation/verify_r125_matrix_tree_connectivity.py`. It regenerates every byte of the CSV, rejects modified CSV and incorrect pinned original source SHA, and compares against the unmodified original R125 source/test/report Git blobs `01bf0a45879dc156ad1dcfcaa23624dc44f86ae5`, `34276d7f9719967712ecd2525c1ab378e05f9440`, `6f2f28dd62b7a01e784603f0edae90e7196fbb16`.

## Execution history and CI evidence

Initial new workflow https://github.com/edwardsage419/Psychohistory-Research/actions/runs/40095004020 **failed** in Python 3.11 and 3.12 before mathematical execution: the verifier default argument referred to `PINN` instead of `PINNED`. This was a verifier implementation typo, preserved as a failed run. A subsequent correction was committed before rerunning.

Final new workflow https://github.com/edwardsage419/Psychohistory-Research/actions/runs/40095044503 completed **success**. Both Python 3.11 and 3.12 jobs independently checked the pinned source bytes, all 1099 archived rows, 25 buckets, six controls, Gilbert recurrence and tamper rejection; both reran the original 54 tests successfully. Both job logs reported identical raw CSV SHA256. This is a programmatically independent third method inside the same project, with no independent external research team.

## B: validity review

No real people or observed network data are used, so train/test leakage, held-out predictive skill, probability calibration, resampling confidence intervals and causal effect estimates are inapplicable to the new graph identity checks. The third algorithm and wrong-SHA/CSV mutation negative controls strengthen finite E1 mathematical reproducibility. They cannot establish empirical Bernoulli edge formation, large-n giant-component asymptotics, real social-network diffusion or historical forecast performance.

Formal maximum grade: `PASS_BOUNDED_INTERNAL_MATRIX_TREE_CONNECTIVITY_E1`. New human E2=0, historical E3=0. R073 and PESEN v0.1 unchanged. Directory crosswalk linkage is recorded separately from scientific evidence.

## A: duplicate source correction

The 2022 Montero-Porras long iterated PD source, previously listed as a new scout candidate, is the same original experiment already scored in R096. The duplicate was separately archived at `research/data_scout/MONTERO_PORRAS_2022_R096_PRIOR_E2_DEDUP_2026-10-24.md`. This round added no new R073 independent dataset score.
