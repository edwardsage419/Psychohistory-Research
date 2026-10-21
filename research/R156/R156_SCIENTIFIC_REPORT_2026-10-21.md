# R156: Reduced AK growth versus diminishing returns: 96 preregistered worlds and parameter identification

Date 2026-10-21. Catalog **P2 / 06-014 Endogenous Growth Models**. [Precomputation freeze](../../protocols/R156_REBELO1991_ROMER1986_1990_AK_CONCAVE_96_TRAJECTORIES_PRESCORE_FREEZE_2026-10-21.md) committed before any stage code at [ed806d1](https://github.com/edwardsage419/Psychohistory-Research/commit/ed806d199bc7753513608bf78545ed680b862d2e). **Evidence class E1, project-authored reduced-form mathematical comparison**. This is not a reproduction of the authors' rich equilibrium or empirical growth models, and not a forecast about any historical economy.

## Original academic source records and access boundary
Publisher records confirmed:
* P. M. Romer, 1986, *Increasing Returns and Long-Run Growth*, *Journal of Political Economy* 94(5):1002–1037, DOI https://doi.org/10.1086/261420, publisher abstract addresses knowledge, increasing returns and endogenous technical change.
* P. M. Romer, 1990, *Endogenous Technological Change*, *Journal of Political Economy* 98(5), Part 2:S71–S102, DOI https://doi.org/10.1086/261725, publisher abstract treats purposeful idea production, nonrival/partially excludable knowledge and monopolistic competition.
* S. Rebelo, 1991, *Long-Run Policy Analysis and Long-Run Growth*, *Journal of Political Economy* 99(3):500–521, DOI https://doi.org/10.1086/261764. Publisher abstract identifies the reproducible-capital core and sustained endogenous growth without increasing overall returns.
These publisher descriptions establish intellectual context; **none of the three complete papers, structural parameter estimates, original evidence or original simulation codes were read/reproduced**. Our equations represent illustrative AK and concave capital accumulation, without occupational choice, demographics, knowledge spillovers, innovation incentives, labor/human capital or real policy data.

## Frozen computational contrast
For a constructed capital stock k and artificial output y=k^alpha at A=1,
\[
\dot{k}=s k^\alpha - \delta k,\qquad k(0)=k_0>0.
\]
Two explicitly different assumptions: AK constant marginal product alpha=1 and diminishing marginal returns alpha=1/2. Use k0∈{1,4,9}, savings s∈{.1,.2,.4,.6}, depreciation delta∈{0,.1,.2,.4}. Exactly **2×3×4×4=96** separately named predeclared scenarios, store k(t), y(t) and net stock flow at t={0,1,5,10}.

Two independently executed computational routes:
1. Exact mathematical forms evaluated using floating point: AK \(k(t)=k_0\exp[(s-\delta)t]\). For alpha=1/2, define x=√k, so \(dx/dt=(s-\delta x)/2\). When delta>0, \(x(t)=s/\delta+(\sqrt{k_0}-s/\delta)e^{-\delta t/2}\); when delta=0, \(x(t)=\sqrt{k_0}+st/2\). Then k=x².
2. Explicit fourth-order Runge-Kutta integrates **k directly**, using only \(s k^\alpha-\delta k\), fixed step h=1/1024; it does not integrate transformed x or look up the closed solution.

All 96 worlds and 4 frozen time checkpoints satisfy independent solution tolerance 1×10⁻⁷, positive stock, valid production/flow, and model-specific invariants. The **maximum absolute RK4/closed-form stock difference is 3.3651×10⁻¹¹**, a numerical agreement rather than exact Fraction identity. The complete [103,608-byte JSON](R156_EXACT_RESULTS.json) retains all 96 paths and provenance.

## Quantified contrasts and interpretation limits
Example same k0=1, s=.2, delta=.1:
| Time | AK alpha=1 stock k | Diminishing alpha=.5 stock k |
|---|---:|---:|
| 0 | 1 | 1 |
| 1 | 1.105170918076 | 1.099919720033 |
| 5 | 1.648721270700 | 1.491327527427 |
| 10 | 2.718281828459 | 1.941756802321 |

AK grows at constant proportional rate s−delta=.1, given fixed parameters and no omitted economic counter-forces. Concave alpha=.5 has fixed stock \(k_*=(s/\delta)^2=4\) when delta>0, reached asymptotically. Under the constructed concave case, if k0<k*, stock rises; if k0>k*, stock falls; if k0=k*, it stays fixed. When delta=0, the concave solution grows as a square of a linear function; its proportional growth rate tends to zero even though its level grows indefinitely. Thus a *positive output stock growth observation over a finite horizon* does not by itself prove persistent endogenous exponential growth, knowledge externalities or a society-wide growth equilibrium.

## Parameter nonidentification and numerical artifact counterexamples
In AK, `(s,delta)=(.2,.1)` and `(.4,.3)` both have the same net rate .1 and **identical complete k(t) paths** at every time for common k0. No precision of observing k(t) alone can distinguish those two primitive values in this reduced form; an additional observation of gross saving/investment or depreciation is required. In the concave model, those two settings share the same initial derivative .1 at k0=1 but diverge later: k(5)≈1.491327527427 and 1.382688637580. Therefore the data requirements and identifiability depend on the model family.

A coarse forward-Euler update h=20 with k0=1, alpha=1, savings .1 and depreciation .4 yields **k_new≈−5**, whereas exact continuous k(20)=exp(−6)=0.002478752176666>0. A negative simulated stock can be a numerical method artifact, even when the underlying differential equation preserves positivity. The original experimental design prespecified this failure example rather than selecting it after checking outcomes.

## Actual verification, archive and scope
[Source program](r156_growth_pair.py); [118 executable unittest methods](test_r156_growth_pair.py) of which 96 separately named full parameter worlds plus 22 independent controls. [First GitHub Actions run 39520340288](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39520340288) succeeded for Python3.11/3.12, with 118 tests per environment and identical outputs/hashes. [Pinned CI and publishing run39520425232](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39520425232) similarly passed dual Python3.11/3.12 118 tests each; a third publication job118962724021 independently reran all 118 tests, verified four immutable SHA256 hashes and pushed complete [JSON](R156_EXACT_RESULTS.json) and [ZIP](R156_Growth_96_Worlds_118_Tests.zip) to permanent main at [archive commit4862754](https://github.com/edwardsage419/Psychohistory-Research/commit/4862754b16894fbbc7e4f5e0bdb629875fdb4358). **590 total real test executions = five runs of 118 distinct methods**, 0 failures; test repetition is reproducibility evidence rather than independent real-world growth evidence.

Pinned SHA256:
* source `4980bbaad13d2162503aa05ac05829035a6d891144913f7db100e33abc1eda0d`
* tests `87ff03e0d15fe1c2edcddc5081488f58f3730fb0fc9df5039984721d32d7cd6a`
* full JSON `bc80a9bac0b7c6d26c6e5c829c761f482a2ba1a9803a097bccd3735aeaf0db88`
* full ZIP `f7b7ddb26215b76cd5b60a4734e4b492206928141356e35768c7eb7ab4366a45`.

Reproduce within `research/R156`: `python r156_growth_pair.py > R156_EXACT_RESULTS.json` then `python -m unittest -q test_r156_growth_pair.py`. Standard library only, archive format ZIP_LZMA.

**CLOSED_BOUNDED_E1** for the frozen pairwise mathematical hypothesis tests, with new individual human/independent forecasts E2=0, external historical forecast E3=0. R073 and PESEN v0.1 remain FROZEN. Next original candidate **R157 P2/06-015 Structural Demographic Theory**, retaining project sequence: all original R candidate studies, catalog classification, then fusion.
