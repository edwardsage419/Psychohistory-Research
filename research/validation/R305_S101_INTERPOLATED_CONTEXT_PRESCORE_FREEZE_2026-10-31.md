# R305 S101 prospective freeze: interpolated context and category switching

UTC date: 2026-10-31. Track R. Parent R305 original frozen source: `a4dfc1f582c9a58eec6cf45b63a34f577800e0eb`. Baseline main: `d9debc5cefa930ea54a8ccd106775bf417d3b602`. New independent finite E1 sensitivity analysis. No modification of original R305, R073 or PESEN v0.1.

## Question and complete artificial universe

Measure how the original R305 project-invented self-categorization choice changes as the four-object feature context is interpolated from X to Y. The original P and Q labels, within/across pair rules, metacontrast B/W, social score r*n_C*MC_C and strict PERSONAL fallback are unchanged. No fitted human SCT model.

Define feature vector for lambda in {0, 1/4, 1/2, 3/4, 1}:
`v(lambda)=(0, 1+3*lambda, 4-3*lambda, 5)`.
Original X, MID, Y correspond exactly to lambda 0, 1/2, 1. Partition P=(0,0,1,1), Q=(0,1,0,1). Calculate within mean of 2 pairs and across mean of 4 pairs with exact rational arithmetic; both within means strictly positive on grid.

For each lambda enumerate r,nP,nQ in {0,1/2,1} and personal threshold t in {0,1,2}. Total 5*3^4=405 decision worlds and 810 labeled category source cells. For each world compute scores and P/Q/PERSONAL with original strict comparison and tie rule. Grid is finite synthetic E1, not sampled subjects or observed time points.

## Prespecified primary outputs

1. Exact MC_P and MC_Q for all five contexts; equality at lambda=1/2 and endpoint parity with original R305.
2. For each fixed (r,nP,nQ,t) 81 configurations, report 5-category trajectory in ascending lambda and the number of adjacent changes among four steps. Report total adjacent changes across 324 comparisons and counts of trajectories with 0,1,2,3,4 changes.
3. Count classifications P, Q and PERSONAL for each lambda across 81 fixed configurations.
4. Negative controls: r=0 yields PERSONAL for every lambda; nP=nQ=0 yields PERSONAL; lambda=0,1/2,1 decisions exactly match original R305 all 243 worlds. No outcome-based filtering.
5. Sensitivity witness: report a full parameter tuple with a category change, if one exists; if none exists report zero. No tuning or expansion of grid after reading results.

## Independent verification and scope

R implementation must generate full 405-row CSV with input and computed exact fractions, plus machine JSON summary. B implementation uses a separate no-import route with explicit six object pairs and independently computes both scores, full row identity, all 324 adjacent changes and baseline parity. Add at least six deterministic corruptions that must be rejected. Distinguish independent internal nonblind programmatic checks from external independent replication. Retain errors and failed tests. No CI unless zero-cost execution independently verified. New S101 acceptance is PARTIAL unless all frozen gates and archival replay are verified; original R305 bounded E1 remains unchanged. No real human E2, historical E3, out-of-sample predictive claims, or causal inference.
