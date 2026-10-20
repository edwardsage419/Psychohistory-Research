# R154 precalculation freeze: stock-flow conservation, feedback and numerical stability

Date: 2026-10-20. Original candidate catalog: **P1/06-012 Stock and Flow System Dynamics**. Baseline: R153 CLOSED_BOUNDED_E1, archived on main by 9aaeccf4290eb6b2d0badda85292cc7a199c57d4.

## Scientific scope and primary-source gate
First-hand book listings checked: Jay W. Forrester (1961), *Industrial Dynamics*, MIT Press (bibliographic entry https://books.google.com/books/about/Industrial_Dynamics.html?id=KRzHAAAAIAAJ); John D. Sterman (2000), *Business Dynamics: Systems Thinking and Modeling for a Complex World*, McGraw Hill official publisher contents https://www.mheducation.com/highered/product/business-dynamics-sterman.html and author MIT page https://mitmgmtfaculty.mit.edu/jsterman/business-dynamics/. The publisher chapters explicitly include stocks, flows, delays, feedback and numerical integration. Neither source book was acquired in full, and no author empirical/calibration dataset is reused. New E2/E3=0; R073 and PESEN v0.1 remain frozen.

## Preregistered 100 exact discrete-time stock-flow trajectories
Artificial compartments A and B represent two conserved resource stocks, no implied human population or economic system. Closed simultaneous transfers with exact fractions:
A[t+1]=(1-p)A[t]+q B[t]; B[t+1]=p A[t]+(1-q)B[t].
Initial total N=10, A0 in {0,2,6,10}, B0=10-A0. Transfer shares p,q independently in {0,1/4,1/2,3/4,1}. Exactly **4×5×5=100** worlds, each with t=0,...,12 inclusive (13 observations, 12 transitions), all computed with Fraction.

Independently calculate analytic A[t]=A_star + (1-p-q)^t(A0-A_star), where A_star=10q/(p+q) if p+q>0; for p+q=0 require A[t]=A0. B[t]=10-A[t]. All 2600 compartment observations and all transitions must match analytical expressions with strict rational equality. Two derivation routes must not call each other. Verify nonnegative stocks, exact N=10, simultaneous opposed transfer consistency.

## Prespecified counterfactuals and boundary cases
1. p=q=0: every stock static.
2. p+q=1: equilibrium reached after one transition, for all A0.
3. p=q=1: exact period-two stock swap; ordinary convergence falsely asserted is failure.
4. p=1,q=0: all mass eventually in B after one step, including initial A=10.
5. Same total series N[t]=10 for all p,q, so observing aggregate N alone cannot identify individual transfer shares. Demonstrate distinct A trajectories compatible with identical N histories.
6. Explicit numerical negative control: interpret p=q=3/4 as per-unit-time continuous rates; naive forward-Euler step h=2 from A=10,B=0 gives A_next=-5,B_next=15, although h=1 remains nonnegative. Preserve clear distinction between continuous-time rates and the discrete-time transition fractions.
7. Delayed-flow negative control: with transfer p=1,q=0, A[-1]=A[0]=10, B[0]=0, lag-one unbounded withdrawal based on old A produces negative A at t=2 after initial A becomes zero; guard must reject impossible negative stock or explicitly label it nonphysical. This is a constructed delay artifact, not a real documented system.
8. Open-system book-keeping example: for valid nonnegative external influx I and outflux O, conservation changes to N[t+1]=N[t]+I-O. Reject outflux exceeding available stock; do not represent an open system as conserving N.

## Acceptance and archival conditions
Use independent direct recurrence and closed form Fraction checks for every one of the 100 parameter worlds; export all 100 complete 13-step histories to a deterministic UTF-8 JSON. At least one distinct real unittest method per frozen parameter tuple plus separately named conservation, equilibrium, delay, numerical, and invalid-input controls. Replicate tests in GitHub Actions Python 3.11 and 3.12. Immutable source code, tests, results JSON and reproducible standard-library ZIP must be submitted to GitHub main, re-read and hash-verified. A positive synthetic algebra result may be closed as BOUNDED_E1, never as actual social/historical forecasting skill.
