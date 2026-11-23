# C036 supplement: lossy transfers at full capacity (synthetic counterexample)

Date: 2026-11-23. Status: ANALYTIC_CANDIDATE. Independent acceptance NOT_RUN.

## Scope and deduplication
Supplement to C036 two-stage adjustable feasibility. C036 assumes conservation of all 10 units during reassignment. This note isolates a distinct failure mode: a transfer with any positive physical loss cannot satisfy scenario requirements that already exhaust the initial budget. It does not modify C035/C036, historical R evidence, or frozen protocols.

## Inputs and assumptions
Initial allocations A=a, B=10-a, nonnegative. Scenario 1 requires final A>=7, B>=3; scenario 2 requires final A>=3, B>=7. Scenario is observable before deadline and transfer is permitted. A transfer of t units from a donor removes t and delivers (1-lambda)t to the receiver, with 0<=lambda<1. Thus final total is 10-lambda*t. No external replenishment, borrowing, or substitution is allowed. The earlier C036 transfer cap k is measured at the donor; this distinction matters if losses exist.

## Exact argument
Each scenario requires a final total >=10. For any lambda>0 and any positive transfer t, final total 10-lambda*t<10, contradicting that requirement. Therefore any feasible scenario must use t=0. A single initial allocation cannot satisfy both scenarios without transfer, because it would require A>=7 and B>=7 with total 10. Consequently no two-stage robust policy exists for any strictly positive loss fraction, even with unlimited transfer capacity. At lambda=0, the original C036 result applies: k>=2 is necessary and sufficient, with initial allocation (5,5) at the boundary.

This is a discontinuity at lambda=0, conditional on both scenarios exactly exhausting available resources. It is not a general claim that small losses always make adjustable decisions impossible. Additional budget slack or replenishment changes the conclusion.

## Reproducible minimal checks
For lambda=0 and k=2, initial (5,5) can transfer 2 to meet (7,3) or (3,7). For lambda=1/10 and t=2, the total after transfer is 49/5 = 9.8, below the required 10. For lambda=1/100 and t=2, total is 499/50 = 9.98, also below 10. With lambda>0, a zero-transfer plan cannot serve both scenarios.

## Baseline and acceptance handoff
Baseline: C036 lossless model, explicitly inapplicable when transfer losses are confirmed. Independent acceptance should check lambda=0, 1/100, 1/10; k=1,2,3; donor-side versus received-side transfer volume; and a slack-budget counterexample where a positive-loss transfer can succeed. Data track must verify whether transfers actually consume resources, which units and deadlines apply, and whether replenishment exists. Product track should explain why an apparently tiny loss can invalidate a plan with no slack. Engineering adoption requires separate owner authorization.

## Evidence and limits
Elementary exact arithmetic and a finite 0.1-grid diagnostic were executed; the proof is analytic and does not rely on the grid. All values are synthetic. No original-paper reproduction, real-world data validation, independent program verification, or scientific acceptance is claimed. No CI or paid API was invoked.
