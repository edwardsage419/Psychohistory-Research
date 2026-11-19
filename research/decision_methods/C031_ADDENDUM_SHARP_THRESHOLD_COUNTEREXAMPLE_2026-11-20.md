# C031 addendum: sharpness of the uniform-radius regret threshold

Date: 2026-11-20 Asia/Singapore. Status: SYNTHETIC_ANALYTIC_CANDIDATE. Independent acceptance NOT_RUN.

## Gap and scope
C031 established a sufficient strict-separation certificate e<0.75 for the rectangular synthetic utility table. This addendum checks whether that threshold is also necessary for **B to have strictly smaller realized worst-scenario regret than both competitors in every allowed joint realization**. This is a distinct logical claim: a sufficient interval certificate need not generally be sharp. C029, C030 and C031 remain unchanged.

Centers: A=(8,2), B=(5.5,5.5), C=(2.5,8), with each of six utility cells independently in [center-e,center+e], 0<=e<=1. All three options are assumed C028 ACCEPT. Define realized worst-scenario regret R(a)=max_s(max_b u(b,s)-u(a,s)).

## Analytic proof
C031's conservative bounds give R(B)<=2.5+2e and R(C)>=5.5-2e, R(A)>=6-2e. Thus, for 0<=e<0.75, R(B)<R(C) and R(B)<R(A) in every allowed joint realization.

To test necessity, construct one jointly feasible realization for any 0<=e<=1:
A=(8-e,2-e), B=(5.5-e,5.5-e), C=(2.5+e,8+e).

In scenario 1, A is best and C's regret is (8-e)-(2.5+e)=5.5-2e. In scenario 2, C is best and B's regret is (8+e)-(5.5-e)=2.5+2e. In scenario 1, B's regret is 2.5; in scenario 2, A's regret is 6+2e. For 0<=e<=1 this implies:
R(B)=2.5+2e, R(C)=5.5-2e, R(A)=6+2e.
At e=0.75, B and C tie at R=4. At every 0.75<e<=1, C has strictly smaller realized worst-scenario regret than B. Hence e<0.75 is **necessary and sufficient** for universal strict superiority of B over A and C for this exact rectangular synthetic table and e range. The counterexample also shows the strict-separation bound is sharp here; it is not a general theorem for other tables.

## Reproduction and evidence
A local independent-from-repository Python enumeration checked all 64 corners of the six-dimensional rectangle at e=0,0.5,0.75,1. The minimum of R(A)-R(B) and R(C)-R(B) across corners was respectively 3,1,0,-1. This is a computational spot check, not a proof that all interior points were exhaustively enumerated. The analytic certificate and feasible witness supply the all-realization argument.

Simple baseline: C029 point centers selects B (worst regrets 6,2.5,5.5) without any robustness claim. The new witness shows why the point ranking alone is insufficient once e reaches 0.75.

## Limits and acceptance handoff
The result assumes independently variable rectangular cells, fixed scenario set, common cardinal utility scale, no unknown hard constraints, and 0<=e<=1. Known dependence restrictions can exclude the witness and alter necessity. The numeric threshold is synthetic utility precision, not a sampling target or empirical accuracy. If intervals or joint feasibility are unknown, return UNKNOWN.

Independent acceptance track: verify the witness at e=0.75 and e=1, rederive the strict lower-bound certificate without using this file as an oracle, and test a coupled uncertainty set where the witness is infeasible. Data track: evaluate whether any real-world uncertainty set is defensible. No formal program test suite, independent replication, empirical calibration or scientific acceptance was performed by this research track. No implementation authorization is implied.
