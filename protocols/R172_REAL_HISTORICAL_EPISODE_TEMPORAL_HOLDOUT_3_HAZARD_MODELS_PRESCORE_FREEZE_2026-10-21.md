# R172 PRE-SCORE FREEZE: authentic historical regime-breakdown event-history forecast benchmark

Date 2026-10-21. Original catalog P1/07-014 Historical Event History Models. This is a genuine original public historical country-year data analysis, **not** the source authors' original statistical model and not a claim of external real-time historical foresight. Protocol committed before executable prediction code or test results.

## Primary source, byte integrity and event definition

* Cox (1972), *Regression Models and Life-Tables*, JRSSB 34(2):187–202, DOI https://doi.org/10.1111/j.2517-6161.1972.tb00899.x: conditional event hazards and censoring, not automatically original-data Cox regression here.
* Berry & Berry (1990), *State Lottery Adoptions as Policy Innovations*, APSR 84(2):395–415, DOI https://doi.org/10.2307/1963526: historical internal determinants and diffusion process motivation; source state-lottery data **not used** here.
* Pérez-Liñán and Mainwaring (2025), *Democratic Trajectories in the Third Wave: Aligning Theory and Methods*, Harvard Dataverse official [DOI10.7910/DVN/WFO1N1](https://doi.org/10.7910/DVN/WFO1N1), version **1.1**, license **CC0-1.0**, historical episodes originally 1974–2017.

Full original data were **actually downloaded, cross-format provenance checked, and permanently archived** in GitHub research/R172/source in [archive commit94ff7c5](https://github.com/edwardsage419/Psychohistory-Research/commit/94ff7c5368000e3dda1cdba10a724337f9bf1422):
- Original *as-uploaded* data format via official Dataverse `?format=original`, **265,851 bytes**, MD5 `4343114d56124f88bce9d9cc3ce81523` matching original official DataFile metadata, SHA256 `ddca691b25a664ce13ef2471184e3d5ae3ed62cb72521e0593bff770efb0e4e6`.
- Dataverse-ingested *table representation* `Original_Replication_dataset.tab`, **428,013 bytes**, SHA256 `ed8e29368d06d0fa6d597df567eb21e7ac27fa849e1cdfd90b76167c8b5778ba`; its byte-level MD5 differs from the MD5 of the original uploaded format, as documented by [Dataverse's tabular format access API](https://guides.dataverse.org/en/latest/api/dataaccess.html). The two exact representations must **not** have MD5 signatures interchanged.
- Original author `Replication code (Stata file)`, **17,387 bytes**, MD5 `2dd571e5f94bd1f79158dcd2b53b0b94`, SHA256 `664cf425684b97b8a7bf835ed748955e2e34426e8a14c0db8abbf98a4fb2e3ad`. Original Stata code was inspected for field usage but **not executed or used to claim primary article reproduction**.

Verified real source shape: 1,731 person-regime **country-years**, 103 transition episodes, **83** distinct source country codes (the Dataverse prose calls it 84 countries; record this unresolved discrepancy rather than silently changing count), years **1975–2017**, exactly **45** yearly `breakdown==1` rows, **1,680** zero-event rows, **6** rows with **missing** `breakdown`; all six belong to **Nigeria episode NGA2011, 2012–2017**, with no recorded endpoint at any year. Exactly 45 episodes have one breakdown event on the final observed year and 58 have no coded event, including NGA2011; all other per-episode year sequences are contiguous with no events after a reported breakdown, and `t==year-t0` throughout. `libdem0` initial index is constant within episodes, one row missing across entire dataset (handle explicitly), otherwise range 24.485476–83.00418. 

**Target is first recorded annual regime breakdown after the transition**, conditional on not having a previously recorded breakdown in this episode. A zero indicator is one observed year at risk with no breakdown; a nonzero event ends the episode. A blank endpoint cannot be equated to 0. Exclude **entire NGA2011 episode** in every model and evaluation (6 rows), leaving at most **1,725 labeled annual rows in 102 eligible episodes** before other fixed cohort/time partitions. All other event-free episodes are right-censored at their last observed calendar year, not given a fictitious breakdown.

## Frozen genuinely retrospective no-future-data split

To avoid same-episode overlap and calendar leakage:
* **Training**: transition year ≤1998, use *only* observed risk-set rows with calendar year ≤1999. For episodes still active at 1999, censor the training view at calendar 1999, even if the source file shows a later event. Older episode follow-up years after 1999 are **withheld and not scored**.
* **Temporal held-out**: transition year ≥1999 and all its actually observed annual outcome labels from calendar year ≥2000 through 2017. The held-out episodes are entirely new transition cohorts and never included in fitting. No future outcomes or future country-year covariates may enter predictors.
* Original episode `id` (e.g. ALB2001) defines grouping, `transition` is episode start year, calendar `year` is risk interval end. Verify these definitions from actual source before scoring; never create artificial unseen observations.
* For forecasting at original transition's first full observed year (age `t=0`), **baseline `libdem0` for that very year might not have been available ex ante**: the M2 model must fall back to the duration-only M1 prediction at t=0. For t≥1, episode's first observed-year `libdem0` is historical baseline information already available. A truly missing `libdem0` always invokes M1 fallback for M2, no test-trained imputation.

## Three frozen, bounded competing annual hazard estimators

All annual hazard probabilities must lie strictly in (0,1); every row predicted from **training estimates only**:
1. **M0 constant baseline**: Laplace-smoothed training hazard \(p_0=(E_{train}+1)/(N_{train}+2)\).
2. **M1 duration-group model**: fixed age buckets t∈[0,2],[3,7],[8,15],[16,∞); for bucket b, \(p_b=(E_b+20p_0)/(N_b+20)\). Prior weight **20** and bin cuts frozen, not optimized after seeing test.
3. **M2 duration plus at-entry liberal-democracy group**: split initial `libdem0` at **50**, only for t≥1 when baseline index is already temporally available, with high/low stratum s. Estimate \(p_{b,s}=(E_{b,s}+20p_b)/(N_{b,s}+20)\), where p_b is M1's previously frozen training-only estimate. Missing index or t=0 falls back to p_b. Do **not** use contemporaneous GDP, future neighbor events, post-outcome information, or later V-Dem variables.

No original Cox partial likelihood coefficients, diffusion mechanism, causal effect of democracy, intervention, or original article estimate is claimed. These are transparent project-defined **Beta-smoothed finite Bernoulli hazard predictions**, not fit via Cox. Use Python exact `fractions.Fraction` for model probabilities and source integer counts. Use float only for log-loss/Brier and bootstrap aggregate results, with 12-decimal reporting precision and no numerical comparisons of exact results.

## Frozen scoring and uncertainty

For **every** eligible held-out episode-year, calculate conditional event log loss \(-[y\log p+(1-y)\log(1-p)]\) and Brier \((y-p)^2\), with the denominator number of observed held-out yearly risk rows. Also sum annual log losses within an episode and average across held-out episodes, noting that episode-length variation means this metric is not same as annual log loss. Baseline M0 is the predeclared comparator. Compute individual M1−M0 and M2−M0 differences in annual and per-episode scores. Lower is better, but **no posthoc choice of best model, threshold, risk-set split, smoothing strength or covariate** is permitted.

For uncertainty, resample **held-out episodes** as units with replacement, random seed `20261021`, **512** draws; bootstrap 2.5th–97.5th percentile intervals for annual loss differences and Brier differences. Do not pretend country episodes from the same country are statistically independent; distinguish this episode bootstrap from valid country-clustered inference and do not claim causal confidence levels.

Store every held-out original `episode_id, country ID, year, t, observed event` and **all three exact rational predictions** in a full deterministic `R172_REAL_HELDOUT_PREDICTIONS.csv`. Store comprehensive training counts, time split, test counts/episodes, source IDs, all three score summaries, all bootstrap points/quantiles, exclusion ledger and evidence limitations in canonical `R172_EXACT_RESULTS.json`. All held-out rows and underlying source bytes must be reproducible by independent runner.

## Controls/acceptance

- At least 60 distinct unittest methods including source original vs ingested MD5 distinction, original author field names and risk-set continuity, missing Nigeria exclusion, event/censor counts, strict cohort/calendar split, no same-episode overlap, first-year M2 fallback, no outcome leakage, predictions strictly in (0,1), exact formula verification, unit tests of synthetic boundary cases, canonical CSV/JSON reproducibility and frozen source hash checks.
- Two Python environments 3.11/3.12, fixed hashes for source code, tests, CSV, JSON and deterministic ZIP. Independently rerun and archive full files to main, verify readback.
- If held-out contains zero positive events or training lacks both positive and zero events, stop and declare evaluation underpowered/blocked rather than invent a positive result. Report train/test counts **after** the frozen split has been executed.
- **Research grade**: can be `CLOSED_BOUNDED_REAL_HISTORICAL_RETROSPECTIVE_HOLDOUT` for this exact public original data task only if tests/CI pass. That is *not* new independent real-world E3 event forecasting, and not R073's independent human repeated-game E2 experiment. Keep new E2=0, new genuine E3=0, and keep R073/PESEN v0.1 FROZEN. Next original R173 to be verified after acceptance.

Project sequence stays all original R studies → taxonomy/classification → fusion.
