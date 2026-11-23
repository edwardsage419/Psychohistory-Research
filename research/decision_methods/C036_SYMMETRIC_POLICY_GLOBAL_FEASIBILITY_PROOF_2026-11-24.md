# C036 supplement: global feasibility of symmetric two-scenario lossy reassignment

Date: 2026-11-24. Status: ANALYTIC_CANDIDATE. Independent acceptance NOT_RUN.

## Scope and provenance

This is an independent analytic extension of C036 and its 2026-11-23 loss supplement. The earlier budget-slack formula was explicitly restricted to symmetric initial allocations. Here a symmetry and convexity argument proves that restriction loses no feasible policies **for the specified two mirror scenarios and linear donor-side transfer loss**. This does not change frozen R evidence, C035/C036, or engineering behavior.

## Decision and assumptions

Initial nonnegative allocations are (a, 10+s-a), where s>=0. Scenario I requires final A>=7 and B>=3. Scenario II requires final A>=3 and B>=7. Both scenarios are observed in time; a separate post-observation transfer is authorized. Transferring t>=0 removes t from the donor and delivers (1-lambda)t to the receiver, 0<=lambda<1. Each scenario's donor-side transfer t<=k, k>=0. There is no external replenishment, borrowing, nonlinearity, minimum transfer size, or scenario-dependent transfer cap. Only one direction is used per scenario.

## Symmetry proof

Permit temporary variables u_s>=0 for A-to-B and v_s>=0 for B-to-A in each scenario, each <=k through u_s+v_s<=k. Final amounts are A_s=a-u_s+(1-lambda)v_s and B_s=10+s-a-v_s+(1-lambda)u_s. Feasibility constraints are linear in (a,u_s,v_s); their joint set is convex. Interchanging A with B and scenario I with scenario II maps every feasible policy to another feasible policy. Averaging the two policies yields a feasible policy with a=(10+s)/2 and mirrored scenario transfers. If the averaged transfer uses both directions, cancel min(u_s,v_s) from both: both final balances weakly increase by lambda times the canceled amount, while donor-side total transfer decreases. Therefore a feasible single-direction policy exists. Consequently, any feasible asymmetric initial policy implies a feasible symmetric initial policy. The converse is immediate.

For 0<=s<4, the symmetric initial amount is 5+s/2<7. In scenario I the least B-to-A donor transfer required is t=(2-s/2)/(1-lambda), with the reverse transfer in scenario II. Feasibility requires t<=k and donor residual 5+s/2-t>=3. The exact necessary and sufficient conditions are

s >= max(0, 2*lambda/(1-lambda/2), 4-2*k*(1-lambda)).

For s>=4, initial allocations can already satisfy both scenarios without transfer, so feasibility holds for all k>=0 and 0<=lambda<1. For 0<=s<4 the formula above applies, including k=0 (then the lower bound is 4 and no such s qualifies). At lambda=0 and s=0 it reduces to k>=2.

## Exact boundary witnesses

* lambda=1/10, k=2: minimum s=2/5; initial (26/5,26/5), transfer 2, final (7,16/5) or reverse.
* lambda=1/10, k=40/19: minimum s=4/19; initial (97/19,97/19), transfer 40/19, final (7,3) or reverse. Decimal-grid enumeration can miss this rational boundary; analytic fractions are required.
* lambda=1/100, k=2: minimum s=1/25; initial (251/50,251/50), transfer 2, final (7,151/50) or reverse.
* lambda=1/10, k=1, s=2: minimum s=11/5 by transfer-cap inequality, so s=2 fails; at s=11/5, initial (61/10,61/10), transfer 1, final (7,51/10) or reverse.

## Baseline, acceptance, and failure conditions

Baseline: C036's lossless transfer bound k>=2 for s=0. The symmetric policy above is globally sufficient and necessary **only under the listed mirror-scenario linear assumptions**. Independent acceptance should test asymmetric initial policies, equality cases, k=0, lambda=0, rational boundaries, s>=4, and directional caps. Test a counterexample with scenario-dependent caps or nonconvex minimum transfer amounts before extending the theorem. Real-world adjustment rights, deadlines, losses, and resource units require data-track evidence. Engineering adoption remains owner-gated.

## Evidence and status

Proof: analytic linear-constraint symmetrization, with exact rational boundary calculations. Synthetic evidence only. No original-paper reproduction is claimed for this elementary derivation. Independent implementation, real-world validation, and scientific acceptance NOT_RUN. No CI, paid API, or private records used.
