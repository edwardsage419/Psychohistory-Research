# R320 S116 prescore freeze: eventual absorption and six-step censoring gap

UTC freeze date: 2026-10-31. Baseline main HEAD: e4df15671c6b6ef714ed4ff62a9b4fe8d0528ad6.
Target key: (r,R320,original_R320_20261024_plus_S116,eventual_absorption_vs_six_step_censoring).
Status: FROZEN BEFORE S116 COMPUTATION. Original R320 PASS_BOUNDED_E1_DISCRETE_ANALOGUE_ONLY and original239 v7.8 are unchanged.

## Frozen artificial source and constraints

Reuse the six original R320 artificial worlds from research/R320/R320_EXACT_6_FIRST_HIT_WORLDS.json: absorbing bounds a in {4,6}, start z=a/2, p in {1/4,1/2,3/4}, horizon T=6. Verify the six world IDs, source blob identity and original 384-row universe. No new human observations, no parameters fitted, no changes to the R073 scoring or PESEN v0.1. R320 remains a discrete finite random-walk analogue, not continuous Wiener DDM.

## Primary exact analytic route

For q=1-p, r=q/p, eventual upper absorption U=(1-r^z)/(1-r^a) if p!=1/2, else U=z/a. Lower L=1-U. Eventual mean first-passage steps E=(a*U-z)/(p-q) if p!=q, else E=z*(a-z). All arithmetic must use exact rational numbers, and all 6 worlds must be reported. From the original frozen six-step first-hit JSON, compute six-step upper/lower masses U6,L6, survival S6, remaining eventual masses U-U6,L-L6, and conditional upper probability given survival (U-U6)/S6. Report exact total eventual vs finite hit gap S6 and mean E vs original E[min(tau,6)]. Require U+L=1, U6+L6+S6=1, residual masses >=0, residual masses sum to S6, E >= E[min(tau,6)], and p complement symmetry.

## Independent B audit and controls

B route must not import the primary code. Solve finite-state absorbing Markov equations with exact Fraction Gaussian elimination for U and E from interior states 1..a-1. Independently reconstruct six-step hitting probabilities by surviving-state forward propagation, compare each original frozen time/side cell, and compute the conditional residual. Verify all six worlds and reject at least 8 prespecified mutations: missing world, duplicate world, altered p, altered eventual upper, altered expected time, altered finite survival, altered residual upper, and false E2 evidence label. Run tests under normal Python and python -O. Preserve any real failures and distinguish B nonblind internal replay from external independent reproduction.

## Outputs and boundaries

Write new-only paths research/validation/r320_s116_eventual_absorption.py, research/validation/R320_S116_EXACT_EVENTUAL_RESULTS.json, research/validation/R320_S116_EVENTUAL_ABSORPTION_SCIENTIFIC_REPORT_2026-11-01.md, research/evidence_audit/b_r320_s116_absorption_linear_audit.py, research/evidence_audit/B_R320_S116_NONBLIND_LINEAR_SYSTEM_AUDIT_2026-11-01.md. A separate scout record may examine public human choice/RT data, with no E2 scoring absent full raw verification. GitHub commit, CI and billing must be reported only if actually verified. Do not dispatch Actions without verified zero-cost condition. E1 artificial extension only; E2=0, E3=0; no external independent team. Original R320, R073, PESEN and original239 remain frozen.
