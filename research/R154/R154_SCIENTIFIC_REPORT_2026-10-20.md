# R154 stock-flow system dynamics: exact feedback histories and artificial nonphysical-step controls

Date: 2026-10-20. Original catalog **P1 / 06-012 Stock and Flow System Dynamics**. Research type **E1 constructed mathematical examples**. [Prescore protocol](../../protocols/R154_FORRESTER_STERMAN_STOCK_FLOW_100_TRAJECTORIES_PRESCORE_FREEZE_2026-10-20.md) committed before code at `e0257e03417ee431ce08ab670156587de4dd3fb0`. No actual historical social stock observations were collected and no individual-level E2 or event-level E3 forecast was made.

## Publisher-verified source scope
* Jay W. Forrester, *Industrial Dynamics* (1961), MIT Press. [Bibliographic book entry](https://books.google.com/books/about/Industrial_Dynamics.html?id=KRzHAAAAIAAJ) lists 1961 MIT Press edition and topics including inventory, delays and rate equations. Book full text was **not** acquired or reviewed page-by-page; no original author model/data replicated.
* John D. Sterman, *Business Dynamics: Systems Thinking and Modeling for a Complex World* (2000), McGraw Hill. [Publisher table of contents](https://www.mheducation.com/highered/product/business-dynamics-sterman.html) identifies Stocks and Flows, Dynamics of Stocks and Flows, Feedback, Delays and Numerical Integration; [MIT author publication record](https://mitmgmtfaculty.mit.edu/jsterman/business-dynamics/) confirms publisher and year. This project does not claim reproduction of particular source equations or empirical calibration.

Our two-stock equations and synthetic interventions were designed for this R series mathematical checkpoint. Their real-world construct validity has not been established.

## Frozen experimental universe and exact result
Artificial stocks A and B carry conserved total N=10. Per-period reciprocal transfer shares p and q satisfy 0≤p,q≤1. Closed simultaneous update:
\[
A_{t+1}=(1-p)A_t+qB_t,\qquad
B_{t+1}=pA_t+(1-q)B_t.
\]
Choose A0 in {0,2,6,10}, p,q independently in {0,1/4,1/2,3/4,1}: **4×5×5=100 fully enumerated parameter worlds**. Record 13 states at t=0,...,12 and 12 ordered transfer pairs (A to B, B to A) per world. All states, steps, directions and metadata appear as Fraction strings in [full 169,095-byte results](R154_EXACT_RESULTS.json).

Two independent mathematical routes:
1. Perform literal exact simultaneous transfers at each of 12 steps.
2. Diagonalize the difference equation. If p+q>0, put \(A_* = 10q/(p+q)\), \(\lambda=1-p-q\), then independently compute
\[
A_t=A_*+\lambda^t(A_0-A_*),\quad B_t=10-A_t.
\]
If p=q=0, use static A_t=A0.

Across all 100 cases, both methods produced **strictly equal Fraction pairs at every one of 1,300 state times**, corresponding to 2,600 stored compartment values. Every transition additionally satisfies directed-flow consistency; all 100 closed systems preserve total N=10 and nonnegativity exactly, with no float-based tolerance or rounding.

## Distinct mechanisms with indistinguishable aggregates
Take initial A0=10 and B0=0. With p=q=0 the stocks remain (10,0). With p=1/2,q=0 the first step becomes (5,5); thereafter A decreases. In both examples N_t stays identically 10 for every t. Therefore **the aggregate N series alone does not identify the internal reciprocal transfers**; access to disaggregated stocks or actual flows is needed to address this specific ambiguity. It does not imply that observations of A,B under a richer design could never estimate p,q.

The mathematical feedback eigenvalue is \(\lambda=1-p-q\):
* p=q=0 gives λ=1 and static compartments.
* p+q=1 gives λ=0, so the balanced fixed point is reached in one step.
* 0<p+q<2 yields |λ|<1 and convergence, except trivial initial equilibrium.
* p=q=1 yields λ=−1 and a two-cycle swap for unequal initial stocks, rather than convergence.

These are constructed discrete-time consequences of the update rule, not empirical estimates of social feedback strength.

## Delay and numerical method traps
Treat 3/4 as a **continuous per-unit-time transfer rate**, which is conceptually distinct from 3/4 as a fixed discrete-time transfer share. Naive forward Euler from (A,B)=(10,0):
* step h=1 produces exact arithmetic (5/2,15/2);
* step h=2 produces **(−5,15)**, an unphysical negative A while still conserving total N=10.

A project-authored one-period delayed withdrawal counterexample uses p=1, original A=10, first action moves the full 10 to B. Reusing the obsolete A=10 to command another 10 of outflow at the next step, when current A=0, yields **(−10,20)**. The strict stock-availability guard explicitly rejects that second command. A delay implementation which conserves totals while letting stocks go negative must not be treated as physically acceptable merely because the conservation check passes.

Open-system bookkeeping is a separate rule: after internal transfers, input I to A and withdrawal O from B give \(N_{t+1}=N_t+I-O\). Example start (5,5), reciprocal halves, external I=2 and O=1: end (7,4), total 11. External outflow above the B stock is rejected. This prevents mistakenly claiming constant N for open systems.

## Exact code and CI evidence
[Code](r154_stock_flow_exact.py), [119 real unittest methods](test_r154_stock_flow_exact.py), [permanent source-and-results ZIP](R154_Stock_Flow_100_Histories_119_Tests.zip), [full JSON](R154_EXACT_RESULTS.json).

[GitHub Actions run 39435566160](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39435566160), status success. Python3.11 job118671535060 and Python3.12 job118671535573 each passed 119 genuinely discovered tests, reproduced all 100 trajectories and matched precomputed SHA256 for original source, tests, results and archive. Independent publish job118671661811 again passed 119 tests, checked all four immutable hashes, and permanently pushed JSON+ZIP to GitHub main in [archive commit 4a792b7](https://github.com/edwardsage419/Psychohistory-Research/commit/4a792b717c03702f1709c9f17e843ff1f94f3a53). **357 total real test executions, exactly 119 distinct test methods, zero failures**; repeated environments increase repeatability evidence, not causal or empirical external validity.

Pinned SHA256:
* source: `2c5e0ade08f6221124c0790d83b1fa94976d9c1c8fa6d85b583a6bfdba139757`
* test: `7818731ac70159157261de1f8721cfe06ec0e9772201dedb0ee3b69ffdeef59c`
* complete JSON: `5df956c879f1183606292827a5827470a0c2adaa06833d766823949b05a1f7a6`
* complete ZIP: `e25f045de436f9aa5fed1bf6be061cd536a3544ba932ceef236330e302e269b5`

For exact reproduction from `research/R154`, use `python r154_stock_flow_exact.py > R154_EXACT_RESULTS.json` followed by `python -m unittest -q test_r154_stock_flow_exact.py`. Python standard library only, ZIP compression ZIP_LZMA.

## Closure and next catalog
**CLOSED_BOUNDED_E1**: the frozen 100-world exact arithmetic and negative controls have all passed, and full source/data are re-readable on main. Author full-text derivation and empirical predictions remain unattempted. New E2=0; new E3=0; R073 and PESEN v0.1 remain frozen. Continue original research candidate R155 **P1/06-013 Bass Diffusion Model** before project-level classification and eventual synthesis.
