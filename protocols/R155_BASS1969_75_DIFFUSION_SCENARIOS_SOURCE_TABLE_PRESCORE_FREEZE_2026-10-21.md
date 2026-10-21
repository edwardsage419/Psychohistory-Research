# R155 precomputation frozen protocol: Bass diffusion continuous time, peak, identifiability and source Table I

2026-10-21, source baseline main `fe713f9feb3bad323ac1626e71f8a2113e44ac91`. Original catalog P1/06-013 **Bass Diffusion Model**. Previous model R154 formally closed E1.

## Primary source and limits
Frank M. Bass (1969), *A New Product Growth for Model Consumer Durables*, *Management Science* 15(5):215–227, DOI https://doi.org/10.1287/mnsc.15.5.215. Publisher record https://pubsonline.informs.org/doi/10.1287/mnsc.15.5.215. Author's original printed paper scanned at https://pdodds.w3.uvm.edu/files/papers/others/1969/bass1969a.pdf ; inspected printed pp. 216–219 including defining hazard, ODE, p. 218 Table I and sales-peak condition. The actual published title includes 'for Model', as confirmed by the author's 2004 correction DOI https://doi.org/10.1287/mnsc.1040.0300. The original consumer durable time-series behind regression Table I were not acquired; no author regression refit or heldout historical sales test claimed. Only published parameters will be transcribed for arithmetic checks.

## Freeze 75 mathematical worlds
At time zero no adopters; non-repeating first-adoption process for a *fixed* m. Fraction of cumulative adopters F follows dF/dt=(p+qF)(1-F), F(0)=0, with p,q>=0 and m>0. Test all Cartesian combinations:
p in {0, 1/200, 1/50, 2/25, 1/5};
q in {0, 1/50, 1/10, 2/5, 4/5};
m in {100,1000,10000}.
Precisely 5×5×3=75 preregistered worlds. Record for times t=(0,1/4,1,3,5,10): cumulative F(t), flow f(t), and numbers mF,mf for each world.

For p>0: closed form F(t)=(-expm1(-(p+q)t))/(1+(q/p)exp(-(p+q)t)); p=0 with zero initial seed produces F(t)=0 for all t (even q>0). q=0 reduces to the independent exponential 1−exp(−pt). f=(p+qF)(1−F). Positive p assures 0<F(t)<1 at positive finite t. F(0)=0 and f(0)=p.

Implement an **independent 4th-order Runge-Kutta ODE numerical solver** evaluating only the RHS, starting F(0)=0 and fixed 1/2048 integration step per time unit; compare all 75×6 cumulative F values to analytic closed form with tolerance 2e-11. Do not use analytic F values to initialize/adjust RK4. Verify f via RHS and finite differences of cumulative F (central h=1e-5 on t>h), tolerance 1e-8.

## Preregistered peak and boundary controls
For p>0 and q>p: the unique **interior** sales rate peak t*=log(q/p)/(p+q). Its cumulative F*=(q−p)/(2q) and peak density f*=(p+q)^2/(4q). At q<=p peak is the boundary t*=0; if p=q=0, f identically zero and all t are maximizers (return t*=None rather than a spurious unique peak). p=0,q>0 yields no adoption from zero seed and also t*=None. Verify density immediately before and after the peak, and derivative sign using analytic forms. Multiple m values must leave *fractions and peak time* identical while adopted count scales exactly with m (allow floating tolerance).

## Original Table I published coefficients: source arithmetic only
For each of three printed Table I rows on p. 218, manually transcribe printed values (dimensionless rate as printed, m in 10^3 units):
* electric refrigerators: p=.0026167, q=.21566, m=40001 (thousands)
* home freezers: p=.018119, q=.17110, m=21973 (thousands)
* black and white television: p=.027877, q=.25105, m=96717 (thousands)
Compute t*, F*, peak annualized first-adoption rate S*=m(p+q)^2/(4q) in table's thousands per year unit, and exact t=0 rate m p in the same unit. Only arithmetic recomputation of printed rounded numbers; cannot assert reproduction of author raw-data regression coefficients or fitted historical peaks.

## Prespecified identification and failure cases
At t=0 observed adoption flow S(0)=m p; construct two distinct (m,p) settings with exactly matching initial flow, but different future curves. This establishes a one-instant identification failure, not global structural nonidentifiability with full observation trajectories. q>0 does not start from F0=0 when p=0. Do not substitute an Euler discrete update for continuous closed form: in a chosen high-rate world p=.2,q=.8 from zero, explicit Euler dt=10 gives F1=2>1, whereas exact continuous F(10)<1. Reject negative/nonfinite p,q,m,t and avoid asserting actual adoption rates when a coarse simulated state violates unit bounds.

## Closure and evidence
At least 75 separately named unittest methods plus controls; both Python 3.11 and 3.12 CI; commit deterministic complete 75-result JSON and entire source/test/JSON standard-library ZIP to main with pinned SHA256, verify repository readback. Report independent solver accuracy, controls, source coefficient arithmetic, and caveats. Scientific class E1 for model arithmetic and **published-table arithmetic check**, not empirical out-of-sample E2 or historical-event predictive E3. Keep R073 and PESEN v0.1 frozen. Next original R series candidate is R156 P2 / 06-014 Endogenous Growth Models; continue catalog before any classification/fusion.
