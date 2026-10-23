# R301 prospective freeze: Bayesian Online Changepoint Detection (BOCPD) and exhaustive segmentation

Date 2026-10-23 Asia/Taipei. Original239 item **02-012 Bayesian Change Point Detection**, priority P1. This protocol is committed **before R301 model code and results**; any changes to tests/targets after freeze require explicit revision. Research scientific scope: **E1 artificial exactly finite Bayesian filtering**, no real human/animal E2, historical E3 or event forecasting. R073 and PESEN v0.1 remain frozen, and full R-series work precedes classification/fusion.

## Original first-party source

Adams, R.P. & MacKay, D.J.C. (2007), *Bayesian Online Changepoint Detection*, arXiv:0710.3742, [first-author Princeton PDF](https://lips.cs.princeton.edu/pdfs/adams2007changepoint.pdf), [original submission](https://arxiv.org/abs/0710.3742), [Princeton original author bibliography](https://lips.cs.princeton.edu/bibliography/adams2007changepoint/). BOCPD represents online *run-length* uncertainty and predictive model conditional on the currently active segment, not a direct scientific identification of a historical event cause. The original article illustrates applications with real datasets, **which are not replicated here**. Earlier R300 Hidden Markov Model considers known-parameter hidden state filtering and is conceptually nearby, not a first-hand original research package for BOCPD. Earlier original-239 2026-10-18 overlay and early ZIP content scan had no confirmed itemwise primary 02-012; this limited file check is **not** proof no earlier related probabilistic code exists.

## Pre-fixed artificial generative model and source universe

Bernoulli observations y_t in {0,1}, fixed segment-rate prior **Beta(1,1)**, independent newly drawn Bernoulli probability after each change. At each boundary between successive observations t-1 and t, independently change segment with fixed hazard h∈{0,1/4,1/2}; when a change occurs, draw a fresh Beta(1,1) prior, otherwise keep segment parameter and update its Beta posterior. There is **no changepoint before t=1**. Define **run length L_t as current segment's inclusive number of observations**, so L_t∈{1,...,t}; if change immediately before y_t then L_t=1. This is explicitly shifted +1 compared with the common zero-based Adams/MacKay run-length definition. The future changepoint event occurs **before** y_(t+1); we do not confuse L_t=1 with an unobserved post-data boundary.

Observed prefixes: for each of all 16 four-bit sequences binary lexicographic, report t∈{1,2,3,4}; three hazard conditions. Thus **3×16×4=192 fully labeled artificial source rows** (48 world identifiers, four source rows each). Repeated short prefixes are present multiple times, as the original full strings share prefixes; normalize evidence only after **deduplicating all unique t-bit prefixes**. There are no human subjects or independently sampled stochastic observations.

For a segment of length n with k ones, marginal likelihood under Beta(1,1) is `B(k+1,n-k+1)/B(1,1)=k!(n-k)!/(n+1)!`. Conditional predictive P(y=1|segment with k ones and n observations)=(k+1)/(n+2). All calculations exact Fractions.

At t=1 the unnormalized joint source message J_1(L=1,y_1)=1/2. At t>=2, given message J_(t-1)(length l, history), **growth/no-change** contributes `(1-h)*J_(t-1)(l)*P(y_t | last l observations)` to J_t(l+1), while **change** contributes `h*J_(t-1)(l)*(1/2)` to J_t(1). Sum all l when necessary; messages J_t are unnormalized joint probability masses over current length and observed history.

Evidence p(y_1:t)=Σ_l J_t(l), posterior P(L_t=l|y_1:t)=J_t(l)/evidence, last-boundary-change posterior P(L_t=1|history) only if t>=2 (zero at t1), and one-step predictive y_(t+1)=1:
`h*(1/2)+(1-h)*Σ_l posterior(l)*(ones(last l y)+1)/(l+2)`.
Hazard h is a fixed **prior**, not a posterior estimate of actual environmental volatility.

## Fully independent proof requirements

Independently enumerate every binary boundary-change vector of length t-1 (2^(t-1) partitions); its prior probability is h^#changes*(1-h)^#growth, and each contiguous segment contributes the exact Beta(1,1)-marginal product. Sum all partitions for evidence, posterior run lengths and predictive next Bernoulli observation; do not import model forward code. Verify 192 original source rows and result JSON field-by-field, plus source/result SHA256 and a tamper suite.

At every t for each hazard, exact evidence summed over the 2^t **unique** observed prefixes equals 1. For h=0, all posterior mass is on L_t=t and last-change posterior=0, with predictive ones(last t bits) Beta mean (k+1)/(t+2). For each h,t1, posterior L1=1; p(y1)=1/2 and next predictive depends on h and observed y1. For any h in [0,1], all probabilities ∈[0,1], positive evidence.

## Prospectively specified counterexamples with exact expected values

At t=4, h=1/4:
* Observation `0000`: prefix evidence **757/5120**, posterior last-boundary change P(L4=1|0000)=**135/757**, next observation 1 prediction **1717/6056**.
* Observation `0001`: prefix evidence **323/5120**, last change posterior **135/323**, next observation 1 prediction **1301/2584**.
The anomalous final 1 increases posterior mass on a new segment relative to same-length constant-zero observations, **but P(change|0001)=135/323 less than 1**, so one novel observation does not prove a true structural change. Both priors and observations are artificial.

At h=0 negative control: P(change|0000)=P(change|0001)=0; predictive 1 after `0000`=1/6, and after `0001`=1/3. An observation can affect the estimate of a stationary Bernoulli rate **without ever declaring a changepoint**.

At h=1/2 and `0001`, last change posterior **15/23**. The same data and different **known exogenous** hazard assumption yields different posterior conclusions, a necessary prior-sensitivity boundary rather than accuracy ranking.

Do **not** estimate false positive rates, detection delays, general historical predictive utility, or human decision parameters from finite chosen strings. P(L4=1) is a *current terminal run-length probability* in this inclusive convention; not P(ever changed) and not automatic posterior probability a real-world event occurred.

## Release gates

Require real executable Python>=3.11 --test / --emit; complete 192-source original CSV, 48-world stage-result JSON and SHA256 receipt; independent no-import exhaustive partition audit and adversarial corruption rejection; GitHub Actions dual Python3.11/3.12 plus independent third audit/archiver all actual completed/success; source/results permanently committed main. Only after all gates permit R301 formally **CLOSED_BOUNDED_E1_ARTIFICIAL_R301_BOCPD_RUN_LENGTH** and v1.5 original-239 crosswalk one changed ID **02-012**, pending48→47, prior R300/R063 provenances unchanged. R073 and PESEN v0.1 frozen.
