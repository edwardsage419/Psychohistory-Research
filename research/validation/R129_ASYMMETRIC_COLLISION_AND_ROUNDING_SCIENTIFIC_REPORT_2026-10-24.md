# R129 independent asymmetric collision and rounded Table 1 scientific report

Date: 2026-10-24. Original239 05-005. Protocol was frozen in earlier commit `7b6d43814a676d041e06b53821a49a7610aaa41d` before this code and computation. Original R129 source Git blob `2e5dd6aa387011b1ddbe39ff09b6ec850e51d027` was read from main. Original 1973 source is Maynard Smith and Price, *The Logic of Animal Conflict*, Nature 246:15-18, DOI 10.1038/246015a0. This is a bounded internal mathematical extension of the existing R129 study.

## Actually executed independent finite checks

A JavaScript implementation, separate from the original Python R129 source, enumerated **49 ordered asymmetric marginal pairs** on the frozen seven-probability grid using 12 explicit atoms per coupling. Both lower and upper couplings were constructed and checked: **196 marginal checks, 98 collision checks, 98 welfare comparisons**. Every case exactly satisfied `max(0,p+q-1) <= P(H,H) <= min(p,q)`; the independent product `p*q` also lay in the interval. For the project's V=2,C=6 toy game, direct four-outcome total-payoff enumeration agreed with `E(total)=2-6*P(H,H)` at both sharp endpoints.

Controls: p=q=1/3 permits collision 0 to 1/3 and total welfare 2 down to 0; p=1,q=1/4 fixes collision 1/4 and welfare 1/2; p=0,q=1 fixes collision 0 and welfare 2. Two deliberately altered integer counts were rejected by the independent audit's check function. All 49 source records were archived.

The **25 cells** of the original author's published one-decimal five-strategy payoff table were independently converted into conservative closed rounding intervals of width 0.1, and compared across five opponent columns. **Seven** candidate best-response entries remain possible under the printed precision, while **three** are robustly strict. Against Mouse, Hawk/Bully remain indistinguishable; against Retaliator, Mouse/Retaliator remain indistinguishable. A strict Retaliator ESS refinement cannot be established from the rounded printed values alone. No claim about the author's unobserved simulation trajectories or their actual rounding rule beyond this conservative interval analysis.

## Scientific scope and remaining gates

The 49-world asymmetric collision result is a **project-created E1 mathematical extension**. The 1973 five-strategy matrix is an author's printed simulation aggregate, not human E2, and no actual animal behavior is reanalyzed. The coupled action distributions are probability constructions and are not automatically correlated equilibria. No new human sample-out prediction, calibration, external independent team replication or historical E3 evidence. New E2=0, E3=0.

This round created a complete deterministic Python replay source but **did not execute that new source against the full GitHub checkout** and did **not initiate new GitHub Actions**. Therefore verdict is `PASS_BOUNDED_INTERNAL_JS_FINITE_E1 / PYTHON_REPLAY_AND_NEW_CI_PENDING`. Existing historical R129 68-test CI remains separate. No original239 queue decrement. R073 and PESEN v0.1 remain frozen. No paid compute or new cost-bearing resources.
