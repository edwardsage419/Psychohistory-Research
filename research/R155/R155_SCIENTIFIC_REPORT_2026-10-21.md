# R155 Bass (1969): author equation audit, 75 controlled diffusion worlds and 3 published coefficient checks

Date: 2026-10-21. Catalog **P1 / 06-013 Bass Diffusion Model**. [Prescore experiment freeze](../../protocols/R155_BASS1969_75_DIFFUSION_SCENARIOS_SOURCE_TABLE_PRESCORE_FREEZE_2026-10-21.md) precedes computation, [freeze commit ff1c9ea](https://github.com/edwardsage419/Psychohistory-Research/commit/ff1c9eae493eb8929b1224cd62f9b2e68bc409ea). **Scientific grade: bounded E1 mathematical reconstruction and direct arithmetic on a small subset of original published coefficients. New E2 human-level independent prediction 0; E3 independently tested historical outcomes 0.**

## Primary author evidence, directly inspected
Frank M. Bass, 1969, *A New Product Growth for Model Consumer Durables*, *Management Science* 15(5), 215–227, DOI https://doi.org/10.1287/mnsc.15.5.215. Publisher [INFORMS original](https://pubsonline.informs.org/doi/10.1287/mnsc.15.5.215) and original [scanned article held by a university](https://pdodds.w3.uvm.edu/files/papers/others/1969/bass1969a.pdf) were checked. Printed **p.216** defines external innovation and imitation, **p.217** gives conditional first-adoption hazard p+qF(t) and the continuous-time sales equation, **p.218** gives Table I published estimates and exact analytic F(t), f(t) and peak-time equation; **p.219** gives author's discrete annual-data regression analogue. Do not silently equate the author's discrete annual regression approximation to our continuous-time RK4 integration. The paper presents empirically fitted results for eleven durable products, but we **did not** acquire those original annual sales histories or recreate the author's regression or heldout forecasts. The odd original title 'for Model' is preserved; author clarifies typo in his [2004 commentary](https://doi.org/10.1287/mnsc.1040.0300).

## Model and 75 preregistered artificial scenarios
Bass continuous-time first purchase fraction F(t) and density f(t):
\[
\frac{dF}{dt}=(p+qF)(1-F),\quad F(0)=0,\quad p,q\ge0,\ m>0,\quad S(t)=m f(t).
\]
The constant market m contains prospective *first-time* buyers only, with no repeat purchases, changing population, competing products, advertising intervention, or network heterogeneity. For p>0,
\[
F(t)=\frac{1-e^{-(p+q)t}}{1+(q/p)e^{-(p+q)t}},\quad
f(t)=(p+qF(t))(1-F(t)).
\]
For p=0 and no seed adopters, F(t)=0, including q>0. For q=0, F(t)=1−exp(−pt).

Preregistered p={0,.005,.02,.08,.2}, q={0,.02,.1,.4,.8}, m={100,1000,10000}, **75 complete and separately identified worlds**. Saved full analytic F, flow f, mF and mf at t={0,.25,1,3,5,10}, plus independent **RK4 solving solely the differential equation** at step size 1/2048. No RK4 initial state or intermediate value comes from the closed form. Across all 75 worlds and six fixed times, **maximum |RK4−closed form| is 2.4×10⁻¹⁵**, below the frozen 2×10⁻¹¹ test tolerance; both algorithms are floating-point, so this is a numerical agreement claim, not arbitrary exact symbolic equality. Full [138,366-byte R155_EXACT_RESULTS.json](R155_EXACT_RESULTS.json) archives every one of the 75×6 observations.

## Peak timing and adoption mechanisms
For p>0, q>p, the density reaches an interior peak at
\[
t_*=\frac{\ln(q/p)}{p+q},\quad
F(t_*)=\frac{q-p}{2q},\quad
f(t_*)=\frac{(p+q)^2}{4q}.
\]
For q≤p the maximum density is at boundary t=0. For p=0 and F0=0 there is no unique peak because adoption never starts. Increasing m scales initial/new/cumulative adopter *counts*, while fractions and interior peak time depend only on p and q.

Numerical preregistered example p=.02, q=.4, m=1000: t*=7.132695889414 in the chosen time units. At t=3, F=.1073486181; at t=10, F=.7577472740. For p=.2, q=.8, m=1000, t*=1.38629436112 and F(10)=.9997730416. These are mathematical scenarios with no observed consumer sample.

## Arithmetic based on published original Table I
The following are **direct manual transcriptions of printed p.218 Table I columns p, q and m (m is measured in thousands of units)**, using the numbers as rounded in the historical article. Computed t* and peak sales belong to this defined mathematical equation, **not** a refit or check of actual annual purchasing data. Time units follow the paper's coefficients; no absolute calendar date can be inferred without defining the author's origin.

| Published product row | Printed p | Printed q | Printed m, thousands | Formula-derived t* | Formula-derived peak sales, thousands per time |
|---|---:|---:|---:|---:|---:|
| Electric refrigerators | .0026167 | .21566 | 40001 | 20.211910 | 2209.306727 |
| Home freezers | .018119 | .17110 | 21973 | 11.866076 | 1149.499643 |
| Black and white television | .027877 | .25105 | 96717 | 7.879661 | 7493.137664 |

The independently recomputed time-zero rate m·p is 104.6706167, 398.128787 and 2696.179809, respectively, in table-thousands per time unit. These directly check the paper's nonlinear coefficient relations using the published rounded parameters. The article's other eight rows and 11 original raw sales series remain outside this work.

## Predeclared failure and identification controls
* Two worlds m=1000,p=.02,q=.4 versus m=2000,p=.01,q=.4 have equal initial adoption flow S(0)=m p=20, while their future F(1) differs (.0242525085 versus .0122104708) and their year-one flow predictions differ. A **single observed initial flow** does not identify p and m separately. This is **not a claim of globally unidentifiable parameters with all adoption times observed**.
* With p=0,q=.8 and F(0)=0, there are no spontaneous adopters, despite a positive imitation coefficient. A seed mechanism would be an additional model assumption.
* With continuous p=.2,q=.8 and dt=10, naive one-step forward Euler produces F=2, exceeding the entire fixed market; exact continuous F(10)=.99977304156678. Conservation and admissibility must be checked independently of apparent time-stepping convergence.

## Verification and archive receipts
[Original source program](r155_bass_continuous.py) and [96 actual unittest methods](test_r155_bass_continuous.py) contain 75 different named full-world tests and 21 separate controls. The first [CI run39519390119](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39519390119) passed 96 tests separately under Python3.11 and 3.12. Both produced byte-identical JSON/ZIP and identical four SHA256 hashes. The second [pinned archive CI run39519534803](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39519534803) passed again under both Python environments with 96 tests per environment, and its independent publication task executed 96 additional tests before committing all original data and source/test ZIP in [archive commit b7891cb](https://github.com/edwardsage419/Psychohistory-Research/commit/b7891cb30ef47d07a3bd3a6ed2b4709e6ceb9ae0). **Five real executions of the 96 methods = 480 individual tests, 96 distinct test methods, 0 failures**.

Pinned SHA256:
* source `5f7fe3a8b539f449906669468f39f401fa62a74e45250271589f61715c7dc5c2`
* tests `8f61e0635f124c05f91003c8d1f2e240824548a5cb4986d360a2b0aeb25ca9c6`
* complete JSON `0b0be2d0edd4ed0564504d97e4dddd417a42f17674e25717649cac672b88949a`
* complete standard-library ZIP `03bea5d262c63b687ba10a097a3465c584841901adcb5fe47bd7b95daf0fdec1`

All original source, tests, result JSON and [R155_Bass_75_Worlds_96_Tests.zip](R155_Bass_75_Worlds_96_Tests.zip) are permanently available in GitHub main. From `research/R155`, run `python r155_bass_continuous.py > R155_EXACT_RESULTS.json` and `python -m unittest -q test_r155_bass_continuous.py`. ZIP uses Python standard library ZIP_LZMA; there are no nonstandard dependencies.

**R155 CLOSED_BOUNDED_E1**, under its preregistered numerical and original published-table arithmetic evaluation. No original-year sales time series, empirical heldout accuracy or demographic event prediction is claimed. R073 and PESEN v0.1 remain frozen. Next original candidate **R156 P2/06-014 Endogenous Growth Models**. Continue the complete original R series, then classify, then fuse.
