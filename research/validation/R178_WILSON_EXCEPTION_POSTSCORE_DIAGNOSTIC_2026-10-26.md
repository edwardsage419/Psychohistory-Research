# R178 postscore diagnostic: one Wilson coverage reversal

Date 2026-10-26. Exploratory analysis after the frozen third method evaluation. No protocol amendment, model retuning or confirmatory claim.

The exact receipt identifies one of 30 worlds where the conventional Wilson score interval has lower coverage than the conventional Wald interval: sample size n=12, true marginal p=1/4, source mechanism INACTIVE_ZIB_Z1_4. Under z=49/25, Wilson includes counts k=1,2,3,4,5; Wald includes k=2,3,4,5,6. The archived original PMF gives P(k=1)=2048/59049 and P(k=6)=4928/59049. The coverage difference Wilson minus Wald is exactly P(1)-P(6)= -320/6561, approximately -4.8773 percentage points.

Original Wald coverage = 116864/177147 = 65.9701%. Wilson coverage = 108224/177147 = 61.0928%. Both remain far below nominal 95%. This counterexample prevents any blanket claim that Wilson coverage dominates Wald under model misspecification, even when Wilson improves 19 of 30 fixed artificial worlds.

Source and exact count PMF: `research/R178/R178_EXACT_RESULTS.json` blob `3b4a5abeaa14b5be32fb258a15aa6bf502b2756c`. Third method frozen protocol commit `8712c87d8af4800f19be7acc9ccc6b7985a74043`. Full receipt: `research/validation/R178_WILSON_SCORE_COVERAGE_EXACT_RECEIPT_2026-10-26.json`. This is an E1 artificial finite support observation, E2=0, E3=0, external independent replication=0.
