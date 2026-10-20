# R153 pre-computation frozen protocol: spatial interaction and OD constraints

Date: 2026-10-20. Candidate: original curriculum P2 / 06-011 Spatial Interaction Models. Parent baseline: R152 CLOSED_BOUNDED_E1, main commit 49051f364697e0acaef90a718edf9dc83d47083f.

## Evidence scope
E1: original mathematical examples and independently computed numerical checks. E2: no new real individual/session observation. E3: no external historical event forecast. This is neither an author's data replication nor proof about actual spatial migration. R073 and PESEN v0.1 remain frozen.

## Primary literature and source restrictions
A. G. Wilson, *Entropy in Urban and Regional Modelling* (1970), Routledge publisher reissue https://www.routledge.com/Entropy-in-Urban-and-Regional-Modelling-Routledge-Revivals/Wilson/p/book/9780415696319 ; D. L. Huff (1964), *Defining and Estimating a Trading Area*, Journal of Marketing 28(3):34-38, DOI 10.1177/002224296402800307 ; A. S. Fotheringham (1983), *A New Set of Spatial-Interaction Models: The Theory of Competing Destinations*, Environment and Planning A 15(1):15-36, DOI 10.1177/0308518X8301500103. Publisher descriptions/abstracts verified; paper/full-book methods and primary empirical datasets are not independently re-created. Our weighted 2x2 matrix is a purpose-built constrained OD example, not claimed as an author's exact algorithm or Huff/Fotheringham competing-destinations fit.

## Frozen model family
Two origins and two destinations, nonnegative real OD matrix T; row budgets O=(a,b), destination totals D=(c,8-c), and a+b=8. Both dimensions are separate sets of locations so diagonal cells are allowed. Choose a,b from {(3,5),(4,4),(6,2)}, c from {2,3,4,5}, and five strictly positive weight matrices W:
W0=((1,1),(1,1)); W1=((2,1),(1,1)); W2=((1,1),(1,2)); W3=((2,1),(1,2)); W4=((1,2),(2,1)).
Exactly 3*4*5=60 scenarios, all enumerated before code.

Origin-only: S_ij=O_i W_ij / sum_k W_ik. Doubly constrained: maximize sum_ij T_ij log(W_ij/T_ij), under row=O and col=D. The unique positive interior solution satisfies T_ij=u_i v_j W_ij. All 2x2 feasible matrices can be parameterized:
T=((x,a-x),(c-x,b-c+x)), L=max(0,c-b), U=min(a,c).
The independent scalar solution solves x*(b-c+x)*W01*W10=(a-x)*(c-x)*W00*W11, with L<x<U, computed using bisection to 1e-11 absolute tolerance. Compare with independently implemented iterative proportional fitting, alternating row/column rescaling, tolerance 1e-10 on all cells and marginals, 30000 iterations max.

## Prespecified checks
1. All 60 parameter tuples executed and archived individually with input and output values.
2. Marginal conservation to 1e-10, both algorithms agree to 1e-9 per cell, and cross-product equalities checked to 1e-9.
3. All five kernels tested under independent row and column positive multiplicative rescalings: doubly constrained T invariant to 1e-9; origin-only S changes under nontrivial destination rescaling.
4. W0 exact rational benchmark: T_ij=O_i D_j/8, with values cross-checked using Fraction and the computed floating solution.
5. Demonstrate origin-only S generally fails to match prescribed D, while doubly constrained T matches both.
6. Structural-zero supported/feasible matrix W=((0,1),(1,1)) for row (3,5), destination (4,4): unique feasible T=((0,3),(4,1)). Verify via exact 2x2 support conditions, independent of any floating optimizer.
7. Structural-zero infeasibility W=((1,0),(0,1)) for same budgets: no admissible OD matrix; explicit rejection rather than silent convergence.
8. Unmatched row/column totals, negative, nonfinite budgets/weights, and entirely forbidden row/column must be rejected.
9. Final report must describe mathematical assumptions, synthetic-only scope, nonidentification boundaries, algorithms, at least one numerical origin-only/doubly-constrained contrast and separate source/CI/archive receipts.

## Closure gate
Precode freeze committed before implementation. A result requires deterministic replay, source+tests on main, executable test evidence, complete scenario JSON, and re-readable GitHub paths. Do not equate multiple CI environments to independent scientific evidence. Freeze survives any later code changes; deviations must be disclosed as an amendment. Research sequence remains all R candidates, then classification, then synthesis.
