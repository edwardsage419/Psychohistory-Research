# R310 S106 pre-score frozen protocol: exact eventual consensus and absorption time

UTC date: 2026-10-31. Scope: E1 synthetic finite mathematical extension only. Original R310 frozen 2026-10-23 at commit 782990a1cae101a3c0fd5ba37f89dc8ed9c2078c. This protocol must be committed before any S106 outcome calculation. No changes to original R310 code, source rows, frozen scoring, R073 or PESEN v0.1.

## Fixed population, graph and transition rules

Four labeled artificial nodes 0,1,2,3; all 16 binary states, ordered lexicographically. Undirected connected graph topologies in original R310: PATH4 edges (0,1),(1,2),(2,3); CYCLE4 edges (0,1),(1,2),(2,3),(0,3); COMPLETE4 all six unordered edges. Asynchronous site update: choose target i uniformly 1/4, then one of its neighbors j uniformly 1/degree(i), set x_i=x_j, leave other bits unchanged. Self-loop *transitions* from equal opinions must be counted; no mutation or simultaneous update. The 416 directed source event rows and 48 artificial worlds of original R310 are the fixed source universe.

Build the exact 16 by 16 stochastic matrix P_G for each graph by aggregating all target-neighbor source probabilities into resulting binary states. Consensus states 0000 and 1111 are absorbing. For each graph and each state x define q_G(x)=Pr(eventual absorption at 1111 | x) and t_G(x)=expected number of individual asynchronous updates until first arrival at either consensus state. Boundaries q(0000)=0, q(1111)=1, t(0000)=t(1111)=0. For the 14 other states solve exact rational linear systems
q(x) = sum_y P_G(x,y) q(y)
t(x) = 1 + sum_y P_G(x,y) t(y).
Solve with exact rational Gaussian elimination and explicit nonzero pivot checks. If any matrix is singular or exact constraints fail, report FAIL and do not silently regularize.

## Frozen tests and claim boundaries

Primary claim: q_G(x) equals degree-weighted density W_G(x)=sum_i degree(i)*x_i / sum_i degree(i) for all 48 worlds. This follows the R310 one-step martingale and almost-sure absorption on the fixed connected finite graphs, but MUST be checked against exact solved q rather than assumed. Secondary claims: t_G(x) is a finite nonnegative rational number, zero only at the two consensus states, and its 14-state first-step residual is exactly zero for every graph. Do not assume any ranking of graph absorption times before computation.

Prespecified checks: 3 matrices each 16 rows normalized; 416 directed events; 48 q/t records; 42 transient q equations and 42 transient t equations; 6 absorbing boundary pairs; q in [0,1]; t>=0; q equals weighted density in all 48 states; for PATH4 state1000 q=1/6, for CYCLE4 and COMPLETE4 state1000 q=1/4; original PATH4 one-step plain expectation remains 7/32. Include complete machine-readable results, source code, failure-preserving tests and a bounded scientific report. A separate independent no-import Fraction auditor must reconstruct transition rows from undirected edges, verify all fields and test tampered source identity, transition probability, q, t, boundary, and E1/E2/E3 label. Independent work within the same research program is NONBLIND_INTERNAL, not external team replication.

No human data, political elections, empirical networks, social forecasts, historical E3, calibration, held-out prediction, causal claim, or model fusion. New scientific status at most PARTIAL_E1_EXTENSION. Existing R310 bounded E1 acceptance remains unchanged. GitHub Actions must not run until cost-free status verified; otherwise use local computation and report CI NOT_RUN. A data scout and B audit are separate supplementary tracks and must not be represented as R main validation.