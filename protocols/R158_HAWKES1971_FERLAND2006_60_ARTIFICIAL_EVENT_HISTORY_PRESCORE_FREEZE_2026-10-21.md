# R158 Frozen prescore protocol: bounded conflict event count-process mathematics and self-excitation interpretation

2026-10-21. Original P2 / 06-016 Conflict Event Process Models. R157 CLOSED_BOUNDED_E1, main commit 80b9c1642ab4ae7c630ef15e243a4915bbee2ae9. No real conflict data allowed or needed for E1 proof, and no violence prediction is claimed.

## Original scholarly sources and boundaries
A. G. Hawkes (1971), *Spectra of Some Self-Exciting and Mutually Exciting Point Processes*, *Biometrika* 58(1):83–90, DOI [10.1093/biomet/58.1.83](https://doi.org/10.1093/biomet/58.1.83), [Oxford original journal abstract](https://academic.oup.com/biomet/article-abstract/58/1/83/224809), JSTOR issue table of contents [1971](https://www.jstor.org/stable/i315467). Hawkes original abstract explicitly discusses the possibility of self-exciting and doubly-stochastic processes with indistinguishable second-order properties. Abstract/TOC directly checked, full 1971 author PDF **not** read, no Hawkes event-times reconstructed.
R. Ferland, A. Latour and D. Oraichi (2006), *Integer-Valued GARCH Process*, *Journal of Time Series Analysis* 27(6):923–942, DOI [10.1111/j.1467-9892.2006.00496.x](https://doi.org/10.1111/j.1467-9892.2006.00496.x), original publisher abstract directly checked, authors introduce Poisson-deviate integer-valued conditional-variance process. Full model/equations/data were **not** acquired; our one-lag conditional Poisson count equation is a **project-authored simplified mathematical analogue** only, not exact Hawkes or INGARCH of either original paper.

## Freeze 60 artificial sequences and conditional intensity model
Observed synthetic nonnegative integer counts n[t] over eight arbitrary periods, no event location, identity, casualty, or real country:
H0=(0,0,0,0,0,0,0,0),
H1=(1,0,2,0,3,0,2,1),
H2=(0,1,3,2,0,1,4,0),
H3=(4,4,0,0,0,0,1,0).
Artificial baseline mu in {1/2,1,2} and feedback alpha in {0,1/4,1/2,3/4,1}. Exactly 4×3×5=60 fixed complete log-score worlds. Conditional intensity for t>=0:
lambda_t = mu + alpha * n[t-1], where n[-1]=0; n_t conditional on past would be Poisson(lambda_t) **under this hypothetical observation model**. Score each frozen observed path using log pmf log P(n_t|past)=n_t log(lambda_t) - lambda_t - log(n_t!). Implement two separate numerical scoring routes: math.lgamma(n_t+1) and independent exact factorial multiplication then log of integer factorial. They must match all worlds to 1e-12. Preserve entire lambda_t as Fraction strings and individual term log scores and sum of log scores as rounded floats. For alpha=0, scores are homogeneous Poisson baseline.

Independent unconditional expectation math, **separate from any observed count history**:
m_t=E[N_t]=mu+alpha*m_{t-1}, m[-1]=0.
Compute t=0..12 by direct Fraction expectation recursion and independent finite geometric sum m_t = mu * sum_{k=0}^t alpha^k; strict exact agreement for mu×alpha all 15 combinations. For alpha<1, stationary mean m_inf=mu/(1-alpha). For alpha=1, no finite stationary limit and m_t=mu(t+1). The values alpha=1 are **finite-horizon mathematical controls**, no stationary process is claimed.

## Predeclared counterexamples and checks
1. An observed count of n[t-1]=4 raises next period conditional expected count by 4alpha relative to baseline, with no valid inference of causal triggering. If alpha=0, conditional mean is constant across all histories.
2. All-zero H0 has identical likelihood for every alpha for any fixed mu, because all previous counts are zero. Thus this history alone does not identify alpha.
3. For H1 with mu=1, alpha=1/2, the positive-feedback model has **lower** conditional log score than alpha=0; for H2 with mu=1/2, alpha=1/2, it has **higher** score than alpha=0. These are preselected artificial examples showing history dependence in scoring, not model-selection evidence for any real dataset.
4. For alpha=1, unconditional mean t=12 is 13mu, not a stationary rate; for alpha=0 it remains mu. For alpha=3/4 finite long-run expectation is 4mu.
5. "One-event" second-order statistics do not generally decide self-excitation versus exogenous modulation (Hawkes original abstract). Our tests only establish conditional likelihood arithmetic, and cannot adjudicate causal mechanism or hidden time-varying baseline with synthetic observations.
6. Validate alpha,mu,counts for finite, correct type and range; negative counts, fractional counts, floats/bools as event counts, negative or out-of-range alpha, nonpositive mu must raise ValueError.
7. Numerical implementation must reject NaN and infinite values and never silently cast a real historical series as these constructed sequences.

## Closure gate
At least 60 different uniquely named unittest methods for full worlds, plus 20 independent controls. Dual Python3.11/3.12 CI, all original code/results deterministic, verify four SHA256 on exact source, tests, complete JSON and standard-library ZIP, publish all permanent files to GitHub main, verify readback before CLOSED_BOUNDED_E1. Do not imply actual conflict-event predictive E2 or E3. R073 and PESEN v0.1 stay frozen. Next original catalog entry R159 P1/07-001 Dual Inheritance Theory only after R158 formal acceptance.
