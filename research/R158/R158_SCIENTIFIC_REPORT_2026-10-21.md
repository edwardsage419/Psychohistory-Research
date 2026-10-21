# R158 Scientific report: discrete Poisson count feedback, conflicting synthetic likelihood rankings, and no causal identification

Date 2026-10-21. Original catalog **P2/06-016 Conflict Event Process Models**. Research standard E1 artificial mathematical checks only, frozen [R158 prescore protocol](../../protocols/R158_HAWKES1971_FERLAND2006_60_ARTIFICIAL_EVENT_HISTORY_PRESCORE_FREEZE_2026-10-21.md) at git commit `e03fd09293e4573fdd6bb42fa701460c7a7713c5`. No conflict event dataset, locations, victims, organizations, casualty rates or historical event times are present, and none of the results is a real violence forecast.

## Primary literature audited before implementation
* Alan G. Hawkes (1971), *Spectra of Some Self-Exciting and Mutually Exciting Point Processes*, *Biometrika* 58(1):83–90, DOI [10.1093/biomet/58.1.83](https://doi.org/10.1093/biomet/58.1.83). Directly checked original [Oxford journal/abstract](https://academic.oup.com/biomet/article-abstract/58/1/83/224809) and [JSTOR original 1971 issue contents](https://www.jstor.org/stable/i315467); full article was not read/recreated. Of special scientific importance, the original abstract explicitly observes that some self-exciting and doubly stochastic point processes share identical second-order properties. Therefore clustering or covariance statistics alone do not establish a self-exciting causal mechanism.
* René Ferland, Alain Latour and Driss Oraichi (2006), *Integer-Valued GARCH Process*, *Journal of Time Series Analysis* 27(6):923–942, DOI [10.1111/j.1467-9892.2006.00496.x](https://doi.org/10.1111/j.1467-9892.2006.00496.x), [original Wiley publisher abstract](https://onlinelibrary.wiley.com/doi/10.1111/j.1467-9892.2006.00496.x). Authors develop a more general Poisson count process with autoregressive conditional variance and an empirical application. Full original article, its exact likelihood and its author dataset were not acquired.

The chosen equation is a **project-constructed single-lag Poisson count model**, not a Hawkes event-time process, and not the complete 2006 INGARCH model. It is only a simple bounded mathematical foil to a constant-rate Poisson model. Treating it as a historical conflict forecasting system would be scientifically unwarranted.

## Frozen world grid and two independently scored likelihoods
Four strictly **artificial** integer-count sequences, each length 8:
* H0=(0,0,0,0,0,0,0,0).
* H1=(1,0,2,0,3,0,2,1).
* H2=(0,1,3,2,0,1,4,0).
* H3=(4,4,0,0,0,0,1,0).

For artificial \(\mu\in\{1/2,1,2\}\), \(\alpha\in\{0,1/4,1/2,3/4,1\}\), **60 predeclared complete models**. With n[−1]=0, the conditional mean is \(\lambda_t=\mu+\alpha n_{t-1}\). Under this artificial Poisson law,
\[
\ell(\mu,\alpha;n)=\sum_{t=0}^{7}\left[n_t\ln \lambda_t-\lambda_t-\ln(n_t!)\right].
\]
Every conditional lambda is stored as exact Fraction, with separate rounded per-period and total floating log scores in [R158_EXACT_RESULTS.json](R158_EXACT_RESULTS.json), and compared with independently calculated log factorial using (a) `math.lgamma(n+1)` and (b) `math.factorial(n)` followed by a numerical log. Both numerical scores agree within 10⁻¹² for every case and period; this is an independent implementation check, not independent empirical validation.

Separate 15 expectation paths under the hypothetical stochastic process are derived **without using observed artificial histories**:
\[
m_t=\mathbb E[N_t]=\mu+\alpha m_{t-1},\quad m_{-1}=0,\quad
m_t=\mu\sum_{k=0}^{t}\alpha^k.
\]
Every 13-time-point path t=0 to 12 is strictly equal as Fraction between independent recurrence and finite geometric sum. For \(0\le\alpha<1\), long-run expected count is \(\mu/(1-\alpha)\). For critical \(\alpha=1\), \(m_t=\mu(t+1)\) is unbounded as t increases and **no stationary expected count is defined**. This does not establish that real violent incidents follow any such branching or reproduction rate.

## Preselected conflicting score and identification outcomes

| Artificial fixed history | mu | alpha=0 total log score | alpha=1/2 total log score | Difference alpha=1/2 minus baseline |
|---|---:|---:|---:|---:|
| H1 alternating counts | 1 | −11.178053830348 | −14.484906649788 | −3.306852819440 |
| H2 locally grouped counts | 1/2 | −17.287579466295 | −15.162960480136 | +2.124618986159 |

The model containing short-lag count feedback is numerically worse in H1 and better in H2, under the prespecified fixed coefficients. These artificial examples demonstrate the direction of *conditional likelihood comparison depends on the event path and baseline*. They offer no estimate of which mechanism explains any real conflict.

**Structural ambiguity of one path:** for H0 every previous observed count is zero; all candidate alpha values yield exactly the same lambda_t=mu and identical likelihood under fixed mu. This **one particular sequence** carries no information about alpha. With a previous count 4, next expected count in the feedback model rises by precisely \(4\alpha\) over the baseline, by mathematical construction. A time-varying unobserved exogenous baseline can imitate such patterns; neither a lag coefficient, a clustered observed sequence nor a scored artificial dataset alone proves event-to-event causal triggering.

**Critical boundary:** when alpha=1, \(m_{12}=13\mu\) and there is no fixed long-run expected count. When alpha=3/4 and mu=1, the stationary expectation is 4. A process with finite conditional means on the eight frozen observed dates does not necessarily admit a stationary unconditional distribution at alpha=1.

## Code, CI, archived artifacts, and research boundaries
* [Source](r158_poisson_count_process.py); [87 discovered unittest methods](test_r158_poisson_count_process.py), 60 uniquely named full parameter/history cases plus 27 additional Poisson normalization, score, identification, criticality, negative type and archive replay tests.
* First [CI run39522593818](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39522593818): Python3.11 and 3.12 ran 87 true tests each, 0 failed and matched source/test/output/ZIP SHA256. Second [pinned run39522688331](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39522688331) ran 87 tests per Python environment; a third independent pinned archive publisher job118970104991 ran 87 more and validated the four fixed SHA256 before pushing the full [44,970-byte JSON](R158_EXACT_RESULTS.json) and [source ZIP](R158_Poisson_Event_60_Worlds_87_Tests.zip) permanently to GitHub main at [archive commit ff041f5](https://github.com/edwardsage419/Psychohistory-Research/commit/ff041f579861599433fede037a16962fc35938f0). Two runs give **435 individual actual test executions of 87 distinct methods**, 0 failures, and no real historical observations.
* Source SHA256 `43890ab779c71d134a713f47c71d40e740f4a224553d5bd6e5d7913d967a94e9`; tests `0f7ddeaade1b842924c9ad4e3e4c30444be5f30a28bf2031954a4c0c9a555d82`; JSON `c3708c476d0d9b8344433b9008197b5622390d82ea52f11896d1cbc08f185635`; ZIP `34aaa668e4cde991a2bc806df48a476bef978b4c305fd247ca573f04966914e4`.
* Replay in `research/R158`: `python r158_poisson_count_process.py > R158_EXACT_RESULTS.json`, then `python -m unittest -q test_r158_poisson_count_process.py`. All standard library, ZIP_LZMA.

**CLOSED_BOUNDED_E1**: the frozen artificial conditional count-process mathematics and two independent Poisson likelihood computations passed all tests. No Hawkes paper experimental replication, no actual conflict event data or test of future political violence, no demonstration of causal self-excitation; E2=0, E3=0. R073 and PESEN v0.1 remain FROZEN. The next original candidate is R159 P1/07-001 Dual Inheritance Theory. As approved, complete all original R candidates before cross-model classification and fusion.
