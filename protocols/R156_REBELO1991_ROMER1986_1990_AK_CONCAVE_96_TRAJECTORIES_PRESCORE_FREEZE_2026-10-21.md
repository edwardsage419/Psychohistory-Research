# R156 prior-computation frozen protocol: reduced-form AK versus diminishing-return stock growth

2026-10-21. Original candidate P2/06-014 Endogenous Growth Models. Prior R155 CLOSED_BOUNDED_E1 from commit 60d9139c364b4f2a361903c6d9703b15d30fe5c5.

## Source scope
Publisher-checked originals:
1. Paul M. Romer, 1986, *Increasing Returns and Long-Run Growth*, Journal of Political Economy 94(5):1002–1037, DOI https://doi.org/10.1086/261420. Publisher abstract invokes knowledge and increasing marginal productivity, unlike a simple diminishing-returns capital process.
2. Paul M. Romer, 1990, *Endogenous Technological Change*, Journal of Political Economy 98(5):S71–S102, DOI https://doi.org/10.1086/261725. Original abstract identifies nonrival partially excludable ideas, incentives and market structure.
3. Sergio Rebelo, 1991, *Long-Run Policy Analysis and Long-Run Growth*, Journal of Political Economy 99(3):500–521, DOI https://doi.org/10.1086/261764. Publisher abstract emphasizes sustained endogenous growth even without increasing returns to scale, under reproducible capital core.
No article full text was acquired. Our tiny fixed-technology models are **project-authored reduced-form counterexamples**, not claimed exact derivations, equilibria or empirical replications of any of the three papers. In particular, they omit purposeful R&D, human capital allocation, labor, utility, market power and nonrival ideas. E1 mathematics only. E2/E3 remain zero.

## Frozen factorial universe: 96 paired worlds
Continuous-time artificial stock k with k(0)>0, A=1:
dk/dt=s k^alpha − delta k.
alpha in {1 (AK constant marginal productivity), 1/2 (concave diminishing returns)}.
k0 in {1,4,9}; s in {1/10,1/5,2/5,3/5}; delta in {0,1/10,1/5,2/5}.
Exactly 2×3×4×4=96 individually enumerated, paired parameter worlds. Record k(0),k(1),k(5),k(10), output y=k^alpha and net stock growth dk/dt. Closed solutions:
AK: k(t)=k0 exp((s−delta)t).
concave alpha=1/2: with x=sqrt(k), dx/dt=(s−delta x)/2, x(t)=s/delta+(sqrt(k0)−s/delta)exp(−delta t/2) when delta>0; x(t)=sqrt(k0)+s t/2 when delta=0; k=x².
Independent numerical route: RK4 integration directly on **k**, evaluating s*k**alpha−delta*k; fixed 1/1024 time step. No analytic curve input except the initial k0. Tolerance absolute 1e−7 (max k remains within reasonable bounds by frozen ranges). Explicit Euler is a negative control, excluded from positive dynamics acceptance.

## Prespecified invariants and controls
1. Every one of the 96 world×4 time results matches RK4 within 1e−7 and remains positive.
2. For all AK trajectories log(k(t)/k0)/t=s−delta for t>0 to 1e−12. For s<delta capital decays exponentially but remains strictly positive. For s=delta stock is static.
3. For all concave worlds delta>0, steady state k*=(s/delta)^2; if k0<k*, k rises monotonically; if k0>k*, k falls monotonically; if k0=k*, stock is stationary. For delta=0, sqrt(k(t)) grows linearly and k grows quadratically; proportional growth approaches zero as t increases.
4. Paired model difference: same s,delta,k0 with alpha=1 vs alpha=1/2 can generate long-term differences despite same initial k (when k0=1), and no universal ordering claimed across parameters.
5. Identifiability negative: AK (s,delta)=(1/5,1/10) and (2/5,3/10) share identical growth s−delta=1/10 and therefore identical whole k(t) paths, even if k(t) observed exactly. Concave models with same k0=1 have matching initial derivative but different later paths.
6. Numerical negative: Euler dt=20 at k0=1, s=1/10,delta=2/5,alpha=1 produces k_new=−5; exact k(20)=exp(−6)>0.
7. Reject nonfinite or negative parameters, invalid alpha, initial k<=0, negative times and invalid step sizes.
8. Compare representative AK constant growth and concave growth with same s,delta under horizon extension to 100, demonstrating no automatic indefinite *per-capita* exponential growth from diminishing returns and finite k* when delta>0.

## Publication and acceptance gate
At least 96 separately named scenario methods, 15+ additional boundary checks. Store all 96 cases and full time trajectories in UTF-8 JSON; run same named tests on Python3.11 and 3.12; independently check fixed SHA256 of source/tests/JSON/ZIP, permanently archive to GitHub main and verify readback before CLOSE. Exact math for formulas; RK4 remains approximate. All evidence E1 only. Keep R073/PESEN v0.1 frozen. Next catalog after successful closure is R157 P2/06-015 Structural Demographic Theory.
