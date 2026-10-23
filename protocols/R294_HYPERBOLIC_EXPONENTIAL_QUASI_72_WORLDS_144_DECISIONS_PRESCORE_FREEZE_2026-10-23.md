# R294 prospective original 01-018 Hyperbolic Discounting bounded time-consistency comparison

Date 2026-10-23 Asia/Taipei. Freeze prior to code and computed results. Original catalogue 01-018 P1, original 239 entries remain unchanged. This is an artificial finite mathematical E1 learning study only, not empirical human intertemporal choice fitting. No promotion of the frozen R073 or PESEN v0.1.

## First-party historical/theoretical anchors

R.H. Strotz (1955), *Myopia and Inconsistency in Dynamic Utility Maximization*, *Review of Economic Studies* 23(3):165–180, DOI https://doi.org/10.2307/2295722 . David Laibson (1997), *Golden Eggs and Hyperbolic Discounting*, *QJE* 112(2):443–477 (journal pagination may differ in e-journal), DOI https://doi.org/10.1162/003355397555253, author-hosted page https://laibson.scholars.harvard.edu/publications/golden-eggs-and-hyperbolic-discounting . These motivate analyzing dynamically inconsistent discount schemes. The formula grids, reward pairs, and counts here are researcher-authored discrete test configurations and **do not reconstruct the authors' original consumption-savings calibration, real subjects, or policy counterfactuals**.

## Frozen complete artificial decision universe

Two reward offers always dated at t_A=1 and t_B=2 with early reward a, delayed reward b. Exactly six positive reward profiles generated in lexicographic product order a∈{2,3,4}, b∈{5,7}. Evaluate policy at both decision points t=0 (A and B both in future), t=1 (A immediately available, B future). Two decisions per world; exact tie chooses A (earlier option).

Three distinct model families:
* HYPERBOLIC: D_k(d)=1/(1+k*d), k∈{0,1/2,1,2,3}; 6×5=30 worlds.
* EXPONENTIAL: D_delta(d)=delta^d, delta∈{1/2,3/5,4/5}; 6×3=18 worlds.
* QUASI_HYPERBOLIC_BETA_DELTA: D_{beta,delta}(0)=1, D_{beta,delta}(d>0)=beta*delta^d, beta∈{1/2,1}, delta∈{3/5,4/5}; 6×2×2=24 worlds.

World total **72**, full original chosen-date decision source rows **144**, all exact rational. 72 worlds are settings, not humans or independent samples. Store model, reward pair, fixed parameters, current decision date, both rewards, both delays, both exact utilities, tie status, selected option and binary preference reversal flag per world. Date t=0 and t=1 decisions must both appear once, even ties. No fitting, no stochastic draws and no data leakage.

## Pre-specified formal claims

1. For each world verify both decisions by enumerating 144 rows and independently calculating two exact discounted utilities. Exact ties always select A.
2. EXPONENTIAL cannot reverse its preference under the one-period shift for any δ because U(B)/U(A)=bδ/a at both t=0 and t=1; the choice threshold is constant.
3. HYPERBOLIC reverses from later B at t0 to sooner A at t1 iff b/a > (1+2k)/(1+k) AND b/a <= 1+k. At k=1 with a=3,b=5, it reverses (t0 U_A=3/2, U_B=5/3; t1 U_A=3, U_B=5/2). No earlier-to-later reversal is permitted across these k≥0.
4. QUASI_HYPERBOLIC reverses B→A iff b*delta>a and b*beta*delta<=a. At a=3,b=5,beta=1/2,delta=4/5 it reverses, but for beta=1 it never reverses. The opposite-direction reversal is absent for beta<=1. Do not assume these mathematical families have identical fitted psychological mechanisms.
5. Independent auditor must reconstruct every row, all 72 reversal flags, and source/JSON SHA256 without importing production source. Negative/tamper tests must reject utility, choice, missing date, source row and JSON alterations.

## Acceptance and evidence boundary

Deliver Python>=3.11 --test/--emit, full144 decision-level synthetic CSV, 72-world exact outcomes JSON, SHA256 receipt, independent source audit program, first-hand theory report, formal acceptance only if two Python testing jobs and independent third GitHub Actions job completed/success, and then original239 v0.8 linking only 01-018 (after v0.7). This is formal math E1 only. Next original priority candidate 01-019 Habit Formation remains unstudied pending primary source audit, with no model fusion before all R learning.
