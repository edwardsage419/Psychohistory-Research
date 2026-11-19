# C021 addendum: three-period plan versus realization, bounded synthetic test

Date: 2026-11-20 (Asia/Singapore). Status: SYNTHETIC_ANALYTIC_CANDIDATE; independent acceptance NOT_RUN. Research-only method card for personal decision workbench. Parent: C021_ODONOGHUE_RABIN_1999_REPEATED_TASK_PROOF_BOUNDARIES_2026-11-19.md. This addendum does not assert reproduction of O'Donoghue and Rabin (1999) Proposition 6.

## Question and input
Can a decision tool distinguish today's action, the date predicted for a future self, and the realized date? Three periods t=1,2,3; one indivisible mandatory task, at most once, no commitment, no new information, costs c=(3,5,8), quasi-hyperbolic cost weights (1,beta*delta,beta*delta^2) from period 1 and (1,beta*delta) from period 2, 0<beta<=1 and 0<delta<=1. At period 3 execution is compulsory. At ties, choose immediate execution. A sophisticated agent predicts future beta correctly. A naive agent predicts future selves with beta=1 while actual future selves retain beta. No stochastic outcomes or user parameter estimates are assumed.

## Exact conditional decisions
Actual period-2 self executes at t=2 iff 5<=8*beta*delta, otherwise at t=3. A naive period-1 agent predicts period-2 execution iff 5<=8*delta. Sophisticated period-1 agent uses the actual future policy. Given predicted t=2, period-1 execution iff 3<=5*beta*delta; given predicted t=3, period-1 execution iff 3<=8*beta*delta^2. A naive period-1 agent uses its *predicted* future policy in the same comparison. To compute realized paths, advance the agent to period 2 using actual beta after a t=1 wait. This distinction is mandatory; predicted t=2 is not realized t=2.

## Worked counterexample and baseline
Set delta=5/8 and beta=1/2. Naive period-1 agent predicts t=2 because 5=8*delta, and chooses to wait because 3>5*beta*delta=25/16. Actual period-2 agent waits because 5>8*beta*delta=5/2. Therefore naive prediction t=2, realized t=3. Sophisticated period-1 agent predicts t=3 and waits because 3>8*beta*delta^2=25/16; its realized date is t=3. Both initial actions match while predictive accuracy differs. Simple time-consistent baseline chooses the lowest discounted cost under beta=1; at delta=5/8, period-1 discounted costs are 3, 25/8, 25/8, so it executes at t=1.

## Boundary caution
The previous informal statement 'delta<=0.625 implies both agents always wait' is false: delta=0.62,beta=0.98 gives 8*beta*delta^2=3.013...>=3, hence sophisticated t=1 execution; naive predicts t=3 and likewise executes t=1. The prior statement 'delta<0.625 implies both always wait' must not enter production. At delta=0.625,beta=0.5 the naive plan/realization discrepancy persists even though initial actions coincide. These examples are model-specific, not empirical estimates.

## Candidate workbench interface
Inputs: mandatory task count, horizon, per-period costs, beta/delta scenarios, commitment ability, tie rule, known future changes. Outputs: feasibility, current action, conditional future policy, predicted date, realized simulated date, mismatch flag, assumption/provenance labels and uncertainty/UNKNOWN. Never present realized simulated date as observed behavior. If parameters cannot be identified, show scenarios rather than point predictions. Failure conditions: variable costs learned later, cancellation, repeated tasks, uncertainty, capacity changes, utility other than specified cost schedule, or different tie rule.

## Acceptance handoff
Independent track should implement backward induction separately and assert: (a) delta=5/8,beta=1/2 naive predicts 2 but realizes 3; sophisticated predicts and realizes 3; (b) delta=0.62,beta=0.98 both execute at 1; (c) test exact equalities 5=8*delta, 5=8*beta*delta, 3=5*beta*delta, 3=8*beta*delta^2 and one-sided perturbations; (d) compare against beta=1 baseline; (e) preserve predicted versus observed versus simulated labels. Future verification should check the source paper's original definitions and theorem scope. This document is an independently constructed toy calculation, with analytic arithmetic only; software tests NOT_RUN, independent reproduction NOT_RUN, real-world validation NOT_RUN, scientific acceptance NOT_RUN.

Source: Ted O'Donoghue and Matthew Rabin (1999), Doing It Now or Later, American Economic Review 89(1):103-124, https://doi.org/10.1257/aer.89.1.103 . Parent C021 is PRIMARY_TEXT_BOUNDED and its original Proposition 6 mathematical transcription remains PARTIAL. No frozen R protocol or evidence grade changes. No personal data, paid API or CI required.
