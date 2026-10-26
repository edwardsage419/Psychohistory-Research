# B independent scientific audit: R178 score interval coverage

Date 2026-10-26. Frozen prior to execution by `protocols/R178_WILSON_SCORE_COVERAGE_THIRD_METHOD_FREEZE_2026-10-26.md` (commit `8712c87d8af4800f19be7acc9ccc6b7985a74043`).

The R route evaluates rational score inequalities and sums included probability masses. The B route independently checks integer cross multiplication and sums *excluded* masses, subtracting from one. For Wilson, the integer criterion is `(k*b-n*a)^2 * 25^2 <= n * 49^2 * a * (b-a)` for p=a/b. For Wald, it is `(k*b-n*a)^2 * n * 25^2 <= 49^2 * k*(n-k)*b^2`. These are equivalent to the prespecified fixed z=49/25 formulas.

Executed checks: 540 cell membership decisions, 60 world level exact coverages, original 30 Wald values, 60 negative control changed Wilson memberships with z=1. Discrepancies: 0; original Wald discrepancies: 0. Scripts and exact receipts archived in distinct B and R paths.

Risk review: no empirical holdout, no empirical calibration, no clustered bootstrap on real data, no independent sample, no real negative cases. The 30 PMFs reuse six parameter settings and five related artificial mechanisms. Scientific state INTERNAL_METHOD_INDEPENDENT_E1 only. E2=0, E3=0, external researcher replication=0. No Actions requested due to unresolved billing free quota.
